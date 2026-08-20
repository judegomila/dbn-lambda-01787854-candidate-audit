#!/usr/bin/env bash
set -euo pipefail

unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME
export PYTHONDONTWRITEBYTECODE=1

root=$(cd "$(dirname "$0")" && pwd)
cd "$root"

python3 scripts/seal.py --check
python3 verifiers/verify_external_exposition.py

# Independently written recomputations of two published constants.  This
# binds the displayed digits to a fresh calculation; the sealed lanes
# below only ever gated on weaker bounds around them.  Sub-second.
# (The prop410 leg is a same-backend mpmath replay: corroboration only.)
python3 verifiers/verify_independent_crosscheck.py

# Authoritative FLINT/Arb certificates for the Proposition 4.10 uniform
# error budget.  The strict parser rejects missing/duplicated gates,
# malformed balls, altered parameters, or failed decisive inequalities.
# Also executed inside the assembly below as prerequisite P17.
python3 verifiers/verify_prop410_arb_logs.py

# Historical upstream artifacts are retained and checked for provenance.
# The repaired target barrier does not consume the old winding/site result.
./scripts/verify_upstream_subset.sh

# This is the fail-closed target entry point.  It executes every stored
# finite/native/window/tail/barrier prerequisite before the exact criterion
# arithmetic can reach its terminal conclusion.
python3 verifiers/verify_assembly_1787854.py

echo "RESULT: STORED UNCONDITIONAL-PROOF REVIEW PASS"
