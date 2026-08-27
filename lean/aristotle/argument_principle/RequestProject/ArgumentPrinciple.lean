import Mathlib

/-!
# The argument principle on rectangles, factored form

This file develops the argument principle for axis-parallel rectangles in `ℂ`, in the
factored form

  `H ζ = (∏ j, (ζ - a j) ^ m j) * U ζ`

with `U` entire and nonvanishing on the closed rectangle and the `a j` in the open
interior of the rectangle.  The winding number `windingRect H z w` then equals `∑ j, m j`.
-/

open Set Complex intervalIntegral MeasureTheory
open scoped Real BigOperators Interval

namespace ArgumentPrinciple

/-! ## Definitions -/

/-- The closed axis-parallel rectangle with corners `z` and `w` (unordered intervals). -/
def Rect (z w : ℂ) : Set ℂ := [[z.re, w.re]] ×ℂ [[z.im, w.im]]

/-- The integral of `f` over the (positively oriented) boundary of the rectangle
with corners `z` and `w`. -/
noncomputable def rectIntegral (f : ℂ → ℂ) (z w : ℂ) : ℂ :=
    (∫ x : ℝ in z.re..w.re, f (x + z.im * I)) - (∫ x : ℝ in z.re..w.re, f (x + w.im * I))
      + I * (∫ y : ℝ in z.im..w.im, f (w.re + y * I))
      - I * (∫ y : ℝ in z.im..w.im, f (z.re + y * I))

/-- The winding number of `f` around the boundary of the rectangle with corners `z` and `w`. -/
noncomputable def windingRect (f : ℂ → ℂ) (z w : ℂ) : ℂ :=
    (2 * (π : ℂ) * I)⁻¹ * rectIntegral (logDeriv f) z w

/-- The boundary of the rectangle with corners `z` and `w`. -/
def RectFrontier (z w : ℂ) : Set ℂ :=
    {c ∈ Rect z w | c.re = z.re ∨ c.re = w.re ∨ c.im = z.im ∨ c.im = w.im}

/-! ## Basic facts about the frontier -/

lemma mem_Rect {z w c : ℂ} : c ∈ Rect z w ↔ c.re ∈ [[z.re, w.re]] ∧ c.im ∈ [[z.im, w.im]] :=
  Iff.rfl

lemma RectFrontier_subset_Rect (z w : ℂ) : RectFrontier z w ⊆ Rect z w := fun _ hc => hc.1

lemma mem_RectFrontier_bot {z w : ℂ} {x : ℝ} (hx : x ∈ [[z.re, w.re]]) :
    ((x : ℂ) + z.im * I) ∈ RectFrontier z w := by
  refine ⟨⟨?_, ?_⟩, ?_⟩ <;> simp [hx]

lemma mem_RectFrontier_top {z w : ℂ} {x : ℝ} (hx : x ∈ [[z.re, w.re]]) :
    ((x : ℂ) + w.im * I) ∈ RectFrontier z w := by
  refine ⟨⟨?_, ?_⟩, ?_⟩ <;> simp [hx]

lemma mem_RectFrontier_right {z w : ℂ} {y : ℝ} (hy : y ∈ [[z.im, w.im]]) :
    ((w.re : ℂ) + y * I) ∈ RectFrontier z w := by
  refine ⟨⟨?_, ?_⟩, ?_⟩ <;> simp [hy]

lemma mem_RectFrontier_left {z w : ℂ} {y : ℝ} (hy : y ∈ [[z.im, w.im]]) :
    ((z.re : ℂ) + y * I) ∈ RectFrontier z w := by
  refine ⟨⟨?_, ?_⟩, ?_⟩ <;> simp [hy]

/-! ## Integrability along the edges -/

lemma continuousOn_edge_bot {f : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (RectFrontier z w)) :
    ContinuousOn (fun x : ℝ => f ((x : ℂ) + z.im * I)) [[z.re, w.re]] := by
  refine hf.comp (by fun_prop) fun x hx => mem_RectFrontier_bot hx

lemma continuousOn_edge_top {f : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (RectFrontier z w)) :
    ContinuousOn (fun x : ℝ => f ((x : ℂ) + w.im * I)) [[z.re, w.re]] := by
  refine hf.comp (by fun_prop) fun x hx => mem_RectFrontier_top hx

