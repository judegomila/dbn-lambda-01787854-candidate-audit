/-
  BarrierAnalyticSkeleton — machine-checked ABSTRACT skeletons of the two
  prose-only analytic reductions in the "closed-barrier" (Polymath15-method)
  zero-free argument for the de Bruijn–Newman bound Λ ≤ 0.1787854.

  An independent referee flagged exactly two steps in the computer-assisted proof
  candidate as prose-only (not machine-checked):

    STEP 1.  The t = 0 endpoint extension.  A strict lower bound on |f_t| valid for
             t ∈ (0, t0] is passed to the closed endpoint t = 0 by continuity, so the
             zero-free conclusion holds on the CLOSED parameter interval [0, t0].

    STEP 2.  B_t ≠ 0 on the compact rectangle R.  Because B_t is a nonvanishing
             factor `M₀` times an exponential `exp(·)` (never zero), the auxiliary
             function `g_t = H_t / B_t` has EXACTLY the same zeros as `H_t` on R, so the
             argument-principle winding count of `g_t` counts zeros of `H_t`, not spurious
             poles.

  This file proves, sorry-free, the REUSABLE ABSTRACT LEMMAS underlying each step,
  reducing the candidate's claim to precisely-stated NAMED HYPOTHESES.  It deliberately
  does NOT build the real Riemann Ξ / H_t / B_t — that is months of separate analytic
  infrastructure.  Everything candidate-specific enters as an explicit hypothesis.

  ## HONEST SCOPE STATEMENT

  What IS machine-checked here: the pure *reduction logic* of both steps.

    • Step 1 (`lowerbound_extends_to_endpoint`): a NON-STRICT bound `c ≤ F t` on a set
      accumulating at 0 from the right passes to `c ≤ F 0` by continuity.  Note carefully:
      a *strict* bound `c < F t` for `t > 0` only yields the *non-strict* `c ≤ F 0` in the
      limit (strictness is NOT preserved by limits).  This is precisely why the candidate
      cannot merely take a limit: it must — and does — evaluate the barrier functional
      DIRECTLY at t = 0 with a strict interior margin.  `strict_lowerbound_on_Icc_of_min`
      is the honest device it actually uses: a continuous function on the compact `[0,t0]`
      attains a global minimum; if that attained minimum exceeds `c`, the strict bound
      holds on the whole closed interval, endpoint included.  `lowerbound_extends_to_endpoint`
      is then the safety net guaranteeing the non-strict bound never fails at the endpoint.

    • Step 2 (`Btmul_ne_zero`, `zeros_Ht_eq_zeros_g_of_B_ne_zero`): `M₀ z ≠ 0` and
      `exp(·) ≠ 0` give `B z ≠ 0`, and on the set where `B z ≠ 0` the zeros of `H/B`
      coincide with the zeros of `H`.

  What is NOT proved here (remains as named hypotheses the candidate must discharge with
  the real analytic setup — this file does NOT eliminate that human-review surface, it
  only SHRINKS it by machine-checking the reduction logic):

    (a) STEP 1's continuity hypothesis for the ACTUAL H_t: that the real barrier functional
        `F : ℝ → ℝ` (built from H_t) is continuous up to and including t = 0.  For the true
        H_t this is joint continuity in (t, ·) up to t = 0, obtained by dominated convergence
        with the integrable dominator `e^{t0 u² + u} |Φ(u)|`.  Here it is the bare hypothesis
        `ContinuousAt F 0` / `ContinuousOn F (Set.Icc 0 t0)`.

    (b) STEP 2's `M0_ne_zero`: that the specific factor M₀ is nonzero on the specific
        rectangle R.  In the candidate this comes from a numerical certificate bounding
        `‖M₀‖` below by a positive constant on R.  `M0_ne_zero_of_lt_norm_on` /
        `M0_ne_zero_of_continuous_pos_on_compact` show the SHAPE by which such a certificate
        discharges the hypothesis, but the certificate itself (the real M₀) is not built here.

  Axiom footprint of every result below is the mathlib-standard
  `[propext, Classical.choice, Quot.sound]` (verified via `#print axioms`).
-/
import Mathlib

open Set Filter Topology

namespace BarrierAnalyticSkeleton

/-! ## STEP 1 — the t = 0 endpoint extension

The barrier gives a lower bound on a real functional `F` (a proxy for `|H_t|` /
the certified margin) for the OPEN parameter range `t ∈ (0, t0]`.  We must extend the
zero-free conclusion to the CLOSED endpoint `t = 0`.  The honest core is that a
*non-strict* bound passes to the limit by continuity. -/

