# STRETCH_BINDING — the binding lemma at the Λ ≤ 0.1965 stretch row, multi-prime form

Package: `packages/stretch_binding/` (this writeup + `verify_stretch_binding.py`,
standalone, /usr/bin/python3, mpmath interval arithmetic prec 220 + sympy exact +
exact rationals, no disk reads, 84/84 checks, exit 0 in ≈ 1 s; logs `verify_log.txt`
and `verify_clean_copy_log.txt`, the latter from a standalone /tmp copy).
Author: the producer line, 2026-06-12. Policy-2 parameter substitution +
strict extension of the verified `packages/record_binding/` (the producer line).
Sources: arXiv:1904.12438v2 (Lemma `trib2`, displays `ftxy`/`ftxy-2`, `res-bound`,
`gamma-bound`, `kappa-bound`, Theorem `eff`, displays (20)–(24); §10's footnoted
Euler-mollifier discussion); the verified packages `criterion_theorem`,
`error_terms_audit`, `y_reduction`, `record_binding`, `tail_bound_box`; the verified
shared-verified results the independent verifier (load-bearing rung-(a) clearance of
`tail_bound_box` — the standing case's release), the independent verifier (site glue,
N(x,t) = 690988 on [X, X+1] × [0, 0.1809]), the survey line P1 (Euler-3 head value
0.1848895863 at this row), the producer (winding slab).

**Row.** t₀ = 177/1000, y₀ = √(39/1000), X = 6 000 000 185 827, N₀ = 690 988,
y_max = √(1 − 2t₀) = √(646/1000). Λ functional: t₀ + y₀²/2 = 393/2000 = 0.1965 exactly.

**RH-height dependency.** Lemmas P1–P3 and the anchors P5: NONE (unconditional
inequalities about finite Dirichlet sums and exact window geometry). The assembled
conditional record statement (§4) consumes RH height T = X/2 = 3 000 000 092 913.5
exactly, supplied **unconditionally** by Platt–Trudgian 2021
(T_PT = 3 000 175 332 800 ≥ X/2, slack exactly 350479773/2).

**Digit law.** Every decimal below is machine-derived inside the verify script —
lower bounds FLOOR-truncated, upper bounds CEILING-truncated, each labeled. Quoted
verified literals from other lines are labeled with their run ids.

---

## 0. What this package adds, exactly

`record_binding` proved sweep ⟹ hypothesis (ii) ⟹ Λ ≤ 0.197 at the record row
t₀ = 71/400 for the **Euler-2** mollifier E₂ = 1 − β₂. The stretch row 0.1965 cannot
use Euler-2: the pinned floor failure (the survey line: 0.0201508110 < 0.03) shows the
Euler-2 selection bound dies at t₀ = 0.177, while the survey line P1 certifies the
**Euler-3** head value 0.1848895863 > 0.03 at the same row. So the binding lemma the
0.1965 assembly needs is the record_binding pipeline (i) **parameterized in t₀** and
(ii) **extended from E₂ to multi-prime Euler mollifiers** E_P = ∏_{p∈P}(1 − β_p),
P ⊆ {2,3,5,7} — with the conversion constant becoming a product C_P and everything
else surviving verbatim. This package proves the extension (P1), certifies the
constants at the stretch row (P2/P3), states the conditional binding theorem with the
**analytic floor θ_min** the sweep threshold must clear (P4), and carries its own
rung-(a) anchors (P5): the SAME parameterized code reproduces every pinned
record_binding digit string at t₀ = 71/400 and the independent verifier's exact site
margins at both rows. The tail leg (N ≥ 5·10⁶) is **cited**, not re-derived:
`packages/tail_bound_box/` is independently verified and citable as of
the independent verifier's pinned rung-(a) anchor validation; its t-box [0.176, 0.181]
contains 0.177 and its y-box [0.1809, √0.648] contains [y₀, √0.646] (exact-rational
containments certified in §4).

## 1. (P1) The multi-prime rewrite lemma

Notation as in record_binding §1: on window N, s_* = σ + iT, b_n = exp((t/4)ln²n),
β_p = b_p p^{−s_*}, α_n = n^y b_n n^{−s_*}.

**Lemma P1.** For every t > 0, every prime p, every complex s_* and every y > 0:

