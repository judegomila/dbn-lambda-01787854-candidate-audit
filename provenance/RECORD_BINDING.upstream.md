# RECORD_BINDING — the binding lemma: certified sweep ⟹ hypothesis (ii) ⟹ Λ ≤ 0.197

Package: `packages/record_binding/` (this writeup + `verify_record_binding.py`,
standalone, /usr/bin/python3, mpmath interval arithmetic prec 220 + sympy exact +
exact rationals, no disk reads, 50/50 checks, exit 0 in ≈ 1 s; logs `verify_log.txt`
and `verify_clean_copy_log.txt`, the latter from a standalone /tmp copy).
Author: the producer line, 2026-06-12. Sources: arXiv:1904.12438v2 (local copy
`sources/p15/debruijn.tex`, TeX labels `trib2`, `ftxy`, `ftxy-2`, `res-bound`,
`gamma-bound`, `kappa-bound`, `eff`, displays (20)–(24)); this certificate's verified packages
`criterion_theorem`, `error_terms_audit`, `y_reduction`, `tail_bound_5e6`; the verified
shared-verified results the producer (winding slab), the producer (Dirichlet
sweep), the independent verifier (second-line sweep).

**RH-height dependency.** Lemmas R1–R3 below: NONE (unconditional inequalities about
finite Dirichlet sums). The assembled record statement (§5) consumes RH height
T = X/2 = 3 000 000 092 913.5 exactly, supplied **unconditionally** by Platt–Trudgian
2021 (T_PT = 3 000 175 332 800 ≥ X/2, margin 350479773/2 exactly).

Digit conventions: every decimal below is machine-derived inside the verify script —
lower bounds FLOOR-truncated, upper bounds CEILING-truncated, each labeled.

---

## 0. What was still missing, exactly

The record claim Λ ≤ 0.197 rests on Cor. 3.2 of `packages/criterion_theorem/` at
t₀ = 71/400, y₀ = √0.039, X = 6 000 000 185 827, y_max = √(1−2t₀) = √0.645. Its three
hypotheses now have these certified suppliers:

- **(i)** RH to height X/2: PT2021, exact arithmetic re-checked here (§5).
- **(iii)** barrier: the producer's verified winding slab
  [0.1809, 1] × [0, 0.1809] at X, containment re-checked here (§5).
- **(ii)** zero-free right region: the producer's verified **Dirichlet sweep**
  certifies the Lemma-`trib2` Euler-2 selection lower bound
  Q(N) on |1−β₂|·|f_{t₀}(x+iy₀)| with **Q(N) > 0.03 for EVERY integer N ≥ N₀ =
  690988**, gap-free to infinity (full grid [N₀, 5·10⁶] + analytic tail legs), with
  the independent verifier the zero-shared-code second line on [N₀, 10⁷).

But hypothesis (ii) demands H_{t₀}(x+iy) ≠ 0 for **all y ∈ [y₀, y_max]**, not a
selection-bound value at the single height y₀. Three conversion steps were nowhere
written down as one certified statement: (R1) the swept trib2 functional is of the
standard-window-majorant form, so the y-quantifier-reduction theorem
(`packages/y_reduction/`) applies to it — `y_reduction` *asserted* this shape (its
form (c)) but did not prove it; (R2) the swept quantity bounds |1−β₂|·|f_{t₀}|, so a
division by a certified sup of |1−β₂| is needed before zero-freeness of f follows;
(R3) the per-window error budgets E_N that `y_reduction`'s interface {m_N > E_N} left
to the sweep lane must be discharged — here replaced by ONE global uniform budget
E_max valid for all N ≥ N₀, x in window N, y ∈ [y₀, y_max]. This package proves and
certifies R1–R3 and assembles the record statement.

## 1. (R1) The trib2 rewrite lemma: the swept functional is a standard window majorant

Notation (paper §10 / display `ftxy-2`): on window N (i.e. N(x) = ⌊√(x/4π + t/16)⌋ = N),
write s_* = σ + iT (paper `sn-def`), b_n = exp((t/4)ln²n), β_n = b_n n^{−s_*},
α_n = n^y b_n n^{−s_*}, β₂ = b₂ 2^{−s_*}, γ as in `gamma-bound`, κ as in `kappa-bound`.

**Lemma R1.** For every t > 0, every complex s_* and every y > 0:

