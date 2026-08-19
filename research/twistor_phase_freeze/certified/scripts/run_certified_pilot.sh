#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/../../../.." && pwd -P)
out=${1:?usage: run_certified_pilot.sh OUTPUT_DIR}
mkdir -p "$out"

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
src="$root/research/twistor_phase_freeze/certified/src/coupled_scalar_obstruction_014.c"
bin="$out/coupled_scalar_obstruction_014"

"${FLINT_CC[@]}" -O2 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" "$src" "${FLINT_LDFLAGS[@]}" \
  -o "$bin" "${FLINT_LIBS[@]}"

for bits in 256 512; do
  "$bin" "$bits" > "$out/coupled_scalar_${bits}.log"
  grep -Fxq "RESULT: CERTIFIED SCALAR OBSTRUCTION FOR 0.14 PHASE-FREEZE LANE" \
    "$out/coupled_scalar_${bits}.log"
done

if "$bin" 255 > "$out/coupled_scalar_reject_255.log" 2>&1; then
  echo "FAIL: verifier accepted 255 bits" >&2
  exit 1
fi

python3 "$root/research/twistor_phase_freeze/certified/verifiers/verify_coupled_scalar_logs.py" \
  --log-dir "$out"

echo "RESULT: CERTIFIED TWISTOR-PHASE PILOT PASS"