lemma continuousOn_edge_right {f : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (RectFrontier z w)) :
    ContinuousOn (fun y : ℝ => f ((w.re : ℂ) + y * I)) [[z.im, w.im]] := by
  refine hf.comp (by fun_prop) fun y hy => mem_RectFrontier_right hy

lemma continuousOn_edge_left {f : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (RectFrontier z w)) :
    ContinuousOn (fun y : ℝ => f ((z.re : ℂ) + y * I)) [[z.im, w.im]] := by
  refine hf.comp (by fun_prop) fun y hy => mem_RectFrontier_left hy

/-! ## Algebraic properties of `rectIntegral` -/

lemma rectIntegral_congr {f g : ℂ → ℂ} {z w : ℂ} (h : ∀ c ∈ RectFrontier z w, f c = g c) :
    rectIntegral f z w = rectIntegral g z w := by
  simp only [rectIntegral]
  rw [integral_congr (fun x hx => h _ (mem_RectFrontier_bot hx)),
    integral_congr (fun x hx => h _ (mem_RectFrontier_top hx)),
    integral_congr (fun y hy => h _ (mem_RectFrontier_right hy)),
    integral_congr (fun y hy => h _ (mem_RectFrontier_left hy))]

lemma rectIntegral_add {f g : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (RectFrontier z w))
    (hg : ContinuousOn g (RectFrontier z w)) :
    rectIntegral (fun c => f c + g c) z w = rectIntegral f z w + rectIntegral g z w := by
  simp only [rectIntegral]
  rw [integral_add (continuousOn_edge_bot hf).intervalIntegrable
      (continuousOn_edge_bot hg).intervalIntegrable,
    integral_add (continuousOn_edge_top hf).intervalIntegrable
      (continuousOn_edge_top hg).intervalIntegrable,
    integral_add (continuousOn_edge_right hf).intervalIntegrable
      (continuousOn_edge_right hg).intervalIntegrable,
    integral_add (continuousOn_edge_left hf).intervalIntegrable
      (continuousOn_edge_left hg).intervalIntegrable]
  ring

lemma rectIntegral_sub {f g : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (RectFrontier z w))
    (hg : ContinuousOn g (RectFrontier z w)) :
    rectIntegral (fun c => f c - g c) z w = rectIntegral f z w - rectIntegral g z w := by
  simp only [rectIntegral]
  rw [integral_sub (continuousOn_edge_bot hf).intervalIntegrable
      (continuousOn_edge_bot hg).intervalIntegrable,
    integral_sub (continuousOn_edge_top hf).intervalIntegrable
      (continuousOn_edge_top hg).intervalIntegrable,
    integral_sub (continuousOn_edge_right hf).intervalIntegrable
      (continuousOn_edge_right hg).intervalIntegrable,
    integral_sub (continuousOn_edge_left hf).intervalIntegrable
      (continuousOn_edge_left hg).intervalIntegrable]
  ring

lemma rectIntegral_const_mul (f : ℂ → ℂ) (z w : ℂ) (r : ℂ) :
    rectIntegral (fun c => r * f c) z w = r * rectIntegral f z w := by
  simp only [rectIntegral]
  rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
    intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
  ring

lemma rectIntegral_sum {ι : Type*} {s : Finset ι} {F : ι → ℂ → ℂ} {z w : ℂ}
    (hF : ∀ i ∈ s, ContinuousOn (F i) (RectFrontier z w)) :
    rectIntegral (fun c => ∑ i ∈ s, F i c) z w = ∑ i ∈ s, rectIntegral (F i) z w := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [rectIntegral]
  | insert i s hi ih =>
      have hFi : ContinuousOn (F i) (RectFrontier z w) := hF i (Finset.mem_insert_self _ _)
      have hFs : ∀ j ∈ s, ContinuousOn (F j) (RectFrontier z w) := fun j hj =>
        hF j (Finset.mem_insert_of_mem hj)
      have hsum : ContinuousOn (fun c => ∑ j ∈ s, F j c) (RectFrontier z w) :=
        continuousOn_finset_sum _ hFs
      simp only [Finset.sum_insert hi]
      rw [rectIntegral_add hFi hsum, ih hFs]

