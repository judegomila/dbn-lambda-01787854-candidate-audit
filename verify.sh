#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")" && pwd)
cd "$root"

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum -c SHA256SUMS
else
  shasum -a 256 -c SHA256SUMS
fi
python3 verifiers/verify_tail_patch_provenance.py
./scripts/verify_upstream_subset.sh
python3 verifiers/verify_stored_logs.py
python3 verifiers/verify_finite_and_binding.py
python3 verifiers/verify_triangle_normalizer_corr_iv.py --prec 180
python3 verifiers/verify_triangle_normalizer_corr_iv.py --prec 256
python3 verifiers/verify_assembly_1787854.py

echo "RESULT: STORED CANDIDATE PASS"
