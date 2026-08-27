import Mathlib
import RequestProject.ArgumentPrinciple

/-!
# The general argument principle on rectangles

Building on the factored argument principle of `RequestProject.ArgumentPrinciple`, this file
proves the argument principle for an arbitrary entire function `H` that is nonvanishing on the
boundary of the rectangle: the winding number `windingRect H z w` counts the zeros of `H` inside
the rectangle with multiplicity.
-/

open Set Complex Filter Topology MeasureTheory
open scoped Real BigOperators Interval

namespace ArgumentPrinciple

/-! ## Factoring out the zeros of an entire function -/

/-- If `H` is entire and does not vanish identically, its order of vanishing at any point is
finite. -/
lemma analyticOrderAt_ne_top {H : ℂ → ℂ} (hH : Differentiable ℂ H) (hne : ∃ x, H x ≠ 0) (p : ℂ) :
    analyticOrderAt H p ≠ ⊤ := by
  intro htop
  obtain ⟨x, hx⟩ := hne
  have hev : ∀ᶠ q in 𝓝 p, H q = 0 := analyticOrderAt_eq_top.mp htop
  have hfreq : ∃ᶠ q in 𝓝[≠] p, H q = 0 := (hev.filter_mono nhdsWithin_le_nhds).frequently
  have hAn : AnalyticOnNhd ℂ H Set.univ := fun y _ => hH.analyticAt y
  exact hx (hAn.eqOn_zero_of_preconnected_of_frequently_eq_zero isPreconnected_univ
    (Set.mem_univ p) hfreq (Set.mem_univ x))

/-- An entire function factors as `(ζ - p) ^ n` times an entire function that is nonzero at `p`,
where `n` is its order of vanishing at `p`. -/
lemma exists_factor_pow_sub {H : ℂ → ℂ} (hH : Differentiable ℂ H) (p : ℂ)
    (htop : analyticOrderAt H p ≠ ⊤) :
    ∃ G : ℂ → ℂ, Differentiable ℂ G ∧ G p ≠ 0 ∧
      ∀ ζ, H ζ = (ζ - p) ^ (analyticOrderNatAt H p) * G ζ := by
  classical
  obtain ⟨g, hg, hgp, hHg⟩ := (hH.analyticAt p).analyticOrderAt_ne_top.mp htop
  set n := analyticOrderNatAt H p with hn
  set G : ℂ → ℂ := fun ζ => if ζ = p then g p else H ζ / (ζ - p) ^ n with hG
  have hGg : G =ᶠ[𝓝 p] g := by
    filter_upwards [hHg] with x hx
    by_cases hxp : x = p
    · simp [hG, hxp]
    · have hne : (x - p) ^ n ≠ 0 := pow_ne_zero _ (sub_ne_zero.mpr hxp)
      simp only [hG, if_neg hxp, hx, smul_eq_mul]
      field_simp
  refine ⟨G, ?_, by simp [hG, hgp], ?_⟩
  · intro ζ
    by_cases h : ζ = p
    · subst h
      exact hg.differentiableAt.congr_of_eventuallyEq hGg
    · have hev : G =ᶠ[𝓝 ζ] fun x => H x / (x - p) ^ n := by
        filter_upwards [isOpen_ne.mem_nhds h] with x hx
        simp [hG, hx]
      have hd : DifferentiableAt ℂ (fun x : ℂ => (x - p) ^ n) ζ := by fun_prop
      exact ((hH ζ).div hd (pow_ne_zero n (sub_ne_zero.mpr h))).congr_of_eventuallyEq hev
  · intro ζ
    by_cases h : ζ = p
    · subst h
      simpa [hG, hn, smul_eq_mul] using hHg.self_of_nhds
    · have hne : (ζ - p) ^ n ≠ 0 := pow_ne_zero _ (sub_ne_zero.mpr h)
      simp only [hG, if_neg h]
      field_simp

