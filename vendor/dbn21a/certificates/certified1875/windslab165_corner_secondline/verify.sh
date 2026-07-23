#!/bin/bash
# verify.sh -- standalone verifier for the windslab165_v2 winding-rectangle
# corner audit (numerics_verifier, s39). Reads ONLY this directory.
# Exit 0 iff every gate passes.
set -e
cd "$(dirname "$0")"
PY=/usr/bin/python3

echo "== gate 0: artifact integrity (md5 pinned in wildcard-s32's verified windslab165_v2 fact)"
echo "8b94fb2802034927ba16eeda4414a9c3  tloop_6e12_y165.txt" | md5sum -c -

echo "== gate 1: hash-seeded selection re-derived from log bytes"
$PY select_rects.py tloop_6e12_y165.txt 2 > /tmp/windslab165_sel.$$
grep -q "seed_sha256 c402ac4ef703a734e865198a848fbd21ad03441025419f5d35897936a2df4009" /tmp/windslab165_sel.$$
grep -q "rect_count 492" /tmp/windslab165_sel.$$
grep -q "^rect 71 .* corners 2$" /tmp/windslab165_sel.$$   # rect 71 -> corner (X,1)
grep -q "^rect 223 .* corners 3$" /tmp/windslab165_sel.$$  # rect 223 -> corner (X+1,1)
grep -q "^rect 492 .* corners 2$" /tmp/windslab165_sel.$$  # final-rect anchor -> corner (X,1)
cat /tmp/windslab165_sel.$$; rm /tmp/windslab165_sel.$$

echo "== gate 2: zero-foreign-toolchain (no ARB/pari/sibling imports)"
$PY - <<'EOF'
import ast, re
src = open("windrect_corner_iv.py").read()
tree = ast.parse(src)
allowed = {"sys", "json", "fractions", "mpmath"}
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for a in node.names:
            assert a.name.split(".")[0] in allowed, a.name
    elif isinstance(node, ast.ImportFrom):
        assert node.module.split(".")[0] in allowed, node.module
lines = src.splitlines()
docstr_spans = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
            and isinstance(node.value.value, str):
        docstr_spans.update(range(node.lineno, node.end_lineno + 1))
bad = re.compile(r"arb_|flint|acb_|\bpari\b|dbn_upper_bound", re.I)
for i, ln in enumerate(lines, 1):
    if i in docstr_spans:
        continue
    ln = ln.split("#")[0]
    assert not bad.search(ln), (i, ln)
print("imports OK:", sorted(allowed), "; no foreign-toolchain references in code")
EOF

echo "== gate 3: chunk coverage + exact recombination + containment"
$PY check_containment.py

echo "== gate 4: one hash-chosen chunk recomputed LIVE and matched"
$PY - <<'EOF'
import hashlib, random, glob, json, subprocess, os
raw = open("tloop_6e12_y165.txt", "rb").read()
rng = random.Random(int(hashlib.sha256(raw).hexdigest(), 16) + 1)  # +1: independent of selection stream
chunks = sorted(glob.glob("runs/r1_c0_*.json"))
chunks = [c for c in chunks if "combined" not in c]
pick = rng.choice(chunks)
d = json.load(open(pick))
out = "/tmp/windslab165_live_chunk.json"
subprocess.run(["/usr/bin/python3", "windrect_corner_iv.py", "corner",
                str(d["X"][0]), str(d["X"][1]), d["y"], d["t"], str(d["N"]),
                str(d["n_lo"]), str(d["n_hi"]), out], check=True)
e = json.load(open(out))
for k in ("A_re", "A_im", "B_re", "B_im"):
    assert d[k] == e[k], (pick, k)
print("live chunk", pick, f"[{d['n_lo']},{d['n_hi']}] matches banked endpoints EXACTLY")
os.remove(out)
EOF

echo "ALL GATES PASS"
