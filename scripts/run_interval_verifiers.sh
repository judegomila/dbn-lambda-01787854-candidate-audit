#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

image=${IMAGE:-dbn21a-flint}
expected=${EXPECTED_IMAGE_ID:-sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538}
historical_image_id=sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538
build_manifest=scripts/REVIEW_CONTAINER_INPUTS.sha256
reviewed_build_manifest_sha=5566fe4ad23c9d0612a76d46c6886c978bd90fc610e40cf11b9330d49ad9cfa4

if command -v sha256sum >/dev/null 2>&1; then
  actual_build_manifest_sha=$(sha256sum "$build_manifest" | awk '{print $1}')
  test "$actual_build_manifest_sha" = "$reviewed_build_manifest_sha"
  sha256sum --strict --check "$build_manifest"
else
  actual_build_manifest_sha=$(shasum -a 256 "$build_manifest" | awk '{print $1}')
  test "$actual_build_manifest_sha" = "$reviewed_build_manifest_sha"
  shasum -a 256 -c "$build_manifest"
fi

actual=$(docker image inspect --format '{{.Id}}' "$image")
if [[ $actual != "$expected" && ${ALLOW_UNPINNED_IMAGE:-0} != 1 ]]; then
  echo "error: wrong image ID: $actual" >&2
  exit 2
fi
if [[ $actual != "$historical_image_id" ]]; then
  test "$(docker image inspect --format '{{.Os}}/{{.Architecture}}' "$image")" = \
    linux/amd64
  test "$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.base.digest"}}' \
    "$image")" = \
    sha256:52df9b1ee71626e0088f7d400d5c6b5f7bb916f8f0c82b474289a4ece6cf3faf
  test "$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.dbn.ubuntu-snapshot"}}' \
    "$image")" = 20260723T000000Z
  test "$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.dbn.platform"}}' \
    "$image")" = linux/amd64
  test "$(docker image inspect --format \
    '{{index .Config.Labels "org.opencontainers.image.source"}}' \
    "$image")" = \
    https://github.com/judegomila/dbn-lambda-01787854-candidate-audit
fi

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

for precision in 180 256; do
  docker run --rm -i --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges \
    --user "$(id -u):$(id -g)" \
    --tmpfs /tmp:rw,exec,nosuid,size=512m \
    "$image" bash -lc \
    "gcc -O2 -DPREC=$precision -x c - -o /tmp/triangle_y_dini -lflint -lm &&
     /tmp/triangle_y_dini" \
    < verifiers/verify_triangle_y_dini_arb.c \
    > "$scratch/triangle_y_dini_${precision}.log"
  cmp \
    "logs/triangle_y_dini_${precision}.log" \
    "$scratch/triangle_y_dini_${precision}.log"
done

python3 verifiers/verify_triangle_normalizer_corr_iv.py --prec 180 \
  > "$scratch/normalizer_180.log"
python3 verifiers/verify_triangle_normalizer_corr_iv.py --prec 256 \
  > "$scratch/normalizer_256.log"
grep -q "RESULT ALL PASS precision 180" "$scratch/normalizer_180.log"
grep -q "RESULT ALL PASS precision 256" "$scratch/normalizer_256.log"

python3 verifiers/verify_tail_1787854_160.py > "$scratch/tail_160.log"
python3 verifiers/verify_tail_1787854_256.py > "$scratch/tail_256.log"
grep -q "TOTAL CHECKS RUN: 93" "$scratch/tail_160.log"
grep -q "TOTAL CHECKS RUN: 93" "$scratch/tail_256.log"
grep -q "RESULT: ALL PASS" "$scratch/tail_160.log"
grep -q "RESULT: ALL PASS" "$scratch/tail_256.log"

python3 verifiers/verify_finite_and_binding.py
python3 verifiers/verify_assembly_1787854.py

echo "RESULT: FRESH INTERVAL VERIFIERS PASS"
