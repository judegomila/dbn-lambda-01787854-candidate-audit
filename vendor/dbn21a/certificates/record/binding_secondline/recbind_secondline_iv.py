#!/usr/bin/env /usr/bin/python3
"""
recbind_secondline_iv.py -- INDEPENDENT SECOND LINE on the producer line's
record_binding package (the independent verification line, a separate run).

ZERO SHARED CODE: every formula below is derived from arXiv:1904.12438
(TeX labels cited inline); the producer line's verify_record_binding.py was
NEVER opened by this line -- only its prose note (RECORD_BINDING.md)
and the verified shared-verified results text were read, to know WHICH
constants to re-derive and to transcribe the producer's PRINTED digit
strings used in the cross-line match gates below.

WHAT IS SECOND-LINED (scope):
  (R1-algebra) the two exact identities behind the trib2 rewrite lemma
      -- s_*-phase cancellation and the b-exponent identity -- verified
      here symbolically (sympy, polynomial identities in u=ln n,
      l2=ln 2), plus c_2 = 0 and c_n >= 0 sign logic, plus the trib2
      rearrangement identity verified in EXACT RATIONALS at even and
      odd N for two coefficient families (one an edge case q = 1).
  (R2) the conversion constant: my own uniform lower bound sigma_min
      on Re s_* over {N >= N0, x in window N, y in [y0, 1]} from
      (res-bound), hence C_my = 1 + b_2^t 2^{-sigma_min} and
      m_min = 0.03 / C_my.
  (R3) my own GLOBAL uniform error budget E_my for e_A+e_B+e_C0 over
      the same region (independent majorant chain; my e_A+e_B majorant
      is deliberately cruder -- integral tail instead of endpoint-cap
      lemma -- so E_my >= their E_max is expected and NOT a
      discrepancy; the e_C0 part matches their printed CEIL exactly).
  (R4) the binding inequality m_min - E_my > 0 and the EXACT-RATIONAL
      record assembly: Lambda <= t0 + y0^2/2 = 197/1000 exactly,
      PT2021 height containment, winding-slab containments.
  (PROBE) a direct two-sided complex-interval evaluation of
      s_* = s + (t/2) alpha(s)  (alpha-def, sn-def) at the in-region
      point x = X+1, y = y0, falsification-testing the one-sided
      (res-bound) freeze direction and the |1-beta_2| <= C_my cap
      pointwise.

NOT second-lined here (honest scope): the y_reduction transfer theorem
itself (F(N,y) <= F(N,y0); the producer line's gates G0/G2/G2a/G3) and the
Dirichlet sweep values Q(N,y0) >= 0.03 (the producer, already
second-lined on [N0, 1e7) by the independent verifier) are CONSUMED as
verified facts, exactly as the producer package consumes them.

RH-height dependency: NONE in any inequality below (finite Dirichlet
sums / closed-form majorants); the assembled record statement consumes
RH to height T = X/2 unconditionally via Platt-Trudgian 2021
(T_PT = 3000175332800 >= X/2 = 3000000092913.5, exact check A2).

PAPER FORMULAS USED (arXiv:1904.12438, all transcribed from the TeX):
 (N-def-main) N(x) = floor(sqrt(x/4pi + t/16)); window N is
     [4pi N^2 - pi t/4, 4pi (N+1)^2 - pi t/4).
 (res-bound)  Re s_* >= (1+y)/2 + (t/4) log(x/4pi)
                        - (t/2x^2)(1 - 3y + 4y(1+y)/x^2)_+
 (gamma-bound) |gamma| <= e^{0.02y} (x/4pi)^{-y/2}
 (kappa-bound) |kappa| <= t y / (2(x-6))
 (eab-bound)  e_A+e_B <= sum_{n<=N} (1+|gamma| N^{|kappa|} n^y)
                 b_n^t n^{-Re s_*} (exp((t^2/16 log^2(x/4pi n^2)
                 + 0.626)/(x-6.66)) - 1)
 (ec-bound)   e_C0 <= (x/4pi)^{-(1+y)/4} exp(-t/16 log^2(x/4pi)
                 + 1.24(3^y+3^{-y})/(N-0.125)
                 + (3|log(x/4pi)+i pi/2|+10.44)/(x-12))
 (alpha-def)  alpha(s) = 1/s + 1/(s-1) - (1/2)log pi
                 + (1/2)Log(s/2) - 1/(2s)
 (sn-def)     s_* = (1+y-ix)/2 + (t/2) alpha((1+y-ix)/2)
 (bn-def)     b_n^t = exp((t/4) log^2 n)

MONOTONICITY ARGUMENTS (proved in RECBIND_SECONDLINE.md section 3;
the script gates every numeric instance they require):
 (M1) corr(x,y) = (t/2x^2)(1-3y+4y(1+y)/x^2)_+ is decreasing in y
      while positive (d/dy inner = -3 + 4(1+2y)/x^2 < 0, gated) and
      decreasing in x; so corr <= corr(xL, y0) =: corr_max on the
      whole region (1-3y0 > 0 gated).
 (M2) sigma1(x,y) = (1+y)/2 + (t/4)log(x/4pi) - corr is therefore
      >= sigma_min := (1+y0)/2 + (t/4)log(xL/4pi) - corr_max.
 (M3) per-term majorant: for x in window N, x/4pi >= N^2 - t/16, so
      Re s_* - (t/4)log n >= Re s_* - (t/4)log N
        >= (1+y0)/2 + (t/4)log N - eps  >=  p
      with eps := -(t/4)log(1 - t/(16 N0^2)) + corr_max (both pieces
      decreasing in N, x) and p := (1+y0)/2 + (t/4)log N0 - eps;
      hence b_n^t n^{-Re s_*} <= n^{-p} for every n <= N, every
      N >= N0.  Sum bound: sum_{n<=N} n^{-p(N)} <= sum_{n>=1} n^{-p}
      <= 1 + 2^{-p} + 2^{1-p}/(p-1)  (integral tail; p > 1 gated).
 (M4) prefactor: |gamma| N^{|kappa|} n^y <= e^{0.02y}
      (N^2/(x/4pi))^{y/2} N^{t/(2(x-6))}
      <= e^{0.02} (1 - t/(16 N0^2))^{-1/2}
         exp(t log N0 / (2(xL - 6)))  =: P_my - 1,
      using y <= 1, N^2/(x/4pi) <= (1-t/16N^2)^{-1} on window N,
      (1-t/16N^2)^{-y/2} increasing in y and worst at N0, and
      log N/(x-6) <= log N/(4pi N^2 - pi t/4 - 6) decreasing in N
      (writeup, algebra: log N'/log N0 <= N'/N0 <= N'^2/N0^2
      <= (4pi N'^2-c)/(4pi N0^2-c) for c > 0).
 (M5) u(x) = ((t^2/16) log^2(x/4pi) + 0.626)/(x - 6.66) decreasing in
      x once log(x/4pi) > 2 (gated: > 26.8); inner log^2(x/4pi n^2)
      <= log^2(x/4pi) for 1 <= n <= N on window N (gated instance:
      |log(x/(4pi N^2))| <= -log(1-t/16N0^2) < log(xL/4pi)).
 (M6) every e_C0 factor is maximized at (xL, N0) over the region
      (writeup section 3.6): exponents -(1+y)/4 log(x/4pi) and
      -t/16 log^2(x/4pi) decrease in x; the N-term decreases in N;
      the last term decreases in x because its numerator derivative
      3 L'/sqrt(...) <= 3/x gives num'(x-12) < 3 < 10.44 < num.
      y-dependence is enclosed by evaluating with y as the full
      interval hull [y0, ymax].

DIGIT DISCIPLINE: every claimed comparison is an EXACT rational
comparison of binary interval endpoints extracted via ._mpi_ (never
str()/float()); printed LOWER bounds FLOOR-truncated, UPPER bounds
CEIL-truncated, labels printed next to each number; cross-line match
gates compare MACHINE-DERIVED truncations of my endpoints against the
producer's printed strings transcribed as string literals.
"""
import sys
from fractions import Fraction

