#!/usr/bin/env python3
# verify_windslab165.py -- self-contained verifier for the FOUNDATION
# winding-slab region certificate at y-floor 0.165 (wildcard-s32).
# Reads ONLY files in its own directory. Exit 0 iff ALL checks pass.
#
# This is the TEXT-AMENDED resubmission of the wildcard-s31 claim
# rejected with verdict "COMPUTE CONFIRMED, TEXT GATES FAIL - repair is
# a text amendment, no re-compute needed": the rejecting verifier
# independently recompiled a bit-identical binary from the pinned
# source and re-ran the full y=0.165 leg with byte-identical output.
# The two failure causes were (1) missing FOUNDATION tag on a
# qualifying region certificate, (2) arf_printd NEAREST-rounded digits
# quoted with no rounding-mode label / no floor truncation. Both are
# repaired in the fact text; this script machine-derives every quoted
# truncation with an explicit nearest-halo guard.

import hashlib, os, re, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
def P(name): return os.path.join(HERE, name)

NCHECK = 0
def ok(label, cond, detail=""):
    global NCHECK
    NCHECK += 1
    status = "PASS" if cond else "FAIL"
    print("[%02d] %-58s %s %s" % (NCHECK, label, status, detail))
    if not cond:
        print("RESULT: FAIL")
        sys.exit(1)

