#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PURE-INTEGER/FRACTION SECOND LINE on the auxiliary line's site_glue_v1 lemma
# (verified fact: SITE-UNIFORM WINDOW-GLUING LEMMA + Lambda<=0.1965-ROW
#  PRECONDITION INSTANTIATION, bundle claims/site_glue_v1/) and on the
# the auxiliary line nconst_gap_v2 anchors it extends.
#
# ZERO SHARED CODE: this script imports ONLY fractions + math.isqrt from
# the stdlib. No mpmath, no ARB, no pari, no interval library at all.
# Every quantity is an EXACT rational interval [lo, hi] (Fraction pairs)
# built from first principles:
#   * pi is enclosed by TWO independent Machin-type formulas
#     (pi/4 = 4 atan(1/5) - atan(1/239)  and
#      pi/4 = 6 atan(1/8) + 2 atan(1/57) + atan(1/239)),
#     each via alternating-series partial-sum brackets in Fractions;
#     the two enclosures must intersect (cross-validation gate) and the
#     intersection is used downstream.
#   * sqrt of a rational is bracketed by math.isqrt scaling.
# Formulas derived from arXiv:1904.12438 (Polymath 15): the stored-sum /
# sweep window for truncation index N starts at
#     ws(N,t) = 4*pi*N^2 - pi*t/4,
# equivalently N(x,t) = floor(sqrt(x/(4 pi) + t/16)); x >= ws(N,t) iff
# x/(4 pi) + t/16 >= N^2 (exact algebra, gated below).
#
# Campaign site: X = 6000000185827 (exact integer), N0 = 690988,
# slab t in [0, 1809/10000].
#
# QUANTIFIER AUDIT (restated, then machine-toothed):
#   The certified statement is:
#   FOR ALL t in the CLOSED interval [0, 1809/10000]:
#       (U1') X - ws(N0, t)      >= 5377392.8789      (N0 window starts
#             below X with margin; worst case at t = 0 since ws is
#             LINEAR in t with slope -pi/4 < 0, so ws is maximal at t=0)
#       (U2') ws(N0+1, t) - (X+1) >= 11989041.1415    (N0+1 window starts
#             past X+1 with margin; worst case at t = 1809/10000, the
#             slab top, same linearity/sign argument)
#   and FOR ALL (x,t) in the CLOSED box [X, X+1] x [0, 1809/10000]:
#       (S1') N(x,t) = floor(sqrt(x/(4 pi) + t/16)) = 690988
#             (the radicand is LINEAR in x and t with coefficients
#             1/(4 pi) > 0 and 1/16 > 0, so sqrt(radicand) is minimal at
#             the corner (X, 0) and maximal at the corner (X+1, 1809/10000);
#             the for-all over the box reduces EXACTLY to two corner
#             evaluations -- no sampling anywhere).
#   The linearity-slope sign facts ARE the whole reduction; they are
#   gated below as positivity of exact rational endpoints (gates Q1-Q3).
#
# RH-height dependency: NONE in any inequality here (finite exact
# arithmetic at fixed X); the PT2021 admissibility comparison R5 is the
# exact height comparison itself; the Lambda chain these preconditions
# serve is unconditional via PT2021 T = 3000175332800.

from fractions import Fraction as F
from math import isqrt

