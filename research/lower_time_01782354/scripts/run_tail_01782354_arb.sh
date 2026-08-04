#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")/.." && pwd -P)
requested_output=${1:-"$root/replay/tail_01782354_arb"}
source_file=verifiers/verify_tail_01782354_arb.c

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
python3 "$root/scripts/replay_guard.py" require "$root" "$source_file"
output=$(python3 "$root/scripts/replay_guard.py" prepare \
  "$root" "$requested_output")
binary="$output/verify_tail_01782354_arb"

"${FLINT_CC[@]}" -O2 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" \
  "$root/$source_file" \
  "${FLINT_LDFLAGS[@]}" -o "$binary" "${FLINT_LIBS[@]}"
python3 "$root/scripts/replay_guard.py" require "$output" \
  verify_tail_01782354_arb

check_log() {
  local bits=$1
  local log=$2
  grep -Fxq \
    "P1113 lower-time Arb verifier: precision=$bits, N1=4050000, M=153814" \
    "$log"
  [[ $(grep -Fc '[PASS]' "$log") -eq 37 ]]
  ! grep -Fq '[FAIL]' "$log"
  grep -Fxq "TOTAL CHECKS: 37; FAILURES: 0" "$log"
  grep -Fxq "RESULT: ALL ARB LOWER-TIME TAIL CHECKS PASS" "$log"
  [[ $(grep -Fc 'RESULT:' "$log") -eq 1 ]]
  for label in \
    "D upper point" \
    "error upper point" \
    "flow-error lower point" \
    "P enclosure width"
  do
    [[ $(grep -Fc "$label = " "$log") -eq 1 ]]
  done
}

for bits in 256 512; do
  log="$output/tail_01782354_arb_${bits}.log"
  "$binary" "$bits" > "$log"
  python3 "$root/scripts/replay_guard.py" require "$output" \
    "$(basename "$log")"
  check_log "$bits" "$log"
done

if "$binary" 255 > "$output/tail_01782354_reject_255.log" 2>&1; then
  echo "FAIL: lower-time Arb tail verifier accepted fewer than 256 bits." >&2
  exit 1
fi
python3 "$root/scripts/replay_guard.py" require "$output" \
  tail_01782354_reject_255.log
grep -Fq "refusing precision below 256 bits" \
  "$output/tail_01782354_reject_255.log"

if [[ ${RUN_SANITIZERS:-0} == 1 ]]; then
  sanitized="$output/verify_tail_01782354_arb_sanitized"
  "${FLINT_CC[@]}" -O1 -g -std=c17 -Wall -Wextra -Werror -pedantic \
    "${FLINT_CPPFLAGS[@]}" \
    -fsanitize=address,undefined -fno-omit-frame-pointer \
    "$root/$source_file" \
    "${FLINT_LDFLAGS[@]}" -o "$sanitized" "${FLINT_LIBS[@]}"
  python3 "$root/scripts/replay_guard.py" require "$output" \
    verify_tail_01782354_arb_sanitized
  asan_options=halt_on_error=1
  if [[ $(uname -s) != Darwin ]]; then
    asan_options=detect_leaks=1:halt_on_error=1
  fi
  sanitized_log="$output/tail_01782354_arb_sanitized.log"
  ASAN_OPTIONS="$asan_options" \
    UBSAN_OPTIONS=halt_on_error=1 \
    "$sanitized" 256 > "$sanitized_log"
  python3 "$root/scripts/replay_guard.py" require "$output" \
    "$(basename "$sanitized_log")"
  check_log 256 "$sanitized_log"
fi

echo "RESULT: LOWER-TIME INDEPENDENT ARB TAIL REPLAY PASS"
