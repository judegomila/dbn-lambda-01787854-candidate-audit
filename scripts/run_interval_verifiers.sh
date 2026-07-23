#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

image=${IMAGE:-dbn21a-flint}
expected=sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538
actual=$(docker image inspect --format '{{.Id}}' "$image")
if [[ $actual != "$expected" && ${ALLOW_UNPINNED_IMAGE:-0} != 1 ]]; then
  echo "error: wrong image ID: $actual" >&2
  exit 2
fi

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

for precision in 180 256; do
  docker run --rm -i "$image" bash -lc \
    "gcc -O2 -DPREC=$precision -x c - -o /tmp/triangle_y_dini -lflint -lm &&
     /tmp/triangle_y_dini" \
    < verifiers/verify_triangle_y_dini_arb.c \
    > "$scratch/triangle_y_dini_${precision}.log"
  cmp \
    "logs/triangle_y_dini_${precision}.log" \
    "$scratch/triangle_y_dini_${precision}.log"
done

python3 verifiers/verify_triangle_normalizer_corr_iv.py --prec 180 \
  > "$scratch/normalizer_180.log"
python3 verifiers/verify_triangle_normalizer_corr_iv.py --prec 256 \
  > "$scratch/normalizer_256.log"
grep -q "RESULT ALL PASS precision 180" "$scratch/normalizer_180.log"
grep -q "RESULT ALL PASS precision 256" "$scratch/normalizer_256.log"

python3 verifiers/verify_tail_1787854_160.py > "$scratch/tail_160.log"
python3 verifiers/verify_tail_1787854_256.py > "$scratch/tail_256.log"
grep -q "TOTAL CHECKS RUN: 93" "$scratch/tail_160.log"
grep -q "TOTAL CHECKS RUN: 93" "$scratch/tail_256.log"
grep -q "RESULT: ALL PASS" "$scratch/tail_160.log"
grep -q "RESULT: ALL PASS" "$scratch/tail_256.log"

python3 verifiers/verify_finite_and_binding.py
python3 verifiers/verify_assembly_1787854.py

echo "RESULT: FRESH INTERVAL VERIFIERS PASS"
