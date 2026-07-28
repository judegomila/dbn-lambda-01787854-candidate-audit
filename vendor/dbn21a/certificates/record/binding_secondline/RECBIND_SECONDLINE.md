# Second line on the producer line's record_binding package

Independent verification line, a separate run (2026-06-12).
Bundle: `recbind_secondline_iv.py` (the certificate, /usr/bin/python3,
mpmath.iv prec 200 + sympy exact + exact `Fraction` rationals, no disk
reads, 35/35 gates, exit 0 in ~2 s) + `verify.sh` + `run_log.txt`
(producing run) + `run_log_tmpcopy.txt` (standalone /tmp clean-copy run).

## Independence statement (zero shared code)

Every formula in the script is transcribed from arXiv:1904.12438 (TeX
labels cited inline in the script header: `N-def-main`, `res-bound`,
`gamma-bound`, `kappa-bound`, `eab-bound`, `ec-bound`, `alpha-def`,
`sn-def`, `bn-def`). the producer line's `verify_record_binding.py` was never
opened by this line; only the prose note `RECORD_BINDING.md` and the
verified shared-verified results text were read — to know WHICH constants to
re-derive, and to transcribe the producer's PRINTED digit strings into
the cross-line match gates (C3, C4, D5, E2; the strings appear in the
script as string literals, compared against MY machine-derived
truncations). The complex-interval helpers (cadd/cmul/cdiv/carg with
half-plane branch-cut guard) are this certificate's own, carried from the
previously verified windrect line. The monotonicity chains (M1)–(M6) below are
derived independently and are NOT the producer's gates (U1)–(U5): where
they used an endpoint-cap (largen) lemma for the Dirichlet-sum bound,
I use a p-series integral tail — deliberately a different majorant, so
agreement of the final budget is a genuine two-line consistency check,
not a re-execution.

## What is certified (script sections)

- **A (assembly, exact rationals):** Λ ≤ t0 + y0²/2 = 197/1000 exactly;
  X/2 = 6000000185827/2 ≤ T_PT = 3000175332800 with margin exactly
  350479773/2 (PT2021, unconditional); winding-slab containments
  y0² = 39/1000 ≥ 0.1809², t0 = 71/400 ≤ 0.1809, y0² + 2t0 = 197/500
  ≤ 1, ymax² = 1 − 2t0 = 129/200; the N0-window brackets [X, X+1]
  (A4a/A4b margins ≥ 5377393 and ≥ 11989041, FLOOR), so the region's
  left edge X + sqrt(1−y0²) ∈ (X, X+1) lies in window N0 = 690988.
- **B (R1 algebra):** the s_*-phase cancellation and the b-exponent
  identity behind the trib2 segment condition, as sympy polynomial
  identities in u = ln n, l2 = ln 2 (exact for all n ≥ 2, all complex
  s_*, all t — the cancellation is identical, not numerical); b_1 = 1
  hence c_2 = 0 (sympy exact); the trib2 rearrangement identity in
  exact rationals at even and odd N for three coefficient families
  including the q = 1 edge case (hypothesis q·a_{n/2} ≤ a_n checked
  per family inside the gate).
- **C (R2):** my own uniform σ_min on Re s_* and conversion constant.
- **D (R3):** my own global uniform error budget E_my.
- **E (R4):** the binding inequality on MY constants.
- **F (probe):** direct two-sided complex-interval s_* and |1−β₂| at
  the exact in-region integer point x = X+1, y = y0, falsification-
  testing the one-sided freeze chain: Re s_* (direct) exceeds σ_min by
  ≥ 3.97703e-8 (FLOOR; consistent with (t/4)·Δx/x ≈ 4e-8 for the
  Δx ≈ 5.4e6 distance from the window-left edge), and the pointwise
  |1−β₂| ∈ [0.727771658129, 0.727771658130] sits below the cap C_my
  with slack ≥ 0.567209 (FLOOR).

## Monotonicity chains (M1)–(M6) — the proofs the gates instantiate