(a) *Segment condition, identically in s_*.* For even n ≥ 2,
β₂α_{n/2}/α_n = 2^{−y} e^{−(t/2)ln2·ln(n/2)} ∈ (0, 1] — REAL, because the s_*-phase
exponent ln n − ln 2 − ln(n/2) vanishes identically and (t/4)(ln²2 + ln²(n/2) − ln²n)
= −(t/2)ln2·ln(n/2) ≤ 0. (Same for the β-side with the 2^{−y} factor absent.) So the
hypothesis of Lemma `trib2` holds at EVERY point of EVERY window, at every height y
simultaneously. [Verified sympy-exact: checks (R1a), (R1c), (R1d).]

(b) *Per-n mass form.* The trib2 proof's rearrangement identity

  Σ_{n=1}^{2N} |1_{n≤N} a_n − 1_{2|n} q a_{n/2}| = (1−q)Σ_{n≤N} a_n + 2q Σ_{N/2<n≤N} a_n

(valid under q a_{n/2} ≤ a_n, a_n ≥ 0, 0 ≤ q ≤ 1) [verified exactly in rationals at
even and odd N: checks (R1b)] gives, with a_n = |β_n| and the n = 1, 2 masses computed
exactly (m₁ = 1, m₂ = 0 since c₂ = b₂ − b₂b₁ = 0):

  |1−β₂| |Σ_{n≤N} β_n| ≥ 1 − Σ_{n≥3} m_n,
  m_n = c_n n^{−σ} (n ≤ N even, c_n := b_n − b₂b_{n/2} ∈ [0, b_n]),
      = b_n n^{−σ} (n ≤ N odd), = b₂ b_{n/2} n^{−σ} (N < n ≤ 2N even),

using the exact identity 2^{−s}(n/2)^{−s} = n^{−s}. All coefficients are
**y-independent and nonnegative**. The α-side upper bound of trib2 and the κ-term Z
of `ftxy` carry the standard second-sum kernel e^{0.02y}(N²−t/16)^{−y/2}n^{−σ₂} after
`gamma-bound` absorption. Hence the certified selection bound is exactly

  Q(N, y) = 1 − F(N, y),  F a *standard window majorant* in the sense of
  `packages/y_reduction/` §1.  ∎

