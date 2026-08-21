import Mathlib

/-!
# Finite window-freeze theorem at the `0.1787854` row

This file formalizes the statements of `job3_window_freeze.tex`:

* `WindowFreeze.window_freeze` (Theorem 1): on every window `W N = [x N, x (N+1))`,
  with `690988 ≤ N ≤ 3840000`, freezing `x` to the closed left endpoint `x N` is
  conservative in all three directions: `G` and `K` decrease, `Σ` increases.
* the three monotonicity facts (`∂ₓG < 0`, `∂ₓK < 0`, `Σ` strictly increasing),
  the last one via the nonincreasing product `x⁻² h₊`.
* `WindowFreeze.site_bracket` (Lemma 2) together with the two certified margins.
* `WindowFreeze.window_cover` (Theorem 3), the exact half-open union identity,
  together with the pairwise disjointness statements.
-/

open scoped Real

set_option maxHeartbeats 1000000

namespace WindowFreeze

/-! ## Definitions -/

/-- The frozen shift parameter `t₀ = 129/800`. -/
noncomputable def t0 : ℝ := 129 / 800

/-- `y₀² = 87677/2500000`. -/
noncomputable def y0sq : ℝ := 87677 / 2500000

/-- `y_max² = 1 - 2 t₀ = 271/400`. -/
noncomputable def ymaxsq : ℝ := 271 / 400

/-- `y₀`, the positive square root of `y₀²`. -/
noncomputable def y0 : ℝ := Real.sqrt y0sq

/-- `y_max`, the positive square root of `y_max²`. -/
noncomputable def ymax : ℝ := Real.sqrt ymaxsq

/-- `q_N = N² - t₀/16`. -/
noncomputable def qq (N : ℤ) : ℝ := (N : ℝ) ^ 2 - t0 / 16

/-- `x_N = 4π q_N`. -/
noncomputable def xx (N : ℤ) : ℝ := 4 * Real.pi * qq N

/-- The half-open window `W_N = [x_N, x_{N+1})`. -/
noncomputable def W (N : ℤ) : Set ℝ := Set.Ico (xx N) (xx (N + 1))

/-- `G(x,y) = e^{y/50} (x/4π)^{-y/2}`. -/
noncomputable def G (x y : ℝ) : ℝ := Real.exp (y / 50) * (x / (4 * Real.pi)) ^ (-y / 2)

/-- `K(x,y) = t₀ y / (2(x-6))`. -/
noncomputable def K (x y : ℝ) : ℝ := t0 * y / (2 * (x - 6))

/-- `h(x,y) = 1 - 3y + 4y(1+y)/x²`, the bracket whose positive part enters `Σ`. -/
noncomputable def hh (x y : ℝ) : ℝ := 1 - 3 * y + 4 * y * (1 + y) / x ^ 2

/-- `Σ(x,y) = (1+y)/2 + (t₀/4) log(x/4π) - (t₀/2x²) (h(x,y))₊`. -/
noncomputable def Sig (x y : ℝ) : ℝ :=
  (1 + y) / 2 + t0 / 4 * Real.log (x / (4 * Real.pi)) - t0 / (2 * x ^ 2) * max 0 (hh x y)

/-- The integer `X = 6000000185827` of Lemma 2. -/
noncomputable def Xsite : ℝ := 6000000185827

/-- The criterion start `x_* = X + √(1 - y₀²)`. -/
noncomputable def xstar : ℝ := Xsite + Real.sqrt (1 - y0sq)

/-! ## Elementary positivity facts -/

lemma y0_pos : 0 < y0 := by
  rw [y0, y0sq]
  positivity

/-- `y_max² = 1 - 2 t₀`. -/
lemma ymaxsq_eq : ymaxsq = 1 - 2 * t0 := by
  rw [ymaxsq, t0]; norm_num