Region R := {N ≥ N0, x in window N (so x ≥ xL := 4πN0²−πt0/4),
y ∈ [y0, 1]} ⊇ the binding lemma's region (ymax < 1). t = t0 = 71/400.

**(M1) corr is maximized at (xL, y0).** corr(x,y) = (t/2x²)·g(x,y)_+,
g = 1 − 3y + 4y(1+y)/x². ∂g/∂y = −3 + 4(1+2y)/x² < 0 on R (gated C1b
at the worst point y = 1, x = xL; the expression is increasing in y and
decreasing in x, so that point dominates). Hence g decreasing in y;
g ≤ g(y0); and 1 − 3y0 > 0 (gated C1a) keeps the positive part active
at y0. In x: both factors t/2x² and g(x, y)_+ are positive and
nonincreasing in x (g loses only its positive 4y(1+y)/x² term as x
grows), so corr ≤ corr(xL, y0) =: corr_max on all of R.

**(M2) σ uniform lower bound.** By (res-bound), Re s_* ≥ σ₁(x,y) =
(1+y)/2 + (t/4)log(x/4π) − corr(x,y) ≥ (1+y0)/2 + (t/4)log(xL/4π)
− corr_max =: σ_min on R (each of the three terms bounded separately:
y ≥ y0, x ≥ xL, corr ≤ corr_max). Then |1−β₂| ≤ 1 + |β₂| =
1 + b₂^t 2^{−Re s_*} ≤ 1 + b₂^t 2^{−σ_min} =: C_my, and the sweep
certificate |1−β₂|·|f| ≥ 0.03 gives |f| ≥ 0.03/C_my =: m_min.

**(M3) Dirichlet-sum majorant (my line; producer used endpoint-cap).**
For n ≤ N and x in window N: b_n^t n^{−Re s_*} = n^{(t/4)ln n − Re s_*}
≤ n^{(t/4)ln N − Re s_*} (n ≥ 1, exponent increased). On window N,
x/4π ≥ N² − t/16, so (t/4)log(x/4π) ≥ (t/2)ln N + (t/4)log(1−t/16N²),
hence Re s_* − (t/4)ln N ≥ (1+y0)/2 + (t/4)ln N − eps(N), with
eps(N) := −(t/4)log(1−t/(16N²)) + corr_max(N) — both pieces decreasing
in N — so for all N ≥ N0 the exponent is ≥ p := (1+y0)/2 +
(t/4)ln N0 − eps(N0) (gated D1: p > 1). Therefore
Σ_{n≤N} b_n^t n^{−Re s_*} ≤ Σ_{n≥1} n^{−p} ≤ 1 + 2^{−p} +
∫_2^∞ x^{−p}dx = 1 + 2^{−p} + 2^{1−p}/(p−1) =: S_my.

**(M4) prefactor.** 1 + |γ|N^{|κ|}n^y ≤ 1 + e^{0.02y}
(N²/(x/4π))^{y/2} N^{|κ|} (by gamma-bound and n ≤ N) ≤ 1 + e^{0.02}
(1−t/16N0²)^{−1/2} exp(t ln N0/(2(xL−6))) =: P_my, using on window N:
N²/(x/4π) ≤ (1−t/16N²)^{−1} (≥ 1, worst at N0, exponent y/2 ≤ 1/2);
|κ| ≤ ty/(2(x−6)) ≤ t/(2(x−6)); and ln N/(xL(N)−6) decreasing in N
(for N' > N0: ln N'/ln N0 ≤ N'/N0 ≤ N'²/N0² ≤ (4πN'²−c)/(4πN0²−c)
for the positive constant c = πt/4 + 6, so the ratio of numerators is
dominated by the ratio of denominators).

**(M5) exp-factor.** u(x) := ((t²/16)log²(x/4π) + 0.626)/(x−6.66):
u'(x) < 0 once L := log(x/4π) > 2, because the numerator's derivative
(t²/8)L/x times (x−6.66) is < (t²/8)L ≤ (t²/16)L² < numerator for
L > 2; L ≥ L0 > 26.8 on R (gated C2). The (eab-bound) inner argument
satisfies log²(x/4πn²) ≤ log²(x/4π) for 1 ≤ n ≤ N on window N because
x/4πn² ∈ [x/4πN², x/4π] and |log(x/4πN²)| ≤ −log(1−t/16N0²) ≪ L0
(gated D3). Hence e_A + e_B ≤ P_my · S_my · (e^{u(xL)} − 1) on R.

**(M6) e_C0.** Each (ec-bound) factor is maximized at x = xL, N = N0
over R: the exponents −((1+y)/4)L and −(t/16)L² decrease in x (L
increasing); 1.24(3^y+3^{−y})/(N−0.125) decreases in N; the last term
(3|L + iπ/2| + 10.44)/(x−12) decreases in x because its numerator's
derivative 3L'·L/sqrt(L²+π²/4) ≤ 3/x gives num'·(x−12) < 3 < 10.44 ≤
num. The y-dependence is enclosed outright by evaluating with y as the
full interval hull [y0, ymax].

## Results (all decimals machine-derived; FLOOR for lower bounds,
CEIL for upper bounds, exact-rational endpoint comparisons throughout)