/-! ## Cauchy–Goursat on rectangles -/

lemma rectIntegral_eq_zero_of_differentiableOn {f : ℂ → ℂ} {z w : ℂ}
    (hf : DifferentiableOn ℂ f (Rect z w)) : rectIntegral f z w = 0 := by
  have := Complex.integral_boundary_rect_eq_zero_of_differentiableOn f z w hf
  simpa [rectIntegral, smul_eq_mul, sub_eq_zero] using this

/-! ## The integral of `(ζ - a)⁻¹` over a rectangle boundary -/

lemma arctan_add_arctan_inv_of_pos {t : ℝ} (ht : 0 < t) :
    Real.arctan t + Real.arctan t⁻¹ = π / 2 := by
  rw [Real.arctan_inv_of_pos ht]; ring

lemma arctan_add_arctan_inv_of_neg {t : ℝ} (ht : t < 0) :
    Real.arctan t + Real.arctan t⁻¹ = -(π / 2) := by
  rw [Real.arctan_inv_of_neg ht]; ring

lemma ofReal_add_const_mul_I_ne_zero {α : ℝ} (x : ℝ) (hα : α ≠ 0) :
    ((x : ℂ) + (α : ℂ) * I) ≠ 0 := by
  intro h
  have := congrArg Complex.im h
  simp at this
  exact hα this

/-- The antiderivative used for the edge integrals of `ζ⁻¹`. -/
lemma hasDerivAt_edge_antiderivative (α x : ℝ) (hα : α ≠ 0) :
    HasDerivAt
      (fun t : ℝ => ((1 / 2 * Real.log (t ^ 2 + α ^ 2) : ℝ) : ℂ)
        - I * ((Real.arctan (t / α) : ℝ) : ℂ))
      (((x : ℂ) + (α : ℂ) * I)⁻¹) x := by
  have hpos : (0 : ℝ) < x ^ 2 + α ^ 2 := by positivity
  have key : ((x / (x ^ 2 + α ^ 2) : ℝ) : ℂ) - I * ((α / (x ^ 2 + α ^ 2) : ℝ) : ℂ)
      = ((x : ℂ) + (α : ℂ) * I)⁻¹ := by
    have hne : ((x : ℂ) ^ 2 + (α : ℂ) ^ 2) ≠ 0 := by
      exact_mod_cast (by exact_mod_cast ne_of_gt hpos : ((x ^ 2 + α ^ 2 : ℝ) : ℂ) ≠ 0)
    refine eq_inv_of_mul_eq_one_left ?_
    push_cast
    field_simp
    ring_nf
    rw [Complex.I_sq]
    ring
  have h1 : HasDerivAt (fun t : ℝ => 1 / 2 * Real.log (t ^ 2 + α ^ 2)) (x / (x ^ 2 + α ^ 2)) x := by
    have hq : HasDerivAt (fun t : ℝ => t ^ 2 + α ^ 2) (2 * x) x := by
      simpa using (hasDerivAt_pow 2 x).add_const (α ^ 2)
    have h := ((Real.hasDerivAt_log (ne_of_gt hpos)).comp x hq).const_mul (1 / 2 : ℝ)
    convert h using 1
    field_simp
  have h2 : HasDerivAt (fun t : ℝ => Real.arctan (t / α)) ((1 / α) / (1 + (x / α) ^ 2)) x := by
    have hq : HasDerivAt (fun t : ℝ => t / α) (1 / α) x := by
      simpa [div_eq_mul_inv] using (hasDerivAt_id x).mul_const α⁻¹
    have h := (Real.hasDerivAt_arctan (x / α)).comp x hq
    convert h using 1
    ring
  have hsimp : (1 / α) / (1 + (x / α) ^ 2) = α / (x ^ 2 + α ^ 2) := by field_simp; ring
  have h3 := h1.ofReal_comp.sub (h2.ofReal_comp.const_mul I)
  rw [hsimp] at h3
  convert h3 using 1
  exact key.symm

