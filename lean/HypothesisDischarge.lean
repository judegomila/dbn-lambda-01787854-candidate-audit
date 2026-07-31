/-
  HypothesisDischarge — progress toward discharging the two candidate-specific
  hypotheses left open by `BarrierAnalyticSkeleton.lean` (see `lean/README.md`):

    (a) joint continuity of the true `H_t` up to `t = 0` (dominated convergence,
        dominator `e^{t0·u² + y0·u}·‖Φ(u)‖`);
    (b) `M0 ≠ 0` on the actual rectangle `R`.

  ## STATUS (honest)

  Part (b) is discharged here IN FULL for the Polymath15 closed form: we transcribe
  `M₀`, `α`, `M_t`, `B_t` verbatim from Polymath (arXiv:1904.12438v2) equations
  (6), (9), (10), (11) — which the candidate's exposition
  (`dan-reworking/latex/gomila-proof-exposition.tex`, §"The effective approximation")
  cites as its definitions — and prove, sorry-free:

    • `M0_ne_zero`          : `M₀ s ≠ 0` whenever `s ≠ 0` and `s ≠ 1`;
    • `M0_ne_zero_of_im_ne_zero`, `Mt_ne_zero`;
    • `Bt_ne_zero`          : `B_t(x+iy) ≠ 0` for every `t, y` and every `x ≠ 0`
                              (the barrier rectangle has `x ≥ 200`, so `x ≠ 0`).

  KEY MATHEMATICAL POINT: nonvanishing of `M₀` is STRUCTURAL, not numerical.
  `M₀ s = (1/8)·(s(s−1)/2)·π^(−s/2)·√(2π)·exp(…)` is a product of factors that are
  each nonzero away from `s ∈ {0, 1}` (`cpow` of a nonzero base and `exp` never
  vanish), and on the rectangle `Im s = −x/2 ≠ 0`.  The numerical certificate's
  lower bound on `‖M₀‖` is NOT needed for hypothesis (b) itself.
  Remaining audit surface for (b): checking that the `M0`/`alpha`/`Mt`/`Bt`
  definitions below agree with the candidate's Arb implementation (they transcribe
  the cited paper equations; that identification is a review step, not a proof step).

  Part (a) is NOT fully discharged.  What IS proved here, sorry-free:

    • `norm_cos_le_exp_abs_im` : `‖cos w‖ ≤ e^{|Im w|}`;
    • `continuousOn_Ht_integral` : JOINT continuity on `[0,t0] × {|Im z| ≤ y0}` of
        `(t, z) ↦ ∫_{u>0} e^{t·u²}·Φ(u)·cos(z·u) du`
      by dominated convergence with dominator `e^{t0·u² + y0·u}·‖Φ(u)‖`,
      for an ABSTRACT `Φ` assumed (i) a.e. strongly measurable on `(0,∞)` and
      (ii) such that the dominator is integrable;
    • `continuousOn_Ht_in_t`, `continuousOn_norm_Ht_in_t` : the specializations
      (fixed `z`, `t ∈ [0, t0]`) consumed by `BarrierAnalyticSkeleton`'s
      `strict_lowerbound_on_Icc_of_min` / `lowerbound_extends_to_endpoint`.

  Remaining for (a), NOT done here: instantiating `Φ` with the actual super-
  exponentially decaying series `Φ(u) = Σ_{n≥1} (2π²n⁴e^{9u} − 3πn²e^{5u})·exp(−πn²e^{4u})`
  and proving the two hypotheses (measurability/continuity of the series and
  integrability of the dominator).  That requires a genuine decay estimate on `Φ`
  and is bounded — but real — work; see `lean/HYPOTHESIS_DISCHARGE_NOTES.md`.

  Everything in this file compiles sorry-free against Lean 4 v4.22.0 + mathlib
  v4.22.0 with axiom footprint `[propext, Classical.choice, Quot.sound]`
  (see the `#print axioms` block at the end).
