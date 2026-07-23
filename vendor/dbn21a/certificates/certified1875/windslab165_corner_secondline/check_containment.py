#!/usr/bin/env /usr/bin/python3
"""
check_containment.py -- final gate of the winding-rectangle second-line
corner audit for the wildcard-s32 windslab165_v2 slab (y0 = 33/200 = 0.165).

For each audited (rectangle, corner) of the producer log tloop_6e12_y165.txt
(md5 8b94fb2802034927ba16eeda4414a9c3, banked inside the VERIFIED
wildcard-s32 windslab165_v2 fact): re-derive the |f_t| interval enclosure
from the banked chunk JSONs (exact-rational endpoint summation re-done HERE,
nothing trusted from the producing run beyond the chunk integrals), then
assert:

  (1) lb|f_t(corner)| >= printed_min - SLACK   (one-sided containment: a mesh
      point can never be below the producer's certified mesh minimum;
      SLACK = 1e-9 covers the log's NEAREST-rounded ~20-digit display of t
      propagated through the log's own ddt bound -- max ddt on the audited
      rectangles is 58502, so 58502 * 1e-18 <= 5.9e-14 -- plus the min
      field's own <= 1e-18 display error; 1e-9 exceeds either by >= 1e4)
  (2) lb|f_t(corner)| > 2e-3                   (non-vanishing direction, same
      margin standard as the banked s9 windrect audit at y0 = 0.1809)
  (3) WIDTH gate: every recombined enclosure has exact-rational width
      hi - lo <= 1e-22, per-corner width printed CEIL-truncated so the
      fact's quoted widths are machine-derived here, never transcribed.
  (4) rect 1's t field is EXACTLY 0 in the log (exact-t anchor: zero
      display-rounding slack at both bottom corners).
  (5) NEAREST-display signature gate for the march-boundary rectangle 492
      corner (X,1) IF its enclosure sits below the printed min: the deficit
      must be < half-ulp 5e-20 of the 20-digit NEAREST (arf_printd) display
      -- a rounding-mode signature, not a discrepancy (the s9 rule).

Exit 0 iff all selected corners pass. Every quoted decimal: FLOOR-truncated
lower endpoints / CEIL-truncated upper endpoints, machine-derived.
RH-height dependency: NONE (finite Dirichlet sums, interval arithmetic).
"""
import sys, json, glob, os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SLACK = Fraction(1, 10**9)
ERRBUDGET = Fraction(2, 1000)
WIDTHCAP = Fraction(1, 10**22)
HALF_ULP_20 = Fraction(5, 10**20)

# (tag, rect, corner_desc, printed_min, expected X as (num,den), y, t_str, N)
# selection: seed = SHA256(tloop_6e12_y165.txt) =
# c402ac4ef703a734e865198a848fbd21ad03441025419f5d35897936a2df4009,
# K=2 picks {71 -> corner 2, 223 -> corner 3} + always-included exact-t
# rect 1 (both bottom corners) + always-included final rect 492 (march
# boundary, corner 2 drawn next from the same seeded stream) -- re-derived
# live by verify.sh gate 1 from the log bytes.
AUDITS = [
    ("r1_c0", 1, "(X, y0)", "4.2783620904181587383",
     (6000000185827, 1), "33/200", "0", 690988),
    ("r1_c1", 1, "(X+1, y0)", "4.2783620904181587383",
     (6000000185828, 1), "33/200", "0", 690988),
    ("r71_c2", 71, "(X, 1)", "4.0342498484369228591",
     (6000000185827, 1), "1", "0.0048489160490838339865", 690988),
    ("r223_c3", 223, "(X+1, 1)", "3.4587604271900031770",
     (6000000185828, 1), "1", "0.018728548512163233847", 690988),
    ("r492_c2", 492, "(X, 1)", "1.4714692759513059035",
     (6000000185827, 1), "1", "0.17354959427234065989", 690988),
]

# exact-t gate: rect 1's t field in the log must be the literal 0
T_EXACT_RECT1 = True

# Two-line VALUE-MATCH gate for the corner that turned out to be the
# producer's mesh argmin (enclosure ~ printed min): assert and print the
# exact-rational max |corner - printed_min| against a CEIL cap quoted in
# the fact, and assert the deficit is below the half-ulp 5e-20 of the
# 20-digit NEAREST (arf_printd) display -- a rounding-mode signature, not
# a discrepancy (the banked s9 rule).
AGREEMENT = {  # tag -> max-diff cap (exact Fraction)
    "r223_c3": Fraction("3.10345e-21"),
}


def floor_trunc(fr, digits=12):
    assert fr > 0
    k = 0
    while fr * 10**k < 10 ** (digits - 1):
        k += 1
    while fr * 10**k >= 10**digits:
        k -= 1
    n = (fr * 10**k).numerator // (fr * 10**k).denominator
    s = str(n)
    return s[0] + "." + s[1:] + "e" + str(digits - 1 - k)