import sympy as sp
from mpmath import iv

iv.prec = 200

FAIL = []
NGATE = [0]


def gate(name, cond, detail=""):
    NGATE[0] += 1
    tag = "PASS" if cond else "FAIL"
    print("[%s] %-44s %s" % (tag, name, detail))
    if not cond:
        FAIL.append(name)


# ---------- exact endpoint extraction (binary, never float/str) ----------
def _frac(end):
    s, man, e, _ = end
    v = Fraction(man) * (Fraction(2) ** e if e >= 0 else Fraction(1, 2 ** (-e)))
    return -v if s else v


def lb(x):
    return _frac(x._mpi_[0])


def ub(x):
    return _frac(x._mpi_[1])


def floor_trunc(fr, digits=10):
    """FLOOR-truncated decimal string of a positive Fraction: printed
    value <= fr, so it is itself a valid lower bound."""
    assert fr > 0
    k = 0
    while fr * 10 ** k < 10 ** (digits - 1):
        k += 1
    while fr * 10 ** k >= 10 ** digits:
        k -= 1
    n = (fr * 10 ** k).numerator // (fr * 10 ** k).denominator
    s = str(n)
    e = digits - 1 - k
    return s[0] + "." + s[1:] + "e" + ("+" if e >= 0 else "-") + str(abs(e))


