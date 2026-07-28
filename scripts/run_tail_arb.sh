#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")/.." && pwd -P)
requested_output=${1:-"$root/replay/tail_arb"}

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
python3 "$root/scripts/replay_guard.py" require "$root" \
  verifiers/verify_tail_arb.c verifiers/verify_tail_arb_logs.py \
  TAIL_LEMMA.md
output=$(python3 "$root/scripts/replay_guard.py" prepare \
  "$root" "$requested_output")
binary="$output/verify_tail_arb"

"${FLINT_CC[@]}" -O2 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" \
  "$root/verifiers/verify_tail_arb.c" \
  "${FLINT_LDFLAGS[@]}" -o "$binary" "${FLINT_LIBS[@]}"
python3 "$root/scripts/replay_guard.py" require "$output" verify_tail_arb

for bits in 256 512; do
  "$binary" "$bits" > "$output/tail_arb_${bits}.log"
  python3 "$root/scripts/replay_guard.py" require "$output" \
    "tail_arb_${bits}.log"
  grep -Fxq "TOTAL CHECKS: 36; FAILURES: 0" \
    "$output/tail_arb_${bits}.log"
  grep -Fxq "RESULT: ALL ARB TAIL CHECKS PASS" \
    "$output/tail_arb_${bits}.log"
done
python3 "$root/verifiers/verify_tail_arb_logs.py" --log-dir "$output"

if "$binary" 255 > "$output/tail_arb_reject_255.log" 2>&1; then
  echo "FAIL: the Arb tail verifier accepted fewer than 256 bits." >&2
  exit 1
fi
python3 "$root/scripts/replay_guard.py" require "$output" \
  tail_arb_reject_255.log
grep -Fq "refusing precision below 256 bits" \
  "$output/tail_arb_reject_255.log"

if [[ ${RUN_SANITIZERS:-0} == 1 ]]; then
  sanitized="$output/verify_tail_arb_sanitized"
  "${FLINT_CC[@]}" -O1 -g -std=c17 -Wall -Wextra -Werror -pedantic \
    "${FLINT_CPPFLAGS[@]}" \
    -fsanitize=address,undefined -fno-omit-frame-pointer \
    "$root/verifiers/verify_tail_arb.c" \
    "${FLINT_LDFLAGS[@]}" -o "$sanitized" "${FLINT_LIBS[@]}"
  python3 "$root/scripts/replay_guard.py" require "$output" \
    verify_tail_arb_sanitized
  asan_options=halt_on_error=1
  if [[ $(uname -s) != Darwin ]]; then
    asan_options=detect_leaks=1:halt_on_error=1
  fi
  ASAN_OPTIONS="$asan_options" \
    UBSAN_OPTIONS=halt_on_error=1 \
    "$sanitized" 256 > "$output/tail_arb_sanitized.log"
  python3 "$root/scripts/replay_guard.py" require "$output" \
    tail_arb_sanitized.log
  grep -Fxq "TOTAL CHECKS: 36; FAILURES: 0" \
    "$output/tail_arb_sanitized.log"
fi

echo "RESULT: INDEPENDENT ARB TAIL REPLAY PASS"
