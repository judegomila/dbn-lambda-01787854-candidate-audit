import Mathlib

/-!
# Two analytic steps in the closed-barrier de Bruijn–Newman argument

This file formalizes the two analytic steps described in `aristotle-basecase.tex`.

Setting: `H : ℝ → ℂ → ℂ` is a family of entire functions (the backward heat flow evolution of
the Riemann `ξ` function), and `B t z = M₀ z * exp (φ t z)` is a nonvanishing factor, so that
`g t = H t / B t` is holomorphic where `B t ≠ 0`.

* **Step 1** (`DeBruijnNewman.norm_le_of_forall_pos`): a uniform lower bound `c ≤ ‖H t z‖` on a
  set `R` for all `t ∈ (0, t₀]` passes to the endpoint `t = 0` provided `t ↦ H t z` is continuous
  at `t = 0` uniformly on `R`; consequently `H 0` is zero free on `R`
  (`DeBruijnNewman.zero_free_endpoint`).

* **Step 2**: if `B` is zero free on `R`, then on `R` the zeros of `g = H / B` coincide with the
  zeros of `H` (`DeBruijnNewman.zeros_div_eq_zeros`), with the same multiplicities
  (`DeBruijnNewman.analyticOrderAt_div_eq`), and the argument-principle winding integral of `g`
  along the boundary of a rectangle equals that of `H`
  (`DeBruijnNewman.windingRect_div_eq`).  Since Mathlib does not (yet) contain the argument
  principle, the statement "the winding number counts the zeros of `H` inside `R`" is recorded
  as `DeBruijnNewman.windingRect_div_eq_zeroCount`, which takes the argument principle for `H`
  itself as a hypothesis.
-/

open Complex Set MeasureTheory intervalIntegral

namespace DeBruijnNewman

/-! ## Step 1: endpoint extension by continuity -/

/-- **Step 1 (endpoint extension by continuity).**
If `c ≤ ‖H t z‖` for all `z ∈ R` and all `t ∈ (0, t₀]`, and `t ↦ H t z` is continuous at `t = 0`
uniformly on `R`, then the bound persists at `t = 0`.

Compactness of `R` is not needed: the uniform continuity hypothesis is what makes the argument
work, so the statement is given for an arbitrary set `R`. -/
theorem norm_le_of_forall_pos {R : Set ℂ} {H : ℝ → ℂ → ℂ} {c t₀ : ℝ} (ht₀ : 0 < t₀)
    (hlow : ∀ t ∈ Ioc (0 : ℝ) t₀, ∀ z ∈ R, c ≤ ‖H t z‖)
    (hcont : ∀ ε > (0 : ℝ), ∃ δ > (0 : ℝ), ∀ t ∈ Ioc (0 : ℝ) δ, ∀ z ∈ R,
      ‖H t z - H 0 z‖ < ε) :
    ∀ z ∈ R, c ≤ ‖H 0 z‖ := by
  intro z hz
  by_contra hlt
  push_neg at hlt
  obtain ⟨δ, hδ, hδ'⟩ := hcont (c - ‖H 0 z‖) (by linarith)
  set t : ℝ := min δ t₀ with ht
  have htpos : 0 < t := lt_min hδ ht₀
  have h1 : c ≤ ‖H t z‖ := hlow t ⟨htpos, min_le_right _ _⟩ z hz
  have h2 : ‖H t z - H 0 z‖ < c - ‖H 0 z‖ := hδ' t ⟨htpos, min_le_left _ _⟩ z hz
  have h3 : ‖H t z‖ ≤ ‖H t z - H 0 z‖ + ‖H 0 z‖ := by
    simpa using norm_add_le (H t z - H 0 z) (H 0 z)
  linarith

/-- **Step 1, zero-freeness.** Under the hypotheses of `norm_le_of_forall_pos` with `c > 0`,
the endpoint function `H 0` is zero free on `R`. -/
theorem zero_free_endpoint {R : Set ℂ} {H : ℝ → ℂ → ℂ} {c t₀ : ℝ} (hc : 0 < c) (ht₀ : 0 < t₀)
    (hlow : ∀ t ∈ Ioc (0 : ℝ) t₀, ∀ z ∈ R, c ≤ ‖H t z‖)
    (hcont : ∀ ε > (0 : ℝ), ∃ δ > (0 : ℝ), ∀ t ∈ Ioc (0 : ℝ) δ, ∀ z ∈ R,
      ‖H t z - H 0 z‖ < ε) :
    ∀ z ∈ R, H 0 z ≠ 0 := by
  intro z hz h0
  have := norm_le_of_forall_pos ht₀ hlow hcont z hz
  rw [h0] at this
  simp at this
  linarith