def ceil_trunc(fr, digits=10):
    """CEIL-truncated decimal string of a positive Fraction: printed
    value >= fr, so it is itself a valid upper bound."""
    assert fr > 0
    k = 0
    while fr * 10 ** k < 10 ** (digits - 1):
        k += 1
    while fr * 10 ** k >= 10 ** digits:
        k -= 1
    num = fr * 10 ** k
    n = num.numerator // num.denominator
    if Fraction(n) != num:
        n += 1
        if n == 10 ** digits:        # carry: 9.99... -> 10.0..., renormalize
            n //= 10
            k -= 1
    s = str(n)
    e = digits - 1 - k
    return s[0] + "." + s[1:] + "e" + ("+" if e >= 0 else "-") + str(abs(e))


def plain_floor(fr, decimals):
    """FLOOR truncation to fixed decimal places (positive fr)."""
    scaled = fr * 10 ** decimals
    n = scaled.numerator // scaled.denominator
    s = str(n).rjust(decimals + 1, "0")
    return s[:-decimals] + "." + s[-decimals:]


def plain_ceil(fr, decimals):
    scaled = fr * 10 ** decimals
    n = scaled.numerator // scaled.denominator
    if Fraction(n) != scaled:
        n += 1
    s = str(n).rjust(decimals + 1, "0")
    return s[:-decimals] + "." + s[-decimals:]


# ---------- campaign parameters (exact) ----------
T0 = Fraction(71, 400)            # t0 = 0.1775 exactly
Y0SQ = Fraction(39, 1000)         # y0^2
YMAXSQ = Fraction(129, 200)       # ymax^2 = 0.645 = 1 - 2 t0 exactly
N0 = 690988
X = 6000000185827
T_PT = 3000175332800              # Platt-Trudgian 2021 height (exact)

t = iv.mpf(71) / 400
y0 = iv.sqrt(iv.mpf(39) / 1000)
ymax = iv.sqrt(iv.mpf(129) / 200)
yiv = y0 + (ymax - y0) * iv.mpf([0, 1])   # interval hull [y0, ymax]

print("=" * 72)
print("SECTION A -- exact-rational record assembly (second line on R4/Sec.5)")
print("=" * 72)

# A1: Lambda <= t0 + y0^2/2 exactly
lam = T0 + Y0SQ / 2
gate("A1 Lambda = t0 + y0^2/2 = 197/1000 exact", lam == Fraction(197, 1000),
     "t0=71/400, y0^2=39/1000 -> %s" % lam)

# A2: PT2021 height containment, exact
xhalf = Fraction(X, 2)
gate("A2 X/2 <= T_PT (PT2021, exact)", xhalf <= T_PT,
     "X/2=%s, T_PT=%d, margin=%s" % (xhalf, T_PT, T_PT - xhalf))
gate("A2b margin equals producer's 350479773/2", T_PT - xhalf == Fraction(350479773, 2))

# A3: winding-slab containments (the producer slab [0.1809,1]x[0,0.1809])
s18 = Fraction(1809, 10000)
gate("A3a y0^2 >= 0.1809^2 (exact)", Y0SQ >= s18 * s18,
     "39/1000 vs %s" % (s18 * s18))
gate("A3b t0 <= 0.1809 (exact)", T0 <= s18, "71/400 = 0.1775")
gate("A3c y0^2 + 2 t0 <= 1 (exact)", Y0SQ + 2 * T0 <= 1,
     "= %s = 0.394" % (Y0SQ + 2 * T0))
gate("A3d ymax^2 = 1 - 2 t0 (exact)", YMAXSQ == 1 - 2 * T0)

