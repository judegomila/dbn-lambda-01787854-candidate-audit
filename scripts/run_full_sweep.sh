#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 EMPTY_OUTPUT_DIRECTORY" >&2
  exit 2
fi

root=$(cd "$(dirname "$0")/.." && pwd)
source_file=$root/src/lemma_sweep_p235711.c
compare=$root/scripts/compare_full_sweep.py
output=$1
image=${IMAGE:-dbn21a-flint}
expected=sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538

mkdir -p "$output"
if [[ -n $(find "$output" -mindepth 1 -maxdepth 1 -print -quit) ]]; then
  echo "error: output directory must be empty: $output" >&2
  exit 2
fi
output=$(cd "$output" && pwd)

actual=$(docker image inspect --format '{{.Id}}' "$image")
if [[ $actual != "$expected" && ${ALLOW_UNPINNED_IMAGE:-0} != 1 ]]; then
  echo "error: wrong image ID: $actual" >&2
  exit 2
fi

# Refuse to spend compute unless this exact bind mount is host-visible.
probe=.triangle_bind_mount_probe
docker run --rm --volume "$output:/out" "$image" \
  bash -lc "printf '%s\\n' visible > /out/$probe"
if [[ ! -f "$output/$probe" ]] \
    || [[ $(<"$output/$probe") != visible ]]; then
  echo "error: Docker bind mount is not host-visible: $output" >&2
  exit 2
fi
rm -f "$output/$probe"

docker run --rm \
  --volume "$source_file:/work/producer.c:ro" \
  --volume "$output:/out" \
  "$image" bash -lc '
set -euo pipefail
gcc -O3 -DTRIANGLE_WEIGHT /work/producer.c -o /tmp/triangle -lflint -lm

run_exact() {
  lo=$1
  hi=$2
  /tmp/triangle "$lo" "$hi" \
    16125 16125 100000 350708 10000000 \
    6 220 14 0.005 t
}

run_later() {
  lo=$1
  hi=$2
  mode=$3
  precision=$4
  order=$5
  half_width=$6
  /tmp/triangle "$lo" "$hi" \
    161250000 161250001 1000000000 350708 10000000 \
    "$mode" "$precision" "$order" "$half_width" t
}

{
  {
    run_exact 690988 690988
    run_exact 690989 690990
    run_exact 690991 690995
  } > /out/p235711_690988_690995.log
  {
    run_exact 690996 691010
    run_exact 691011 691050
    run_exact 691051 691150
    run_exact 691151 691500
  } > /out/p235711_690996_691500.log
  {
    run_exact 691501 693000
    run_exact 693001 697000
  } > /out/p235711_691501_697000.log
  {
    run_exact 697001 707000
    run_exact 707001 718000
    run_exact 718001 728999
  } > /out/p235711_697001_728999.log
} &
p11_pid=$!

run_later 729000 818999 5 200 14 0.005 \
  > /out/p2357_729000_818999.log &
p7_pid=$!

run_later 819000 1027999 4 200 14 0.005 \
  > /out/p235_819000_1027999.log &
p235_pid=$!

{
  run_later 1028000 1030000 3 240 16 0.00025 \
    > /out/p23_1028000_1030000.log
  run_later 1030001 1050000 3 240 16 0.00025 \
    > /out/p23_1030001_1050000.log
  run_later 1050001 1100000 3 220 14 0.002 \
    > /out/p23_1050001_1100000.log
  run_later 1100001 1300000 3 220 14 0.01 \
    > /out/p23_1100001_1300000.log
  run_later 1300001 1700000 3 220 14 0.01 \
    > /out/p23_1300001_1700000.log
  run_later 1700001 2200000 3 220 14 0.01 \
    > /out/p23_1700001_2200000.log
  run_later 2200001 2800000 3 220 14 0.01 \
    > /out/p23_2200001_2800000.log
  run_later 2800001 3300000 3 220 14 0.01 \
    > /out/p23_2800001_3300000.log
  run_later 3300001 3840000 3 220 14 0.01 \
    > /out/p23_3300001_3840000.log
} &
p23_pid=$!

wait "$p11_pid"
wait "$p7_pid"
wait "$p235_pid"
wait "$p23_pid"
'

python3 "$compare" "$output"