def ceil_trunc(fr, digits=6):
    assert fr > 0
    k = 0
    while fr * 10**k < 10 ** (digits - 1):
        k += 1
    while fr * 10**k >= 10**digits:
        k -= 1
    num = fr * 10**k
    n = -((-num.numerator) // num.denominator)
    if n == 10**digits:
        n, k = 10 ** (digits - 1), k - 1
    s = str(n)
    out = s[0] + "." + s[1:] + "e" + str(digits - 1 - k)
    assert Fraction(s[0] + "." + s[1:]) * Fraction(10) ** (digits - 1 - k) >= fr
    return out


def main():
    import subprocess, re
    ok = True
    # gate (4): rect 1 t field exactly 0 in the log
    log = open(os.path.join(HERE, "tloop_6e12_y165.txt")).read()
    m = re.search(r"Rectangle\(1\)\s*:\s*([^,]+),", log)
    assert m and m.group(1).strip() == "0", "rect 1 t not exact 0"
    print("rect 1 t field is the literal 0 (exact-t anchor) PASS")
    for tag, rect, cdesc, pmin, (xn, xd), y, t, N in AUDITS:
        chunks = sorted(c for c in
                        glob.glob(os.path.join(HERE, "runs", f"{tag}_*.json"))
                        if "combined" not in c)
        assert chunks, f"no chunks for {tag}"
        # coverage: chunks tile [1, N] exactly, no gaps/overlaps
        spans = sorted((json.load(open(c))["n_lo"], json.load(open(c))["n_hi"])
                       for c in chunks)
        assert spans[0][0] == 1 and spans[-1][1] == N, (tag, spans[0], spans[-1])
        for (a, b), (c2, d2) in zip(spans, spans[1:]):
            assert c2 == b + 1, (tag, b, c2)
        out = os.path.join(HERE, "runs", f"{tag}_combined.json")
        r = subprocess.run(
            ["/usr/bin/python3", os.path.join(HERE, "windrect_corner_iv.py"),
             "combine", out] + chunks,
            capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout, r.stderr)
            ok = False
            continue
        d = json.load(open(out))
        assert d["X"] == [xn, xd], (tag, d["X"])
        assert Fraction(d["y"]) == Fraction(y), (tag, d["y"])
        assert d["N"] == N, (tag, d["N"])
        lo = Fraction(d["mod_lo"])
        hi = Fraction(d["mod_hi"])
        pm = Fraction(pmin)
        c1 = lo >= pm - SLACK
        c2 = lo > ERRBUDGET
        width = hi - lo
        c3 = width <= WIDTHCAP
        ratio = floor_trunc(lo / pm, 6)
        print(f"rect {rect} corner {cdesc}: lb|f|={floor_trunc(lo)} (FLOOR) "
              f"printed_min={pmin} ratio(lb/min)={ratio} (FLOOR) "
              f"width={ceil_trunc(width)} (CEIL) "
              f"containment={'PASS' if c1 else 'FAIL'} "
              f"nonvanish={'PASS' if c2 else 'FAIL'} "
              f"width<=1e-22={'PASS' if c3 else 'FAIL'}")
        ok = ok and c1 and c2 and c3
        if tag in AGREEMENT:
            maxdiff = max(abs(pm - lo), abs(pm - hi))
            c4 = maxdiff <= AGREEMENT[tag]
            c4b = pm > hi and pm - lo <= HALF_ULP_20
            print(f"  value-match {tag}: max|corner-printed_min|="
                  f"{ceil_trunc(maxdiff)} (CEIL) <= {AGREEMENT[tag]} "
                  f"{'PASS' if c4 else 'FAIL'}; NEAREST-display signature: "
                  f"printed min sits {ceil_trunc(pm - lo)} (CEIL) above the "
                  f"enclosure, < half-ulp 5e-20 of a 20-digit NEAREST "
                  f"display: {'PASS' if c4b else 'FAIL'}")
            ok = ok and c4 and c4b
        if tag == "r492_c2":
            # march-boundary corner: if the printed min sits above my
            # enclosure it must be by < half-ulp of a 20-digit NEAREST
            # display (rounding-mode signature); if my lb exceeds the min
            # the corner simply is not the argmin (print the gap).
            if pm > hi:
                c5 = pm - lo <= HALF_ULP_20
                print(f"  r492 NEAREST-display signature: printed min sits "
                      f"{ceil_trunc(pm - lo)} (CEIL) above the enclosure, "
                      f"< half-ulp 5e-20 of a 20-digit NEAREST display: "
                      f"{'PASS' if c5 else 'FAIL'}")
                ok = ok and c5
            else:
                print(f"  r492 corner above printed min by "
                      f"{floor_trunc(max(lo - pm, width))} (FLOOR of lo-pm "
                      f"or width if straddling) -- corner not the argmin "
                      f"or exact match; containment gate already decisive")
    print("ALL PASS" if ok else "FAILURES PRESENT")
    sys.exit(0 if ok else 1)


main()
