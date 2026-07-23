#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
vendor="$root/vendor/dbn21a"

check_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$@"
  else
    shasum -a 256 "$@"
  fi
}

manifest_hash=$(check_sha256 "$vendor/UPSTREAM_MANIFEST.sha256" | awk '{print $1}')
expected=dee28651ec9f5295d8c28d9d045e2d2049753cc9f8e84ab0286dc6491fb8de91
if [[ $manifest_hash != "$expected" ]]; then
  echo "error: upstream manifest hash mismatch" >&2
  exit 1
fi

(
  cd "$vendor"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c SELECTED_MANIFEST.sha256
  else
    shasum -a 256 -c SELECTED_MANIFEST.sha256
  fi
)

(
  cd "$vendor/certificates/record/criterion_theorem"
  python3 verify_criterion.py
)
(
  cd "$vendor/certificates/record/error_terms_audit"
  python3 verify_error_audit.py
)
(
  cd "$vendor/certificates/certified1965/site_glue"
  python3 verify_site_glue.py
)
(
  cd "$vendor/certificates/certified1965/site_glue_secondline"
  bash verify.sh
)
(
  cd "$vendor/certificates/certified1875/windslab165_v2"
  python3 verify_windslab165.py
)
echo "[DOCUMENTARY] windslab corner second line is provenance-checked but"
echo "[DOCUMENTARY] is not run as a target gate; it samples only five corners"

echo "RESULT: VENDORED UPSTREAM ARITHMETIC REPLAY PASS"
echo "NOTICE: THIS IS ARTIFACT REPLAY, NOT THEOREM VALIDATION"