/--
**Non-strict lower bound extends to the endpoint (nhdsWithin form).**

If `F` is continuous at `0` within a set `s` that has `0` in its closure (i.e. `0` is a
limit point / accumulation point of `s`), and `c ≤ F t` throughout `s`, then `c ≤ F 0`.

Proof: `F` tends to `F 0` along `𝓝[s] 0`; that filter is `NeBot` because `0 ∈ closure s`;
the set `{x | c ≤ x}` is closed, and the bound holds eventually (indeed everywhere on `s`),
so it passes to the limit via `le_of_tendsto`.
-/
theorem lowerbound_extends_to_endpoint_within
    {F : ℝ → ℝ} {s : Set ℝ} {c : ℝ}
    (hmem : (0 : ℝ) ∈ closure s)
    (hcont : ContinuousWithinAt F s 0)
    (hbound : ∀ t ∈ s, c ≤ F t) :
    c ≤ F 0 := by
  haveI hne : (𝓝[s] (0 : ℝ)).NeBot := mem_closure_iff_nhdsWithin_neBot.mp hmem
  have htend : Filter.Tendsto F (𝓝[s] (0 : ℝ)) (𝓝 (F 0)) := hcont
  refine ge_of_tendsto htend ?_
  filter_upwards [self_mem_nhdsWithin] with t ht using hbound t ht

/--
**Non-strict lower bound extends to the endpoint `t = 0` (`Set.Ioc` form).**

The concrete instance used by the candidate: `F` continuous at `0`, and `c ≤ F t` for
every `t ∈ (0, t0]` with `0 < t0`.  Then `c ≤ F 0`.

Honesty note (see module docstring): this passes a NON-STRICT bound to the endpoint.  A
strict bound `c < F t` for `t > 0` does NOT give `c < F 0` in the limit — only `c ≤ F 0`.
So this lemma is the SAFETY NET; for a strict endpoint conclusion the candidate evaluates
directly at `t = 0` (see `strict_lowerbound_on_Icc_of_min`).
-/
theorem lowerbound_extends_to_endpoint
    {F : ℝ → ℝ} {c t0 : ℝ} (ht0 : 0 < t0)
    (hcont : ContinuousAt F 0)
    (hbound : ∀ t ∈ Set.Ioc (0 : ℝ) t0, c ≤ F t) :
    c ≤ F 0 := by
  have hmem : (0 : ℝ) ∈ closure (Set.Ioc (0 : ℝ) t0) := by
    rw [closure_Ioc (ne_of_lt ht0)]
    exact ⟨le_refl 0, le_of_lt ht0⟩
  exact lowerbound_extends_to_endpoint_within hmem hcont.continuousWithinAt hbound

/--
**Strict lower bound on the CLOSED interval via the attained minimum.**

`F` continuous on the compact `[0, t0]` (with `0 ≤ t0`) attains a global minimum at some
`x₀ ∈ [0, t0]` (`IsCompact.exists_isMinOn`).  If, at whatever point the minimum is attained,
the value strictly exceeds `c` (hypothesis `hmargin` — this is the candidate's *direct
evaluation with a strict interior margin*), then `c < F t` for EVERY `t ∈ [0, t0]`,
endpoint `t = 0` included.

This is the honest device the candidate actually relies on to obtain a STRICT bound on the
closed interval: strictness is supplied by a direct evaluation at the minimizer, not by a
limit.
-/
theorem strict_lowerbound_on_Icc_of_min
    {F : ℝ → ℝ} {c t0 : ℝ} (ht0 : 0 ≤ t0)
    (hcont : ContinuousOn F (Set.Icc 0 t0))
    (hmargin : ∀ x₀ ∈ Set.Icc (0 : ℝ) t0, IsMinOn F (Set.Icc 0 t0) x₀ → c < F x₀) :
    ∀ t ∈ Set.Icc (0 : ℝ) t0, c < F t := by
  obtain ⟨x₀, hx₀mem, hx₀min⟩ :=
    (isCompact_Icc.exists_isMinOn (Set.nonempty_Icc.mpr ht0) hcont)
  intro t ht
  have hc : c < F x₀ := hmargin x₀ hx₀mem hx₀min
  exact lt_of_lt_of_le hc (isMinOn_iff.mp hx₀min t ht)

/-! ## STEP 2 — `B_t ≠ 0` on the rectangle, so `g_t = H_t / B_t` counts zeros of `H_t`

`B_t = M₀ · exp(·)`.  The exponential never vanishes, so `B_t ≠ 0` reduces to `M₀ ≠ 0`.
On the set where `B_t ≠ 0`, the zeros of `g_t = H_t / B_t` coincide with the zeros of `H_t`,
so the argument-principle winding count of `g_t` counts exactly the zeros of `H_t`. -/

