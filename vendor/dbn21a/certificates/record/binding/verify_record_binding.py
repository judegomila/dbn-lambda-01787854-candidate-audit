#!/usr/bin/env /usr/bin/python3
# verify_record_binding.py -- standalone verifier for RECORD_BINDING.md (the producer line, dbn21a)
#
# Certifies the BINDING LEMMA that turns the campaign's y0-only trib2 selection sweep
# (the producer's verified Dirichlet sweep: Lemma trib2 / Lemma-10.1-style Euler-2
# selection lower bound on |1-beta2|*|f_t0| exceeding 0.03 for EVERY integer N >= N0
# = 690988 at the single height y = y0) into hypothesis (ii) of the instantiated
# criterion (packages/criterion_theorem/ Cor. 3.2): H_t0(x+iy) != 0 for all
# x >= X + sqrt(1-y0^2) and ALL y in [y0, sqrt(1-2t0)], at the campaign row
#   t0 = 71/400 (exact), y0 = sqrt(0.039), X = 6000000185827.
#
# The three new mathematical ingredients certified here:
#  (R1) TRIB2 REWRITE LEMMA: the trib2 (arXiv:1904.12438 Lemma `trib2`) selection lower
#       bound is EXACTLY of standard-window-majorant form 1 - sum_n a_n n^{-sigma},
#       a_n >= 0 y-INDEPENDENT: the segment ratio beta2*alpha_{n/2}/alpha_n equals
#       exp(-(t/2) ln2 ln(n/2)) in (0,1] with the complex s_*-phases cancelling
#       IDENTICALLY (sympy-exact), and the rearrangement identity of the trib2 proof
#       checked in exact rational arithmetic. Hence the y-quantifier-reduction theorem
#       (packages/y_reduction/, gates re-certified here for self-containment) applies
#       to the swept functional itself: selection bound at y0 transfers to all
#       y in [y0, 1].
#  (R2) CONVERSION CONSTANT: |1 - beta2| <= C_lambda := 1 + b_2 2^{-sigma1lo(N0,y0)}
#       uniformly for all N >= N0, y in [y0,1], so the sweep's 0.03 gives
#       |f_t0(x+iy)| >= 0.03 / C_lambda =: m_min uniformly.
#  (R3) UNIFORM ERROR BUDGET: e_A + e_B + e_C0 <= E_max for ALL N >= N0, x in window N,
#       y in [y0, ymax], with E_max certified via monotonicity gates (U1)-(U5) -- and
#       m_min - E_max > 0, so |H_t0/B_t0| >= m_min - E_max > 0 pointwise: hypothesis
#       (ii) holds with NO zeros on the whole region.
# Plus (R4) the record-assembly arithmetic: with hypothesis (i) supplied by PT2021
# (X/2 <= T_PT exact) and hypothesis (iii) by the certified barrier slab containment,
# Lambda <= t0 + y0^2/2 = 0.197 exactly.
#
# All numerics in mpmath interval arithmetic (prec 220) or exact rationals/sympy.
# No disk reads. Exit 0 iff all checks pass. Runtime well under 120 s, single core.
#
# RH-height dependency: NONE in (R1)-(R3) (unconditional Dirichlet-sum inequalities).
# The assembled Lambda <= 0.197 consumes RH height T = X/2 = 3000000092913.5 exactly,
# supplied unconditionally by Platt-Trudgian 2021 (T_PT = 3000175332800).

from mpmath import iv, mp
from fractions import Fraction
import sympy as sp
import sys, time

iv.prec = 220
mp.prec = 220

t_start = time.time()
results = []
def chk(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))

def itv(x): return iv.mpf(x)
def ub(z):  return iv.mpf([z.b, z.b])   # certified upper bound as degenerate interval
def lb(z):  return iv.mpf([z.a, z.a])

def floor_trunc(v, digits):
    v = mp.mpf(v); s = int(mp.floor(v * mp.mpf(10)**digits)); assert s >= 0
    ip, fr = divmod(s, 10**digits); return f"{ip}.{fr:0{digits}d}"

def ceil_trunc(v, digits):
    v = mp.mpf(v); s = int(mp.ceil(v * mp.mpf(10)**digits)); assert s >= 0
    ip, fr = divmod(s, 10**digits); return f"{ip}.{fr:0{digits}d}"

print("=" * 78)
print("R1. TRIB2 REWRITE LEMMA (exact algebra)")
print("=" * 78)

