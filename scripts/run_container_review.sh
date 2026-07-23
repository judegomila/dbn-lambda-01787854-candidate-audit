#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

./verify.sh

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

for precision in 180 256; do
  gcc -O2 -DPREC="$precision" \
    verifiers/verify_triangle_y_dini_arb.c \
    -o "$scratch/triangle_y_dini_$precision" -lflint -lm
  "$scratch/triangle_y_dini_$precision" \
    > "$scratch/triangle_y_dini_$precision.log"
  cmp \
    "logs/triangle_y_dini_$precision.log" \
    "$scratch/triangle_y_dini_$precision.log"
done

gcc -O3 -DTRIANGLE_WEIGHT \
  src/lemma_sweep_p235711.c \
  -o "$scratch/triangle_producer" -lflint -lm

for precision in 180 256; do
  python3 verifiers/verify_triangle_normalizer_corr_iv.py \
    --prec "$precision" > "$scratch/normalizer_$precision.log"
  grep -q "RESULT ALL PASS precision $precision" \
    "$scratch/normalizer_$precision.log"
done

python3 verifiers/verify_tail_1787854_160.py > "$scratch/tail_160.log"
python3 verifiers/verify_tail_1787854_256.py > "$scratch/tail_256.log"
grep -q "TOTAL CHECKS RUN: 93" "$scratch/tail_160.log"
grep -q "TOTAL CHECKS RUN: 93" "$scratch/tail_256.log"
grep -q "RESULT: ALL PASS" "$scratch/tail_160.log"
grep -q "RESULT: ALL PASS" "$scratch/tail_256.log"

echo "RESULT: CONTAINER REVIEW PASS"