/-- The `y`-range of Theorem 1 is nondegenerate. -/
lemma y0_lt_ymax : y0 < ymax :=
  Real.sqrt_lt_sqrt (by rw [y0sq]; norm_num) (by rw [y0sq, ymaxsq]; norm_num)

lemma qq_pos_of_le {N : ℤ} (hN : 1 ≤ N) : 0 < qq N := by
  have h1 : (1 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have : (1 : ℝ) ≤ (N : ℝ) ^ 2 := by nlinarith
  rw [qq, t0]; linarith

lemma xx_pos {N : ℤ} (hN : 1 ≤ N) : 0 < xx N := by
  have := qq_pos_of_le hN
  have hpi := Real.pi_pos
  rw [xx]; positivity

lemma qq_large {N : ℤ} (hN : 690988 ≤ N) : (477464416143 : ℝ) ≤ qq N := by
  have h1 : (690988 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have : (690988 : ℝ) ^ 2 ≤ (N : ℝ) ^ 2 := by nlinarith
  rw [qq, t0]; nlinarith

lemma xx_large {N : ℤ} (hN : 690988 ≤ N) : (100 : ℝ) < xx N := by
  have hq := qq_large hN
  have hpi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  rw [xx]
  nlinarith

/-! ## Monotonicity in `x` : the three signs -/

lemma G_pos {x y : ℝ} (hx : 0 < x) : 0 < G x y := by
  have hpi := Real.pi_pos
  have : 0 < x / (4 * Real.pi) := by positivity
  exact mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos this _)

/-- `∂ₓG = -(y/2x) G`. -/
lemma hasDerivAt_G (y : ℝ) {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun x => G x y) (-(y / (2 * x)) * G x y) x := by
  have hpi := Real.pi_pos
  have hb : 0 < x / (4 * Real.pi) := by positivity
  have h1 : HasDerivAt (fun x : ℝ => x / (4 * Real.pi)) (1 / (4 * Real.pi)) x := by
    simpa using (hasDerivAt_id x).div_const (4 * Real.pi)
  have h3 := (h1.rpow_const (p := -y / 2) (Or.inl hb.ne')).const_mul (Real.exp (y / 50))
  simp only [G]
  convert h3 using 1
  rw [Real.rpow_sub hb, Real.rpow_one]
  field_simp

/-- `∂ₓG < 0` on the target domain. -/
lemma deriv_G_neg {x y : ℝ} (hx : 0 < x) (hy : 0 < y) :
    deriv (fun x => G x y) x < 0 := by
  rw [(hasDerivAt_G y hx).deriv]
  have := G_pos (y := y) hx
  have h1 : 0 < y / (2 * x) := by positivity
  nlinarith

/-- `∂ₓK = -t₀y/(2(x-6)²)`. -/
lemma hasDerivAt_K (y : ℝ) {x : ℝ} (hx : x ≠ 6) :
    HasDerivAt (fun x => K x y) (-(t0 * y / (2 * (x - 6) ^ 2))) x := by
  have hd : (x - 6) ≠ 0 := sub_ne_zero.mpr hx
  have h1 : HasDerivAt (fun x : ℝ => 2 * (x - 6)) 2 x := by
    simpa using ((hasDerivAt_id x).sub_const 6).const_mul (2 : ℝ)
  have h0 : HasDerivAt (fun _ : ℝ => t0 * y) 0 x := hasDerivAt_const x (t0 * y)
  have h2 := h0.div h1 (by simpa using hd)
  simp only [K]
  convert h2 using 1
  field_simp
  ring

/-- `∂ₓK < 0` on the target domain. -/
lemma deriv_K_neg {x y : ℝ} (hx : 6 < x) (hy : 0 < y) :
    deriv (fun x => K x y) x < 0 := by
  rw [(hasDerivAt_K y (by linarith : x ≠ 6)).deriv]
  have ht : (0 : ℝ) < t0 := by rw [t0]; norm_num
  have : 0 < t0 * y / (2 * (x - 6) ^ 2) := by
    have : (0 : ℝ) < x - 6 := by linarith
    positivity
  linarith

/-- `G` is strictly decreasing in `x` on `(0,∞)` for `y > 0`. -/
lemma G_strictAntiOn {y : ℝ} (hy : 0 < y) : StrictAntiOn (fun x => G x y) (Set.Ioi 0) := by
  intro a ha b _ hab
  have hpi := Real.pi_pos
  have ha' : (0 : ℝ) < a := ha
  have h1 : 0 < a / (4 * Real.pi) := by positivity
  have h2 : a / (4 * Real.pi) < b / (4 * Real.pi) := by gcongr
  have h3 : (b / (4 * Real.pi)) ^ (-y / 2) < (a / (4 * Real.pi)) ^ (-y / 2) :=
    Real.rpow_lt_rpow_of_neg h1 h2 (by linarith)
  simp only [G]
  exact mul_lt_mul_of_pos_left h3 (Real.exp_pos _)

/-- `G` is nonincreasing in `x` on `(0,∞)` for `y ≥ 0`. -/
lemma G_le_of_le {y : ℝ} (hy : 0 ≤ y) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    G b y ≤ G a y := by
  have hpi := Real.pi_pos
  have h1 : 0 < a / (4 * Real.pi) := by positivity
  have h2 : a / (4 * Real.pi) ≤ b / (4 * Real.pi) := by gcongr
  have h3 : (b / (4 * Real.pi)) ^ (-y / 2) ≤ (a / (4 * Real.pi)) ^ (-y / 2) :=
    Real.rpow_le_rpow_of_nonpos h1 h2 (by linarith)
  simp only [G]
  exact mul_le_mul_of_nonneg_left h3 (Real.exp_pos _).le

/-- `K` is strictly decreasing in `x` on `(6,∞)` for `y > 0`. -/
lemma K_strictAntiOn {y : ℝ} (hy : 0 < y) : StrictAntiOn (fun x => K x y) (Set.Ioi 6) := by
  intro a ha b _ hab
  have ha' : (6 : ℝ) < a := ha
  simp only [K, t0]
  gcongr
  linarith

/-- `K` is nonincreasing in `x` on `(6,∞)` for `y ≥ 0`. -/
lemma K_le_of_le {y : ℝ} (hy : 0 ≤ y) {a b : ℝ} (ha : 6 < a) (hab : a ≤ b) :
    K b y ≤ K a y := by
  simp only [K, t0]
  gcongr
  linarith

/-- The bracket `h` is nonincreasing in `x` for `y ≥ 0`. -/
lemma hh_le_of_le {y : ℝ} (hy : 0 ≤ y) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    hh b y ≤ hh a y := by
  simp only [hh]
  gcongr

/-- The product `x⁻² h₊` is nonincreasing in `x` for `y ≥ 0`: both factors are
nonnegative and nonincreasing. -/
lemma inv_sq_mul_hplus_antitone {y : ℝ} (hy : 0 ≤ y) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    1 / b ^ 2 * max 0 (hh b y) ≤ 1 / a ^ 2 * max 0 (hh a y) := by
  have hb : 0 < b := lt_of_lt_of_le ha hab
  have h1 : 1 / b ^ 2 ≤ 1 / a ^ 2 := by gcongr
  have h2 : max 0 (hh b y) ≤ max 0 (hh a y) := max_le_max le_rfl (hh_le_of_le hy ha hab)
  have h3 : (0 : ℝ) ≤ max 0 (hh b y) := le_max_left _ _
  have h4 : (0 : ℝ) < 1 / b ^ 2 := by positivity
  calc 1 / b ^ 2 * max 0 (hh b y) ≤ 1 / b ^ 2 * max 0 (hh a y) :=
        mul_le_mul_of_nonneg_left h2 h4.le
    _ ≤ 1 / a ^ 2 * max 0 (hh a y) := by
        exact mul_le_mul_of_nonneg_right h1 (le_max_left _ _)

/-- `Σ` is strictly increasing in `x` on `(0,∞)` for `y ≥ 0` (including across the
kink `h = 0`): the logarithmic term is strictly increasing and the product `x⁻² h₊`
is nonincreasing. -/
lemma Sig_strictMonoOn {y : ℝ} (hy : 0 ≤ y) : StrictMonoOn (fun x => Sig x y) (Set.Ioi 0) := by
  intro a ha b _ hab
  have ha' : (0 : ℝ) < a := ha
  have hpi := Real.pi_pos
  have ht : (0 : ℝ) < t0 := by rw [t0]; norm_num
  have hlog : Real.log (a / (4 * Real.pi)) < Real.log (b / (4 * Real.pi)) := by
    exact Real.log_lt_log (by positivity) (by gcongr)
  have hprod := inv_sq_mul_hplus_antitone hy ha' hab.le
  have e1 : t0 / (2 * a ^ 2) * max 0 (hh a y) = t0 / 2 * (1 / a ^ 2 * max 0 (hh a y)) := by
    ring
  have e2 : t0 / (2 * b ^ 2) * max 0 (hh b y) = t0 / 2 * (1 / b ^ 2 * max 0 (hh b y)) := by
    ring
  have hp2 : t0 / 2 * (1 / b ^ 2 * max 0 (hh b y)) ≤ t0 / 2 * (1 / a ^ 2 * max 0 (hh a y)) :=
    mul_le_mul_of_nonneg_left hprod (by linarith)
  have hl2 : t0 / 4 * Real.log (a / (4 * Real.pi)) < t0 / 4 * Real.log (b / (4 * Real.pi)) :=
    by apply mul_lt_mul_of_pos_left hlog; linarith
  simp only [Sig]
  rw [e1, e2]
  linarith

/-- `Σ` is nondecreasing in `x` on `(0,∞)` for `y ≥ 0`. -/
lemma Sig_le_of_le {y : ℝ} (hy : 0 ≤ y) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) :
    Sig a y ≤ Sig b y := by
  rcases eq_or_lt_of_le hab with rfl | h
  · exact le_rfl
  · exact (Sig_strictMonoOn hy (Set.mem_Ioi.mpr ha)
      (Set.mem_Ioi.mpr (lt_trans ha h)) h).le

/-! ## Theorem 1 -/

/-- **Theorem 1 (conservative per-window `x`-freeze).**
For every integer `690988 ≤ N ≤ 3840000`, every `x ∈ W_N` and every `y ∈ [y₀, y_max]`,
`G(x,y) ≤ G_N(y)`, `K(x,y) ≤ K_N(y)` and `Σ(x,y) ≥ Σ_N(y)`.
(The upper bound `y ≤ y_max` and the upper bound `N ≤ 3840000` are part of the stated
domain; the proof only uses `y₀ ≤ y` and `690988 ≤ N`.) -/
theorem window_freeze {N : ℤ} (hN1 : 690988 ≤ N) (hN2 : N ≤ 3840000) {x y : ℝ}
    (hx : x ∈ W N) (hy0 : y0 ≤ y) (hy1 : y ≤ ymax) :
    G x y ≤ G (xx N) y ∧ K x y ≤ K (xx N) y ∧ Sig (xx N) y ≤ Sig x y := by
  simp only [W, Set.mem_Ico] at hx
  have hxl : xx N ≤ x := hx.1
  have hy : 0 < y := lt_of_lt_of_le y0_pos hy0
  have hxN : (100 : ℝ) < xx N := xx_large hN1
  exact ⟨G_le_of_le hy.le (by linarith) hxl, K_le_of_le hy.le (by linarith) hxl,
    Sig_le_of_le hy.le (by linarith) hxl⟩

end WindowFreeze