# A4: the N0 window contains the region's left edge X + sqrt(1-y0^2).
# window N: [4pi N^2 - pi t/4, 4pi (N+1)^2 - pi t/4)  by (N-def-main)
xL = 4 * iv.pi * N0 ** 2 - iv.pi * t / 4
xR = 4 * iv.pi * (N0 + 1) ** 2 - iv.pi * t / 4
gate("A4a window-left xL < X (interval ub vs exact)", ub(xL) < X,
     "X - ub(xL) >= %s (FLOOR)" % floor_trunc(X - ub(xL), 8))
gate("A4b X + 1 < window-right xR", X + 1 < lb(xR),
     "lb(xR) - (X+1) >= %s (FLOOR)" % floor_trunc(lb(xR) - (X + 1), 8))
# left edge X + sqrt(1-y0^2) in (X, X+1) since 0 < sqrt(1-y0^2) < 1 (exact: 0 < 1-y0^2 < 1)
gate("A4c 0 < 1 - y0^2 < 1 (exact)", 0 < 1 - Y0SQ < 1, "left edge in (X, X+1)")

print()
print("=" * 72)
print("SECTION B -- R1 algebra second line (sympy exact + exact rationals)")
print("=" * 72)

# B1: the two exponent identities behind Lemma trib2's segment condition,
# as polynomial identities in u = log n, l2 = log 2 (exact for n > 0,
# where log(n/2) = u - l2).
u, l2, ss, tt = sp.symbols("u l2 s t")
# phase exponent of beta_2 alpha_{n/2} / alpha_n : -s*l2 - s*(u-l2) + s*u
phase = -ss * l2 - ss * (u - l2) + ss * u
gate("B1a s_*-phase cancels identically (sympy)", sp.expand(phase) == 0,
     "-s ln2 - s ln(n/2) + s ln n == 0")
# b-exponent: (t/4)(l2^2 + (u-l2)^2 - u^2) == -(t/2) l2 (u - l2)
bexp = sp.expand(tt / 4 * (l2 ** 2 + (u - l2) ** 2 - u ** 2) + tt / 2 * l2 * (u - l2))
gate("B1b b-exponent identity (sympy)", bexp == 0,
     "(t/4)(ln^2 2+ln^2(n/2)-ln^2 n) == -(t/2) ln2 ln(n/2)")
# B1c: c_2 = b_2 - b_2 b_1 = 0 because b_1 = exp((t/4) ln^2 1) = 1 (sympy exact)
gate("B1c b_1 = exp((t/4) ln^2 1) = 1, hence c_2 = 0 (sympy)",
     sp.exp(tt / 4 * sp.log(1) ** 2) == 1, "c_2 = b_2(1 - b_1) = 0")