| quantity | my line | producer printed | gate |
|---|---|---|---|
| C_λ (CEIL 10dp) | 1.2949811496 | 1.2949811496 | C3 MATCH |
| m_min (FLOOR 10dp) | 0.0231663603 | 0.0231663603 | C4 MATCH |
| e_C0 (CEIL 6sig) | 1.04589e-7 | 1.04589e-7 | D5 MATCH |
| e_A+e_B (CEIL) | 4.0765946e-12 | 1.78e-12 | D4/D6 (see below) |
| E total (CEIL) | 1.0459223e-7 | 1.04590e-7 | D6 |
| binding margin (FLOOR 10dp) | 0.0231662557 | 0.0231662557 | E2 MATCH |
| ratio m_min/E (FLOOR int) | 221492 | 221497 | E3 (> 2e5) |

**The e_A+e_B difference is NOT a discrepancy.** Both numbers are
upper bounds for the same true quantity; mine is larger because (M3)'s
integral-tail majorant (S_my ≤ 5.906039822, CEIL) is deliberately
cruder than the producer's endpoint-cap chain (their S_max ≤ 2.569).
Gate D6 verifies 0 ≤ E_my − E_prod ≤ my eAB term, i.e. the entire
excess is attributable to the eAB leg while the e_C0 legs digit-match.
The binding margin's 10-digit FLOOR is nevertheless IDENTICAL on the
two lines (E2) because the margin is dominated by m_min: a genuine
two-line value match on the package's headline number.

## Scope honesty

Consumed as verified facts, exactly as the producer consumes them (not
re-derived here): the Dirichlet sweep Q(N, y0) ≥ 0.03 for N ≥ N0
(the producer; second-lined on [N0, 1e7) by the independent verifier),
the y_reduction transfer theorem F(N,y) ≤ F(N,y0) and its gates
G0/G2/G2a/G3 (the producer line y_reduction package), the winding-slab fact
(the producer; corner-audited by the independent verifier), and
hypothesis (S) (the frozen y-independent exponent convention). What IS
independently re-derived: the R1 algebra (B gates), the R2 conversion
chain (C gates, my own monotonicity proofs), a global error budget of
my own construction (D gates), the binding inequality and full exact
assembly (E, A gates), plus the pointwise falsification probe (F).

## RH-height dependency

NONE in every inequality certified here (finite Dirichlet sums and
closed-form majorants at fixed parameters). The assembled record
statement Λ ≤ 0.197 consumes RH to height T = X/2 = 3000000092913.5
unconditionally via Platt–Trudgian 2021 (gate A2: T_PT =
3000175332800 ≥ X/2, margin exactly 350479773/2).

## Verify

    bash verify.sh        # from this directory or any copy of it

Runs the certificate standalone (no disk reads outside the dir), pins
the script md5, requires `TOTAL GATES RUN: 35` + `RESULT: ALL PASS` +
exit 0. ~2 s, single core.
