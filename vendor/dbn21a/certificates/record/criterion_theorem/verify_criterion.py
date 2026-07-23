#!/usr/bin/env python3
"""Standalone verifier for THEOREM_LAMBDA_CRITERION.md (package criterion_theorem).

Checks, in EXACT rational / interval / symbolic arithmetic:
  [A] Lemma 0.1 (x = 2T, y = 1-2sigma normalization) symbolically with sympy,
      plus a numerical spot check H_0(2*gamma_1) ~ 0 at the first zeta zero.
  [B] Theorem 2.1 instantiation arithmetic at (X, t0, y0) = (5e12+194858, 0.186, 0.16733):
      Lambda functional, RH-height consumption vs T_PT, validity inequalities,
      N-constancy of N = floor(sqrt(x/4pi + t/16)) on the barrier slab (interval arith).
  [C] Corollaries 3.1 / 3.2 arithmetic (X' = 6e12+185827) incl. region containment
      and the 2*T_PT admissibility ceiling.
  [D] Floor remark arithmetic: 0.19-row height requirement vs T_PT.
Exit 0 iff all checks pass. Runtime well under 120 s; no network, no repo code.
"""
import sys
from fractions import Fraction as F

import sympy as sp
import mpmath
from mpmath import mp, mpf, iv

FAIL = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAIL.append(name)

# ---------- [A] Lemma 0.1: normalization x = 2T, y = 1 - 2 sigma ----------
sigma, T = sp.symbols('sigma T', real=True)
s = sigma + sp.I*T
# z(s) = -2*I*(s - 1/2);  H_0(z) = (1/8) xi(1/2 + i z/2)  =>  1/2 + i z(s)/2 == s
z = -2*sp.I*(s - sp.Rational(1, 2))
check("A1 symbolic: 1/2 + i*z(s)/2 == s", sp.simplify(sp.Rational(1, 2) + sp.I*z/2 - s) == 0)
x_expr = sp.expand(sp.re(z))
y_expr = sp.expand(sp.im(z))
check("A2 symbolic: Re z = 2T", sp.simplify(x_expr - 2*T) == 0)
check("A3 symbolic: Im z = 1 - 2 sigma", sp.simplify(y_expr - (1 - 2*sigma)) == 0)
# strip map: sigma in [0,1] <-> y in [-1,1]; critical line sigma=1/2 <-> y=0
check("A4 critical line maps to y=0", y_expr.subs(sigma, sp.Rational(1, 2)) == 0)

# numerical spot check: H_0(2*gamma_1) ~= 0, H_0(2*gamma_1 + 0.5) not small
mp.dps = 40
gamma1 = mpmath.zetazero(1).imag          # 14.13472514...
def H0(zv):
    sv = mpf(1)/2 + 1j*zv/2
    xi = sv*(sv-1)/2 * mpmath.pi**(-sv/2) * mpmath.gamma(sv/2) * mpmath.zeta(sv)
    return xi/8
h_at = abs(H0(2*gamma1)); h_off = abs(H0(2*gamma1 + mpf(1)/2))
check("A5 numeric: |H0(2*gamma1)| < 1e-30 and |H0(2*gamma1+0.5)| > 1e-6 * scale",
      h_at < mpf('1e-30') and h_off > mpf('1e6') * h_at and h_off > mpf('1e-12'))

# ---------- [B] Theorem 2.1 instantiation (exact rationals) ----------
X  = 5 * 10**12 + 194858
t0 = F('0.186'); y0 = F('0.16733')
T_PT = 3_000_175_332_800
lam = t0 + y0*y0/2
check("B1 Lambda = t0 + y0^2/2 = 0.19999966445 exactly", lam == F('0.19999966445'))
check("B2 Lambda < 0.2", lam < F('0.2'))
check("B3 X/2 = 2500000097429 exactly and <= T_PT", F(X, 2) == 2500000097429 and F(X, 2) <= T_PT)
check("B4 margin T_PT - X/2 = 500175235371", T_PT - F(X, 2) == 500175235371)
check("B5 canopy validity y0^2 + 2 t0 <= 1", y0*y0 + 2*t0 == F('0.3999993289') and y0*y0 + 2*t0 <= 1)
check("B6 (ii)-range nonempty y0^2 <= 1 - 2 t0", y0*y0 <= 1 - 2*t0)
check("B7 region (eq. `region`): 0 < t0 <= 1/2, X >= 200", 0 < t0 <= F(1, 2) and X >= 200)
check("B8 slab superset: sqrt(1-y0^2) <= 1 i.e. y0^2 >= 0", y0*y0 >= 0)

# N-constancy on the slab x in [X, X+1], t in [0, t0], N = floor(sqrt(x/4pi + t/16))
# interval arithmetic: enclose sqrt(x/(4 pi) + t/16) over the box and check floor constant.
iv.dps = 60
box = iv.sqrt(iv.mpf([X, X+1])/(4*iv.pi) + iv.mpf([0, float(t0)])/16)
N_lo = int(mpmath.floor(box.a))
N_hi = int(mpmath.floor(box.b))
check("B9 N constant = 630783 on slab (interval arithmetic)", N_lo == N_hi == 630783)

# ---------- [C] Corollaries 3.1 / 3.2 ----------
Xp = 6 * 10**12 + 185827
t0p = F('0.1809'); y0p = F('0.1809')
lam31 = t0p + y0p*y0p/2
check("C1 Cor3.1 Lambda = 0.197262405 exactly", lam31 == F('0.197262405'))
check("C2 Cor3.1 X'/2 = 3000000092913.5 <= T_PT, margin 175239886.5",
      F(Xp, 2) == F('3000000092913.5') and F(Xp, 2) <= T_PT and T_PT - F(Xp, 2) == F('175239886.5'))
check("C3 Cor3.1 validity: y0'^2 + 2 t0' = 0.39452481 <= 1 and y0'^2 <= 1 - 2 t0'",
      y0p*y0p + 2*t0p == F('0.39452481') and y0p*y0p <= 1 - 2*t0p)
t0q = F('0.1775'); y0q2 = F('0.039')   # y0'' = sqrt(0.039)
lam32 = t0q + y0q2/2
check("C4 Cor3.2 Lambda = 0.197 exactly", lam32 == F('0.197'))
check("C5 Cor3.2 validity: y0''^2 + 2 t0'' = 0.394 <= 1 and y0''^2 <= 1 - 2 t0''",
      y0q2 + 2*t0q == F('0.394') and y0q2 <= 1 - 2*t0q)
# containment of barrier regions: y0''^2 >= y0'^2 and t0'' <= t0'
check("C6 region containment: 0.039 >= 0.1809^2 and 0.1775 <= 0.1809",
      y0q2 >= y0p*y0p and t0q <= t0p)
check("C7 admissibility ceiling: X' <= 2*T_PT = 6000350665600",
      Xp <= 2*T_PT and 2*T_PT == 6_000_350_665_600)

# ---------- [D] floor remark ----------
X19 = 2 * 10**13 + 131252
check("D1 0.19-row needs T >= X/2 = 10000000065626 > T_PT",
      F(X19, 2) == 10_000_000_065_626 and F(X19, 2) > T_PT)
# ratio floor-truncated 3.33313...
ratio = F(X19, 2) / T_PT
check("D2 ratio in (3.33313, 3.33314)", F('3.33313') < ratio < F('3.33314'))

print()
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
print("ALL CHECKS PASSED (criterion_theorem package)")
sys.exit(0)