(a) *Phase cancellation, identically in s_*.* For p | n,
β_p α_{n/p}/α_n = p^{−y} e^{−(t/2)ln p·ln(n/p)} ∈ (0, 1) — REAL: the s_*-exponent
ln n − ln p − ln(n/p) vanishes identically, and ln²p + ln²(n/p) − ln²n =
−2 ln p·ln(n/p) ≤ 0 (= 0 iff n = p). The β-side ratio is the same without p^{−y}.
[Verified sympy-exact for each p ∈ {2,3,5,7}: checks (P1a), (P1b).]

(b) *Mass form.* Expanding E_P f by inclusion-exclusion over S ⊆ P with q_S = ∏_{p∈S}p
(exact Dirichlet algebra p^{−s}(n/p)^{−s} = n^{−s}), the coefficient of n^{−s_*} is
c_n = Σ_{S: q_S | n} (−1)^{|S|} (∏_{p∈S} b_p) b_{n/q_S} — every factor y-INDEPENDENT.
The n = 1 coefficient is exactly 1 (only S = ∅ divides 1; check (P1c); exact-rational
instance at P = {2,3}, n ∈ {1, 6}: check (P1d)). Hence the frozen-convention selection
lower bound has the form Q_P(N, y) = 1 − Σ_{n≥2} m_n(y), m_n = |c_n| n^{−σ} with
y-independent masses — a *standard window majorant* in the sense of
`packages/y_reduction/` §1, for EVERY P ⊆ {2,3,5,7}.  ∎

**Transfer.** The y_reduction gates re-certified at t₀ = 177/1000 (script: G0 with
8/x_{N₀}² < 3y₀; Y1(N₀) ≤ −6.70, interval [−6.7029388683, −6.7029388682]; G3 frozen
κ_F > 0) give Q_P(N, y) ≥ Q_P(N, y₀) for all N ≥ N₀, y ∈ [y₀, 1]: a sweep at the
single height y₀ controls the whole y-interval, exactly as at the record row.
Hypothesis (S) of record_binding §1 (frozen-convention sweep) carries over verbatim.

## 2. (P2) The conversion constants C_P

Re s_* ≥ σ₁(N, y) = (1+y)/2 + (t/2)ln N − δ₁ on the whole region (res-bound, audited;
δ₁ frozen at N₀ with both terms decreasing in N, δ₁ < 1.04e−15 also at this row;
σ₁ increasing in N and y). Hence, uniformly for all N ≥ N₀, x in window N, y ∈ [y₀,1]:

  |E_P(x+iy)| ≤ ∏_{p∈P} (1 + b_p p^{−σ₁(N₀,y₀)}) =: C_P,
  σ₁(N₀,y₀) ≥ **1.7887022679** (FLOOR-truncated).

Certified values (CEILING-truncated, machine-derived):

| P | C_P ≤ |
|---|---|
| {2} | 1.2956514986 |
| {2,3} | 1.4871894818 |
| {2,3,5,7} | 1.6384739261 |

with the monotonicity C_{2} < C_{2,3} < C_{2,3,5,7} certified (more primes never
shrink the constant — the price of a larger family is paid here, cf. the earlier note's
conversion-table rule). A sweep value Q_P ≥ θ therefore gives
|f_{t₀}| ≥ θ/C_P =: m_min on the region.

## 3. (P3) The global error budget at the stretch row

The (20)–(24)/Theorem-`eff` budget under the monotonicity gates (U1)–(U5) of
record_binding §3, all re-certified at t₀ = 177/1000 (gates L₀ > 26.89 analog,
ln N₀ > 1/2, cap gates term1 < −0.50 / term2 < −0.61, factor-3 gate): uniformly over
{N ≥ N₀, x in window N, y ∈ [y₀, y_max]},

  e_A + e_B ≤ **0.00000000000178** (CEILING), e_{C,0} ≤ **0.000000106979** (CEILING),
  **E_max ≤ 0.000000106981** (CEILING).

E_max is independent of P — the mollifier enters the binding inequality only through
C_P (certified: the three runs share the identical E_max endpoint).

## 4. (P4) The conditional binding theorem and the analytic floor θ_min

**Theorem (stretch binding, conditional).** Let P ⊆ {2,3,5,7} and suppose a
frozen-convention sweep (hypothesis (S)) certifies Q_P(N, y₀) ≥ θ for EVERY integer
N with N₀ ≤ N < 5·10⁶, with θ > θ_min(P) := C_P · E_max. Then for all x ≥ X + √0.961
in those windows and all y ∈ [y₀, y_max]:

  |H_{t₀}/B_{t₀}|(x+iy) ≥ θ/C_P − E_max > 0.