/-- An entire function factors as a finite product of powers `(ζ - p) ^ (order of `H` at `p`)`,
`p` ranging over any finite set, times an entire function that is nonzero on that set. -/
lemma exists_factor_prod {H : ℂ → ℂ} (hH : Differentiable ℂ H) (hne : ∃ x, H x ≠ 0)
    (S : Finset ℂ) :
    ∃ G : ℂ → ℂ, Differentiable ℂ G ∧ (∀ p ∈ S, G p ≠ 0) ∧
      ∀ ζ, H ζ = (∏ p ∈ S, (ζ - p) ^ (analyticOrderNatAt H p)) * G ζ := by
  classical
  induction S using Finset.induction_on generalizing H with
  | empty => exact ⟨H, hH, by simp, by simp⟩
  | insert q T hq ih =>
      obtain ⟨G₁, hG₁, hG₁q, hHfac⟩ :=
        exists_factor_pow_sub hH q (analyticOrderAt_ne_top hH hne q)
      obtain ⟨G, hG, hGT, hG₁fac⟩ := ih hG₁ ⟨q, hG₁q⟩
      have horder : ∀ p ∈ T, analyticOrderNatAt G₁ p = analyticOrderNatAt H p := by
        intro p hp
        have hpq : p ≠ q := fun h => hq (h ▸ hp)
        have hHeq : H = (fun ζ : ℂ => (ζ - q) ^ (analyticOrderNatAt H q)) * G₁ := by
          funext ζ; simpa using hHfac ζ
        have h1 : AnalyticAt ℂ (fun ζ : ℂ => (ζ - q) ^ (analyticOrderNatAt H q)) p := by fun_prop
        have h0 : analyticOrderAt (fun ζ : ℂ => (ζ - q) ^ (analyticOrderNatAt H q)) p = 0 := by
          rw [h1.analyticOrderAt_eq_zero]
          exact pow_ne_zero _ (sub_ne_zero.mpr hpq)
        have hmul := analyticOrderAt_mul h1 (hG₁.analyticAt p)
        rw [← hHeq, h0, zero_add] at hmul
        rw [analyticOrderNatAt, analyticOrderNatAt, hmul]
      refine ⟨G, hG, ?_, ?_⟩
      · intro p hp
        rcases Finset.mem_insert.mp hp with rfl | hp
        · intro h0
          exact hG₁q (by rw [hG₁fac p, h0, mul_zero])
        · exact hGT p hp
      · intro ζ
        rw [Finset.prod_insert hq, hHfac ζ, hG₁fac ζ, mul_assoc]
        congr 2
        exact Finset.prod_congr rfl fun p hp => by rw [horder p hp]

/-! ## Finiteness of the zero set -/

lemma isCompact_Rect (z w : ℂ) : IsCompact (Rect z w) := by
  have h : Rect z w =
      (fun p : ℝ × ℝ => (p.1 : ℂ) + (p.2 : ℂ) * I) '' ([[z.re, w.re]] ×ˢ [[z.im, w.im]]) := by
    ext c
    simp only [Rect, Complex.mem_reProdIm, Set.mem_image, Set.mem_prod]
    constructor
    · rintro ⟨h1, h2⟩
      exact ⟨(c.re, c.im), ⟨h1, h2⟩, by simp⟩
    · rintro ⟨⟨x, y⟩, ⟨h1, h2⟩, rfl⟩
      simpa using ⟨h1, h2⟩
  rw [h]
  exact (isCompact_uIcc.prod isCompact_uIcc).image (by fun_prop)

/-- The zeros of a nonzero entire function in a compact set form a finite set. -/
lemma finite_zeros_of_isCompact {H : ℂ → ℂ} (hH : Differentiable ℂ H) (hne : ∃ x, H x ≠ 0)
    {K : Set ℂ} (hK : IsCompact K) : {p | p ∈ K ∧ H p = 0}.Finite := by
  by_contra hinf
  rw [Set.not_finite] at hinf
  obtain ⟨x, -, hx⟩ := hinf.exists_accPt_of_subset_isCompact hK fun p hp => hp.1
  rw [accPt_iff_frequently_nhdsNE] at hx
  have hfreq : ∃ᶠ y in 𝓝[≠] x, H y = 0 := hx.mono fun y hy => hy.2
  have hAn : AnalyticOnNhd ℂ H Set.univ := fun y _ => hH.analyticAt y
  obtain ⟨y, hy⟩ := hne
  exact hy (hAn.eqOn_zero_of_preconnected_of_frequently_eq_zero isPreconnected_univ
    (Set.mem_univ x) hfreq (Set.mem_univ y))

/-- The zeros of an entire function inside a rectangle form a finite set, provided the function
does not vanish identically. -/
lemma finite_zeros_Rect {z w : ℂ} {H : ℂ → ℂ} (hH : Differentiable ℂ H) (hne : ∃ x, H x ≠ 0) :
    {p | p ∈ Rect z w ∧ H p = 0}.Finite :=
  finite_zeros_of_isCompact hH hne (isCompact_Rect z w)

/-! ## The general argument principle -/

lemma mem_RectFrontier_left_corner (z w : ℂ) : z ∈ RectFrontier z w :=
  ⟨⟨left_mem_uIcc, left_mem_uIcc⟩, Or.inl rfl⟩

/-- A zero of `H` inside the rectangle, `H` being nonvanishing on the boundary, lies in the open
interior of the rectangle. -/
lemma mem_Ioo_of_zero_mem_Rect {z w : ℂ} (hre : z.re < w.re) (him : z.im < w.im) {H : ℂ → ℂ}
    (hbd : ∀ c ∈ RectFrontier z w, H c ≠ 0) {p : ℂ} (hp : p ∈ Rect z w) (hp0 : H p = 0) :
    p.re ∈ Ioo z.re w.re ∧ p.im ∈ Ioo z.im w.im := by
  have hnf : p ∉ RectFrontier z w := fun h => hbd p h hp0
  have h4 : ¬(p.re = z.re ∨ p.re = w.re ∨ p.im = z.im ∨ p.im = w.im) := fun h => hnf ⟨hp, h⟩
  push_neg at h4
  obtain ⟨h1, h2, h3, h4⟩ := h4
  have hre' : p.re ∈ Icc z.re w.re := by
    rw [← Set.uIcc_of_le hre.le]; exact hp.1
  have him' : p.im ∈ Icc z.im w.im := by
    rw [← Set.uIcc_of_le him.le]; exact hp.2
  exact ⟨⟨lt_of_le_of_ne hre'.1 (Ne.symm h1), lt_of_le_of_ne hre'.2 h2⟩,
    ⟨lt_of_le_of_ne him'.1 (Ne.symm h3), lt_of_le_of_ne him'.2 h4⟩⟩