/-! ## Step 2: the nonvanishing factor -/

/-- The nonvanishing factor `B z = M₀ z * exp (φ z)`. -/
noncomputable def Bfun (M₀ phi : ℂ → ℂ) : ℂ → ℂ := fun z => M₀ z * Complex.exp (phi z)

/-- `B = M₀ * exp φ` vanishes exactly where `M₀` does, since `exp` never vanishes. -/
theorem Bfun_ne_zero_iff (M₀ phi : ℂ → ℂ) (z : ℂ) : Bfun M₀ phi z ≠ 0 ↔ M₀ z ≠ 0 := by
  simp [Bfun, Complex.exp_ne_zero]

/-- **Step 2, zero sets.** Where `B` is nonvanishing, the zeros of `g = H / B` on `R` are exactly
the zeros of `H` on `R`. -/
theorem zeros_div_eq_zeros {R : Set ℂ} {H B : ℂ → ℂ} (hB : ∀ z ∈ R, B z ≠ 0) :
    {z ∈ R | H z / B z = 0} = {z ∈ R | H z = 0} := by
  ext z
  simp only [Set.mem_setOf_eq, div_eq_zero_iff]
  constructor
  · rintro ⟨hz, h | h⟩
    · exact ⟨hz, h⟩
    · exact absurd h (hB z hz)
  · rintro ⟨hz, h⟩
    exact ⟨hz, Or.inl h⟩

/-- **Step 2, multiplicities.** Dividing by a function that is analytic and nonzero at `z₀` does
not change the order of vanishing at `z₀`. -/
theorem analyticOrderAt_div_eq {H B : ℂ → ℂ} {z₀ : ℂ} (hH : AnalyticAt ℂ H z₀)
    (hB : AnalyticAt ℂ B z₀) (hBz : B z₀ ≠ 0) :
    analyticOrderAt (fun z => H z / B z) z₀ = analyticOrderAt H z₀ := by
  have hinv : AnalyticAt ℂ (fun z => (B z)⁻¹) z₀ := hB.inv hBz
  have hfun : (fun z => H z / B z) = (fun z => H z * (B z)⁻¹) := by
    funext z; rw [div_eq_mul_inv]
  have hinvzero : analyticOrderAt (fun z => (B z)⁻¹) z₀ = 0 :=
    analyticOrderAt_eq_zero.2 (Or.inr (inv_ne_zero hBz))
  rw [hfun, show (fun z => H z * (B z)⁻¹) = H * (fun z => (B z)⁻¹) from rfl,
    analyticOrderAt_mul hH hinv, hinvzero, add_zero]

/-! ### The winding integral along the boundary of a rectangle -/

/-- The closed rectangle with opposite corners `z` and `w`. -/
def Rect (z w : ℂ) : Set ℂ := (uIcc z.re w.re) ×ℂ (uIcc z.im w.im)

/-- The integral of `f` along the (positively oriented) boundary of the rectangle with opposite
corners `z` and `w`, in the form used by Mathlib's rectangle Cauchy theorem. -/
noncomputable def rectIntegral (f : ℂ → ℂ) (z w : ℂ) : ℂ :=
  (∫ x : ℝ in z.re..w.re, f (x + z.im * I)) - (∫ x : ℝ in z.re..w.re, f (x + w.im * I)) +
    I * (∫ y : ℝ in z.im..w.im, f (w.re + y * I)) -
    I * (∫ y : ℝ in z.im..w.im, f (z.re + y * I))

/-- The argument-principle winding number of `f` along the boundary of the rectangle with
opposite corners `z` and `w`, i.e. `(2πi)⁻¹ ∮ f'/f`. -/
noncomputable def windingRect (f : ℂ → ℂ) (z w : ℂ) : ℂ :=
  (2 * Real.pi * I)⁻¹ * rectIntegral (logDeriv f) z w

