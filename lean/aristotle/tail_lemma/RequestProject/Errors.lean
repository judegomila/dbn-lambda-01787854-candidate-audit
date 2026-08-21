import RequestProject.Basic

/-!
# Lemma 6 : error monotonicity

With `L = log(x/(4π))`, `A = t²/16`, `c = 0.626 = 313/500`, `b = 6.66 = 333/50`, the quantity
`(A L² + c)/(x - b)` has negative derivative on the window domain `L > 2`, and so does
`(3√(L² + π²/4) + 10.50)/(x - 12)`.  Hence both are maximal at the window's left edge and
decrease with `N`.
-/

namespace Job2

open Real

/-- `L = log (x/(4π))`. -/
noncomputable def Lx (x : ℝ) : ℝ := Real.log (x / (4 * Real.pi))

/-- The `Δ`-quantity of Hypothesis H2, as a function of `x = X_N(t)`. -/
noncomputable def DeltaErr (t x : ℝ) : ℝ := (t^2/16 * Lx x ^ 2 + 313/500) / (x - 333/50)

/-- The `e_{C,0}`-quantity `Q(L)/(x-12)` of Hypothesis H2. -/
noncomputable def Qerr (x : ℝ) : ℝ :=
  (3 * Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4) + 21/2) / (x - 12)

/-- The window domain `{x : L > 2} = (4π e², ∞)`. -/
noncomputable def Dom : Set ℝ := Set.Ioi (4 * Real.pi * Real.exp 2)

lemma exp_two_ge_three : (3:ℝ) ≤ Real.exp 2 := by
  have := Real.add_one_le_exp (2:ℝ)
  linarith

lemma dom_gt_36 {x : ℝ} (hx : x ∈ Dom) : 36 < x := by
  have hpi : (3:ℝ) < Real.pi := Real.pi_gt_three
  have he : (3:ℝ) ≤ Real.exp 2 := exp_two_ge_three
  have hmem : 4 * Real.pi * Real.exp 2 < x := hx
  nlinarith

lemma dom_L_gt_two {x : ℝ} (hx : x ∈ Dom) : 2 < Lx x := by
  have hpi : (0:ℝ) < 4 * Real.pi := by positivity
  have hmem : 4 * Real.pi * Real.exp 2 < x := hx
  have hx0 : 0 < x := lt_trans (by positivity) hmem
  have hdiv : Real.exp 2 < x / (4 * Real.pi) := by
    rw [lt_div_iff₀ hpi]
    linarith [hmem]
  rw [Lx, Real.lt_log_iff_exp_lt (div_pos hx0 hpi)]
  exact hdiv

/-- The derivative of `L`. -/
lemma hasDerivAt_Lx {x : ℝ} (hx : 0 < x) : HasDerivAt Lx (1/x) x := by
  have hpi : (0:ℝ) < 4 * Real.pi := by positivity
  have h1 : HasDerivAt (fun z : ℝ => z / (4 * Real.pi)) (1/(4 * Real.pi)) x := by
    simpa using (hasDerivAt_id x).div_const (4 * Real.pi)
  have h2 := h1.log (ne_of_gt (div_pos hx hpi))
  have heq : (1/(4 * Real.pi)) / (x / (4 * Real.pi)) = 1/x := by
    field_simp
  rw [heq] at h2
  exact h2

lemma hasDerivAt_DeltaErr {t x : ℝ} (hx : 0 < x) (hxb : x - 333/50 ≠ 0) :
    HasDerivAt (DeltaErr t)
      ((t^2/16 * (2 * Lx x * (1/x)) * (x - 333/50) - (t^2/16 * Lx x ^ 2 + 313/500))
        / (x - 333/50)^2) x := by
  have hL := hasDerivAt_Lx hx
  have hsq : HasDerivAt (fun z : ℝ => Lx z ^ 2) (2 * Lx x * (1/x)) x := by
    simpa [mul_comm, mul_assoc, mul_left_comm] using hL.pow 2
  have hg : HasDerivAt (fun z : ℝ => t^2/16 * Lx z ^ 2 + 313/500)
      (t^2/16 * (2 * Lx x * (1/x))) x := (hsq.const_mul (t^2/16)).add_const _
  have hh : HasDerivAt (fun z : ℝ => z - 333/50) 1 x := (hasDerivAt_id x).sub_const _
  have := hg.div hh (by simpa using hxb)
  simpa [DeltaErr, mul_one] using this

lemma deriv_DeltaErr_neg {t x : ℝ} (hx : x ∈ Dom) : deriv (DeltaErr t) x < 0 := by
  have hx36 : 36 < x := dom_gt_36 hx
  have hx0 : (0:ℝ) < x := by linarith
  have hL : 2 < Lx x := dom_L_gt_two hx
  have hxb : x - 333/50 ≠ 0 := by intro h; linarith [h]
  rw [(hasDerivAt_DeltaErr hx0 hxb).deriv]
  have hA : (0:ℝ) ≤ t^2/16 := by positivity
  have hb : (0:ℝ) < (x - 333/50)^2 := pow_pos (by linarith) 2
  apply div_neg_of_neg_of_pos ?_ hb
  have hfrac : (1/x) * (x - 333/50) ≤ 1 := by
    rw [one_div, inv_mul_eq_div, div_le_one hx0]
    linarith
  have hfrac0 : 0 ≤ (1/x) * (x - 333/50) :=
    mul_nonneg (by positivity) (by linarith)
  have hAL : 0 ≤ t^2/16 * Lx x := by nlinarith
  nlinarith [mul_nonneg hAL (by linarith : (0:ℝ) ≤ Lx x - 2)]

