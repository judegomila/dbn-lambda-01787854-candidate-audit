#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

if [[ $# -ne 1 ]]; then
  echo "usage: $0 FRESH_OUTPUT_DIRECTORY" >&2
  exit 2
fi

root=$(cd "$(dirname "$0")/.." && pwd -P)
source_file=$root/src/lemma_sweep_p23571113.c
verifier=$root/verifiers/verify_finite_01782354.py
output=$(python3 "$root/scripts/replay_guard.py" prepare "$root" "$1")
image=${IMAGE:-dbn21a-flint}
expected=${EXPECTED_IMAGE_ID:-sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538}

python3 "$root/scripts/replay_guard.py" require "$root" \
  src/lemma_sweep_p23571113.c verifiers/verify_finite_01782354.py

actual=$(docker image inspect --format '{{.Id}}' "$image")
if [[ $actual != "$expected" && ${ALLOW_UNPINNED_IMAGE:-0} != 1 ]]; then
  echo "error: wrong image ID: $actual" >&2
  exit 2
fi

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

started=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
source_sha=$(sha256_file "$source_file")
commit=$(git -C "$root" rev-parse HEAD 2>/dev/null || printf unavailable)
dirty=false
if [[ -n $(git -C "$root" status --porcelain --untracked-files=all) ]]; then
  dirty=true
fi
{
  echo "purpose=exploratory complete finite Triangle replay for 0.1782354"
  echo "started_utc=$started"
  echo "repository_commit=$commit"
  echo "repository_dirty=$dirty"
  echo "producer_sha256=$source_sha"
  echo "container_image=$image"
  echo "container_image_id=$actual"
  echo "target_t=1607/10000"
  echo "target_y2=87677/2500000"
  echo "target_lambda=891177/5000000"
  echo "finite_N=690988..4050000"
} > "$output/REPLAY_METADATA.txt"

docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --tmpfs /tmp:rw,exec,nosuid,size=2g \
  --volume "$source_file:/work/producer.c:ro" \
  --volume "$output:/out" \
  "$image" bash -lc '
set -euo pipefail
gcc -O3 -std=c17 -Wall -Wextra -Werror -pedantic \
  -DTRIANGLE_WEIGHT /work/producer.c -o /tmp/triangle -lflint -lm

run_exact() {
  /tmp/triangle "$1" "$2" \
    16070 16070 100000 350708 10000000 \
    "$3" "$4" "$5" "$6" t
}

run_exact 690988 728999 7 220 14 0.005 \
  > /out/p23571113_690988_728999.log &
p13_pid=$!
run_exact 729000 774999 6 220 14 0.005 \
  > /out/p235711_729000_774999.log &
p11_pid=$!
run_exact 775000 849999 5 220 14 0.005 \
  > /out/p2357_775000_849999.log &
p7_pid=$!
run_exact 850000 1074999 4 220 14 0.005 \
  > /out/p235_850000_1074999.log &
p5_pid=$!
{
  run_exact 1075000 1100000 3 240 16 0.00025 \
    > /out/p23_1075000_1100000.log
  run_exact 1100001 1300000 3 220 14 0.01 \
    > /out/p23_1100001_1300000.log
  run_exact 1300001 1700000 3 220 14 0.01 \
    > /out/p23_1300001_1700000.log
  run_exact 1700001 2200000 3 220 14 0.01 \
    > /out/p23_1700001_2200000.log
  run_exact 2200001 2800000 3 220 14 0.01 \
    > /out/p23_2200001_2800000.log
  run_exact 2800001 3300000 3 220 14 0.01 \
    > /out/p23_2800001_3300000.log
  run_exact 3300001 4050000 3 220 14 0.01 \
    > /out/p23_3300001_4050000.log
} &
p23_pid=$!

wait "$p13_pid"
wait "$p11_pid"
wait "$p7_pid"
wait "$p5_pid"
wait "$p23_pid"
'

python3 "$verifier" "$output" | tee "$output/finite_01782354_verify.log"
finished=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
echo "finished_utc=$finished" >> "$output/REPLAY_METADATA.txt"

if command -v sha256sum >/dev/null 2>&1; then
  (cd "$output" && sha256sum ./*.log ./REPLAY_METADATA.txt) \
    > "$output/REPLAY_SHA256SUMS"
else
  (cd "$output" && shasum -a 256 ./*.log ./REPLAY_METADATA.txt) \
    > "$output/REPLAY_SHA256SUMS"
fi

echo "RESULT: LOWER-TIME FULL FINITE REPLAY PASS"