/-- Integrability of `f` along each of the four sides of the rectangle. -/
def SideIntegrable (f : ℂ → ℂ) (z w : ℂ) : Prop :=
  IntervalIntegrable (fun x : ℝ => f (x + z.im * I)) volume z.re w.re ∧
  IntervalIntegrable (fun x : ℝ => f (x + w.im * I)) volume z.re w.re ∧
  IntervalIntegrable (fun y : ℝ => f (w.re + y * I)) volume z.im w.im ∧
  IntervalIntegrable (fun y : ℝ => f (z.re + y * I)) volume z.im w.im

theorem rectIntegral_sub {f g : ℂ → ℂ} {z w : ℂ} (hf : SideIntegrable f z w)
    (hg : SideIntegrable g z w) :
    rectIntegral (fun ζ => f ζ - g ζ) z w = rectIntegral f z w - rectIntegral g z w := by
  obtain ⟨hf1, hf2, hf3, hf4⟩ := hf
  obtain ⟨hg1, hg2, hg3, hg4⟩ := hg
  simp only [rectIntegral, intervalIntegral.integral_sub hf1 hg1,
    intervalIntegral.integral_sub hf2 hg2, intervalIntegral.integral_sub hf3 hg3,
    intervalIntegral.integral_sub hf4 hg4]
  ring

/-- Each of the four sides of the rectangle is contained in the rectangle. -/
theorem side_mem_rect (z w : ℂ) :
    (∀ x ∈ uIcc z.re w.re, ((x : ℂ) + z.im * I) ∈ Rect z w) ∧
    (∀ x ∈ uIcc z.re w.re, ((x : ℂ) + w.im * I) ∈ Rect z w) ∧
    (∀ y ∈ uIcc z.im w.im, ((w.re : ℂ) + y * I) ∈ Rect z w) ∧
    (∀ y ∈ uIcc z.im w.im, ((z.re : ℂ) + y * I) ∈ Rect z w) := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> intro u hu <;>
    simp only [Rect, Complex.mem_reProdIm, Complex.add_re, Complex.add_im, Complex.ofReal_re,
      Complex.ofReal_im, Complex.mul_re, Complex.mul_im, Complex.I_re, Complex.I_im] <;>
    simp <;> tauto

theorem sideIntegrable_of_continuousOn {f : ℂ → ℂ} {z w : ℂ} (hf : ContinuousOn f (Rect z w)) :
    SideIntegrable f z w := by
  obtain ⟨s1, s2, s3, s4⟩ := side_mem_rect z w
  have hc1 : Continuous fun x : ℝ => ((x : ℂ) + z.im * I) := by fun_prop
  have hc2 : Continuous fun x : ℝ => ((x : ℂ) + w.im * I) := by fun_prop
  have hc3 : Continuous fun y : ℝ => ((w.re : ℂ) + y * I) := by fun_prop
  have hc4 : Continuous fun y : ℝ => ((z.re : ℂ) + y * I) := by fun_prop
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact ((hf.comp hc1.continuousOn s1)).intervalIntegrable
  · exact ((hf.comp hc2.continuousOn s2)).intervalIntegrable
  · exact ((hf.comp hc3.continuousOn s3)).intervalIntegrable
  · exact ((hf.comp hc4.continuousOn s4)).intervalIntegrable

/-- The set of points of the rectangle lying on its boundary. -/
def RectFrontier (z w : ℂ) : Set ℂ :=
  {ζ ∈ Rect z w | ζ.re = z.re ∨ ζ.re = w.re ∨ ζ.im = z.im ∨ ζ.im = w.im}

theorem side_mem_rectFrontier (z w : ℂ) :
    (∀ x ∈ uIcc z.re w.re, ((x : ℂ) + z.im * I) ∈ RectFrontier z w) ∧
    (∀ x ∈ uIcc z.re w.re, ((x : ℂ) + w.im * I) ∈ RectFrontier z w) ∧
    (∀ y ∈ uIcc z.im w.im, ((w.re : ℂ) + y * I) ∈ RectFrontier z w) ∧
    (∀ y ∈ uIcc z.im w.im, ((z.re : ℂ) + y * I) ∈ RectFrontier z w) := by
  obtain ⟨s1, s2, s3, s4⟩ := side_mem_rect z w
  refine ⟨fun x hx => ⟨s1 x hx, ?_⟩, fun x hx => ⟨s2 x hx, ?_⟩, fun y hy => ⟨s3 y hy, ?_⟩,
    fun y hy => ⟨s4 y hy, ?_⟩⟩ <;> simp