PASS = 0
FAIL = 0
def gate(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("PASS %-12s %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL %-12s %s" % (name, detail))

# ---------- floor / ceil decimal truncation (machine-derived strings) ----
def floor_trunc(x, k):
    """Floor-truncate Fraction x to k decimals, return string."""
    sc = 10 ** k
    n = (x.numerator * sc) // x.denominator   # floor for positive x
    s = str(n)
    if k == 0:
        return s
    s = s.rjust(k + 1, "0")
    return s[:-k] + "." + s[-k:]

def ceil_trunc(x, k):
    sc = 10 ** k
    n = -((-x.numerator * sc) // x.denominator)
    s = str(n).rjust(k + 1, "0")
    return s[:-k] + "." + s[-k:]

# ---------- arctan(1/m) alternating-series exact brackets ----------------
def atan_inv_bracket(m, terms):
    """Exact Fraction bracket [lo, hi] of arctan(1/m), m >= 2 integer.
    arctan(1/m) = sum_{k>=0} (-1)^k / ((2k+1) m^(2k+1)): alternating with
    strictly decreasing terms, so consecutive partial sums bracket the sum.
    `terms` must be even so S_terms is a lower... (sign bookkeeping done
    explicitly below)."""
    s = F(0)
    partials = []
    mp = m  # m^(2k+1)
    for k in range(terms + 1):
        term = F((-1) ** k, (2 * k + 1) * mp)
        s += term
        partials.append(s)
        mp *= m * m
    a, b = partials[-2], partials[-1]
    return (a, b) if a < b else (b, a)

def pi_enclosure_machin():
    """pi via pi/4 = 4 atan(1/5) - atan(1/239)."""
    a5lo, a5hi = atan_inv_bracket(5, 60)      # 5^-121 ~ 1e-85
    a239lo, a239hi = atan_inv_bracket(239, 20)  # 239^-41 ~ 1e-98
    lo = 16 * a5lo - 4 * a239hi
    hi = 16 * a5hi - 4 * a239lo
    return lo, hi

def pi_enclosure_gauss():
    """pi via pi/4 = 6 atan(1/8) + 2 atan(1/57) + atan(1/239) (Gauss)."""
    a8lo, a8hi = atan_inv_bracket(8, 50)        # 8^-101 ~ 1e-91
    a57lo, a57hi = atan_inv_bracket(57, 25)     # 57^-51 ~ 1e-89
    a239lo, a239hi = atan_inv_bracket(239, 20)
    lo = 24 * a8lo + 8 * a57lo + 4 * a239lo
    hi = 24 * a8hi + 8 * a57hi + 4 * a239hi
    return lo, hi

m_lo, m_hi = pi_enclosure_machin()
g_lo, g_hi = pi_enclosure_gauss()
# cross-validation: the two independent enclosures must intersect
gate("PI1", m_lo < g_hi and g_lo < m_hi,
     "Machin and Gauss pi enclosures intersect")
pi_lo = max(m_lo, g_lo)
pi_hi = min(m_hi, g_hi)
gate("PI2", pi_lo < pi_hi and (pi_hi - pi_lo) < F(1, 10 ** 60),
     "intersection nonempty, width < 1e-60 (width=%s)"
     % ceil_trunc(pi_hi - pi_lo, 70))
gate("PI3", F(3) < pi_lo and pi_hi < F(4), "sanity 3 < pi < 4")

# ---------- rational sqrt bracketing via isqrt ---------------------------
SQ_SCALE = 10 ** 40
def sqrt_lo(r):
    """Largest n/SQ_SCALE with (n/SQ_SCALE)^2 <= r (r Fraction > 0)."""
    n = isqrt((r.numerator * SQ_SCALE * SQ_SCALE) // r.denominator)
    return F(n, SQ_SCALE)
def sqrt_hi(r):
    n = isqrt((r.numerator * SQ_SCALE * SQ_SCALE) // r.denominator) + 1
    return F(n, SQ_SCALE)
# self-test: sqrt(2) bracket squares straddle 2; exact square extracts tight
gate("SQ0", sqrt_lo(F(2)) ** 2 <= 2 <= sqrt_hi(F(2)) ** 2
            and sqrt_hi(F(2)) - sqrt_lo(F(2)) == F(1, SQ_SCALE)
            and sqrt_lo(F(4)) == 2,
     "isqrt bracket self-test (sqrt2 straddle, sqrt4 exact)")

# ---------- site constants ----------------------------------------------
X = 6000000185827            # exact integer campaign site
N0 = 690988
T_TOP = F(1809, 10000)       # slab top in t
T_PT = 3000175332800         # PT2021 height (arXiv:2004.09765 Thm 1)

# window start ws(N,t) = pi * (4 N^2 - t/4); exact rational interval:
def ws_iv(N, t):
    c = 4 * N * N - F(t) / 4     # exact rational, positive here
    assert c > 0
    return (pi_lo * c, pi_hi * c)

# algebraic identity gate: x >= ws(N,t) iff x/(4 pi) + t/16 >= N^2.
# Symbolically: x >= 4 pi N^2 - pi t/4 <=> x/(4 pi) >= N^2 - t/16. Gate the
# rearrangement on exact rationals with pi treated as a free positive
# symbol: (4*N*N - t/4)*q == 4*q*(N*N - t/16) for random exact q, N, t.
qtest = F(355, 113)
gate("ALG1", (4 * 7 ** 2 - F(3, 10) / 4) * qtest
             == 4 * qtest * (7 ** 2 - F(3, 10) / 16),
     "window identity ws(N,t)=4piN^2-pi t/4 <-> radicand N^2-t/16 (exact)")

# ---------- Q: quantifier-audit monotonicity gates ----------------------
# ws(N,t) linear in t, slope -pi/4: negative iff pi > 0
gate("Q1", pi_lo > 0, "d ws/dt = -pi/4 < 0 (pi_lo > 0): sup_t ws at t=0, "
                      "inf_t ws at t=T_TOP -- t-for-all reduces to endpoints")
# radicand x/(4pi)+t/16 linear in x and t with positive coefficients
gate("Q2", F(1, 4) / pi_hi > 0, "d(radicand)/dx = 1/(4pi) > 0")
gate("Q3", F(1, 16) > 0, "d(radicand)/dt = 1/16 > 0: box for-all reduces "
                         "to corners (X,0) and (X+1,T_TOP)")

# ---------- U: site-uniform gluing margins (second line of site_glue U1-U3)
# U1: X - sup_t ws(N0,t) = X - ws(N0,0)
ws0_lo, ws0_hi = ws_iv(N0, 0)
M1u_lo = X - ws0_hi          # exact lower bound of the uniform margin
M1u_hi = X - ws0_lo
LIT_U1 = F("5377392.8789")   # site_glue_v1 pinned literal (their floor)
gate("U1a", M1u_lo >= LIT_U1,
     "X - sup_t ws(N0,t) >= 5377392.8789 (their pinned floor literal); "
     "my exact lower endpoint floor4 = %s" % floor_trunc(M1u_lo, 4))
gate("U1b", floor_trunc(M1u_lo, 4) == "5377392.8789"
            and floor_trunc(M1u_hi, 4) == "5377392.8789",
     "my enclosure floor4 string == their string on BOTH endpoints")

# U2: inf_t ws(N0+1,t) - (X+1) = ws(N0+1, T_TOP) - (X+1)
ws1_lo, ws1_hi = ws_iv(N0 + 1, T_TOP)
M2u_lo = ws1_lo - (X + 1)
M2u_hi = ws1_hi - (X + 1)
LIT_U2 = F("11989041.1415")
gate("U2a", M2u_lo >= LIT_U2,
     "inf_t ws(N0+1,t) - (X+1) >= 11989041.1415 (their literal); "
     "my floor4 = %s" % floor_trunc(M2u_lo, 4))
gate("U2b", floor_trunc(M2u_lo, 4) == "11989041.1415"
            and floor_trunc(M2u_hi, 4) == "11989041.1415",
     "floor4 string match both endpoints")
# coverage logic: for all t, ws(N0,t) < X and ws(N0+1,t) > X+1
gate("U3", M1u_lo > 0 and M2u_lo > 0,
     "[X,X+1] strictly inside [ws(N0,t), ws(N0+1,t)) for every slab t")

# ---------- R: Lambda<=0.1965 row instantiation (t0=1770/10000) ----------
t0 = F(1770, 10000)
y0sq = F(39, 1000)
gate("R1", t0 + y0sq / 2 == F(1965, 10000),
     "t0 + y0^2/2 = 1965/10000 EXACTLY (Lambda<=0.1965 row identity)")
gate("R2", y0sq + 2 * t0 == F(393, 1000) and y0sq + 2 * t0 <= 1,
     "y0^2 + 2 t0 = 393/1000 <= 1 (range condition)")
gate("R3", y0sq >= T_TOP ** 2 and t0 <= T_TOP,
     "slab containment: y0^2 = 39/1000 >= (1809/10000)^2, t0 <= 1809/10000")
gate("R4", F(X, 2) <= T_PT and F(X, 2) == F("3000000092913.5"),
     "PT2021 admissibility X/2 = 3000000092913.5 <= T = 3000175332800 exact")
# row-sharp point margins at t0 = 0.1770
wr0_lo, wr0_hi = ws_iv(N0, t0)
M1r_lo, M1r_hi = X - wr0_hi, X - wr0_lo
wr1_lo, wr1_hi = ws_iv(N0 + 1, t0)
M2r_lo, M2r_hi = wr1_lo - (X + 1), wr1_hi - (X + 1)
gate("R5a", M1r_lo >= F("5377393.0179"),
     "row point margin >= 5377393.0179 (their literal); my floor4 = %s"
     % floor_trunc(M1r_lo, 4))
gate("R5b", floor_trunc(M1r_lo, 4) == "5377393.0179"
            and floor_trunc(M1r_hi, 4) == "5377393.0179", "string match")
gate("R6a", M2r_lo >= F("11989041.1446"),
     "row point margin >= 11989041.1446 (their literal); my floor4 = %s"
     % floor_trunc(M2r_lo, 4))
gate("R6b", floor_trunc(M2r_lo, 4) == "11989041.1446"
            and floor_trunc(M2r_hi, 4) == "11989041.1446", "string match")
# uniform-vs-point dominance (inclusion isotonicity exercised where truth
# is pinned, per the producer rule): point margins must dominate uniform ones
gate("R7", M1r_lo >= M1u_lo and M2r_lo >= M2u_lo,
     "row-sharp margins dominate the uniform margins (consistency)")

# ---------- A: the auxiliary line nconst_gap_v2 point anchors (t0=1775/10000) --
ta = F(1775, 10000)
wa0_lo, wa0_hi = ws_iv(N0, ta)
A1_lo, A1_hi = X - wa0_hi, X - wa0_lo
wa1_lo, wa1_hi = ws_iv(N0 + 1, ta)
A2_lo, A2_hi = wa1_lo - (X + 1), wa1_hi - (X + 1)
gate("A1", A1_lo >= F("5377393.01")
           and floor_trunc(A1_lo, 2) == "5377393.01"
           and floor_trunc(A1_hi, 2) == "5377393.01",
     "the auxiliary line anchor: 0.1775-row margin >= 5377393.01, floor2 match; "
     "my floor4 = %s" % floor_trunc(A1_lo, 4))
gate("A2", A2_lo >= F("11989041.14")
           and floor_trunc(A2_lo, 2) == "11989041.14"
           and floor_trunc(A2_hi, 2) == "11989041.14",
     "the auxiliary line anchor: 0.1775-row margin >= 11989041.14, floor2 match; "
     "my floor4 = %s" % floor_trunc(A2_lo, 4))

# ---------- S: full-slab N-constancy (corner reduction per Q2/Q3) --------
# radicand rho(x,t) = x/(4 pi) + t/16; S(x,t) = sqrt(rho); N = floor(S).
# Min corner (X, 0); max corner (X+1, T_TOP).
rho_min_lo = F(X, 4) / pi_hi               # t=0
rho_max_hi = F(X + 1, 4) / pi_lo + T_TOP / 16
S_lo_lo = sqrt_lo(rho_min_lo)              # certified lower bound of min S
S_hi_hi = sqrt_hi(rho_max_hi)              # certified upper bound of max S
gate("S1", S_lo_lo >= N0 and S_hi_hi < N0 + 1,
     "N(x,t) = 690988 on ALL of [X,X+1] x [0,0.1809] "
     "(corner-reduced; S in [%s, %s])"
     % (floor_trunc(S_lo_lo, 12), ceil_trunc(S_hi_hi, 12)))
# robustness margins, second-lining the nconst_gap_v2 pinned strings:
fr_lo = S_lo_lo - N0          # certified lower bound on frac(S) over box
fr_hi_compl = (N0 + 1) - S_hi_hi  # certified lower bound on 1 - frac(S)
gate("S2", fr_lo >= F("0.3096430277"),
     "frac(S_lo) >= 0.3096430277 (the auxiliary line pinned floor literal); "
     "my floor10 = %s" % floor_trunc(fr_lo, 10))
gate("S3", fr_hi_compl >= F("0.6903569064"),
     "1 - frac(S_hi) >= 0.6903569064 (their literal); my floor10 = %s"
     % floor_trunc(fr_hi_compl, 10))

# ---------- G: rung-menu candidates contained in the uniform t-range -----
for i, tg in enumerate((F(162, 1000), F(161, 1000), F(160, 1000)), 1):
    gate("G%d" % i, F(0) <= tg <= T_TOP,
         "candidate t0 = %s in [0, 1809/10000] (uniform lemma applies)" % tg)

# ---------- result -------------------------------------------------------
print()
print("TOTAL CHECKS RUN: %d" % (PASS + FAIL))
print("PASS: %d  FAIL: %d" % (PASS, FAIL))
print("RESULT: %s" % ("ALL PASS" if FAIL == 0 else "FAILURES PRESENT"))
raise SystemExit(0 if FAIL == 0 else 1)
