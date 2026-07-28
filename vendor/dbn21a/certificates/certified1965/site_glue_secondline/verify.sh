#!/bin/bash
# Verifier for the siteglue second line. Self-contained: reads only this
# directory. Expected: exit 0 in ~1 s.
set -u
cd "$(dirname "$0")"
PY=/usr/bin/python3
fail() { echo "VERIFY FAIL: $1"; exit 1; }

# 1) pin the second-line script
md5=$(md5sum siteglue_pureint.py | cut -d' ' -f1)
[ "$md5" = "12bb96a9c648e6d2dd19bbcb05fb7248" ] || fail "md5 mismatch for siteglue_pureint.py (got $md5)"

# 2) zero-foreign-toolchain gate: the script must import ONLY fractions+math
$PY - <<'EOF' || exit 1
import ast, sys
tree = ast.parse(open('siteglue_pureint.py').read())
mods = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        mods |= {a.name.split('.')[0] for a in node.names}
    elif isinstance(node, ast.ImportFrom):
        mods.add(node.module.split('.')[0])
allowed = {'fractions', 'math'}
bad = mods - allowed
if bad:
    print("VERIFY FAIL: foreign imports", bad); sys.exit(1)
print("import audit OK:", sorted(mods))
EOF
[ $? -eq 0 ] || fail "import audit"

# 3) live re-run
out=$($PY siteglue_pureint.py 2>&1); rc=$?
echo "$out" | tail -4
[ $rc -eq 0 ] || fail "live run exit $rc"
echo "$out" | grep -q "^TOTAL CHECKS RUN: 30$" || fail "expected 30 checks"
echo "$out" | grep -q "^PASS: 30  FAIL: 0$" || fail "expected 30/0"
echo "$out" | grep -q "^RESULT: ALL PASS$" || fail "ALL PASS line missing"

# 4) load-bearing pinned-literal gates present in the live output
for g in U1a U1b U2a U2b R5b R6b A1 A2 S1 S2 S3; do
  echo "$out" | grep -q "^PASS $g " || fail "gate $g not PASS in live run"
done
# the producer's literals appear machine-derived in the live log
for lit in 5377392.8789 11989041.1415 5377393.0179 11989041.1446 0.3096430277 0.6903569064; do
  echo "$out" | grep -q "$lit" || fail "pinned literal $lit absent from live log"
done

# 5) live PASS lines byte-identical to the pinned run_log.txt
diff <(echo "$out" | grep '^PASS') <(grep '^PASS' run_log.txt) \
  || fail "live PASS lines differ from pinned run_log.txt"

echo "VERIFY OK: siteglue second line reproduces (30/30, pinned literals machine-derived)"
exit 0