/-- If `f` is entire and nonvanishing on the boundary of the rectangle, then its logarithmic
derivative is integrable along each side. -/
theorem sideIntegrable_logDeriv {f : ℂ → ℂ} {z w : ℂ} (hf : Differentiable ℂ f)
    (hne : ∀ ζ ∈ RectFrontier z w, f ζ ≠ 0) : SideIntegrable (logDeriv f) z w := by
  have hderiv : Differentiable ℂ (deriv f) := by
    have h2 := (analyticOnNhd_univ_iff_differentiable.mpr hf).deriv
    intro x
    exact (h2 x (Set.mem_univ x)).differentiableAt
  obtain ⟨s1, s2, s3, s4⟩ := side_mem_rectFrontier z w
  have hc1 : Continuous fun x : ℝ => ((x : ℂ) + z.im * I) := by fun_prop
  have hc2 : Continuous fun x : ℝ => ((x : ℂ) + w.im * I) := by fun_prop
  have hc3 : Continuous fun y : ℝ => ((w.re : ℂ) + y * I) := by fun_prop
  have hc4 : Continuous fun y : ℝ => ((z.re : ℂ) + y * I) := by fun_prop
  have key : ∀ (a b : ℝ) (p : ℝ → ℂ), Continuous p → (∀ u ∈ uIcc a b, p u ∈ RectFrontier z w) →
      IntervalIntegrable (fun u : ℝ => logDeriv f (p u)) volume a b := by
    intro a b p hp hmem
    apply ContinuousOn.intervalIntegrable
    apply ContinuousOn.div
    · exact (hderiv.continuous.comp hp).continuousOn
    · exact (hf.continuous.comp hp).continuousOn
    · exact fun u hu => hne _ (hmem u hu)
  exact ⟨key _ _ _ hc1 s1, key _ _ _ hc2 s2, key _ _ _ hc3 s3, key _ _ _ hc4 s4⟩

/-- Cauchy's theorem for a rectangle: the boundary integral of a function that is holomorphic on
the closed rectangle vanishes. -/
theorem rectIntegral_eq_zero {f : ℂ → ℂ} {z w : ℂ} (hf : DifferentiableOn ℂ f (Rect z w)) :
    rectIntegral f z w = 0 := by
  have := Complex.integral_boundary_rect_eq_zero_of_differentiableOn f z w hf
  simpa [rectIntegral, Complex.real_smul, smul_eq_mul] using this

