#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

if [[ -n ${REVIEW_OUTPUT:-} ]]; then
  scratch=$(python3 "$root/scripts/replay_guard.py" prepare \
    "$root" "$REVIEW_OUTPUT")
else
  scratch=$(mktemp -d)
  trap 'rm -rf "$scratch"' EXIT
fi

./verify.sh

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

RUN_SANITIZERS=1 ./scripts/run_tail_arb.sh "$scratch/tail_arb"
./scripts/run_direct_singletons.sh "$scratch/direct_singletons"
./scripts/run_barrier_replay.sh "$scratch/barrier"

echo "RESULT: CONTAINER REVIEW PASS"