# B2: trib2 rearrangement identity, exact rationals, even and odd N,
# two deterministic coefficient families satisfying q a_{n/2} <= a_n:
def rearr_check(N, q, a):
    LHS = Fraction(0)
    for n in range(1, 2 * N + 1):
        term = (a(n) if n <= N else Fraction(0)) - (q * a(n // 2) if n % 2 == 0 else Fraction(0))
        LHS += abs(term)
    RHS = (1 - q) * sum(a(n) for n in range(1, N + 1)) \
        + 2 * q * sum(a(n) for n in range(1, N + 1) if 2 * n > N)
    # hypothesis check: q a_{n/2} <= a_n for even n <= 2N
    hyp = all(q * a(n // 2) <= a(n) for n in range(2, 2 * N + 1, 2))
    return hyp and LHS == RHS, LHS, RHS

for (N_, q_, fam, lbl) in [
        (8, Fraction(1, 3), lambda n: Fraction(1, n), "N=8 q=1/3 a_n=1/n"),
        (9, Fraction(1, 3), lambda n: Fraction(1, n), "N=9 q=1/3 a_n=1/n"),
        (8, Fraction(1), lambda n: Fraction(1), "N=8 q=1 a_n=1 (edge)"),
        (9, Fraction(1, 5), lambda n: Fraction(1, n * n), "N=9 q=1/5 a_n=1/n^2")]:
    ok, L_, R_ = rearr_check(N_, q_, fam)
    gate("B2 rearrangement identity %s" % lbl, ok, "LHS=RHS=%s" % L_)

print()
print("=" * 72)
print("SECTION C -- R2 second line: uniform sigma_min, C_my, m_min")
print("=" * 72)

# (M1) instances
one_minus_3y0 = 1 - 3 * y0
gate("C1a 1 - 3 y0 > 0 (positive part active at y0)", lb(one_minus_3y0) > 0,
     ">= %s (FLOOR)" % floor_trunc(lb(one_minus_3y0), 8))
dinner = -3 + 4 * (1 + 2 * iv.mpf(1)) / xL ** 2   # at worst y=1
gate("C1b d/dy inner = -3 + 4(1+2y)/x^2 < 0 (y<=1, x>=xL)", ub(dinner) < 0,
     "<= -%s" % floor_trunc(-ub(dinner), 6))
corr_max = (t / (2 * xL ** 2)) * (1 - 3 * y0 + 4 * y0 * (1 + y0) / xL ** 2)
gate("C1c corr_max > 0", lb(corr_max) > 0,
     "corr_max <= %s (CEIL)" % ceil_trunc(ub(corr_max), 6))

L0 = iv.log(xL / (4 * iv.pi))
gate("C2 L0 = log(xL/4pi) > 26.8 (also > 2 for M5)", lb(L0) > Fraction(268, 10),
     "L0 >= %s (FLOOR)" % floor_trunc(lb(L0), 12))

sigma_min = (1 + y0) / 2 + (t / 4) * L0 - corr_max
sigma_min_lb = lb(sigma_min)
print("sigma_min >= %s (FLOOR, 12 digits)" % floor_trunc(sigma_min_lb, 12))

b2t = iv.exp(t / 4 * iv.log(2) ** 2)
C_my = 1 + b2t * iv.exp(-sigma_min * iv.log(2))
C_my_ub = ub(C_my)
print("C_my = 1 + b_2^t 2^{-sigma_min} <= %s (CEIL, 11 digits)" % ceil_trunc(C_my_ub, 11))
gate("C3 cross-line digit match: C_lambda", plain_ceil(C_my_ub, 10) == "1.2949811496",
     "my CEIL-10dp %s == producer printed 1.2949811496" % plain_ceil(C_my_ub, 10))

m_min = (iv.mpf(3) / 100) / C_my
m_min_lb = lb(m_min)
print("m_min = 0.03/C_my >= %s (FLOOR, 11 digits)" % floor_trunc(m_min_lb, 11))
gate("C4 cross-line digit match: m_min", plain_floor(m_min_lb, 10) == "0.0231663603",
     "my FLOOR-10dp %s == producer printed 0.0231663603" % plain_floor(m_min_lb, 10))

print()
print("=" * 72)
print("SECTION D -- R3 second line: my own global uniform error budget E_my")
print("=" * 72)

# (M3): p and S
eps = -(t / 4) * iv.log(1 - t / (16 * iv.mpf(N0) ** 2)) + corr_max
p = (1 + y0) / 2 + (t / 4) * iv.log(N0) - eps
gate("D1 p > 1 (integral tail valid)", lb(p) > 1,
     "p >= %s (FLOOR)" % floor_trunc(lb(p), 10))
S_my = 1 + iv.exp(-p * iv.log(2)) + iv.exp((1 - p) * iv.log(2)) / (p - 1)
print("S_my = 1 + 2^-p + 2^(1-p)/(p-1) <= %s (CEIL)" % ceil_trunc(ub(S_my), 10))

# (M4): prefactor
P_my = 1 + iv.exp(iv.mpf(2) / 100) \
    * iv.exp(-iv.log(1 - t / (16 * iv.mpf(N0) ** 2)) / 2) \
    * iv.exp(t * iv.log(N0) / (2 * (xL - 6)))
print("P_my <= %s (CEIL)" % ceil_trunc(ub(P_my), 10))
gate("D2 cross-line consistency: P_my <= 2.0203 (producer's P_max print)",
     ub(P_my) <= Fraction(20203, 10000),
     "my CEIL %s" % plain_ceil(ub(P_my), 4))

# (M5): u at xL; monotone decrease gate 2(x-6.66)/x < 2 < L0 (universal
# for x > 6.66 since 2(x-6.66)/x < 2; L0 > 2 gated at C2)
u1 = (t * t / 16 * L0 * L0 + iv.mpf(626) / 1000) / (xL - iv.mpf(666) / 100)
print("u1(xL) <= %s (CEIL)" % ceil_trunc(ub(u1), 8))
# inner-argument gate: on window N, x/(4pi N^2) >= 1 - t/(16 N^2), so
# |log(x/4pi n^2)| <= max(L(x), -log(1-t/16N0^2)) = L(x):
inner_edge = -iv.log(1 - t / (16 * iv.mpf(N0) ** 2))
gate("D3 |log(x/4piN^2)| edge <= L0 (inner max at n=1)",
     ub(inner_edge) < lb(L0),
     "edge <= %s (CEIL) << L0" % ceil_trunc(ub(inner_edge), 6))

eAB_my = P_my * S_my * (iv.exp(u1) - 1)
eAB_ub = ub(eAB_my)
print("e_A + e_B <= %s (CEIL, my majorant)" % ceil_trunc(eAB_ub, 8))
gate("D4 eAB sanity: my (cruder) bound still < 1e-11", eAB_ub < Fraction(1, 10 ** 11),
     "NOTE producer's sharper endpoint-cap bound 1.78e-12 < mine; both valid uppers")

# (M6): e_C0 at (xL, N0), y as the full hull [y0, ymax]
mod_iv = iv.sqrt(L0 * L0 + iv.pi ** 2 / 4)
eC0_my = iv.exp(-(1 + yiv) / 4 * L0) * iv.exp(
    -t / 16 * L0 * L0
    + iv.mpf(124) / 100 * (iv.exp(yiv * iv.log(3)) + iv.exp(-yiv * iv.log(3)))
    / (N0 - iv.mpf(125) / 1000)
    + (3 * mod_iv + iv.mpf(1044) / 100) / (xL - 12))
eC0_ub = ub(eC0_my)
print("e_C0 <= %s (CEIL)" % ceil_trunc(eC0_ub, 8))
gate("D5 cross-line digit match: e_C0 CEIL-6sig",
     ceil_trunc(eC0_ub, 6) == "1.04589e-7",
     "my CEIL %s == producer printed 1.04589e-7 (0.000000104589)" % ceil_trunc(eC0_ub, 6))

E_my = eAB_ub + eC0_ub
print("E_my = (eA+eB)_ub + eC0_ub <= %s (CEIL, exact-rational sum)" % ceil_trunc(E_my, 8))
# Both E_my and the producer's E_max are valid upper bounds for the same
# true quantity; mine is the larger because my eAB majorant is cruder.
# Gate that the excess is nonnegative AND attributable ENTIRELY to the
# eAB leg (i.e. bounded by my whole eAB term -- the eC0 legs agree, D5):
E_prod = Fraction(104590, 10 ** 12)   # producer's printed CEIL 0.000000104590
gate("D6 0 <= E_my - E_prod <= my_eAB_ub (excess = eAB majorant gap only)",
     0 <= E_my - E_prod <= eAB_ub,
     "E_my - E_prod = %s (CEIL) <= eAB_ub = %s"
     % (ceil_trunc(E_my - E_prod, 4), ceil_trunc(eAB_ub, 4)))

print()
print("=" * 72)
print("SECTION E -- R4 second line: the binding inequality, my constants")
print("=" * 72)

bind = m_min_lb - E_my
gate("E1 binding: m_min - E_my > 0", bind > 0,
     "margin >= %s (FLOOR, exact rational arithmetic)" % floor_trunc(bind, 11))
gate("E2 cross-line digit match: binding margin FLOOR-10dp",
     plain_floor(bind, 10) == "0.0231662557",
     "my FLOOR %s == producer printed 0.0231662557" % plain_floor(bind, 10))
ratio = m_min_lb / E_my
RATIO_FLOOR = ratio.numerator // ratio.denominator
gate("E3 ratio m_min/E_my > 2e5 (5+ orders of safety on my line)",
     ratio > 200000, "my ratio >= %d (FLOOR int; producer's 221497 used their"
     " sharper E_max, mine is smaller as expected)" % RATIO_FLOOR)

print()
print("=" * 72)
print("SECTION F -- pointwise falsification probe at x = X+1, y = y0")
print("=" * 72)

# Direct two-sided complex-interval evaluation of s_* (sn-def, alpha-def)
# at the exact integer x = X+1 (inside window N0 by A4), y = y0.
def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def csub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cdiv(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def cscale(a, r):
    return (a[0] * r, a[1] * r)


def carg(z):
    re, im = z
    # certified half-plane assertion so the branch cut cannot be straddled
    assert lb(re) > 0 or lb(im) > 0 or ub(im) < 0, "carg: no certified half-plane"
    a = iv.atan2(im, re)
    assert ub(a) - lb(a) < 3, "carg: branch-cut straddle"
    return a


def clog(z):
    return (iv.log(z[0] * z[0] + z[1] * z[1]) / 2, carg(z))


HALF = iv.mpf(1) / 2
ONE = (iv.mpf(1), iv.mpf(0))
LOG_PI = iv.log(iv.pi)


def alpha(s):
    """(alpha-def): 1/s + 1/(s-1) - (1/2)log pi + (1/2)Log(s/2) - 1/(2s)."""
    inv_s = cdiv(ONE, s)
    inv_sm1 = cdiv(ONE, csub(s, ONE))
    half_log_s2 = cscale(clog(cscale(s, HALF)), HALF)
    out = cadd(inv_s, inv_sm1)
    out = (out[0] - LOG_PI / 2, out[1])
    out = cadd(out, half_log_s2)
    out = csub(out, cscale(inv_s, HALF))
    return out


xp = iv.mpf(X) + 1                      # exact integer point
s_pt = ((1 + y0) / 2, -xp / 2)          # s = (1+y0-ix)/2
al = alpha(s_pt)
s_star = cadd(s_pt, cscale(al, t / 2))
sigma_pt = s_star[0]
print("Re s_*(X+1, y0) in [%s, %s] (FLOOR/CEIL 14 digits)" %
      (floor_trunc(lb(sigma_pt), 14), ceil_trunc(ub(sigma_pt), 14)))
gate("F1 direct Re s_* >= sigma_min (res-bound freeze direction holds)",
     lb(sigma_pt) > sigma_min_lb,
     "gap >= %s (FLOOR)" % floor_trunc(lb(sigma_pt) - sigma_min_lb, 6))
# direct |1 - beta_2| at the point: beta_2 = exp((t/4)ln^2 2 - s_* ln 2)
w = csub((t / 4 * iv.log(2) ** 2, iv.mpf(0)), cscale(s_star, iv.log(2)))
r = iv.exp(w[0])
beta2 = (r * iv.cos(w[1]), r * iv.sin(w[1]))
one_minus = csub(ONE, beta2)
ab = iv.sqrt(one_minus[0] ** 2 + one_minus[1] ** 2)
print("|1 - beta_2|(X+1, y0) in [%s, %s]" %
      (floor_trunc(lb(ab), 12), ceil_trunc(ub(ab), 12)))
gate("F2 pointwise |1-beta_2| <= C_my (cap not violated)", ub(ab) <= C_my_ub,
     "slack >= %s (FLOOR)" % floor_trunc(C_my_ub - ub(ab), 6))
gate("F3 pointwise |1-beta_2| >= 1 - b2^t 2^{-sigma_pt} (two-sided sanity)",
     lb(ab) >= lb(1 - b2t * iv.exp(-sigma_pt * iv.log(2))),
     "")

print()
print("TOTAL GATES RUN: %d" % NGATE[0])
if FAIL:
    print("RESULT: FAILURES: %s" % FAIL)
    sys.exit(1)
print("RESULT: ALL PASS")
print()
print("CERTIFIED (second line, this certificate's code only):")
print("  * exact assembly: Lambda <= 197/1000 given (i) PT2021, (ii) binding,")
print("    (iii) slab containments -- all re-checked above in exact rationals;")
print("  * R1 algebra: phase cancellation + b-exponent + rearrangement identity")
print("    verified independently (sympy polynomial + exact rationals);")
print("  * R2: |1-beta_2| <= C_my <= 1.2949811496 (CEIL) and |f_t0| >= m_min")
print("    >= 0.0231663603 (FLOOR) uniformly on {N>=N0, x in window N, y in")
print("    [y0,1]}, via my own (res-bound) freeze chain (M1)-(M2);")
print("  * R3: my own global budget E_my <= %s (CEIL): e_C0 part" % ceil_trunc(E_my, 6))
print("    digit-matches the producer (1.04589e-7 CEIL); eAB part uses an")
print("    independent, cruder majorant (integral tail) -- both valid uppers;")
print("  * R4: m_min - E_my >= 0.0231662557 (FLOOR) > 0 on MY constants --")
print("    the same 10-digit floor the producer printed: two-line value match.")
print("  RH-height dependency: NONE above; the assembled record consumes RH")
print("  to T = X/2 unconditionally via PT2021 (gate A2).")
sys.exit(0)