-/
import Mathlib

open Set Filter Topology MeasureTheory

namespace HypothesisDischarge

/-! ## Part (b): `M₀ ≠ 0`, `M_t ≠ 0`, `B_t ≠ 0` — structural, no numerics

Definitions transcribed from Polymath, arXiv:1904.12438v2:

  (6)  `M₀(s) := (1/8)·(s(s−1)/2)·π^(−s/2)·√(2π)·exp((s/2 − 1/2)·Log(s/2) − s/2)`
  (9)  `α(s)  := 1/(2s) + 1/(s−1) + (1/2)·Log(s/(2π))`
  (10) `M_t(s) := exp((t/4)·α(s)²)·M₀(s)`
  (11) `B_t(x+iy) := M_t((1 + y − ix)/2)`

`Complex.log` in mathlib IS the standard branch (imaginary part in `(−π, π]`),
matching the paper's `Log`. -/

/-- Polymath15 eq. (6): the factor `M₀`. -/
noncomputable def M0 (s : ℂ) : ℂ :=
  (1 / 8) * (s * (s - 1) / 2) * (Real.pi : ℂ) ^ (-s / 2) *
    (Real.sqrt (2 * Real.pi) : ℂ) *
    Complex.exp ((s / 2 - 1 / 2) * Complex.log (s / 2) - s / 2)

/-- Polymath15 eq. (9): the log-derivative `α = M₀'/M₀` (second displayed form). -/
noncomputable def alpha (s : ℂ) : ℂ :=
  1 / (2 * s) + 1 / (s - 1) + (1 / 2) * Complex.log (s / (2 * Real.pi))

/-- Polymath15 eq. (10): the deformation `M_t`. -/
noncomputable def Mt (t : ℝ) (s : ℂ) : ℂ :=
  Complex.exp ((t : ℂ) / 4 * alpha s ^ 2) * M0 s

/-- Polymath15 eq. (11): the barrier denominator `B_t(x+iy) = M_t((1+y−ix)/2)`. -/
noncomputable def Bt (t : ℝ) (x y : ℝ) : ℂ :=
  Mt t ((1 + (y : ℂ) - (x : ℂ) * Complex.I) / 2)

/-- **`M₀ s ≠ 0` for `s ∉ {0, 1}` — structural nonvanishing.**  Every factor of
`M₀` is nonzero: the rational constant, `s(s−1)/2` (using `s ≠ 0, 1`), the complex
power `π^(−s/2)` (`cpow` of a nonzero base never vanishes), `√(2π) > 0`, and the
exponential.  No numerical certificate enters. -/
theorem M0_ne_zero {s : ℂ} (hs0 : s ≠ 0) (hs1 : s ≠ 1) : M0 s ≠ 0 := by
  unfold M0
  refine mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero ?_ ?_) ?_) ?_) ?_
  · norm_num
  · exact div_ne_zero (mul_ne_zero hs0 (sub_ne_zero.mpr hs1)) two_ne_zero
  · exact Complex.cpow_ne_zero_iff.mpr
      (Or.inl (Complex.ofReal_ne_zero.mpr Real.pi_ne_zero))
  · exact Complex.ofReal_ne_zero.mpr
      (ne_of_gt (Real.sqrt_pos.mpr (by positivity)))
  · exact Complex.exp_ne_zero _

/-- A complex number with nonzero imaginary part is neither `0` nor `1`. -/
theorem ne_zero_ne_one_of_im_ne_zero {s : ℂ} (h : s.im ≠ 0) : s ≠ 0 ∧ s ≠ 1 :=
  ⟨fun h0 => h (by simp [h0]), fun h1 => h (by simp [h1])⟩