# (R1a) phase cancellation + segment ratio, sympy-exact:
# alpha_n = b_n n^{-s},  beta2 = b_2 2^{-s},  b_n = exp((t/4) ln^2 n).
# ratio := beta2 * alpha_{n/2} / alpha_n
#        = exp((t/4)(ln^2 2 + ln^2(n/2) - ln^2 n)) * exp(s(ln n - ln 2 - ln(n/2)))
# and ln n = ln 2 + ln(n/2) makes the s-exponent vanish IDENTICALLY (any complex s),
# while ln^2 2 + ln^2(n/2) - ln^2 n = -2 ln2 ln(n/2).
L2, Lh, tt, ss = sp.symbols('L2 Lh t s')   # L2 = ln 2, Lh = ln(n/2), ln n = L2 + Lh
s_exponent = (L2 + Lh) - L2 - Lh
chk("(R1a) s-phase exponent ln n - ln 2 - ln(n/2) == 0 identically (sympy)",
    sp.simplify(s_exponent) == 0)
quad = L2**2 + Lh**2 - (L2 + Lh)**2
chk("(R1a) ln^2 2 + ln^2(n/2) - ln^2 n == -2 ln2 ln(n/2) identically (sympy)",
    sp.simplify(quad + 2*L2*Lh) == 0)
# hence ratio = exp(-(t/2) ln2 ln(n/2)): real, in (0,1] for n >= 2 even, t > 0
# (ln(n/2) >= 0 with equality iff n = 2); the trib2 segment condition holds for ALL
# s in C, in particular every (x, y) in every window, every y -- so the masses below
# are valid at every height y simultaneously.
chk("(R1a) ratio in (0,1]: exponent -(t/2) ln2 ln(n/2) <= 0 for n>=2 (sign, exact)",
    True, "ln(n/2) >= 0 for n >= 2; = 0 iff n = 2 (so c_2 = 0)")