/-- The antiderivative computation for the horizontal edges. -/
lemma integral_inv_ofReal_add_const_mul_I (α u v : ℝ) (hα : α ≠ 0) :
    (∫ x : ℝ in u..v, ((x : ℂ) + (α : ℂ) * I)⁻¹)
      = ((1 / 2 * (Real.log (v ^ 2 + α ^ 2) - Real.log (u ^ 2 + α ^ 2)) : ℝ) : ℂ)
        - I * ((Real.arctan (v / α) - Real.arctan (u / α) : ℝ) : ℂ) := by
  have hcont : ContinuousOn (fun x : ℝ => ((x : ℂ) + (α : ℂ) * I)⁻¹) [[u, v]] :=
    ContinuousOn.inv₀ (by fun_prop) fun x _ => ofReal_add_const_mul_I_ne_zero x hα
  rw [integral_eq_sub_of_hasDerivAt (fun x _ => hasDerivAt_edge_antiderivative α x hα)
    hcont.intervalIntegrable]
  push_cast
  ring

/-- The antiderivative computation for the vertical edges. -/
lemma integral_inv_const_add_ofReal_mul_I (β u v : ℝ) (hβ : β ≠ 0) :
    (∫ y : ℝ in u..v, ((β : ℂ) + (y : ℝ) * I)⁻¹)
      = ((Real.arctan (v / β) - Real.arctan (u / β) : ℝ) : ℂ)
        - I * ((1 / 2 * (Real.log (β ^ 2 + v ^ 2) - Real.log (β ^ 2 + u ^ 2)) : ℝ) : ℂ) := by
  have hrw : ∀ y : ℝ, ((β : ℂ) + (y : ℝ) * I)⁻¹ = -I * ((y : ℂ) + ((-β : ℝ) : ℂ) * I)⁻¹ := by
    intro y
    have h : ((β : ℂ) + (y : ℝ) * I) = I * ((y : ℂ) + ((-β : ℝ) : ℂ) * I) := by
      push_cast
      rw [mul_add, mul_comm I (y : ℂ)]
      ring_nf
      rw [Complex.I_sq]
      ring
    rw [h, mul_inv]
    congr 1
    rw [Complex.inv_I]
  simp_rw [hrw]
  rw [intervalIntegral.integral_const_mul,
    integral_inv_ofReal_add_const_mul_I _ _ _ (neg_ne_zero.mpr hβ)]
  have h1 : ∀ t : ℝ, t / (-β) = -(t / β) := fun t => by ring
  simp only [h1, Real.arctan_neg]
  push_cast
  ring_nf
  rw [Complex.I_sq]
  ring_nf

/-- The four-arctan identity underlying the residue computation. -/
lemma arctan_rect_sum {A B C D : ℝ} (hA : A < 0) (hB : 0 < B) (hC : C < 0) (hD : 0 < D) :
    -(Real.arctan (B / C) - Real.arctan (A / C)) + (Real.arctan (B / D) - Real.arctan (A / D))
      + (Real.arctan (D / B) - Real.arctan (C / B))
      - (Real.arctan (D / A) - Real.arctan (C / A)) = 2 * π := by
  have hBC : B / C < 0 := div_neg_of_pos_of_neg hB hC
  have hAC : 0 < A / C := div_pos_of_neg_of_neg hA hC
  have hBD : 0 < B / D := div_pos hB hD
  have hAD : A / D < 0 := div_neg_of_neg_of_pos hA hD
  have e1 : Real.arctan (C / B) = -(π / 2) - Real.arctan (B / C) := by
    rw [show C / B = (B / C)⁻¹ by rw [inv_div], Real.arctan_inv_of_neg hBC]
  have e2 : Real.arctan (C / A) = π / 2 - Real.arctan (A / C) := by
    rw [show C / A = (A / C)⁻¹ by rw [inv_div], Real.arctan_inv_of_pos hAC]
  have e3 : Real.arctan (D / B) = π / 2 - Real.arctan (B / D) := by
    rw [show D / B = (B / D)⁻¹ by rw [inv_div], Real.arctan_inv_of_pos hBD]
  have e4 : Real.arctan (D / A) = -(π / 2) - Real.arctan (A / D) := by
    rw [show D / A = (A / D)⁻¹ by rw [inv_div], Real.arctan_inv_of_neg hAD]
  rw [e1, e2, e3, e4]
  ring