/-- `M₀ ≠ 0` off the real axis (in particular on the barrier rectangle, where the
argument `(1+y−ix)/2` has imaginary part `−x/2 ≠ 0`). -/
theorem M0_ne_zero_of_im_ne_zero {s : ℂ} (h : s.im ≠ 0) : M0 s ≠ 0 :=
  (ne_zero_ne_one_of_im_ne_zero h).elim fun h0 h1 => M0_ne_zero h0 h1

/-- `M_t s ≠ 0` for `s ∉ {0, 1}`: the deformation factor is an exponential. -/
theorem Mt_ne_zero (t : ℝ) {s : ℂ} (hs0 : s ≠ 0) (hs1 : s ≠ 1) : Mt t s ≠ 0 :=
  mul_ne_zero (Complex.exp_ne_zero _) (M0_ne_zero hs0 hs1)

/-- **Hypothesis (b), discharged for the Polymath15 closed form:**
`B_t(x+iy) ≠ 0` for every `t ∈ ℝ`, `y ∈ ℝ` and every `x ≠ 0`.
The candidate's rectangle `R` lies in `x ≥ 200`, so `x ≠ 0` holds there. -/
theorem Bt_ne_zero (t : ℝ) {x : ℝ} (hx : x ≠ 0) (y : ℝ) : Bt t x y ≠ 0 := by
  unfold Bt
  have him : ((1 + (y : ℂ) - (x : ℂ) * Complex.I) / 2).im = -x / 2 := by
    simp
  have h : ((1 + (y : ℂ) - (x : ℂ) * Complex.I) / 2).im ≠ 0 := by
    rw [him]
    exact div_ne_zero (neg_ne_zero.mpr hx) two_ne_zero
  obtain ⟨h0, h1⟩ := ne_zero_ne_one_of_im_ne_zero h
  exact Mt_ne_zero t h0 h1

/-- Set-level corollary in the exact shape consumed by
`BarrierAnalyticSkeleton.zeros_Ht_eq_zeros_g_on` / `M0_ne_zero_of_lt_norm_on`:
on ANY set of arguments avoiding the real axis, `M₀` is nonvanishing. -/
theorem M0_ne_zero_on {K : Set ℂ} (hK : ∀ s ∈ K, s.im ≠ 0) :
    ∀ s ∈ K, M0 s ≠ 0 :=
  fun s hs => M0_ne_zero_of_im_ne_zero (hK s hs)

/-! ## Part (a): joint continuity of the parametric integral (abstract `Φ`)

`H_t(z) = ∫_{u>0} e^{t·u²}·Φ(u)·cos(z·u) du` (Polymath15 normalization, up to the
constant `1/8` and the even reflection, which do not affect continuity).  We prove
joint continuity on `[0,t0] × {|Im z| ≤ y0}` by dominated convergence
(`MeasureTheory.continuousOn_of_dominated`) with the README's dominator.

`Φ` is ABSTRACT here: the two hypotheses `hΦ` (a.e. strong measurability) and
`hdom` (integrability of the dominator) are exactly what remains to be proved
about the concrete super-exponentially decaying `Φ`. -/

/-- `‖cos w‖ ≤ e^{|Im w|}` — the elementary bound driving the dominator.
(`cos w = (e^{iw} + e^{−iw})/2` and `‖e^{±iw}‖ = e^{∓Im w} ≤ e^{|Im w|}`.) -/
theorem norm_cos_le_exp_abs_im (w : ℂ) : ‖Complex.cos w‖ ≤ Real.exp |w.im| := by
  rw [Complex.cos, norm_div]
  have h2 : ‖(2 : ℂ)‖ = 2 := by norm_num
  rw [h2]
  have hb : ‖Complex.exp (w * Complex.I) + Complex.exp (-w * Complex.I)‖
      ≤ Real.exp |w.im| + Real.exp |w.im| := by
    refine (norm_add_le _ _).trans ?_
    have e1 : ‖Complex.exp (w * Complex.I)‖ ≤ Real.exp |w.im| := by
      rw [Complex.norm_exp, Complex.mul_I_re]
      exact Real.exp_le_exp.mpr (neg_le_abs w.im)
    have e2 : ‖Complex.exp (-w * Complex.I)‖ ≤ Real.exp |w.im| := by
      rw [Complex.norm_exp, Complex.mul_I_re, Complex.neg_im, neg_neg]
      exact Real.exp_le_exp.mpr (le_abs_self w.im)
    exact add_le_add e1 e2
  linarith