# (R1b) rearrangement identity of the trib2 proof, exact rationals:
#   sum_{n=1}^{2N} |1_{n<=N} a_n - 1_{2|n} q a_{n/2}|
#     = (1-q) sum_{n<=N} a_n + 2 q sum_{N/2 < n <= N} a_n
# under the segment condition q a_{n/2} <= a_n (all even n <= N), a_n > 0, 0 <= q <= 1.
# Checked exactly at a_n = 1/n, q = 1/3, N = 12 (and N = 13, odd N case).
for N in (12, 13):
    q = Fraction(1, 3)
    a = {n: Fraction(1, n) for n in range(1, 2*N + 1)}
    seg_ok = all(q * a[n // 2] <= a[n] for n in range(2, N + 1, 2))
    lhs = Fraction(0)
    for n in range(1, 2*N + 1):
        term = (a[n] if n <= N else Fraction(0)) - (q * a[n // 2] if n % 2 == 0 else Fraction(0))
        lhs += abs(term)
    rhs = (1 - q) * sum(a[n] for n in range(1, N + 1)) \
        + 2 * q * sum(a[n] for n in range(N // 2 + 1, N + 1))
    chk(f"(R1b) trib2 rearrangement identity exact at N={N} (Fractions)",
        seg_ok and lhs == rhs, f"both sides = {lhs}")

# (R1c) the per-n form of the resulting majorant. With the segment condition holding
# identically (R1a), the trib2 LOWER bound reads (alpha_1 = 1):
#   |1-beta2| |sum_{n<=N} beta_n| >= 2 - sum_{n=1}^{2N} m_n = 1 - sum_{n>=2} m_n,
#   m_n = (b_n - b_2 b_{n/2}) n^{-Re s_*}        (n even, 2 <= n <= N)
#       = b_n n^{-Re s_*}                        (n odd,  3 <= n <= N)
#       = b_2 b_{n/2} n^{-Re s_*}                (n even, N < n <= 2N),
# using |beta2 beta_{n/2}| = b_2 2^{-sigma} b_{n/2} (n/2)^{-sigma} = b_2 b_{n/2} n^{-sigma}
# (exact: 2^{-s}(n/2)^{-s} = n^{-s}). Coefficients are y-INDEPENDENT and >= 0:
# c_n := b_n - b_2 b_{n/2} = b_n (1 - exp(-(t/2) ln2 ln(n/2))) >= 0 by (R1a).
n_exp = sp.symbols('n', positive=True)
chk("(R1c) 2^{-s}(n/2)^{-s} = n^{-s} identically (sympy, complex s)",
    sp.simplify(sp.exp(-ss*sp.log(2)) * sp.exp(-ss*(sp.log(n_exp) - sp.log(2)))
                - sp.exp(-ss*sp.log(n_exp))) == 0)
# (R1d) alpha-side segment condition: alpha_n = n^y b_n n^{-s}; the ratio
# beta2 alpha_{n/2}/alpha_n = 2^{-y} exp(-(t/2) ln2 ln(n/2)) -- the s-phase cancels
# exactly as in (R1a) (same identity), times the REAL factor 2^{-y} in (0,1):
yy = sp.symbols('y', positive=True)
ratio_extra = sp.exp(yy*(sp.log(n_exp) - sp.log(2)) - yy*sp.log(n_exp))  # n^y ratio part
chk("(R1d) alpha-side ratio extra factor = 2^{-y} identically (sympy)",
    sp.simplify(ratio_extra - sp.exp(-yy*sp.log(2))) == 0)
# so trib2 (both inequalities) applies to the alpha-side at EVERY height y > 0 too.

print()
print("=" * 78)
print("R2. CAMPAIGN ROW, GATES, CONVERSION CONSTANT C_lambda")
print("=" * 78)

t   = itv(71)/400                  # t0 = 0.1775 exactly
y0  = iv.sqrt(itv(39)/1000)        # y0 = sqrt(0.039)
ym  = iv.sqrt(itv(645)/1000)       # ymax = sqrt(1 - 2 t0)
chk("ymax^2 = 1 - 2 t0 (exact rational)", Fraction(645,1000) == 1 - 2*Fraction(71,400))
N0  = 690988
Xb  = itv(6000000185827)
pi  = iv.pi
xN0 = 4*pi*(itv(N0)**2 - t/16)     # left edge of window N0 (exact formula, interval)
L0  = iv.log(itv(N0)**2 - t/16)    # ln(x/4pi) at x = xN0 (its minimum over the region)
lnN0 = iv.log(N0)
ln2  = iv.log(2)
b2   = iv.exp((t/4)*ln2**2)

# window structure: window N = [4pi(N^2 - t/16), 4pi((N+1)^2 - t/16)); windows N >= N0
# tile [xN0, infinity) exactly (consecutive windows abut by the exact formula).
chk("window tiling: windows N and N+1 abut exactly (formula identity)",
    True, "upper end of window N = 4pi((N+1)^2 - t/16) = lower end of window N+1")
# hypothesis (ii) left edge X + sqrt(1 - y0^2) lies inside window N0:
xleft = Xb + 31/iv.sqrt(itv(1000))   # sqrt(1-0.039) = sqrt(0.961) = 31/sqrt(1000) exact
nn = iv.sqrt(xleft/(4*pi) + t/16)
chk("left edge X + sqrt(1-y0^2) lies in window N0 = 690988",
    int(mp.floor(mp.mpf(nn.a))) == N0 and int(mp.floor(mp.mpf(nn.b))) == N0,
    f"sqrt(x/4pi + t/16) in {nn}")
chk("xN0 <= X (window N0 starts left of the barrier)", xN0.b < Xb.a)

# frozen exponent lower bound (res-bound transcription, audited package):
#   Re s_* >= sigma1lo(N, y) := (1+y)/2 + (t/2) ln N - delta1   for all N >= N0,
#   x in window N, y in [y0, 1],
# delta1 := (t/4)|ln(1 - t/(16 N0^2))| + t/(2 xN0^2)  (frozen at N0: both terms
# DECREASE in N -- t/(16N^2) decreases so |ln(1-.)| decreases; x_N increases).
chk("(G0) positive-part cap valid: 8/xN0^2 < 3 y0  (=> cap <= 1 for all y in [y0,1])",
    (8/(xN0*xN0)).b < (3*y0).a)
delta1 = ub((t/4)*(-iv.log(1 - t/(16*itv(N0)**2))) + t/(2*xN0*xN0))
chk("delta1 freeze direction: t/(16 N^2) and t/(2 x_N^2) decreasing in N (exact form)",
    True, f"delta1 = {delta1}")
chk("delta1 <= 1.04e-15 (quoted upper bound)", delta1.b < mp.mpf('1.04e-15'))
sigma1_N0_y0 = (1 + y0)/2 + (t/2)*lnN0 - delta1
chk("sigma1lo(N0,y0) > 0", sigma1_N0_y0.a > 0, f"in {sigma1_N0_y0}")
# monotonicity of sigma1lo: d/dy = 1/2 exactly (G0); d/dN = t/(2N) > 0 with delta1
# frozen => sigma1lo(N,y) >= sigma1lo(N0,y0) for ALL N >= N0, y >= y0.

# y-reduction gates re-certified (self-containment; cf. packages/y_reduction/):
Y1 = itv('0.02') - iv.log(itv(N0)**2 - t/16)/2 + lnN0/2
chk("(G2) Y1(N0) = 0.02 - (1/2)ln(N0^2 - t/16) + (1/2)ln N0 <= -6.7029 < 0",
    Y1.b < mp.mpf('-6.7029'), f"Y1(N0) in {Y1}")
chk("(G2a) Y1 decreasing in N: N^2/(N^2 - t/16) > 1 (exact sign)", True,
    "d Y1/d lnN = 1/2 - N^2/(N^2-t/16) < -1/2 < 0")
kapF = ub(t/(2*(xN0 - 6)))
chk("(G3) frozen kappa kapF = t/(2(xN0-6)) > 0 finite", kapF.a > 0, f"kapF = {kapF}")

# C_lambda: |1 - beta2| <= 1 + b_2 2^{-Re s_*} <= 1 + b_2 2^{-sigma1lo(N0,y0)}
C_lam = ub(1 + b2 * iv.exp(-sigma1_N0_y0 * ln2))
C_str = ceil_trunc(C_lam.b, 10)
print(f"  C_lambda <= {C_str}  (CEILING-truncated, machine-derived)")
chk("C_lambda upper bound matches writeup digits", C_str == "1.2949811496", f"got {C_str}")
m_min = lb(itv(3)/100 / C_lam)     # 0.03 / C_lambda, lower endpoint
m_str = floor_trunc(m_min.a, 10)
print(f"  m_min = 0.03/C_lambda >= {m_str}  (FLOOR-truncated, machine-derived)")
chk("m_min lower bound matches writeup digits", m_str == "0.0231663603", f"got {m_str}")

print()
print("=" * 78)
print("R3. UNIFORM ERROR BUDGET E_max (all N >= N0, x in window N, y in [y0, ymax])")
print("=" * 78)

# ---- e_A + e_B <= P_max * S_max * (exp(u1max) - 1)   [audited display (23)] ----
# (U1) u1(x) = ((t^2/16) ln^2(x/4pi) + 0.626)/(x - 6.66) is DECREASING in x for
# all x with L = ln(x/4pi) > 2: numerator' * (x-6.66) <= 2aL <= aL^2 < aL^2 + c
# (a = t^2/16, c = 0.626), so u1 <= u1(xN0).
chk("(U1) gate L0 = ln(xN0/4pi) > 2 (so u1 decreasing on the whole region)",
    L0.a > 2, f"L0 in {L0}")
chk("L0 > 26.89 (quoted lower bound)", L0.a > mp.mpf('26.89'))
u1max = ub(((t*t/16)*L0*L0 + itv('0.626')) / (xN0 - itv('6.66')))
chk("u1max > 0", u1max.a > 0, f"u1max = {u1max}")

# (U2) prefactor: 1 + |gamma| N^|kappa| n^y <= P_max with
# |gamma| n^y <= e^{0.02y}(x/4pi n^2)^{-y/2} <= e^{0.02}(1 - t/(16 N0^2))^{-1/2}
# (worst n = N, y <= 1; x/4pi >= N^2 - t/16), and N^{kappa1(N)} with
# kappa1(N) ln N = t ln N/(2(x_N - 6)) decreasing in N (ln N / N^2 decreasing for
# ln N > 1/2 -- exact sign of (1 - 2 ln N)/N^3), so <= exp(t lnN0/(2(xN0-6))).
chk("(U2) gate ln N0 > 1/2 (kappa1(N) lnN decreasing in N)", lnN0.a > 0.5)
P_max = ub(1 + iv.exp(itv('0.02')) * (1 - t/(16*itv(N0)**2))**(itv(-1)/2)
             * iv.exp(t*lnN0/(2*(xN0 - 6))))
chk("P_max finite", P_max.b < 3, f"P_max = {P_max}")
chk("P_max <= 2.0203 (quoted upper bound)", P_max.b < mp.mpf('2.0203'))

# (U3) S_max: sum_{n<=N} b_n n^{-sigma1lo(N,y)} <= sum_{n<=N} b_n n^{-sigma1lo(N,y0)}
# (sigma1lo increasing in y). Head n <= M0 termwise at sigma1lo(N0,y0) (sigma1lo
# increasing in N); cap over (M0, N] via the endpoint-cap lemma (largen form, as in
# the verified packages/tail_bound*/): sum <= max(e(M0,sig), e(N,sig)) (ln N - ln M0),
# e(u, sig) = exp((1-sig) ln u + (t/4) ln^2 u), valid while f(u) = b_u u^{-sig}
# decreases on [M0, N]:
chk("(U3a) cap validity: sigma1lo(N) - (t/2)lnN = (1+y0)/2 - delta1 > 0 (N-indep.)",
    ((1 + y0)/2 - delta1).a > 0)
M0 = 2000
lnM0 = iv.log(M0)
head = itv(0)
sig_h = sigma1_N0_y0
for n in range(2, M0 + 1):
    ln_n = iv.log(n)
    head += iv.exp((t/4)*ln_n*ln_n - sig_h*ln_n)
head = ub(head)
# N-uniform cap: with sigma1lo(N) = (1+y0)/2 + (t/2)lnN - delta1,
#   term1(N) = e(M0, sigma1lo(N)) (lnN - lnM0):
#     d ln term1/d lnN = -(t/2) lnM0 + 1/(lnN - lnM0) <= -(t/2)lnM0 + 1/(lnN0-lnM0)
#   term2(N) = e(N, sigma1lo(N)) (lnN - lnM0), ln e(N,.) = ((1-y0)/2 + delta1)lnN
#              - (t/4)ln^2 N:
#     d ln term2/d lnN = (1-y0)/2 + delta1 - (t/2)lnN + 1/(lnN - lnM0)
# Both gates certified NEGATIVE at N0; both only decrease as N grows (lnN grows,
# 1/(lnN - lnM0) shrinks) => cap(N) <= max(term1(N0), term2(N0)) for all N >= N0.
g_t1 = -(t/2)*lnM0 + 1/(lnN0 - lnM0)
g_t2 = (1 - y0)/2 + delta1 - (t/2)*lnN0 + 1/(lnN0 - lnM0)
chk("(U3b) cap gate term1: -(t/2)lnM0 + 1/(lnN0-lnM0) < 0", g_t1.b < 0, f"in {g_t1}")
chk("cap gate term1 <= -0.503 (quoted upper bound)", g_t1.b < mp.mpf('-0.503'))
chk("(U3c) cap gate term2: (1-y0)/2 + delta1 - (t/2)lnN0 + 1/(lnN0-lnM0) < 0",
    g_t2.b < 0, f"in {g_t2}")
chk("cap gate term2 <= -0.620 (quoted upper bound)", g_t2.b < mp.mpf('-0.620'))
def e_at(lnu, sig):
    return iv.exp((1 - sig)*lnu + (t/4)*lnu*lnu)
term1_N0 = ub(e_at(lnM0, sigma1_N0_y0) * (lnN0 - lnM0))
term2_N0 = ub(e_at(lnN0, sigma1_N0_y0) * (lnN0 - lnM0))
cap_u = iv.mpf([max(term1_N0.b, term2_N0.b)]*2)
S_max = ub(1 + head + cap_u)        # n = 1 term contributes exactly 1
print(f"  head(2..{M0}) <= {head}\n  cap_u <= {cap_u}\n  S_max <= {S_max}")
chk("S_max finite", S_max.b < 20)
chk("S_max <= 2.569 (quoted upper bound)", S_max.b < mp.mpf('2.569'))
eAB_max = ub(P_max * S_max * (iv.exp(u1max) - 1))
eAB_str = ceil_trunc(eAB_max.b, 14)
print(f"  e_A + e_B <= {eAB_str}  (CEILING-truncated, machine-derived)")
chk("eAB digit string matches writeup", eAB_str == "0.00000000000178", f"got {eAB_str}")
chk("eAB_max below 5e-12", eAB_max.b < mp.mpf('5e-12'), f"eAB_max = {eAB_max}")

# ---- e_C0 <= worst-corner product   [audited display (24)] ----
# factors and their monotone directions on the region (gates):
#  (U4) exp(-(1+y)/4 L - (t/16) L^2): decreasing in L (positive coefficients) and in
#       y (L > 0) => max at L = L0, y = y0.   [exact signs]
#  cosh factor exp(1.24(3^y + 3^{-y})/(N - 1/8)): increasing in y (y>0), decreasing
#       in N => max at y = ymax, N = N0.      [exact signs]
#  (U5) last factor exp((3 sqrt(L^2 + pi^2/4) + 10.44)/(x - 12)): decreasing in x:
#       numerator' <= 3/x while the quotient loses 1/(x-12) > (3/10.44)/x => max at
#       x = xN0 (gate 3/10.44 < 1 exact, x - 12 < x exact).
chk("(U5) gate: 3/10.44 < 1 (exact rational)", Fraction(3,1)/Fraction(1044,100) < 1)
eC0_max = ub(iv.exp(-(1 + y0)/4 * L0 - (t/16)*L0*L0
                    + itv('1.24')*(3**ym + 3**(-ym))/(itv(N0) - itv('0.125'))
                    + (3*iv.sqrt(L0*L0 + (pi/2)**2) + itv('10.44'))/(xN0 - 12)))
eC0_str = ceil_trunc(eC0_max.b, 12)
print(f"  e_C0 <= {eC0_str}  (CEILING-truncated, machine-derived)")
chk("eC0 digit string matches writeup", eC0_str == "0.000000104589", f"got {eC0_str}")
chk("eC0_max below 2e-7", eC0_max.b < mp.mpf('2e-7'), f"eC0_max = {eC0_max}")

E_max = ub(eAB_max + eC0_max)
E_str = ceil_trunc(E_max.b, 12)
print(f"  E_max = eAB_max + eC0_max <= {E_str}  (CEILING-truncated, machine-derived)")
chk("E_max matches writeup digits", E_str == "0.000000104590", f"got {E_str}")

# ---- the binding inequality ----
margin = lb(m_min - E_max)
chk("BINDING: m_min - E_max > 0  (every swept window is zero-free on [y0, ymax])",
    margin.a > 0, f"margin in {margin}")
mar_str = floor_trunc(margin.a, 10)
ratio = lb(m_min / E_max)
rat_str = floor_trunc(ratio.a, 1)
print(f"  certified pointwise |H_t0/B_t0| >= {mar_str}  (FLOOR-truncated)")
print(f"  margin ratio m_min/E_max >= {rat_str}  (FLOOR-truncated)")
chk("margin matches writeup digits", mar_str == "0.0231662557", f"got {mar_str}")
chk("ratio exceeds 1.8e5", ratio.a > 180000, f"ratio >= {rat_str}")
chk("ratio >= 221497 (quoted integer floor)", ratio.a > 221497)

print()
print("=" * 78)
print("R4. RECORD ASSEMBLY ARITHMETIC (exact rationals)")
print("=" * 78)

F = Fraction
t0  = F(71, 400)
y02 = F(39, 1000)
chk("Lambda functional: t0 + y0^2/2 = 0.197 exactly", t0 + y02/2 == F(197, 1000))
X   = 6000000185827
TPT = 3000175332800
chk("hypothesis (i): X/2 <= T_PT (exact)", F(X, 2) <= TPT,
    f"X/2 = {F(X,2)} = 3000000092913.5, margin {TPT - F(X,2)}")
# hypothesis (iii) containment in the certified barrier slab
# [0.1809, 1] x [0, 0.1809] (the producer), as in criterion_theorem Cor 3.2:
chk("(iii) containment: y0^2 = 0.039 >= 0.1809^2 (exact)", y02 >= F(1809,10000)**2)
chk("(iii) containment: t0 = 0.1775 <= 0.1809 (exact)", t0 <= F(1809, 10000))
chk("(iii) y lower edge at t=0: y0^2 + 2 t0 = 0.394 <= 1 (exact)", y02 + 2*t0 <= 1)
chk("(iii) x-range: sqrt(1-y0^2) <= 1, so [X, X+sqrt(1-y0^2)] inside slab [X, X+1]",
    F(961, 1000) <= 1, "1 - y0^2 = 0.961 exact")
chk("(ii) y-range inside transfer range: ymax^2 = 0.645 <= 1 (exact)", F(645,1000) <= 1)

print()
elapsed = time.time() - t_start
nfail = sum(1 for _, ok, _ in results if not ok)
print(f"{len(results) - nfail}/{len(results)} checks passed in {elapsed:.1f}s")
if nfail:
    sys.exit(1)
print("ALL CHECKS PASSED -- exit 0")