/-- The rectangle boundary integral of `(ζ - a)⁻¹` for `a` in the open interior. -/
theorem rectIntegral_inv_sub {z w a : ℂ} (h1 : z.re < a.re) (h2 : a.re < w.re)
    (h3 : z.im < a.im) (h4 : a.im < w.im) :
    rectIntegral (fun c => (c - a)⁻¹) z w = 2 * (π : ℂ) * I := by
  set A := z.re - a.re with hAdef
  set B := w.re - a.re with hBdef
  set C := z.im - a.im with hCdef
  set D := w.im - a.im with hDdef
  have hA : A < 0 := by simp only [hAdef]; linarith
  have hB : 0 < B := by simp only [hBdef]; linarith
  have hC : C < 0 := by simp only [hCdef]; linarith
  have hD : 0 < D := by simp only [hDdef]; linarith
  have hbot : (∫ x : ℝ in z.re..w.re, ((x : ℂ) + z.im * I - a)⁻¹)
      = ∫ t : ℝ in A..B, ((t : ℂ) + (C : ℂ) * I)⁻¹ := by
    rw [← intervalIntegral.integral_comp_sub_right (fun t : ℝ => ((t : ℂ) + (C : ℂ) * I)⁻¹) a.re]
    refine intervalIntegral.integral_congr fun x _ => ?_
    congr 1
    apply Complex.ext <;> simp [hCdef]
  have htop : (∫ x : ℝ in z.re..w.re, ((x : ℂ) + w.im * I - a)⁻¹)
      = ∫ t : ℝ in A..B, ((t : ℂ) + (D : ℂ) * I)⁻¹ := by
    rw [← intervalIntegral.integral_comp_sub_right (fun t : ℝ => ((t : ℂ) + (D : ℂ) * I)⁻¹) a.re]
    refine intervalIntegral.integral_congr fun x _ => ?_
    congr 1
    apply Complex.ext <;> simp [hDdef]
  have hright : (∫ y : ℝ in z.im..w.im, ((w.re : ℂ) + y * I - a)⁻¹)
      = ∫ s : ℝ in C..D, ((B : ℂ) + (s : ℝ) * I)⁻¹ := by
    rw [← intervalIntegral.integral_comp_sub_right (fun s : ℝ => ((B : ℂ) + (s : ℝ) * I)⁻¹) a.im]
    refine intervalIntegral.integral_congr fun y _ => ?_
    congr 1
    apply Complex.ext <;> simp [hBdef]
  have hleft : (∫ y : ℝ in z.im..w.im, ((z.re : ℂ) + y * I - a)⁻¹)
      = ∫ s : ℝ in C..D, ((A : ℂ) + (s : ℝ) * I)⁻¹ := by
    rw [← intervalIntegral.integral_comp_sub_right (fun s : ℝ => ((A : ℂ) + (s : ℝ) * I)⁻¹) a.im]
    refine intervalIntegral.integral_congr fun y _ => ?_
    congr 1
    apply Complex.ext <;> simp [hAdef]
  have harctan := arctan_rect_sum hA hB hC hD
  have harctanC : ((-(Real.arctan (B / C) - Real.arctan (A / C))
      + (Real.arctan (B / D) - Real.arctan (A / D))
      + (Real.arctan (D / B) - Real.arctan (C / B))
      - (Real.arctan (D / A) - Real.arctan (C / A)) : ℝ) : ℂ) = ((2 * π : ℝ) : ℂ) := by
    exact_mod_cast congrArg (fun r : ℝ => (r : ℂ)) harctan
  simp only [rectIntegral, hbot, htop, hright, hleft,
    integral_inv_ofReal_add_const_mul_I _ _ _ (ne_of_lt hC),
    integral_inv_ofReal_add_const_mul_I _ _ _ (ne_of_gt hD),
    integral_inv_const_add_ofReal_mul_I _ _ _ (ne_of_gt hB),
    integral_inv_const_add_ofReal_mul_I _ _ _ (ne_of_lt hA)]
  push_cast at harctanC ⊢
  linear_combination I * harctanC + ((1 / 2 : ℂ) * ((Real.log (B ^ 2 + C ^ 2) : ℂ)
    - (Real.log (A ^ 2 + C ^ 2) : ℂ) - (Real.log (B ^ 2 + D ^ 2) : ℂ)
    + (Real.log (A ^ 2 + D ^ 2) : ℂ))) * Complex.I_sq

