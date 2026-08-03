#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

here=$(cd "$(dirname "$0")" && pwd -P)
root=$(cd "$here/../../.." && pwd -P)

anchor=${ANCHOR:-6000342141913}
expected_n=${EXPECTED_N:-691008}
output=${1:-"$root/replay/static-reanchor-$expected_n"}

if [[ ${ACKNOWLEDGE_UNPROVED_NEW_SITE_TAIL:-0} != 1 ]]; then
  echo "error: the existing Taylor-tail checker is pinned to the old X,N" >&2
  echo "set ACKNOWLEDGE_UNPROVED_NEW_SITE_TAIL=1 to run only a transcript smoke pilot" >&2
  exit 2
fi

if [[ -e "$output" ]]; then
  echo "error: output path already exists: $output" >&2
  exit 2
fi
mkdir -p "$output"

source "$root/scripts/flint_flags.sh"
flint_resolve_flags

common=(-O3 "${FLINT_CPPFLAGS[@]}")
"${FLINT_CC[@]}" "${common[@]}" \
  "$root/barrier/src/StoredSumSinglemat_interval.c" \
  "${FLINT_LDFLAGS[@]}" -o "$output/storedsum_interval" \
  "${FLINT_LIBS[@]}"
"${FLINT_CC[@]}" "${common[@]}" \
  "$root/barrier/src/TloopSinglemat_closed_cert.c" \
  "${FLINT_LDFLAGS[@]}" -o "$output/barrier_closed" \
  "${FLINT_LIBS[@]}"

"$output/storedsum_interval" "$anchor" 20 \
  > "$output/storedsum_interval_regenerated.txt"
"$output/barrier_closed" 0 0.16125 0.1809 0 \
  "$output/storedsum_interval_regenerated.txt" \
  > "$output/barrier_target_closed.log"

python3 "$here/validate_barrier_transcript.py" \
  "$output/barrier_target_closed.log" \
  --expected-n "$expected_n"

echo "anchor=$anchor" > "$output/RESEARCH_PARAMETERS.txt"
echo "expected_n=$expected_n" >> "$output/RESEARCH_PARAMETERS.txt"
echo "new_site_taylor_tail=NOT_CERTIFIED" >> "$output/RESEARCH_PARAMETERS.txt"
echo "new_site_uniform_error=NOT_CERTIFIED" >> "$output/RESEARCH_PARAMETERS.txt"
echo "status=unsealed research only" >> "$output/RESEARCH_PARAMETERS.txt"
