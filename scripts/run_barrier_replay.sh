#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")/.." && pwd -P)
requested_output=${1:-"$root/replay/barrier"}

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
python3 "$root/scripts/replay_guard.py" require "$root" \
  barrier/src/StoredSumSinglemat_interval.c \
  barrier/src/StoredSumTaylorTail_cert.c \
  barrier/src/TloopSinglemat_closed_cert.c \
  barrier/src/verify_uniform_error_01787854.c \
  barrier/data/storedsum_nolemma_6000000185827_dig_20.txt \
  barrier/compare_storedsum_intervals.py \
  verifiers/verify_barrier_binding.py
output=$(python3 "$root/scripts/replay_guard.py" prepare \
  "$root" "$requested_output")

common=(-O3 "${FLINT_CPPFLAGS[@]}")
"${FLINT_CC[@]}" "${common[@]}" \
  "$root/barrier/src/StoredSumSinglemat_interval.c" \
  "${FLINT_LDFLAGS[@]}" -o "$output/storedsum_interval" "${FLINT_LIBS[@]}"
"${FLINT_CC[@]}" "${common[@]}" \
  "$root/barrier/src/StoredSumTaylorTail_cert.c" \
  "${FLINT_LDFLAGS[@]}" -o "$output/storedsum_taylor_tail" "${FLINT_LIBS[@]}"
"${FLINT_CC[@]}" "${common[@]}" \
  "$root/barrier/src/TloopSinglemat_closed_cert.c" \
  "${FLINT_LDFLAGS[@]}" -o "$output/barrier_closed" "${FLINT_LIBS[@]}"
"${FLINT_CC[@]}" -O2 "${FLINT_CPPFLAGS[@]}" \
  "$root/barrier/src/verify_uniform_error_01787854.c" \
  "${FLINT_LDFLAGS[@]}" -o "$output/uniform_error" "${FLINT_LIBS[@]}"
python3 "$root/scripts/replay_guard.py" require "$output" \
  storedsum_interval storedsum_taylor_tail barrier_closed uniform_error

"$output/storedsum_interval" 6000000185827 20 \
  > "$output/storedsum_interval_regenerated.txt"
python3 "$root/scripts/replay_guard.py" require "$output" \
  storedsum_interval_regenerated.txt
python3 "$root/barrier/compare_storedsum_intervals.py" \
  "$root/barrier/data/storedsum_nolemma_6000000185827_dig_20.txt" \
  "$output/storedsum_interval_regenerated.txt" \
  > "$output/storedsum_provenance.log"
python3 "$root/scripts/replay_guard.py" require "$output" \
  storedsum_provenance.log
"$output/storedsum_taylor_tail" \
  > "$output/storedsum_taylor_tail.log"
python3 "$root/scripts/replay_guard.py" require "$output" \
  storedsum_taylor_tail.log
"$output/uniform_error" \
  > "$output/uniform_error.log"
python3 "$root/scripts/replay_guard.py" require "$output" uniform_error.log
"$output/barrier_closed" 0 0.16125 0.1809 0 \
  "$root/barrier/data/storedsum_nolemma_6000000185827_dig_20.txt" \
  > "$output/barrier_target_closed.log"
python3 "$root/scripts/replay_guard.py" require "$output" \
  barrier_target_closed.log

BARRIER_LOG="$output/barrier_target_closed.log" \
BARRIER_TAIL_LOG="$output/storedsum_taylor_tail.log" \
BARRIER_PROVENANCE_LOG="$output/storedsum_provenance.log" \
BARRIER_REGENERATED="$output/storedsum_interval_regenerated.txt" \
BARRIER_UNIFORM_ERROR_LOG="$output/uniform_error.log" \
  python3 "$root/verifiers/verify_barrier_binding.py"

echo "RESULT: FRESH CLOSED-BARRIER REPLAY PASS"
