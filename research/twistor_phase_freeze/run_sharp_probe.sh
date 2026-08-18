#!/usr/bin/env bash
set -euo pipefail

# Unsealed research probe for the source's sharp two-channel L-type branch.
# It intentionally does not define TRIANGLE_WEIGHT.

root=$(cd "$(dirname "$0")/../.." && pwd -P)
output=${1:-"$root/replay/twistor-sharp-probe"}
mkdir -p "$output"

source "$root/scripts/flint_flags.sh"
flint_resolve_flags
source_file="$root/research/lower_time_01782354/src/lemma_sweep_p23571113.c"
binary="${TMPDIR:-/tmp}/twistor-sharp-singleton-$$"
trap 'rm -f "$binary"' EXIT

"${FLINT_CC[@]}" -O3 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" "$source_file" \
  "${FLINT_LDFLAGS[@]}" -o "$binary" "${FLINT_LIBS[@]}"

# Each item is: time numerator over 100000, N, mollifier mode.
times=(${PROBE_TIMES:-13000 12500 12000})
if [[ -n ${PROBE_ROWS:-} ]]; then
  IFS=';' read -r -a rows <<<"$PROBE_ROWS"
else
  rows=(
    "690988 7"
    "850000 4"
    "1075000 3"
    "4050000 3"
  )
fi

for tnum in "${times[@]}"; do
  for spec in "${rows[@]}"; do
    read -r n mtype <<<"$spec"
    log="$output/sharp_t${tnum}_N${n}_m${mtype}.log"
    {
      echo "STATUS: UNSEALED RESEARCH ONLY"
      echo "INVOCATION: sharp_singleton $n $n $tnum $tnum 100000 350708 10000000 $mtype 256 16 0.00025 n"
      LEMMA_DEBUG=1 "$binary" "$n" "$n" \
        "$tnum" "$tnum" 100000 350708 10000000 \
        "$mtype" 256 16 0.00025 n
    } >"$log"
  done
done

{
  echo -e "time_num\tN\tmtype\tstatus\tdebug_lbound"
  for log in "$output"/sharp_t*_N*_m*.log; do
    base=$(basename "$log")
    tnum=$(sed -E 's/^sharp_t([0-9]+)_N.*/\1/' <<<"$base")
    n=$(sed -E 's/^sharp_t[0-9]+_N([0-9]+)_m.*/\1/' <<<"$base")
    mtype=$(sed -E 's/^.*_m([0-9]+)\.log$/\1/' <<<"$base")
    status=$(grep -E '^N ' "$log" | tail -1 || true)
    debug=$(grep -E '^DBG N ' "$log" | tail -1 || true)
    printf '%s\t%s\t%s\t%s\t%s\n' "$tnum" "$n" "$mtype" "$status" "$debug"
  done
} >"$output/summary.tsv"

cat "$output/summary.tsv"
echo "RESULT: UNSEALED SHARP SINGLETON PROBE COMPLETE"