/-- **Joint continuity of the `H_t`-shaped parametric integral on
`[0, t0] × {z : |Im z| ≤ y0}`, down to and including `t = 0`.**

Dominated convergence with dominator `u ↦ e^{t0·u² + y0·u}·‖Φ(u)‖` (the dominator
named in `lean/README.md`, with `e^u` generalized to `e^{y0·u}`; take `y0 = 1` to
recover it).  The only facts about `Φ` used are `hΦ` and `hdom`. -/
theorem continuousOn_Ht_integral
    (Φ : ℝ → ℂ) (t0 y0 : ℝ)
    (hΦ : AEStronglyMeasurable Φ (volume.restrict (Set.Ioi (0 : ℝ))))
    (hdom : Integrable (fun u : ℝ => Real.exp (t0 * u ^ 2 + y0 * u) * ‖Φ u‖)
      (volume.restrict (Set.Ioi (0 : ℝ)))) :
    ContinuousOn
      (fun p : ℝ × ℂ =>
        ∫ u in Set.Ioi (0 : ℝ),
          Complex.exp ((p.1 : ℂ) * (u : ℂ) ^ 2) * Φ u * Complex.cos (p.2 * (u : ℂ)))
      (Set.Icc 0 t0 ×ˢ {z : ℂ | |z.im| ≤ y0}) := by
  apply MeasureTheory.continuousOn_of_dominated
      (bound := fun u : ℝ => Real.exp (t0 * u ^ 2 + y0 * u) * ‖Φ u‖)
  · -- a.e. strong measurability of the integrand at each parameter value
    rintro ⟨t, z⟩ ⟨ht, hz⟩
    have h1 : Continuous fun u : ℝ => Complex.exp ((t : ℂ) * (u : ℂ) ^ 2) := by
      fun_prop
    have h2 : Continuous fun u : ℝ => Complex.cos (z * (u : ℂ)) := by fun_prop
    exact (h1.aestronglyMeasurable.mul hΦ).mul h2.aestronglyMeasurable
  · -- the uniform dominating bound
    rintro ⟨t, z⟩ ⟨ht, hz⟩
    simp only [Set.mem_Icc] at ht
    simp only [Set.mem_setOf_eq] at hz
    filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
    have hu0 : (0 : ℝ) ≤ u := le_of_lt hu
    have hexp : ‖Complex.exp ((t : ℂ) * (u : ℂ) ^ 2)‖ = Real.exp (t * u ^ 2) := by
      rw [show ((t : ℂ) * (u : ℂ) ^ 2) = ((t * u ^ 2 : ℝ) : ℂ) by push_cast; ring,
        Complex.norm_exp, Complex.ofReal_re]
    have hcos : ‖Complex.cos (z * (u : ℂ))‖ ≤ Real.exp (y0 * u) := by
      refine (norm_cos_le_exp_abs_im _).trans (Real.exp_le_exp.mpr ?_)
      have him : (z * (u : ℂ)).im = z.im * u := by simp [Complex.mul_im]
      rw [him, abs_mul, abs_of_nonneg hu0]
      exact mul_le_mul_of_nonneg_right hz hu0
    calc ‖Complex.exp ((t : ℂ) * (u : ℂ) ^ 2) * Φ u * Complex.cos (z * (u : ℂ))‖
        = Real.exp (t * u ^ 2) * ‖Φ u‖ * ‖Complex.cos (z * (u : ℂ))‖ := by
          rw [norm_mul, norm_mul, hexp]
      _ ≤ Real.exp (t0 * u ^ 2) * ‖Φ u‖ * Real.exp (y0 * u) := by
          have h1 : Real.exp (t * u ^ 2) ≤ Real.exp (t0 * u ^ 2) :=
            Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_right ht.2 (sq_nonneg u))
          exact mul_le_mul (mul_le_mul_of_nonneg_right h1 (norm_nonneg _)) hcos
            (norm_nonneg _) (by positivity)
      _ = Real.exp (t0 * u ^ 2 + y0 * u) * ‖Φ u‖ := by
          rw [Real.exp_add]; ring
  · exact hdom
  · -- continuity in the parameter for each fixed u
    exact Eventually.of_forall fun u =>
      Continuous.continuousOn (by fun_prop)

