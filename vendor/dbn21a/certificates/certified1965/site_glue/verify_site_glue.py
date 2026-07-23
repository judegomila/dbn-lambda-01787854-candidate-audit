#!/usr/bin/env /usr/bin/python3
# verify_site_glue.py -- SITE-UNIFORM window-gluing lemma at X = 6000000185827
# + Lambda<=0.1965-row / rung-menu instantiations.
#
# Self-contained: imports mpmath + stdlib only, reads no files, exit 0 iff all pass.
#
# Lemma (SITE_GLUE.md section 3): at the campaign site X = 6000000185827,
# N0 = 690988, for EVERY t0 in [0, 1809/10000] (the full certified-barrier
# slab t-range) the Polymath-15 sweep-window gluing inequalities hold with
# t0-UNIFORM exact-rational margins:
#   (U1)  X - ws(N0, t0)      >= 5377392.8789   (window N0 starts below X)
#   (U2)  ws(N0+1, t0) - (X+1) >= 11989041.1415  (window N0+1 starts past X+1)
# where ws(N, t) = 4*pi*N^2 - pi*t/4 is the exact window-start formula
# (window N = [4pi(N^2 - t/16), 4pi((N+1)^2 - t/16)), as in the pinned
# record_binding tiling identity). Together with the pinned full-slab
# N-constancy lemma (the auxiliary line, re-asserted here as supporting check S1),
# this retires preconditions P10/P11 of ANY record chain run at this site
# with t0 <= 0.1809 -- in particular the Lambda<=0.1965 row (t0 = 1770/10000)
# and the rung-menu candidates t0 = 162/1000, 161/1000, 160/1000.
#
# Method: ws is evaluated over the WHOLE t-interval hull in directed-rounded
# interval arithmetic (mpmath.iv prec 250); margins are exact rational
# comparisons of binary interval endpoints (no monotonicity argument needed).
# Endpoint extraction reads the exact stored binary tuples from _mpi_
# (the the auxiliary line-verified v2 path), self-tested in C0. Every printed
# decimal is a FLOOR truncation machine-derived from the exact endpoint
# rational, and every certified threshold string is gated to EQUAL the
# machine-printed truncation (C2c pattern).

import sys
from fractions import Fraction
from mpmath import iv

iv.prec = 250

X = 6000000185827
N0 = 690988
T_PT = 3000175332800                  # PT2021 RH-verification height (exact)
T_SLAB = Fraction(1809, 10000)        # certified winding-slab t-top
T_1965 = Fraction(1770, 10000)        # Lambda<=0.1965 row t0
Y0SQ_1965 = Fraction(39, 1000)        # y0^2 of the 0.1965 row (y0 = sqrt(0.039))
RUNGS = [Fraction(162, 1000), Fraction(161, 1000), Fraction(160, 1000)]

CHECKS = 0
def check(name, cond):
    global CHECKS
    CHECKS += 1
    print(("PASS" if cond else "FAIL"), name)
    if not cond:
        print("RESULT: FAIL")
        sys.exit(1)

def tup_to_frac(t):
    """Exact rational value of a raw mpf tuple (sign, man, exp, bc).
    Pure integer arithmetic on the stored mantissa/exponent: no rounding,
    no precision context involved."""
    sign, man, exp, bc = t
    if man == 0:
        return Fraction(0)
    v = Fraction(int(man)) * (Fraction(2) ** int(exp))
    return -v if sign else v

def endpoints(x):
    """EXACT rational endpoints of an iv.mpf, read from its _mpi_ tuples."""
    a, b = x._mpi_
    return tup_to_frac(a), tup_to_frac(b)

def floor_trunc(fr, digits):
    """FLOOR truncation of a nonnegative Fraction to `digits` decimals,
    machine-derived (integer arithmetic only)."""
    assert fr >= 0
    scaled = (fr.numerator * 10**digits) // fr.denominator
    s = str(scaled).rjust(digits + 1, "0")
    return s[:-digits] + "." + s[-digits:]

def ivf(fr):
    """Exact interval embedding of a Fraction."""
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)

pi = iv.pi

def ws_iv(N, t_interval):
    """Interval enclosure of the window-start formula ws(N,t) = 4 pi N^2 - pi t/4
    over the whole t-interval."""
    return 4 * pi * iv.mpf(N) ** 2 - pi * t_interval / 4

# ---------- C0: extraction-path self-test (verified v2 pattern) ----------
u = iv.mpf(1) / iv.mpf(3)
u_lo, u_hi = endpoints(u)
third = Fraction(1, 3)
tol = Fraction(1, 2 ** 248)
check("C0a extraction exact-bracket of 1/3 (0 < gaps < 2^-248)",
      0 < third - u_lo < tol and 0 < u_hi - third < tol)
x_lo, x_hi = endpoints(iv.mpf(X))
check("C0b extraction of exactly representable X is exact",
      x_lo == x_hi == Fraction(X))

# ---------- U1/U2: t0-UNIFORM gluing margins over the FULL slab t-range ----------
t_full = ivf(T_SLAB) * iv.mpf([0, 1])     # exact hull of [0, 0.1809]