/-- **Step 2 (winding counts zeros, not poles).**
If `H` and `B` are entire, `B` is zero free on the closed rectangle and `H` is zero free on its
boundary, then the winding integral of `g = H / B` along the boundary of the rectangle equals that
of `H`: dividing by the nonvanishing factor `B` contributes nothing. -/
theorem windingRect_div_eq {H B : ℂ → ℂ} {z w : ℂ} (hH : Differentiable ℂ H)
    (hB : Differentiable ℂ B) (hBne : ∀ ζ ∈ Rect z w, B ζ ≠ 0)
    (hHne : ∀ ζ ∈ RectFrontier z w, H ζ ≠ 0) :
    windingRect (fun ζ => H ζ / B ζ) z w = windingRect H z w := by
  have hBfront : ∀ ζ ∈ RectFrontier z w, B ζ ≠ 0 := fun ζ hζ => hBne ζ hζ.1
  have hlog : ∀ ζ ∈ RectFrontier z w,
      logDeriv (fun x => H x / B x) ζ = logDeriv H ζ - logDeriv B ζ := by
    intro ζ hζ
    exact logDeriv_div ζ (hHne ζ hζ) (hBfront ζ hζ) (hH ζ) (hB ζ)
  -- the boundary integrals of `logDeriv (H/B)` and of `logDeriv H - logDeriv B` agree
  have hgi : SideIntegrable (logDeriv H) z w := sideIntegrable_logDeriv hH hHne
  have hbi : SideIntegrable (logDeriv B) z w := sideIntegrable_logDeriv hB hBfront
  have hcongr : rectIntegral (logDeriv fun x => H x / B x) z w =
      rectIntegral (fun ζ => logDeriv H ζ - logDeriv B ζ) z w := by
    obtain ⟨s1, s2, s3, s4⟩ := side_mem_rectFrontier z w
    simp only [rectIntegral]
    rw [intervalIntegral.integral_congr (g := fun x : ℝ => logDeriv H ((x : ℂ) + z.im * I) -
        logDeriv B ((x : ℂ) + z.im * I)) (fun x hx => hlog _ (s1 x hx)),
      intervalIntegral.integral_congr (g := fun x : ℝ => logDeriv H ((x : ℂ) + w.im * I) -
        logDeriv B ((x : ℂ) + w.im * I)) (fun x hx => hlog _ (s2 x hx)),
      intervalIntegral.integral_congr (g := fun y : ℝ => logDeriv H ((w.re : ℂ) + y * I) -
        logDeriv B ((w.re : ℂ) + y * I)) (fun y hy => hlog _ (s3 y hy)),
      intervalIntegral.integral_congr (g := fun y : ℝ => logDeriv H ((z.re : ℂ) + y * I) -
        logDeriv B ((z.re : ℂ) + y * I)) (fun y hy => hlog _ (s4 y hy))]
  have hBzero : rectIntegral (logDeriv B) z w = 0 := by
    apply rectIntegral_eq_zero
    have hderivB : Differentiable ℂ (deriv B) := by
      have h2 := (analyticOnNhd_univ_iff_differentiable.mpr hB).deriv
      intro x
      exact (h2 x (Set.mem_univ x)).differentiableAt
    intro ζ hζ
    exact (((hderivB ζ).div (hB ζ) (hBne ζ hζ)).differentiableWithinAt)
  simp only [windingRect]
  rw [hcongr, rectIntegral_sub hgi hbi, hBzero, sub_zero]

/-- **Step 2, conclusion.** Mathlib does not contain the argument principle, so we record it as a
hypothesis for `H`: if the winding integral of `H` along the boundary of the rectangle counts the
`N` zeros of `H` inside it, then so does the winding integral of `g = H / B`. -/
theorem windingRect_div_eq_zeroCount {H B : ℂ → ℂ} {z w : ℂ} {N : ℕ} (hH : Differentiable ℂ H)
    (hB : Differentiable ℂ B) (hBne : ∀ ζ ∈ Rect z w, B ζ ≠ 0)
    (hHne : ∀ ζ ∈ RectFrontier z w, H ζ ≠ 0)
    (hAP : windingRect H z w = N) :
    windingRect (fun ζ => H ζ / B ζ) z w = N := by
  rw [windingRect_div_eq hH hB hBne hHne, hAP]

/-! ### Specialization to the factor `B = M₀ * exp φ` -/

/-- On a set where `M₀` is zero free, the zeros of `H / (M₀ exp φ)` are exactly the zeros of `H`. -/
theorem zeros_div_Bfun_eq_zeros {R : Set ℂ} {H M₀ phi : ℂ → ℂ} (hM : ∀ z ∈ R, M₀ z ≠ 0) :
    {z ∈ R | H z / Bfun M₀ phi z = 0} = {z ∈ R | H z = 0} :=
  zeros_div_eq_zeros fun z hz => (Bfun_ne_zero_iff M₀ phi z).2 (hM z hz)

/-- The winding integral of `g = H / (M₀ exp φ)` along the boundary of a rectangle on which `M₀`
is zero free (and on whose boundary `H` is zero free) equals that of `H`. -/
theorem windingRect_div_Bfun_eq {H M₀ phi : ℂ → ℂ} {z w : ℂ} (hH : Differentiable ℂ H)
    (hM : Differentiable ℂ M₀) (hphi : Differentiable ℂ phi)
    (hMne : ∀ ζ ∈ Rect z w, M₀ ζ ≠ 0) (hHne : ∀ ζ ∈ RectFrontier z w, H ζ ≠ 0) :
    windingRect (fun ζ => H ζ / Bfun M₀ phi ζ) z w = windingRect H z w :=
  windingRect_div_eq hH (hM.mul (Complex.differentiable_exp.comp hphi))
    (fun ζ hζ => (Bfun_ne_zero_iff M₀ phi ζ).2 (hMne ζ hζ)) hHne

end DeBruijnNewman