/-- **Lemma 6, first part.** `Δ = (A L² + c)/(x - b)` decreases in `x` on the window domain. -/
theorem lemma6_delta_antitone (t : ℝ) : StrictAntiOn (DeltaErr t) Dom := by
  refine strictAntiOn_of_deriv_neg (convex_Ioi _) (fun x hx => ?_) (fun x hx => ?_)
  · have hx0 : (0:ℝ) < x := by linarith [dom_gt_36 hx]
    have hxb : x - 333/50 ≠ 0 := by
      intro h; linarith [dom_gt_36 hx, h]
    exact ((hasDerivAt_DeltaErr hx0 hxb).continuousAt).continuousWithinAt
  · rw [interior_Ioi] at hx
    exact deriv_DeltaErr_neg hx

lemma sqrt_pos_of_dom {x : ℝ} (hx : x ∈ Dom) : 0 < Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4) := by
  apply Real.sqrt_pos.2
  have := dom_L_gt_two hx
  nlinarith [Real.pi_gt_three]

lemma L_le_sqrt {x : ℝ} (hx : x ∈ Dom) : Lx x ≤ Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4) := by
  have hL : 2 < Lx x := dom_L_gt_two hx
  have h := Real.sqrt_le_sqrt
    (show Lx x ^ 2 ≤ Lx x ^ 2 + Real.pi ^ 2 / 4 by nlinarith [Real.pi_gt_three])
  rwa [Real.sqrt_sq (by linarith : (0:ℝ) ≤ Lx x)] at h

lemma hasDerivAt_Qerr {x : ℝ} (hx : x ∈ Dom) :
    HasDerivAt Qerr
      ((3 * ((2 * Lx x * (1/x)) / (2 * Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4))) * (x - 12)
        - (3 * Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4) + 21/2)) / (x - 12)^2) x := by
  have hx36 : 36 < x := dom_gt_36 hx
  have hx0 : (0:ℝ) < x := by linarith
  have hL := hasDerivAt_Lx hx0
  have hu : HasDerivAt (fun z : ℝ => Lx z ^ 2 + Real.pi ^ 2 / 4) (2 * Lx x * (1/x)) x := by
    have hsq : HasDerivAt (fun z : ℝ => Lx z ^ 2) (2 * Lx x * (1/x)) x := by
      simpa [mul_comm, mul_assoc, mul_left_comm] using hL.pow 2
    exact hsq.add_const _
  have hune : Lx x ^ 2 + Real.pi ^ 2 / 4 ≠ 0 := by
    have := dom_L_gt_two hx
    nlinarith [Real.pi_gt_three]
  have hsqrt := hu.sqrt hune
  have hnum : HasDerivAt (fun z : ℝ => 3 * Real.sqrt (Lx z ^ 2 + Real.pi ^ 2 / 4) + 21/2)
      (3 * ((2 * Lx x * (1/x)) / (2 * Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4)))) x :=
    (hsqrt.const_mul 3).add_const _
  have hden : HasDerivAt (fun z : ℝ => z - 12) 1 x := (hasDerivAt_id x).sub_const _
  have hne : (fun z : ℝ => z - 12) x ≠ 0 := by simp only; intro h; linarith [h]
  have := hnum.div hden hne
  simpa [Qerr, mul_one] using this

lemma deriv_Qerr_neg {x : ℝ} (hx : x ∈ Dom) : deriv Qerr x < 0 := by
  have hx36 : 36 < x := dom_gt_36 hx
  have hx0 : (0:ℝ) < x := by linarith
  have hL : 2 < Lx x := dom_L_gt_two hx
  set s := Real.sqrt (Lx x ^ 2 + Real.pi ^ 2 / 4) with hs
  have hs0 : 0 < s := sqrt_pos_of_dom hx
  have hLs : Lx x ≤ s := L_le_sqrt hx
  rw [(hasDerivAt_Qerr hx).deriv]
  have hden : (0:ℝ) < (x - 12)^2 := pow_pos (by linarith) 2
  apply div_neg_of_neg_of_pos ?_ hden
  have hrw : 3 * ((2 * Lx x * (1/x)) / (2 * s)) * (x - 12)
      = 3 * (Lx x / s) * ((x - 12)/x) := by
    field_simp
  rw [hrw]
  have h1 : Lx x / s ≤ 1 := (div_le_one hs0).2 hLs
  have h2 : (x - 12)/x ≤ 1 := (div_le_one hx0).2 (by linarith)
  have h3 : 0 ≤ Lx x / s := div_nonneg (by linarith) hs0.le
  have h4 : 0 ≤ (x - 12)/x := div_nonneg (by linarith) hx0.le
  nlinarith

/-- **Lemma 6, second part.** `Q(L)/(x-12) = (3√(L²+π²/4) + 10.50)/(x-12)` decreases in `x`
on the window domain. -/
theorem lemma6_Q_antitone : StrictAntiOn Qerr Dom := by
  refine strictAntiOn_of_deriv_neg (convex_Ioi _) (fun x hx => ?_) (fun x hx => ?_)
  · exact ((hasDerivAt_Qerr hx).continuousAt).continuousWithinAt
  · rw [interior_Ioi] at hx
    exact deriv_Qerr_neg hx

end Job2