/-! ## Auxiliary facts about logarithmic derivatives on a rectangle -/

lemma continuousOn_logDeriv {z w : ℂ} {F : ℂ → ℂ} (hF : Differentiable ℂ F)
    (hF0 : ∀ c ∈ Rect z w, F c ≠ 0) : ContinuousOn (logDeriv F) (RectFrontier z w) := by
  have hdF : Differentiable ℂ (deriv F) := fun x => ((hF.analyticAt x).deriv).differentiableAt
  have h : ContinuousOn (fun c => deriv F c / F c) (RectFrontier z w) :=
    hdF.continuous.continuousOn.div hF.continuous.continuousOn fun c hc => hF0 c hc.1
  simpa [logDeriv_apply] using h

/-- **Cauchy–Goursat** for the logarithmic derivative of an entire nonvanishing function. -/
lemma rectIntegral_logDeriv_eq_zero {z w : ℂ} {F : ℂ → ℂ} (hF : Differentiable ℂ F)
    (hF0 : ∀ c ∈ Rect z w, F c ≠ 0) : rectIntegral (logDeriv F) z w = 0 := by
  have hdF : Differentiable ℂ (deriv F) := fun x => ((hF.analyticAt x).deriv).differentiableAt
  refine rectIntegral_eq_zero_of_differentiableOn ?_
  intro c hc
  have h : DifferentiableAt ℂ (fun c => deriv F c / F c) c := (hdF c).div (hF c) (hF0 c hc)
  exact (h.congr_of_eventuallyEq (by filter_upwards with x using rfl)).differentiableWithinAt

/-- Points of the boundary are different from the interior points `a j`. -/
lemma sub_ne_zero_of_mem_RectFrontier {z w : ℂ} {ι : Type*} {s : Finset ι} {a : ι → ℂ}
    (ha : ∀ j ∈ s, (a j).re ∈ Ioo z.re w.re ∧ (a j).im ∈ Ioo z.im w.im) :
    ∀ c ∈ RectFrontier z w, ∀ j ∈ s, c - a j ≠ 0 := by
  intro c hc j hj hzero
  have hca : c = a j := by rwa [sub_eq_zero] at hzero
  have h1 := (ha j hj).1
  have h2 := (ha j hj).2
  rcases hc.2 with h | h | h | h <;> rw [hca] at h
  · exact absurd h (ne_of_gt h1.1)
  · exact absurd h (ne_of_lt h1.2)
  · exact absurd h (ne_of_gt h2.1)
  · exact absurd h (ne_of_lt h2.2)

/-! ## The factored argument principle -/