/-- **The argument principle on a rectangle.**  If `H` is entire and nonvanishing on the boundary
of the rectangle with corners `z` and `w`, and `S` is the (finite) set of zeros of `H` in the
rectangle, then the winding number `W (H; z, w)` equals the number of zeros of `H` inside the
rectangle, counted with multiplicity. -/
theorem windingRect_eq_sum_analyticOrder {z w : ℂ} (hre : z.re < w.re) (him : z.im < w.im)
    {H : ℂ → ℂ} (hH : Differentiable ℂ H) (hbd : ∀ c ∈ RectFrontier z w, H c ≠ 0)
    (S : Finset ℂ) (hS : ∀ p, p ∈ S ↔ (p ∈ Rect z w ∧ H p = 0)) :
    windingRect H z w = ∑ p ∈ S, (analyticOrderNatAt H p : ℂ) := by
  have hne : ∃ x, H x ≠ 0 := ⟨z, hbd z (mem_RectFrontier_left_corner z w)⟩
  obtain ⟨G, hG, hGS, hfac⟩ := exists_factor_prod hH hne S
  have hG0 : ∀ c ∈ Rect z w, G c ≠ 0 := by
    intro c hc
    by_cases h : H c = 0
    · exact hGS c ((hS c).mpr ⟨hc, h⟩)
    · intro h0
      exact h (by rw [hfac c, h0, mul_zero])
  have ha : ∀ p ∈ S, (p : ℂ).re ∈ Ioo z.re w.re ∧ (p : ℂ).im ∈ Ioo z.im w.im := by
    intro p hp
    obtain ⟨hp1, hp2⟩ := (hS p).mp hp
    exact mem_Ioo_of_zero_mem_Rect hre him hbd hp1 hp2
  have hHfun : H = fun c => (∏ p ∈ S, (c - p) ^ (analyticOrderNatAt H p)) * G c := funext hfac
  conv_lhs => rw [hHfun]
  exact windingRect_prod_mul (continuousOn_logDeriv hG hG0) (rectIntegral_logDeriv_eq_zero hG hG0)
    (fun c hc => hG0 c hc.1) (fun c _ => hG.differentiableAt) ha

/-- **The argument principle on a rectangle**, stated with a finite sum over the zero set. -/
theorem windingRect_eq_finsum_analyticOrder {z w : ℂ} (hre : z.re < w.re) (him : z.im < w.im)
    {H : ℂ → ℂ} (hH : Differentiable ℂ H) (hbd : ∀ c ∈ RectFrontier z w, H c ≠ 0) :
    windingRect H z w
      = ∑ᶠ p ∈ {p | p ∈ Rect z w ∧ H p = 0}, (analyticOrderNatAt H p : ℂ) := by
  classical
  have hne : ∃ x, H x ≠ 0 := ⟨z, hbd z (mem_RectFrontier_left_corner z w)⟩
  have hfin : {p | p ∈ Rect z w ∧ H p = 0}.Finite := finite_zeros_Rect hH hne
  have hcoe : (hfin.toFinset : Set ℂ) = {p | p ∈ Rect z w ∧ H p = 0} := hfin.coe_toFinset
  rw [← hcoe, finsum_mem_coe_finset]
  exact windingRect_eq_sum_analyticOrder hre him hH hbd hfin.toFinset fun p => by
    simp [Set.Finite.mem_toFinset]

/-! ## A sanity check -/

/-- The winding number of the identity function around a rectangle containing the origin is `1`. -/
theorem windingRect_id_eq_one : windingRect (id : ℂ → ℂ) (-1 - I) (1 + I) = 1 := by
  have hre : (-1 - I : ℂ).re < (1 + I : ℂ).re := by norm_num
  have him : (-1 - I : ℂ).im < (1 + I : ℂ).im := by norm_num
  have hbd : ∀ c ∈ RectFrontier (-1 - I : ℂ) (1 + I), id c ≠ 0 := by
    rintro c hc rfl
    rcases hc.2 with h | h | h | h <;> norm_num at h
  have hS : ∀ p : ℂ, p ∈ ({0} : Finset ℂ) ↔ (p ∈ Rect (-1 - I : ℂ) (1 + I) ∧ id p = 0) := by
    intro p
    simp only [Finset.mem_singleton, id]
    constructor
    · rintro rfl
      exact ⟨⟨by simp, by simp⟩, rfl⟩
    · exact fun h => h.2
  rw [windingRect_eq_sum_analyticOrder hre him differentiable_id hbd ({0} : Finset ℂ) hS]
  simp [analyticOrderNatAt, analyticOrderAt_id]

end ArgumentPrinciple