w_n0 = ws_iv(N0, t_full)
_, w_n0_hi = endpoints(w_n0)              # sup over t of ws(N0, t), outward-rounded
u1 = Fraction(X) - w_n0_hi
s_u1 = floor_trunc(u1, 4)
print("U1 uniform margin X - sup_t ws(N0,t) >=", s_u1, "(FLOOR truncation of exact endpoint rational)")
check("U1 window-N0 start < X uniformly in t0 in [0,0.1809], margin >= 5377392.8789",
      u1 >= Fraction(53773928789, 10**4))

w_n1 = ws_iv(N0 + 1, t_full)
w_n1_lo, _ = endpoints(w_n1)              # inf over t of ws(N0+1, t), outward-rounded
u2 = w_n1_lo - Fraction(X + 1)
s_u2 = floor_trunc(u2, 4)
print("U2 uniform margin inf_t ws(N0+1,t) - (X+1) >=", s_u2, "(FLOOR truncation of exact endpoint rational)")
check("U2 window-(N0+1) start > X+1 uniformly in t0 in [0,0.1809], margin >= 11989041.1415",
      u2 >= Fraction(119890411415, 10**4))

check("U3 printed digit strings EQUAL certified thresholds (no transcription drift)",
      s_u1 == "5377392.8789" and s_u2 == "11989041.1415")

# ---------- S1: supporting re-assertion of the pinned full-slab N-constancy ----------
# (the auxiliary line verified lemma; re-run here so the bundle is self-supporting:
#  uniform gluing + constancy together retire P10/P11 at any t0 <= 0.1809.)
x_iv = iv.mpf([X, X + 1])
S = iv.sqrt(x_iv / (4 * pi) + t_full / 16)
S_lo, S_hi = endpoints(S)
check("S1 N(x,t) = %d constant on slab [X,X+1] x [0,0.1809] (pinned earlier, re-asserted)" % N0,
      (S_lo.numerator // S_lo.denominator) ==
      (S_hi.numerator // S_hi.denominator) == N0)

# ---------- S2: window-identity sanity at both t-extremes ----------
# N evaluated just past the (outward-rounded) window-N0 start equals N0:
# the formula ws really is the start of N0's window at each t-extreme.
for tv in (Fraction(0), T_SLAB):
    w = ws_iv(N0, ivf(tv))
    _, w_hi = endpoints(w)
    xw = iv.mpf(w_hi.numerator) / iv.mpf(w_hi.denominator) + 1
    Sw = iv.sqrt(xw / (4 * pi) + ivf(tv) / 16)
    a, b = endpoints(Sw)
    check("S2 N(ws(N0,t)+1, t) = N0 at t = %s" % tv,
          (a.numerator // a.denominator) == (b.numerator // b.denominator) == N0)

# ---------- R: Lambda<=0.1965-row instantiation (t0 = 1770/10000) ----------
check("R1 0.1965-row functional arithmetic t0 + y0^2/2 = 1965/10000 EXACTLY",
      T_1965 + Y0SQ_1965 / 2 == Fraction(1965, 10000))
check("R2 0.1965-row criterion validity y0^2 + 2 t0 = 393/1000 <= 1",
      Y0SQ_1965 + 2 * T_1965 == Fraction(393, 1000) <= 1)
check("R3 0.1965-row range condition y0^2 <= 1 - 2 t0",
      Y0SQ_1965 <= 1 - 2 * T_1965)
check("R4 0.1965-row slab containment: y0^2 >= (1809/10000)^2 and t0 <= 1809/10000",
      Y0SQ_1965 >= T_SLAB ** 2 and T_1965 <= T_SLAB)
check("R5 admissibility X/2 <= T_PT exactly (PT2021)",
      Fraction(X, 2) <= T_PT)

# point gluing margins at the row's own t0 (sharper than the uniform ones)
w_a = ws_iv(N0, ivf(T_1965))
_, w_a_hi = endpoints(w_a)
r6 = Fraction(X) - w_a_hi
s_r6 = floor_trunc(r6, 4)
print("R6 point margin X - ws(N0, 0.1770) >=", s_r6, "(FLOOR truncation of exact endpoint rational)")
check("R6 0.1965-row window-N0 start < X, margin >= 5377393.0179",
      r6 >= Fraction(53773930179, 10**4))

w_b = ws_iv(N0 + 1, ivf(T_1965))
w_b_lo, _ = endpoints(w_b)
r7 = w_b_lo - Fraction(X + 1)
s_r7 = floor_trunc(r7, 4)
print("R7 point margin ws(N0+1, 0.1770) - (X+1) >=", s_r7, "(FLOOR truncation of exact endpoint rational)")
check("R7 0.1965-row window-(N0+1) start > X+1, margin >= 11989041.1446",
      r7 >= Fraction(119890411446, 10**4))

check("R8 printed digit strings EQUAL certified thresholds (no transcription drift)",
      s_r6 == "5377393.0179" and s_r7 == "11989041.1446")

# ---------- G: rung-menu coverage (uniform lemma applies to each rung t0) ----------
for t0 in RUNGS:
    check("G rung t0 = %s lies in [0, 1809/10000] (uniform U1/U2 + S1 apply)" % t0,
          Fraction(0) <= t0 <= T_SLAB)

print("TOTAL CHECKS RUN: %d" % CHECKS)
print("RESULT: ALL PASS")
sys.exit(0)