/--
**The barrier denominator `B = M₀ · exp(·)` is nonvanishing** given `M₀ z ≠ 0`.

`Complex.exp_ne_zero` supplies nonvanishing of the exponential factor; `mul_ne_zero`
combines it with the hypothesis `M0 z ≠ 0`.
-/
theorem Btmul_ne_zero {M0 : ℂ → ℂ} {z : ℂ} (hM0 : M0 z ≠ 0) (w : ℂ) :
    M0 z * Complex.exp w ≠ 0 :=
  mul_ne_zero hM0 (Complex.exp_ne_zero w)

/--
**A uniform positive lower bound on `‖M₀‖` over a set forces `M₀ ≠ 0` there.**

This is the SHAPE by which the candidate's numerical certificate (which bounds `‖M₀‖` below
by a positive constant `δ` on the rectangle) discharges the `M0_ne_zero` hypothesis.
-/
theorem M0_ne_zero_of_lt_norm_on {M0 : ℂ → ℂ} {K : Set ℂ} {δ : ℝ}
    (hδ : 0 < δ) (h : ∀ z ∈ K, δ ≤ ‖M0 z‖) :
    ∀ z ∈ K, M0 z ≠ 0 := by
  intro z hz
  have : 0 < ‖M0 z‖ := lt_of_lt_of_le hδ (h z hz)
  exact norm_pos_iff.mp this

/--
**Convenience: continuity + pointwise positivity of `‖M₀‖` on a compact set yields a
UNIFORM positive lower bound, hence nonvanishing.**

The real content is the upgrade from *pointwise* `0 < ‖M₀ z‖` to a *uniform* constant `δ > 0`
on the compact rectangle (`IsCompact.exists_isMinOn` gives a global minimizer whose value is
positive).  This is exactly what a certificate over a compact rectangle provides.  We return
both the uniform bound and the nonvanishing conclusion.
-/
theorem M0_ne_zero_of_continuous_pos_on_compact
    {M0 : ℂ → ℂ} {K : Set ℂ}
    (hK : IsCompact K) (hne : K.Nonempty)
    (hcont : ContinuousOn (fun z => ‖M0 z‖) K)
    (hpos : ∀ z ∈ K, 0 < ‖M0 z‖) :
    ∃ δ > 0, (∀ z ∈ K, δ ≤ ‖M0 z‖) ∧ (∀ z ∈ K, M0 z ≠ 0) := by
  obtain ⟨z₀, hz₀mem, hz₀min⟩ := hK.exists_isMinOn hne hcont
  refine ⟨‖M0 z₀‖, hpos z₀ hz₀mem, ?_, ?_⟩
  · intro z hz; exact isMinOn_iff.mp hz₀min z hz
  · exact M0_ne_zero_of_lt_norm_on (hpos z₀ hz₀mem) (fun z hz => isMinOn_iff.mp hz₀min z hz)

/--
**The exact logical reduction (pointwise): where `B ≠ 0`, `H = 0 ↔ H/B = 0`.**

`div_eq_zero_iff` says `H z / B z = 0 ↔ H z = 0 ∨ B z = 0`; the disjunct `B z = 0` is ruled
out by the hypothesis, leaving `H z = 0`.  This is precisely why counting zeros of the
auxiliary `g = H / B` counts zeros of `H` and not spurious poles.
-/
theorem zeros_Ht_eq_zeros_g_of_B_ne_zero {H B : ℂ → ℂ} {z : ℂ} (hB : B z ≠ 0) :
    H z = 0 ↔ (H z / B z) = 0 := by
  rw [div_eq_zero_iff]
  constructor
  · intro h; exact Or.inl h
  · rintro (h | h)
    · exact h
    · exact absurd h hB

/--
**Set-level form: on a set `S` where `B ≠ 0`, the zeros of `H/B` are exactly the zeros of `H`.**

This is the statement directly consumed by the argument-principle step on the rectangle `R`
(take `S = R`): the winding-number zero count of `g = H/B` equals the zero count of `H`.
-/
theorem zeros_Ht_eq_zeros_g_on {H B : ℂ → ℂ} {S : Set ℂ}
    (hB : ∀ z ∈ S, B z ≠ 0) :
    ∀ z ∈ S, (H z = 0 ↔ (H z / B z) = 0) :=
  fun z hz => zeros_Ht_eq_zeros_g_of_B_ne_zero (hB z hz)

end BarrierAnalyticSkeleton
