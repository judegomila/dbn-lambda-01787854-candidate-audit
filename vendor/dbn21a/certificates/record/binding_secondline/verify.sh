#!/bin/bash
# verify.sh -- standalone verifier for the recbind2 second-line bundle.
# Usage: bash verify.sh   (from this directory or any clean copy of it)
# Requires: /usr/bin/python3 with mpmath + sympy. ~2 s, single core.
set -u
cd "$(dirname "$0")"

PY=/usr/bin/python3

# 1. pin the certificate script
want_md5="ada7fcdf09e9d072efbae160443a2f4e"
got_md5=$(md5sum recbind_secondline_iv.py | cut -d' ' -f1)
if [ "$got_md5" != "$want_md5" ]; then
    echo "FAIL: recbind_secondline_iv.py md5 mismatch ($got_md5 != $want_md5)"
    exit 1
fi
echo "[ok] script md5 pinned: $want_md5"

# 2. run the certificate fresh
out=$($PY recbind_secondline_iv.py 2>&1)
rc=$?
echo "$out" | tail -25
if [ $rc -ne 0 ]; then
    echo "FAIL: certificate exited $rc"
    exit 1
fi

# 3. required markers
echo "$out" | grep -q "TOTAL GATES RUN: 35" || { echo "FAIL: gate count != 35"; exit 1; }
echo "$out" | grep -q "RESULT: ALL PASS" || { echo "FAIL: not ALL PASS"; exit 1; }
# the four cross-line digit-match gates must each have passed
for g in "C3 cross-line digit match" "C4 cross-line digit match" \
         "D5 cross-line digit match" "E2 cross-line digit match"; do
    echo "$out" | grep -q "\[PASS\] $g" || { echo "FAIL: missing PASS for '$g'"; exit 1; }
done
echo "[ok] 35/35 gates, all four cross-line digit matches PASS"
echo "VERIFY OK"
exit 0