Combined with the independently verified tail certificate `packages/tail_bound_box/`
(citable per the independent verifier; covers ALL N ≥ 5·10⁶ with t-box ∋ 0.177 and
y-box ⊇ [y₀, √0.646], certified |H_t/B_t| ≥ 0.0833079015 > 0 there), hypothesis (ii)
of Cor. 3.2 holds in full; with (i) X/2 ≤ T_PT (exact, slack 350479773/2) and (iii)
the barrier-slab containments (y₀² = 0.039 ≥ 0.1809², t₀ = 0.177 ≤ 0.1809,
y₀² + 2t₀ = 393/1000 ≤ 1 — all exact-rational, the an earlier run identities), **Λ ≤ 0.1965**.

Certified floors and margins (machine-derived):

- θ_min({2}) ≤ 0.000000138610, θ_min({2,3}) ≤ 0.000000159101,
  θ_min({2,3,5,7}) ≤ 0.000000175285 (all CEILING).
- At the design threshold θ = 0.03: m_min({2,3}) ≥ 0.0201722782, binding margin
  m_min − E_max ≥ **0.0201721712** (FLOOR); margins also positive for {2} and
  {2,3,5,7}.
- The 0.03 design threshold exceeds the Euler-3 analytic floor by a factor
  ≥ **188560.6** (FLOOR) — quantifying, at this row, the earlier note's structural point:
  the analytic stack constrains the sweep threshold at the 1e−7 scale; 0.03 is purely
  a numerics-side design constant with ~5 orders of magnitude of headroom.
- The pinned Euler-3 head value 0.1848895863 (the survey line P1, quoted verified
  literal) exceeds θ_min({2,3}) by a factor ≥ **1162096.4** (FLOOR) and exceeds 0.03.
  What remains open for the 0.1965 assembly is therefore EXACTLY the sweep quantifier
  — Q_{2,3}(N, y₀) ≥ θ for every N ∈ [N₀, 5·10⁶), not just the head windows — which
  is the producer/numerics lane work, not analytic work. No analytic gap remains.

## 5. (P5) Rung-(a) anchors (built into the verify script)

Per the verification policy, this package's machinery is the already-pinned
record_binding pipeline (same kernel class) with a parameter promotion (t₀, P); the
script therefore carries two anchor reproductions in DIFFERENT regimes:

- **Anchor 1 (record row, t₀ = 71/400, P = {2}).** The parameterized code reproduces
  ALL verified record_binding digit strings at their stated rounding modes:
  C_λ 1.2949811496 (ceil10), m_min 0.0231663603 (floor10), e_A+e_B 0.00000000000178
  (ceil14), e_{C,0} 0.000000104589 (ceil12), E_max 0.000000104590 (ceil12), margin
  0.0231662557 (floor10), ratio floor ≥ 221497, plus the pinned gate literals
  (δ₁ ≤ 1.04e−15, Y1 ≤ −6.7029, L₀ > 26.89, cap gates ≤ −0.503/−0.620,
  P_max ≤ 2.0203, S_max ≤ 2.569). 14 checks.
- **Anchor 2 (site geometry, both rows).** The window formula reproduces
  the independent verifier's pinned exact site margins on BOTH interval endpoints at
  floor4: record row 5377393.0183 / 11989041.1442, stretch row 5377393.0179 /
  11989041.1446. 4 checks.

NO discrepancy found in either anchor.

## 6. Novelty boundary

Not in any pinned package: (a) the multi-prime rewrite Lemma P1 (record_binding R1
covered only p = 2; the inclusion-exclusion mass form and the per-p phase
cancellations are new); (b) the conversion-constant table C_P at the stretch row and
the proof that E_max is P-independent; (c) the analytic floor θ_min = C_P·E_max as an
explicit certified object — the precise statement of "what the (20)–(24)/(71)–(74)
stack requires of a sweep threshold", resolving what s9 mollifier note opened
qualitatively; (d) the stretch-row instantiation of every gate; (e) the assembled
conditional 0.1965 statement that cites tail_bound_box as a hypothesis — the FIRST
such citation, made legal by the independent verifier's pinned clearance of the
our standing requirement. Nothing here re-runs a sweep, re-derives a pinned numeric,
or duplicates record_binding (whose theorem is unconditional-given-the-0.197-sweep at
a different row and a single mollifier).