/-- Specialization at a fixed `z` with `|Im z| ≤ y0`: `t ↦ H_t(z)` is continuous on
the CLOSED interval `[0, t0]` — the continuity hypothesis shape consumed by
`BarrierAnalyticSkeleton.strict_lowerbound_on_Icc_of_min` and
`lowerbound_extends_to_endpoint`. -/
theorem continuousOn_Ht_in_t
    (Φ : ℝ → ℂ) (t0 y0 : ℝ) (z : ℂ) (hz : |z.im| ≤ y0)
    (hΦ : AEStronglyMeasurable Φ (volume.restrict (Set.Ioi (0 : ℝ))))
    (hdom : Integrable (fun u : ℝ => Real.exp (t0 * u ^ 2 + y0 * u) * ‖Φ u‖)
      (volume.restrict (Set.Ioi (0 : ℝ)))) :
    ContinuousOn
      (fun t : ℝ =>
        ∫ u in Set.Ioi (0 : ℝ),
          Complex.exp ((t : ℂ) * (u : ℂ) ^ 2) * Φ u * Complex.cos (z * (u : ℂ)))
      (Set.Icc 0 t0) := by
  have hjoint := continuousOn_Ht_integral Φ t0 y0 hΦ hdom
  have hemb : ContinuousOn (fun t : ℝ => ((t, z) : ℝ × ℂ)) (Set.Icc 0 t0) :=
    (continuous_id.prodMk continuous_const).continuousOn
  have hcomp := hjoint.comp hemb fun t ht => Set.mk_mem_prod ht hz
  simpa [Function.comp] using hcomp

/-- Norm version: `t ↦ ‖H_t(z)‖` is continuous on `[0, t0]` (the real-valued
barrier functional `F` of the skeleton is built from such norms). -/
theorem continuousOn_norm_Ht_in_t
    (Φ : ℝ → ℂ) (t0 y0 : ℝ) (z : ℂ) (hz : |z.im| ≤ y0)
    (hΦ : AEStronglyMeasurable Φ (volume.restrict (Set.Ioi (0 : ℝ))))
    (hdom : Integrable (fun u : ℝ => Real.exp (t0 * u ^ 2 + y0 * u) * ‖Φ u‖)
      (volume.restrict (Set.Ioi (0 : ℝ)))) :
    ContinuousOn
      (fun t : ℝ =>
        ‖∫ u in Set.Ioi (0 : ℝ),
          Complex.exp ((t : ℂ) * (u : ℂ) ^ 2) * Φ u * Complex.cos (z * (u : ℂ))‖)
      (Set.Icc 0 t0) :=
  (continuousOn_Ht_in_t Φ t0 y0 z hz hΦ hdom).norm

/-! ## Axiom audit -/

#print axioms M0_ne_zero
#print axioms Bt_ne_zero
#print axioms M0_ne_zero_on
#print axioms norm_cos_le_exp_abs_im
#print axioms continuousOn_Ht_integral
#print axioms continuousOn_Ht_in_t
#print axioms continuousOn_norm_Ht_in_t

end HypothesisDischarge
