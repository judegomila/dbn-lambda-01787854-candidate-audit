#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")" && pwd)
cd "$root"

python3 scripts/seal.py --check

# Historical upstream artifacts are retained and checked for provenance.
# The repaired target barrier does not consume the old winding/site result.
./scripts/verify_upstream_subset.sh

# This is the fail-closed target entry point.  It executes every stored
# finite/native/window/tail/barrier prerequisite before the exact criterion
# arithmetic can reach its terminal conclusion.
python3 verifiers/verify_assembly_1787854.py

echo "RESULT: STORED UNCONDITIONAL-CANDIDATE REVIEW PASS"
