#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")/.." && pwd -P)
requested_output=${1:-"$root/replay/direct_singletons"}

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
python3 "$root/scripts/replay_guard.py" require "$root" \
  src/lemma_sweep_p235711.c verifiers/verify_direct_singletons.py
output=$(python3 "$root/scripts/replay_guard.py" prepare \
  "$root" "$requested_output")
mkdir -p "$output/p11"
producer="$output/triangle_producer"
log="$output/direct_singletons_256.log"

"${FLINT_CC[@]}" -O3 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" \
  -DTRIANGLE_WEIGHT "$root/src/lemma_sweep_p235711.c" \
  "${FLINT_LDFLAGS[@]}" -o "$producer" "${FLINT_LIBS[@]}"
python3 "$root/scripts/replay_guard.py" require "$output" triangle_producer
: > "$log"

run_exact() {
  local n=$1
  "$producer" "$n" "$n" \
    16125 16125 100000 350708 10000000 \
    6 256 16 0.00025 n
}

run_box() {
  local n=$1
  local mtype=$2
  "$producer" "$n" "$n" \
    161250000 161250001 1000000000 350708 10000000 \
    "$mtype" 256 16 0.00025 n
}

run_exact 690988 >> "$log"
pids=()
pid_labels=()
wait_batch() {
  local failed=0
  local index
  for index in "${!pids[@]}"; do
    if ! wait "${pids[$index]}"; then
      echo "FAIL: direct singleton N=${pid_labels[$index]} failed." >&2
      failed=1
    fi
  done
  pids=()
  pid_labels=()
  [[ $failed -eq 0 ]]
}

for n in 690995 690996 691500 691501 697000 697001 728999; do
  run_exact "$n" > "$output/p11/N_${n}.log" &
  pids+=("$!")
  pid_labels+=("$n")
  if [[ ${#pids[@]} -eq 3 ]]; then
    wait_batch
  fi
done
wait_batch
python3 "$root/scripts/replay_guard.py" require "$output" \
  p11/N_690995.log p11/N_690996.log p11/N_691500.log \
  p11/N_691501.log p11/N_697000.log p11/N_697001.log \
  p11/N_728999.log
for n in 690995 690996 691500 691501 697000 697001 728999; do
  cat "$output/p11/N_${n}.log" >> "$log"
done

run_box 729000 5 >> "$log"
run_box 818999 5 >> "$log"
run_box 819000 4 >> "$log"
run_box 1027999 4 >> "$log"
for n in \
  1028000 1030000 1030001 1050000 1050001 1100000 \
  1100001 1300000 1300001 1700000 1700001 2200000 \
  2200001 2800000 2800001 3300000 3300001 3840000
do
  run_box "$n" 3 >> "$log"
done

python3 "$root/scripts/replay_guard.py" require "$output" \
  direct_singletons_256.log
python3 "$root/verifiers/verify_direct_singletons.py" "$log"
echo "RESULT: FRESH DIRECT SINGLETON REPLAY PASS"