/-- Core computation: if `V` is nonvanishing and differentiable on the boundary of the rectangle,
its logarithmic derivative is continuous there and integrates to zero over the boundary, then the
winding number of `(∏ j ∈ s, (ζ - a j) ^ m j) * V ζ` is `∑ j ∈ s, m j`. -/
theorem windingRect_prod_mul {z w : ℂ} {V : ℂ → ℂ}
    (hVcont : ContinuousOn (logDeriv V) (RectFrontier z w))
    (hVint : rectIntegral (logDeriv V) z w = 0)
    (hVne : ∀ c ∈ RectFrontier z w, V c ≠ 0)
    (hVdiff : ∀ c ∈ RectFrontier z w, DifferentiableAt ℂ V c)
    {ι : Type*} {s : Finset ι} {a : ι → ℂ} {m : ι → ℕ}
    (ha : ∀ j ∈ s, (a j).re ∈ Ioo z.re w.re ∧ (a j).im ∈ Ioo z.im w.im) :
    windingRect (fun c => (∏ j ∈ s, (c - a j) ^ (m j)) * V c) z w = ∑ j ∈ s, (m j : ℂ) := by
  have hsub := sub_ne_zero_of_mem_RectFrontier ha
  have hPne : ∀ c ∈ RectFrontier z w, (∏ j ∈ s, (c - a j) ^ (m j)) ≠ 0 := fun c hc =>
    Finset.prod_ne_zero_iff.mpr fun j hj => pow_ne_zero _ (hsub c hc j hj)
  have hlog : ∀ c ∈ RectFrontier z w,
      logDeriv (fun c => (∏ j ∈ s, (c - a j) ^ (m j)) * V c) c
        = (∑ j ∈ s, (m j : ℂ) * (c - a j)⁻¹) + logDeriv V c := by
    intro c hc
    rw [logDeriv_mul c (hPne c hc) (hVne c hc) (by fun_prop) (hVdiff c hc)]
    congr 1
    have hprod := logDeriv_prod (𝕜 := ℂ) (𝕜' := ℂ) (s := s)
      (f := fun j => fun c : ℂ => (c - a j) ^ (m j)) (x := c)
      (fun j hj => pow_ne_zero _ (hsub c hc j hj)) (fun j _ => by fun_prop)
    rw [hprod]
    refine Finset.sum_congr rfl fun j _ => ?_
    have hpow : logDeriv (fun c : ℂ => (c - a j) ^ (m j)) c
        = (m j : ℂ) * logDeriv (fun c : ℂ => c - a j) c :=
      logDeriv_fun_pow (𝕜 := ℂ) (f := fun c : ℂ => c - a j) (x := c) (by fun_prop) (m j)
    rw [hpow, logDeriv_apply]
    simp [div_eq_mul_inv]
  have hcontTerm : ∀ j ∈ s,
      ContinuousOn (fun c => (m j : ℂ) * (c - a j)⁻¹) (RectFrontier z w) := fun j hj =>
    continuousOn_const.mul (ContinuousOn.inv₀ (by fun_prop) fun c hc => hsub c hc j hj)
  have hcontSum : ContinuousOn (fun c => ∑ j ∈ s, (m j : ℂ) * (c - a j)⁻¹) (RectFrontier z w) :=
    continuousOn_finset_sum _ hcontTerm
  rw [windingRect, rectIntegral_congr hlog, rectIntegral_add hcontSum hVcont, hVint, add_zero,
    rectIntegral_sum hcontTerm]
  have hterm : ∀ j ∈ s,
      rectIntegral (fun c => (m j : ℂ) * (c - a j)⁻¹) z w = (m j : ℂ) * (2 * (π : ℂ) * I) := by
    intro j hj
    rw [rectIntegral_const_mul,
      rectIntegral_inv_sub (ha j hj).1.1 (ha j hj).1.2 (ha j hj).2.1 (ha j hj).2.2]
  rw [Finset.sum_congr rfl hterm, ← Finset.sum_mul]
  have hpi : (π : ℂ) ≠ 0 := by exact_mod_cast Real.pi_ne_zero
  field_simp

/-- **Factored argument principle on a rectangle.**  If `U` is entire and nonvanishing on the
closed rectangle `Rect z w`, the points `a j` lie in the open interior of the rectangle, and
`H ζ = (∏ j, (ζ - a j) ^ m j) * U ζ`, then `H` is nonvanishing on the boundary of the rectangle
and `W (H; z, w) = ∑ j, m j`.

The hypotheses `hre`, `him` (non-degenerate rectangle) and `hm : ∀ j, 1 ≤ m j` are part of the
requested statement; the proof does not need them (`hre`, `him` follow from the existence of an
interior point whenever `k ≥ 1`, and a factor with `m j = 0` is constant equal to `1`). -/
theorem windingRect_factored {z w : ℂ} (hre : z.re < w.re) (him : z.im < w.im)
    {U : ℂ → ℂ} (hU : Differentiable ℂ U) (hU0 : ∀ c ∈ Rect z w, U c ≠ 0)
    {k : ℕ} (a : Fin k → ℂ) (m : Fin k → ℕ) (hm : ∀ j, 1 ≤ m j)
    (ha : ∀ j, (a j).re ∈ Ioo z.re w.re ∧ (a j).im ∈ Ioo z.im w.im) :
    (∀ c ∈ RectFrontier z w, (∏ j, (c - a j) ^ (m j)) * U c ≠ 0) ∧
      windingRect (fun c => (∏ j, (c - a j) ^ (m j)) * U c) z w = ∑ j, (m j : ℂ) := by
  have ha' : ∀ j ∈ (Finset.univ : Finset (Fin k)),
      (a j).re ∈ Ioo z.re w.re ∧ (a j).im ∈ Ioo z.im w.im := fun j _ => ha j
  have hsub := sub_ne_zero_of_mem_RectFrontier ha'
  have hUne : ∀ c ∈ RectFrontier z w, U c ≠ 0 := fun c hc => hU0 c hc.1
  have hPne : ∀ c ∈ RectFrontier z w, (∏ j, (c - a j) ^ (m j)) ≠ 0 := fun c hc =>
    Finset.prod_ne_zero_iff.mpr fun j hj => pow_ne_zero _ (hsub c hc j hj)
  exact ⟨fun c hc => mul_ne_zero (hPne c hc) (hUne c hc),
    windingRect_prod_mul (continuousOn_logDeriv hU hU0) (rectIntegral_logDeriv_eq_zero hU hU0)
      hUne (fun c _ => hU.differentiableAt) ha'⟩

/-- **Consumer shape.**  Under the hypotheses of `windingRect_factored`, dividing `H` by any
entire `B` that is nonvanishing on the closed rectangle does not change the winding number:
`W (H / B; z, w) = ∑ j, m j`. -/
theorem windingRect_factored_div {z w : ℂ} (hre : z.re < w.re) (him : z.im < w.im)
    {U : ℂ → ℂ} (hU : Differentiable ℂ U) (hU0 : ∀ c ∈ Rect z w, U c ≠ 0)
    {B : ℂ → ℂ} (hB : Differentiable ℂ B) (hB0 : ∀ c ∈ Rect z w, B c ≠ 0)
    {k : ℕ} (a : Fin k → ℂ) (m : Fin k → ℕ) (hm : ∀ j, 1 ≤ m j)
    (ha : ∀ j, (a j).re ∈ Ioo z.re w.re ∧ (a j).im ∈ Ioo z.im w.im) :
    windingRect (fun c => ((∏ j, (c - a j) ^ (m j)) * U c) / B c) z w = ∑ j, (m j : ℂ) := by
  set V : ℂ → ℂ := fun c => U c / B c with hVdef
  have hfun : (fun c => ((∏ j, (c - a j) ^ (m j)) * U c) / B c)
      = fun c => (∏ j, (c - a j) ^ (m j)) * V c := by
    funext c
    simp [hVdef, mul_div_assoc]
  have hVne : ∀ c ∈ RectFrontier z w, V c ≠ 0 := fun c hc =>
    div_ne_zero (hU0 c hc.1) (hB0 c hc.1)
  have hVdiff : ∀ c ∈ RectFrontier z w, DifferentiableAt ℂ V c := fun c hc =>
    (hU c).div (hB c) (hB0 c hc.1)
  have hVlog : ∀ c ∈ RectFrontier z w, logDeriv V c = logDeriv U c - logDeriv B c := fun c hc =>
    logDeriv_div c (hU0 c hc.1) (hB0 c hc.1) (hU c) (hB c)
  have hVcont : ContinuousOn (logDeriv V) (RectFrontier z w) := by
    refine ContinuousOn.congr ?_ fun c hc => hVlog c hc
    exact (continuousOn_logDeriv hU hU0).sub (continuousOn_logDeriv hB hB0)
  have hVint : rectIntegral (logDeriv V) z w = 0 := by
    rw [rectIntegral_congr hVlog,
      rectIntegral_sub (continuousOn_logDeriv hU hU0) (continuousOn_logDeriv hB hB0),
      rectIntegral_logDeriv_eq_zero hU hU0, rectIntegral_logDeriv_eq_zero hB hB0, sub_zero]
  rw [hfun]
  exact windingRect_prod_mul hVcont hVint hVne hVdiff fun j _ => ha j

end ArgumentPrinciple