**Consequence (transfer).** The y_reduction theorem (gates (G0), (G2), (G2a), (G3)
re-certified in this package's script for self-containment: Y₁(N₀) ≤ −6.7029, etc.)
gives F(N, y) ≤ F(N, y₀) for all N ≥ N₀, y ∈ [y₀, 1]. Therefore the sweep certificate
Q(N, y₀) ≥ 0.03 implies

  |1−β₂(x+iy)| · |f_{t₀}(x+iy)| ≥ Q(N, y) ≥ Q(N, y₀) ≥ 0.03
  for ALL x in window N and ALL y ∈ [y₀, y_max] (y_max = √0.645 < 1).

*(Hypothesis (S) — scope of R1, stated honestly.)* The transfer applies to a sweep
whose certified value is the trib2/Lemma-10.1 selection bound with the frozen
y-independent exponent corrections (δ₁, frozen κ) — the published lemmasawtooth /
moll2_arb convention that the survey line's convention finding and the producer's
provenance audit pin for the campaign artifacts. A hypothetical sweep using exact
per-(x,y) κ(y) would additionally need |κ(y)| ≤ κ_F, which gate (G3)'s freeze
(κ_F = t/(2(x_{N₀}−6)), valid for all y ≤ 1, x ≥ x_{N₀}) supplies.

## 2. (R2) The conversion constant

By `res-bound` (transcription audited in `packages/error_terms_audit/`, freeze
direction certified): Re s_* ≥ σ₁(N, y) := (1+y)/2 + (t/2)lnN − δ₁ for all N ≥ N₀,
x in window N, y ∈ [y₀, 1], with δ₁ frozen at N₀ (check (G0): 8/x_{N₀}² < 3y₀ makes
the positive-part cap valid on the whole region; δ₁ ≈ 1.04e−15). σ₁ is increasing in
both N and y, so

  |1−β₂| ≤ 1 + b₂ 2^{−Re s_*} ≤ **C_λ := 1 + b₂ 2^{−σ₁(N₀,y₀)} ≤ 1.2949811496**
  (CEILING-truncated), uniformly on the whole region. Hence

  **|f_{t₀}(x+iy)| ≥ 0.03/C_λ =: m_min ≥ 0.0231663603** (FLOOR-truncated)

for all x ≥ X + √(1−y₀²) (every window N ≥ N₀, the left edge certified to lie in
window N₀ = 690988) and all y ∈ [y₀, y_max].

## 3. (R3) The global uniform error budget

The audited effective-approximation bounds (paper (20)–(24) / Theorem `eff`) are
bounded over the ENTIRE region {N ≥ N₀, x in window N, y ∈ [y₀, y_max]} by certified
monotonicity gates (all interval-verified, script section R3):

- **(U1)** u₁(x) = ((t²/16)ln²(x/4π) + 0.626)/(x − 6.66) is decreasing in x once
  L = ln(x/4π) > 2 (gate: L₀ > 26.89), so u_n ≤ u₁(x_{N₀}); the inner-argument
  maximum over n is at n = 1 (as in the audit).
- **(U2)** prefactor 1 + |γ|N^{|κ|}n^y ≤ P_max ≤ 2.0203: |γ|n^y ≤
  e^{0.02}(1 − t/(16N₀²))^{−1/2} (worst n = N, y = 1); N^{|κ|} decreasing in N for
  ln N > 1/2 (gate).
- **(U3)** Σ_{n≤N} b_n n^{−Re s_*} ≤ S_max ≤ 2.569: head n ≤ 2000 termwise at
  σ₁(N₀,y₀), tail by the endpoint-cap (largen) lemma with BOTH cap endpoints certified
  decreasing in N (gates (U3b), (U3c): log-derivatives ≤ −0.503, −0.620 at N₀, both
  monotone helpful) — so one evaluation at N₀ covers all N.
- ⟹ **e_A + e_B ≤ P_max·S_max·(e^{u₁max} − 1) ≤ 0.00000000000178** (CEILING-truncated).
- **(U4/U5)** e_{C,0} (display (24)): the three factors are maximized separately at
  (L₀, y₀), (y_max, N₀), and x_{N₀} (factor-3 gate 3/10.44 < 1), giving
  **e_{C,0} ≤ 0.000000104589** (CEILING-truncated).

  **E_max := e_A + e_B + e_{C,0} ≤ 0.000000104590** (CEILING-truncated),

uniformly — no per-window budget E_N remains to be discharged; the interface family
{m_N > E_N} of `y_reduction` §4 collapses to the single inequality of §4 below.
(Consistency: E_max agrees to 3 digits with the verified improvement_memo's certified
error-budget total ≈ 1.0466e−7, computed there at the worst point only.)

## 4. The binding inequality

  **m_min − E_max ≥ 0.0231662557 > 0** (FLOOR-truncated; ratio m_min/E_max ≥ 221497).

By Theorem `eff` (audited), |H_{t₀}/B_{t₀}|(x+iy) ≥ |f_{t₀}(x+iy)| − (e_A+e_B+e_{C,0})
≥ m_min − E_max > 0 pointwise, and B_{t₀} is non-vanishing for y > 0 (paper §2):

**Theorem (binding).** Given the producer's certified sweep (Q(N, y₀) ≥ 0.03 for
every integer N ≥ N₀, under hypothesis (S)), H_{t₀}(x+iy) ≠ 0 for every
x ≥ X + √(1−y₀²) and every y ∈ [y₀, y_max] — i.e. **hypothesis (ii) of Cor. 3.2 holds
in full**, with certified pointwise margin |H_{t₀}/B_{t₀}| ≥ 0.0231662557.

## 5. Record assembly (exact arithmetic, script section R4)

With (i) X/2 = 3 000 000 092 913.5 ≤ T_PT (exact; PT2021 unconditional), (ii) by §4,
and (iii) by containment of the Cor.-3.2 barrier region in the producer's
certified winding slab (y₀² = 0.039 ≥ 0.1809², t₀ = 0.1775 ≤ 0.1809, y₀²+2t₀ =
0.394 ≤ 1, √(1−y₀²) ≤ 1 — all exact-rational, re-checked):

  **Λ ≤ t₀ + y₀²/2 = 0.197 exactly** — unconditional given PT2021,
  conditional within the system only on the named verified facts:
  the producer (slab winding), the producer (sweep, hypothesis (S)),
  and the criterion chain of `packages/criterion_theorem/`.

## 6. Novelty boundary

`packages/y_reduction/` proved the abstract transfer for the coefficient-free majorant
class and left (caveat 1) the sweep-functional membership asserted, (caveat 2) the
per-window budgets m_N, E_N to the sweep lane. This package: (a) **proves** membership
(Lemma R1 — the sympy-exact phase cancellation and exact-rational rearrangement are in
no other package); (b) adds the conversion constant C_λ (nowhere else: the sweep
certifies |1−β₂|·|f|, every prior tail package bounded |λf−1| with a different λ);
(c) replaces the open per-window error interface by ONE certified global E_max over
all N ≥ N₀ (the audit evaluated 5 points; tail_bound_5e6 only N ≥ 5·10⁶); (d) states
the assembled record implication with every input named. Nothing here re-runs or
re-derives any verified numeric: the sweep values, slab winding, and PT2021 height are
consumed as cited verified facts.
