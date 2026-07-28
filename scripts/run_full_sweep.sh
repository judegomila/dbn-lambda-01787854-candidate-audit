#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

if [[ $# -ne 1 ]]; then
  echo "usage: $0 EMPTY_OUTPUT_DIRECTORY" >&2
  exit 2
fi

root=$(cd "$(dirname "$0")/.." && pwd -P)
source_file=$root/src/lemma_sweep_p235711.c
compare=$root/scripts/compare_full_sweep.py
build_manifest=$root/scripts/REVIEW_CONTAINER_INPUTS.sha256
reviewed_build_manifest_sha=1dbed4db14784e2764190039aa5fca014f25fd6a9d63e9b7f3730a935942159d
requested_output=$1
image=${IMAGE:-dbn21a-flint}
expected=${EXPECTED_IMAGE_ID:-sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

requested_build_manifest_sha=${EXPECTED_BUILD_MANIFEST_SHA256:-$reviewed_build_manifest_sha}
if [[ $requested_build_manifest_sha != "$reviewed_build_manifest_sha" ]]; then
  echo "error: unreviewed build-manifest identity requested" >&2
  exit 2
fi
actual_build_manifest_sha=$(sha256_file "$build_manifest")
if [[ $actual_build_manifest_sha != "$reviewed_build_manifest_sha" ]]; then
  echo "error: reviewed container build-input manifest has changed" >&2
  exit 2
fi
if command -v sha256sum >/dev/null 2>&1; then
  (cd "$root" && sha256sum --strict --check "$build_manifest")
else
  (cd "$root" && shasum -a 256 -c "$build_manifest")
fi

python3 "$root/scripts/replay_guard.py" require "$root" \
  src/lemma_sweep_p235711.c scripts/compare_full_sweep.py

repository_dirty=false
if git -C "$root" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    && [[ -n $(git -C "$root" status --porcelain --untracked-files=all) ]]; then
  repository_dirty=true
fi
if [[ $repository_dirty == true && ${ALLOW_DIRTY_REPO:-0} != 1 ]]; then
  echo "error: refusing a complete replay from a dirty repository" >&2
  exit 2
fi

output=$(python3 "$root/scripts/replay_guard.py" prepare \
  "$root" "$requested_output")

actual=$(docker image inspect --format '{{.Id}}' "$image")
if [[ $actual != "$expected" && ${ALLOW_UNPINNED_IMAGE:-0} != 1 ]]; then
  echo "error: wrong image ID: $actual" >&2
  exit 2
fi
if [[ $actual != sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538 ]]; then
  platform_label=$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.dbn.platform"}}' "$image")
  base_label=$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.base.digest"}}' "$image")
  snapshot_label=$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.dbn.ubuntu-snapshot"}}' "$image")
  source_label=$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.source"}}' "$image")
  if [[ $platform_label != linux/amd64 \
      || $base_label != sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf \
      || $snapshot_label != 20260723T000000Z \
      || $source_label != https://github.com/judegomila/dbn-lambda-01787854-candidate-audit ]]; then
    echo "error: image labels do not match the reviewed build identity" >&2
    exit 2
  fi
fi

source_sha=$(sha256_file "$source_file")
started=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
commit=$(git -C "$root" rev-parse HEAD 2>/dev/null || printf 'unavailable')
platform=$(docker image inspect --format '{{.Os}}/{{.Architecture}}' "$image")
{
  echo "purpose=complete finite Triangle replay"
  echo "started_utc=$started"
  echo "repository_commit=$commit"
  echo "repository_dirty=$repository_dirty"
  echo "producer_sha256=$source_sha"
  echo "review_container_inputs_sha256=$actual_build_manifest_sha"
  echo "command=IMAGE=$image EXPECTED_IMAGE_ID=$expected ./scripts/run_full_sweep.sh $output"
  echo "container_image=$image"
  echo "container_image_id=$actual"
  echo "container_platform=$platform"
  docker run --rm --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges \
    --user "$(id -u):$(id -g)" \
    --tmpfs /tmp:rw,exec,nosuid,size=256m \
    "$image" bash -lc \
    'gcc --version | head -n 1; dpkg-query -W libflint-dev libgmp-dev libmpfr-dev 2>/dev/null || true'
} > "$output/REPLAY_METADATA.txt"

# Refuse to spend compute unless this exact bind mount is host-visible.
probe=.triangle_bind_mount_probe
docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --volume "$output:/out" "$image" \
  bash -lc "printf '%s\\n' visible > /out/$probe"
if [[ ! -f "$output/$probe" ]] \
    || [[ $(<"$output/$probe") != visible ]]; then
  echo "error: Docker bind mount is not host-visible: $output" >&2
  exit 2
fi
rm -f "$output/$probe"

docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --tmpfs /tmp:rw,exec,nosuid,size=2g \
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

finished=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
echo "finished_utc=$finished" >> "$output/REPLAY_METADATA.txt"
if command -v sha256sum >/dev/null 2>&1; then
  (
    cd "$output"
    sha256sum ./*.log ./REPLAY_METADATA.txt
  ) > "$output/REPLAY_SHA256SUMS"
else
  (
    cd "$output"
    shasum -a 256 ./*.log ./REPLAY_METADATA.txt
  ) > "$output/REPLAY_SHA256SUMS"
fi
echo "RESULT: FULL SWEEP REPLAY AND METADATA PASS"