def md5(name):
    h = hashlib.md5()
    with open(P(name), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------------------------------------------------------------
# E0: floor-truncation self-tests (both negative-direction cases).
# floor_trunc(fr, k) = the k-decimal-place FLOOR truncation of the
# exact rational fr, as a string. For fr >= 0 this equals ordinary
# digit truncation; self-tests cover negatives too.
# ---------------------------------------------------------------
def floor_trunc(fr, places):
    scaled = fr * 10**places
    fl = scaled.numerator // scaled.denominator  # true floor (works for negatives)
    neg = fl < 0
    s = str(abs(fl)) if not neg else str(fl)[1:]
    # if fl<0, floor already moved AWAY from zero: e.g. floor(-1.23*100)=-123 -> -1.23 exact,
    # floor(-1.234*100)=-124 -> -1.24 (correct floor truncation, magnitude UP)
    s = s.rjust(places + 1, "0")
    out = s[:-places] + "." + s[-places:]
    return ("-" + out) if neg else out

ok("E0a floor_trunc(+1.23456,4) == 1.2345",
   floor_trunc(Fraction(123456, 100000), 4) == "1.2345")
ok("E0b floor_trunc(+0.99999,4) == 0.9999",
   floor_trunc(Fraction(99999, 100000), 4) == "0.9999")
ok("E0c floor_trunc(-1.23451,4) == -1.2346 (floor, not toward-zero)",
   floor_trunc(Fraction(-123451, 100000), 4) == "-1.2346")
ok("E0d floor_trunc(-1.20000,4) == -1.2000 (exact stays exact)",
   floor_trunc(Fraction(-12, 10), 4) == "-1.2000")

# ---------------------------------------------------------------
# G1-G6: md5 pins (tool identity chain, verified wildcard-s31 lineage)
# ---------------------------------------------------------------
ok("G1 md5 TloopthreadedV4.c (pinned source)",
   md5("TloopthreadedV4.c") == "36419d8866f6838a103a81024afdcbfe")
ok("G2 md5 storedsums_6e12.txt (pinned input matrix)",
   md5("storedsums_6e12.txt") == "c188d487c920a4167d78b68fc357f9fa")
ok("G3 md5 tloop binary (bit-identical rebuild pinned by rejecting verifier)",
   md5("tloop") == "204b33c4118ea584d518ac27af7690d5")
ok("G4 md5 tloop_6e12_y165.txt (the y=0.165 leg log)",
   md5("tloop_6e12_y165.txt") == "8b94fb2802034927ba16eeda4414a9c3")
ok("G5 md5 banked_tloop_6e12_y1809.txt (banked barrier_hunter-s2 artifact)",
   md5("banked_tloop_6e12_y1809.txt") == "2a395fe6219af7959b3dd2febc8b981b")
ok("G6 md5 anchor_fresh.txt (verified wildcard-s31 fresh anchor rerun)",
   md5("anchor_fresh.txt") == "68afee397ff2c3a9f5d88646137ae953")

# ---------------------------------------------------------------
# G7-G14: full parse of the y=0.165 leg log
# ---------------------------------------------------------------
y165 = open(P("tloop_6e12_y165.txt")).read().splitlines()

hdr = [l for l in y165 if l.startswith("Processing the barrier")]
ok("G7 exactly one header line", len(hdr) == 1)
HDR_EXPECT = ("Processing the barrier for X= 6000000185827.00000000000000000"
              "...6000000185828.00000000000000000 (N = 690988), "
              "y0 = 0.1650000000...1 , t = 0...0.1809000000")
ok("G8 header == slab [6000000185827,6000000185828], N=690988, y0=0.165..1, t=0..0.1809",
   hdr[0].strip() == HDR_EXPECT, "|" + hdr[0].strip()[:60] + "...|")

RECT_RE = re.compile(
    r"^Rectangle\((\d+)\) : ([0-9.e+-]+), ([0-9.e+-]+), ([0-9.e+-]+), "
    r"([0-9.]+), ([0-9.e+-]+), (\d+)\s*$")
rects = []
for l in y165:
    if l.startswith("Rectangle("):
        m = RECT_RE.match(l)
        ok_parse = m is not None
        if not ok_parse:
            ok("G9 rectangle line parse", False, l[:60])
        rects.append(m.groups())
ok("G9 all 492 Rectangle lines parse; count == 492", len(rects) == 492,
   "count=%d" % len(rects))
ok("G10 indices 1..492 contiguous",
   [int(r[0]) for r in rects] == list(range(1, 493)))

ts = [Fraction(r[1]) for r in rects]
ok("G11 t-march starts at 0 and is STRICTLY monotone increasing",
   ts[0] == 0 and all(ts[i + 1] > ts[i] for i in range(len(ts) - 1)))
ok("G12 every per-rectangle winding field is the exact string 0.0000000000",
   all(r[4] == "0.0000000000" for r in rects))

overall = [l for l in y165 if l.startswith("Overall winding number:")]
ok("G13 overall winding line present once and == 0.000000",
   len(overall) == 1 and overall[0].split(":")[1].strip() == "0.000000",
   "|" + overall[0].strip() + "|")

cw = [l for l in y165 if l.startswith("cpu/wall(s):")]
ok("G14 cpu/wall line == '857.702 189.055'",
   len(cw) == 1 and cw[0].split(":")[1].split() == ["857.702", "189.055"])

# ---------------------------------------------------------------
# G15-G18: DIGIT LAW -- machine-derived floor truncations of the two
# quoted log quantities, with an explicit nearest-halo guard.
# The log strings are arf_printd output: NEAREST-rounded 20-significant-
# digit decimals of the underlying arb midpoints, so the true value v
# satisfies |v - printed| <= 0.5 ulp(printed digit 20) < 1e-18 here.
# A 10-decimal-place FLOOR truncation of the printed string is a valid
# floor truncation of v itself provided the printed tail beyond the
# truncation point exceeds the halo (tail > 1e-18): then
# trunc <= printed - tail + tail = printed - 0 and v > printed - 1e-18
# >= trunc + tail - 1e-18 > trunc. Guard checked explicitly.
# ---------------------------------------------------------------
HALO = Fraction(1, 10**18)

min5 = min(Fraction(r[5]) for r in rects)
last5 = Fraction(rects[-1][5])
ok("G15 min 5th field (min-mesh |(A+B)/B0_eff|) attained at Rectangle(492)",
   min5 == last5 and rects[-1][5] == "1.4714692759513059035")
tail_min5 = min5 - Fraction(floor_trunc(min5, 10))
ok("G16 halo guard: printed-tail beyond 10 places (%s) > 1e-18" % floor_trunc(tail_min5, 15),
   tail_min5 > HALO)
ok("G17 machine floor-10 truncation of min-mesh == 1.4714692759",
   floor_trunc(min5, 10) == "1.4714692759")

tmax = ts[-1]
ok("G18a final t printed string == 0.17354959427234065989",
   rects[-1][1] == "0.17354959427234065989")
tail_t = tmax - Fraction(floor_trunc(tmax, 10))
ok("G18b halo guard for final t: tail > 1e-18", tail_t > HALO)
ok("G18c machine floor-10 truncation of final t == 0.1735495942",
   floor_trunc(tmax, 10) == "0.1735495942")

# ---------------------------------------------------------------
# G19-G22: RUNG-(a) ANCHOR (foundation gate item 2a).
# The SAME binary re-ran the banked barrier_hunter-s2 y0=0.1809 leg
# fresh on this host (verified wildcard-s31 fact): Rectangle+Overall
# projections byte-identical to the banked pod artifact, while timings
# DIFFER (genuine rerun, not a file copy).
# ---------------------------------------------------------------
def proj(name):
    return [l for l in open(P(name)).read().splitlines()
            if l.startswith("Rectangle(") or l.startswith("Overall winding number:")]

pb, pf = proj("banked_tloop_6e12_y1809.txt"), proj("anchor_fresh.txt")
ok("G19 anchor projections: 444 Rectangle lines + 1 Overall line each",
   len(pb) == 445 and len(pf) == 445)
ok("G20 fresh anchor rerun byte-identical to banked artifact on all 445 lines",
   pb == pf)

def cpuwall(name):
    l = [x for x in open(P(name)).read().splitlines() if x.startswith("cpu/wall(s):")]
    return l[0].split(":")[1].split() if l else None

cb, cf = cpuwall("banked_tloop_6e12_y1809.txt"), cpuwall("anchor_fresh.txt")
ok("G21 banked anchor cpu/wall == 255.515/33.8; fresh == 672.509/190.56",
   cb == ["255.515", "33.8"] and cf == ["672.509", "190.56"])
ok("G22 timings DISTINCT while projections identical (genuine rerun law)",
   cb != cf)

# banked anchor header shares slab/N/t-range and storedsums with the new leg
hb = [l for l in open(P("banked_tloop_6e12_y1809.txt")).read().splitlines()
      if l.startswith("Processing the barrier")][0].strip()
ok("G23 anchor header: same slab/N/t-range, y0 = 0.1809..1 (the banked floor)",
   hb == HDR_EXPECT.replace("y0 = 0.1650000000", "y0 = 0.1809000000"))
ok("G24 extension is strict: 492 rects at y-floor 0.165 vs 444 at 0.1809",
   len(rects) == 492 and len(pb) - 1 == 444)

# ---------------------------------------------------------------
# G25-G28: exact design-point coverage arithmetic (Fractions only)
# ---------------------------------------------------------------
t0_hl = Fraction(14913, 80000) - Fraction(33, 200)**2 / 2      # heightlever row
t0_m172 = Fraction(18634552, 10**8) - Fraction(1652, 10**4)**2 / 2  # mass172 row
ok("G25 heightlever t0 = 14913/80000 - (33/200)^2/2 == 108/625 == 0.1728 EXACT",
   t0_hl == Fraction(108, 625) and floor_trunc(t0_hl, 4) == "0.1728")
ok("G26 mass172 t0 = 18634552/10^8 - (1652/10^4)^2/2 == 1727/10000 EXACT",
   t0_m172 == Fraction(1727, 10000) and floor_trunc(t0_m172, 4) == "0.1727")
ok("G27 both t0 inside certified t-range [0, 1809/10^4]",
   0 <= t0_m172 < t0_hl <= Fraction(1809, 10**4))
ok("G28 both row heights on/above certified y-floor 33/200 = 0.165",
   Fraction(33, 200) >= Fraction(165, 1000) and Fraction(1652, 10**4) >= Fraction(165, 1000))

print("TOTAL CHECKS RUN: %d" % NCHECK)
print("RESULT: ALL PASS")
sys.exit(0)
