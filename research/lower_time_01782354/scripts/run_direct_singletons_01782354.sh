#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

if [[ $# -ne 2 ]]; then
  echo "usage: $0 FRESH_OUTPUT_DIRECTORY FINITE_LOG_DIRECTORY" >&2
  exit 2
fi

root=$(cd "$(dirname "$0")/.." && pwd -P)
finite_logs=$(cd "$2" && pwd -P)
output=$(python3 "$root/scripts/replay_guard.py" prepare "$root" "$1")
source_file=$root/src/lemma_sweep_p23571113.c
verifier=$root/verifiers/verify_direct_singletons_01782354.py

python3 "$root/scripts/replay_guard.py" require "$root" \
  src/lemma_sweep_p23571113.c \
  verifiers/verify_direct_singletons_01782354.py

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
binary=$output/triangle_producer
"${FLINT_CC[@]}" -O3 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" -DTRIANGLE_WEIGHT "$source_file" \
  "${FLINT_LDFLAGS[@]}" -o "$binary" "${FLINT_LIBS[@]}"

mkdir "$output/rows"
specs=(
  "690988 7" "728999 7"
  "729000 6" "774999 6"
  "775000 5" "849999 5"
  "850000 4" "1074999 4"
  "1075000 3" "1100000 3"
  "1100001 3" "1300000 3"
  "1300001 3" "1700000 3"
  "1700001 3" "2200000 3"
  "2200001 3" "2800000 3"
  "2800001 3" "3300000 3"
  "3300001 3" "4050000 3"
)

run_one() {
  local n=$1
  local mode=$2
  "$binary" "$n" "$n" \
    16070 16070 100000 350708 10000000 \
    "$mode" 256 16 0.00025 n > "$output/rows/N_${n}.log"
}

pids=()
labels=()
wait_batch() {
  local failed=0
  local i
  for i in "${!pids[@]}"; do
    if ! wait "${pids[$i]}"; then
      echo "FAIL: direct singleton ${labels[$i]}" >&2
      failed=1
    fi
  done
  pids=()
  labels=()
  [[ $failed -eq 0 ]]
}

for spec in "${specs[@]}"; do
  read -r n mode <<< "$spec"
  run_one "$n" "$mode" &
  pids+=("$!")
  labels+=("N=$n mode=$mode")
  if [[ ${#pids[@]} -eq 4 ]]; then
    wait_batch
  fi
done
wait_batch

direct_log=$output/direct_singletons_01782354.log
: > "$direct_log"
for spec in "${specs[@]}"; do
  read -r n _ <<< "$spec"
  cat "$output/rows/N_${n}.log" >> "$direct_log"
done

python3 "$verifier" "$direct_log" "$finite_logs" \
  | tee "$output/direct_singletons_01782354_verify.log"
echo "RESULT: LOWER-TIME DIRECT SINGLETON REPLAY PASS"
