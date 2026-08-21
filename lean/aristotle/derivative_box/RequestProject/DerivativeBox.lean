import Mathlib

/-!
# Spatial-box, discrete-sum and holomorphic-quadrature contracts

Formalization of `job6_derivative_box.tex`.

Throughout, `X > 0` is the barrier abscissa with `X^2 > 8`, the spatial box is
`x ∈ [X, X+1]`, `y ∈ [ymin, 1]`, and

* `qbox x = x / (4π)`,
* `hbox x y = 1 - 3y + 4y(1+y)/x^2`,
* `cbox x y = (1/4) log (qbox x) - (hbox x y)₊ / (2 x^2)`.
-/

set_option autoImplicit false

namespace DerivativeBox

open Real Set MeasureTheory

/-! ## Basic definitions -/

/-- `q(x) = x / (4π)`. -/
noncomputable def qbox (x : ℝ) : ℝ := x / (4 * Real.pi)

/-- `h(x,y) = 1 - 3y + 4y(1+y)/x²`. -/
noncomputable def hbox (x y : ℝ) : ℝ := 1 - 3 * y + 4 * y * (1 + y) / x ^ 2

/-- `c(x,y) = ¼ log q(x) - h(x,y)₊ / (2x²)`. -/
noncomputable def cbox (x y : ℝ) : ℝ :=
  (1 / 4) * Real.log (qbox x) - max (hbox x y) 0 / (2 * x ^ 2)

/-! ## Lemma 1: uniform spatial envelope -/

/-- The `y`-derivative of `h` is `-3 + 4(1+2y)/x²`. -/
theorem hbox_hasDerivAt_y (x y : ℝ) :
    HasDerivAt (fun z => hbox x z) (-3 + 4 * (1 + 2 * y) / x ^ 2) y := by
  have h1 : HasDerivAt (fun z : ℝ => 1 - 3 * z) (-3) y := by
    simpa using ((hasDerivAt_id y).const_mul (3 : ℝ)).const_sub 1
  have h3 : HasDerivAt (fun z : ℝ => 4 * z * (1 + z)) (4 * (1 + 2 * y)) y := by
    have h := ((hasDerivAt_id y).const_mul (4 : ℝ)).mul ((hasDerivAt_id y).const_add (1 : ℝ))
    simp only [id] at h
    convert h using 1
    ring
  simpa [hbox] using h1.add (h3.div_const (x ^ 2))

/-- On the box, `h_y < 0`. -/
theorem hbox_deriv_y_neg (x y : ℝ) (h8 : 8 < x ^ 2) (hy1 : y ≤ 1) :
    -3 + 4 * (1 + 2 * y) / x ^ 2 < 0 := by
  have hx2 : (0 : ℝ) < x ^ 2 := by linarith
  have h : 4 * (1 + 2 * y) / x ^ 2 < 3 := by
    rw [div_lt_iff₀ hx2]; nlinarith
  linarith

/-- The `x`-derivative of `h` is `-8y(1+y)/x³`. -/
theorem hbox_hasDerivAt_x (x y : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun u => hbox u y) (-(8 * y * (1 + y) / x ^ 3)) x := by
  have h : HasDerivAt (fun u : ℝ => 4 * y * (1 + y) / u ^ 2) (-(8 * y * (1 + y) / x ^ 3)) x := by
    have h1 := ((hasDerivAt_pow 2 x).inv (pow_ne_zero 2 hx)).const_mul (4 * y * (1 + y))
    convert h1 using 1
    field_simp
    ring
  have h2 := h.const_add (1 - 3 * y)
  simpa [hbox, div_eq_mul_inv, mul_comm, mul_assoc, mul_left_comm, sub_eq_add_neg] using h2

/-- On the box, `h_x ≤ 0`. -/
theorem hbox_deriv_x_nonpos (x y : ℝ) (hx : 0 < x) (hy0 : 0 ≤ y) :
    -(8 * y * (1 + y) / x ^ 3) ≤ 0 := by
  have h : 0 ≤ 8 * y * (1 + y) / x ^ 3 := by positivity
  linarith

/-- `h` decreases in both variables on the box. -/
theorem hbox_anti (x₁ x₂ y₁ y₂ : ℝ) (hx₁ : 0 < x₁) (h8 : 8 < x₁ ^ 2) (hx : x₁ ≤ x₂)
    (hy : y₁ ≤ y₂) (hy0 : 0 ≤ y₁) (hy1 : y₂ ≤ 1) :
    hbox x₂ y₂ ≤ hbox x₁ y₁ := by
  have hx2 : (0 : ℝ) < x₁ ^ 2 := by positivity
  have h1 : 4 * y₂ * (1 + y₂) / x₂ ^ 2 ≤ 4 * y₂ * (1 + y₂) / x₁ ^ 2 := by
    apply div_le_div_of_nonneg_left (by nlinarith) (by positivity)
    nlinarith
  have key : 4 * y₂ * (1 + y₂) / x₁ ^ 2 - 4 * y₁ * (1 + y₁) / x₁ ^ 2 ≤ 3 * (y₂ - y₁) := by
    rw [div_sub_div_same, div_le_iff₀ hx2]
    nlinarith
  simp only [hbox]
  linarith

/-- The logarithmic term `¼ log q(x)` is monotone in `x`. -/
theorem log_qbox_mono (x₁ x₂ : ℝ) (hx₁ : 0 < x₁) (hx : x₁ ≤ x₂) :
    Real.log (qbox x₁) ≤ Real.log (qbox x₂) := by
  have hpi : (0 : ℝ) < 4 * Real.pi := by positivity
  refine Real.log_le_log (div_pos hx₁ hpi) ?_
  simp only [qbox]
  gcongr

/-- The logarithmic term `¼ log q(x)` is strictly monotone in `x`. -/
theorem log_qbox_strictMono (x₁ x₂ : ℝ) (hx₁ : 0 < x₁) (hx : x₁ < x₂) :
    Real.log (qbox x₁) < Real.log (qbox x₂) := by
  have hpi : (0 : ℝ) < 4 * Real.pi := by positivity
  refine Real.log_lt_log (div_pos hx₁ hpi) ?_
  simp only [qbox]
  gcongr

/-- The positive-part correction decreases in both variables on the box. -/
theorem hbox_pos_div_anti (x₁ x₂ y₁ y₂ : ℝ) (hx₁ : 0 < x₁) (h8 : 8 < x₁ ^ 2) (hx : x₁ ≤ x₂)
    (hy : y₁ ≤ y₂) (hy0 : 0 ≤ y₁) (hy1 : y₂ ≤ 1) :
    max (hbox x₂ y₂) 0 / (2 * x₂ ^ 2) ≤ max (hbox x₁ y₁) 0 / (2 * x₁ ^ 2) := by
  have hmax : max (hbox x₂ y₂) 0 ≤ max (hbox x₁ y₁) 0 :=
    max_le_max (hbox_anti x₁ x₂ y₁ y₂ hx₁ h8 hx hy hy0 hy1) le_rfl
  have h0 : (0 : ℝ) ≤ max (hbox x₂ y₂) 0 := le_max_right _ _
  have hx2 : (0 : ℝ) < 2 * x₁ ^ 2 := by positivity
  gcongr

/-- `c` increases in both variables on the box. -/
theorem cbox_mono (x₁ x₂ y₁ y₂ : ℝ) (hx₁ : 0 < x₁) (h8 : 8 < x₁ ^ 2) (hx : x₁ ≤ x₂)
    (hy : y₁ ≤ y₂) (hy0 : 0 ≤ y₁) (hy1 : y₂ ≤ 1) :
    cbox x₁ y₁ ≤ cbox x₂ y₂ := by
  have hq := log_qbox_mono x₁ x₂ hx₁ hx
  have hdiv := hbox_pos_div_anti x₁ x₂ y₁ y₂ hx₁ h8 hx hy hy0 hy1
  simp only [cbox]
  linarith

/-- `c` is *strictly* increasing in `x` on the box (the logarithmic term strictly increases
while the positive-part correction is nonincreasing). -/
theorem cbox_strictMono_x (x₁ x₂ y : ℝ) (hx₁ : 0 < x₁) (h8 : 8 < x₁ ^ 2) (hx : x₁ < x₂)
    (hy0 : 0 ≤ y) (hy1 : y ≤ 1) :
    cbox x₁ y < cbox x₂ y := by
  have hq := log_qbox_strictMono x₁ x₂ hx₁ hx
  have hdiv := hbox_pos_div_anti x₁ x₂ y y hx₁ h8 hx.le le_rfl hy0 hy1
  simp only [cbox]
  linarith

/-- **Uniform spatial envelope.** The pointwise bound of Polymath Lemma 8.4, taken as a
hypothesis, upgrades to the uniform bound at the corner `(X, ymin)` of the box. -/
theorem cbox_envelope (X ymin x y t s : ℝ) (hX : 0 < X) (h8 : 8 < X ^ 2) (hxX : X ≤ x)
    (hymin : 0 ≤ ymin) (hy : ymin ≤ y) (hy1 : y ≤ 1) (ht : 0 ≤ t)
    (hpt : (1 + y) / 2 + t * cbox x y ≤ s) :
    (1 + y) / 2 + t * cbox X ymin ≤ s := by
  have hmono := cbox_mono X x ymin y hX h8 hxX hy hymin hy1
  nlinarith

/-- With `X² > 8` and `0 ≤ y ≤ 1` one has `h₊ ≤ 1`. -/
theorem hbox_le_one (x y : ℝ) (h8 : 8 < x ^ 2) (hy0 : 0 ≤ y) (hy1 : y ≤ 1) :
    hbox x y ≤ 1 := by
  have hx2 : (0 : ℝ) < x ^ 2 := by linarith
  have h : 4 * y * (1 + y) / x ^ 2 ≤ 3 * y := by
    rw [div_le_iff₀ hx2]; nlinarith
  simp only [hbox]; linarith

/-- Derivative of the correction term `h/(2x²)` in `x`. -/
theorem hbox_div_hasDerivAt_x (x y : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun u => hbox u y / (2 * u ^ 2))
      (-(4 * y * (1 + y) / x ^ 5) - hbox x y / x ^ 3) x := by
  have hden : HasDerivAt (fun u : ℝ => 2 * u ^ 2) (4 * x) x := by
    have h := (hasDerivAt_pow 2 x).const_mul (2 : ℝ)
    convert h using 1; ring
  have hne : (2 : ℝ) * x ^ 2 ≠ 0 := by positivity
  have h := (hbox_hasDerivAt_x x y hx).div hden hne
  convert h using 1
  simp only [hbox]
  field_simp
  ring

/-- The derivative of `¼ log q(x)` is `1/(4x)`. -/
theorem log_qbox_hasDerivAt (x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun u => (1 / 4) * Real.log (qbox u)) (1 / (4 * x)) x := by
  have hpi : (0 : ℝ) < 4 * Real.pi := by positivity
  have h1 : HasDerivAt (fun u : ℝ => u / (4 * Real.pi)) (1 / (4 * Real.pi)) x := by
    simpa using (hasDerivAt_id x).div_const (4 * Real.pi)
  have h2 : HasDerivAt (fun u : ℝ => Real.log (u / (4 * Real.pi))) (1 / x) x := by
    have h := (Real.hasDerivAt_log (x := x / (4 * Real.pi)) (by positivity)).comp x h1
    convert h using 1
    field_simp
  have h3 := h2.const_mul (1 / 4 : ℝ)
  simp only [qbox]
  convert h3 using 1
  field_simp

/-- Where `h > 0`, the `x`-derivative of the correction term has absolute value at most
`1/x³ + 8/x⁵ ≤ 2/x³`. -/
theorem hbox_div_deriv_abs_le (x y : ℝ) (hx : 0 < x) (h8 : 8 < x ^ 2) (hy0 : 0 ≤ y)
    (hy1 : y ≤ 1) (hh : 0 < hbox x y) :
    |(-(4 * y * (1 + y) / x ^ 5) - hbox x y / x ^ 3)| ≤ 2 / x ^ 3 := by
  have hx5 : (0 : ℝ) < x ^ 5 := by positivity
  have hx3 : (0 : ℝ) < x ^ 3 := by positivity
  have e1 : 4 * y * (1 + y) / x ^ 5 ≤ 8 / x ^ 5 := by
    gcongr
    nlinarith
  have e2 : hbox x y / x ^ 3 ≤ 1 / x ^ 3 := by
    gcongr
    exact hbox_le_one x y h8 hy0 hy1
  have e3 : 8 / x ^ 5 ≤ 1 / x ^ 3 := by
    rw [div_le_div_iff₀ hx5 hx3]; nlinarith
  have e4 : (0 : ℝ) ≤ 4 * y * (1 + y) / x ^ 5 := by positivity
  have e5 : (0 : ℝ) ≤ hbox x y / x ^ 3 := div_nonneg hh.le hx3.le
  have e6 : (2 : ℝ) / x ^ 3 = 1 / x ^ 3 + 1 / x ^ 3 := by ring
  rw [abs_le]
  constructor <;> linarith

/-- In the region `h > 0`, `c` is differentiable in `x`. -/
theorem cbox_hasDerivAt_x_of_pos (x y : ℝ) (hx : 0 < x) (hh : 0 < hbox x y) :
    HasDerivAt (fun u => cbox u y)
      (1 / (4 * x) + (4 * y * (1 + y) / x ^ 5 + hbox x y / x ^ 3)) x := by
  have hcont : ContinuousAt (fun u => hbox u y) x := (hbox_hasDerivAt_x x y hx.ne').continuousAt
  have hev : ∀ᶠ u in nhds x, cbox u y = (1 / 4) * Real.log (qbox u) - hbox u y / (2 * u ^ 2) := by
    filter_upwards [continuousAt_const.eventually_lt hcont hh] with u hu
    simp [cbox, max_eq_left hu.le]
  have h := (log_qbox_hasDerivAt x hx).sub (hbox_div_hasDerivAt_x x y hx.ne')
  refine (h.congr_of_eventuallyEq hev).congr_deriv ?_
  ring

/-- In the region `h < 0`, `c` is differentiable in `x` with derivative `1/(4x)`. -/
theorem cbox_hasDerivAt_x_of_neg (x y : ℝ) (hx : 0 < x) (hh : hbox x y < 0) :
    HasDerivAt (fun u => cbox u y) (1 / (4 * x)) x := by
  have hcont : ContinuousAt (fun u => hbox u y) x := (hbox_hasDerivAt_x x y hx.ne').continuousAt
  have hev : ∀ᶠ u in nhds x, cbox u y = (1 / 4) * Real.log (qbox u) := by
    filter_upwards [hcont.eventually_lt continuousAt_const hh] with u hu
    simp [cbox, max_eq_right hu.le]
  exact (log_qbox_hasDerivAt x hx).congr_of_eventuallyEq hev

/-- **Quantitative `c_x > 0`.** Under `X² > 8` and the gate `1/(4(X+1)) - 2/X³ > 0`, at every
point of the spatial box away from the positive-part kink, `c` is differentiable in `x`, its
derivative differs from `1/(4x)` by at most `2/x³`, and it is at least
`1/(4(X+1)) - 2/X³ > 0`. -/
theorem cbox_deriv_x_pos (X x y : ℝ) (hX : 0 < X) (h8 : 8 < X ^ 2)
    (hgate : 0 < 1 / (4 * (X + 1)) - 2 / X ^ 3) (hx1 : X ≤ x) (hx2 : x ≤ X + 1)
    (hy0 : 0 ≤ y) (hy1 : y ≤ 1) (hne : hbox x y ≠ 0) :
    ∃ d : ℝ, HasDerivAt (fun u => cbox u y) d x ∧ |d - 1 / (4 * x)| ≤ 2 / x ^ 3 ∧
      1 / (4 * (X + 1)) - 2 / X ^ 3 ≤ d ∧ 0 < d := by
  have hx0 : 0 < x := lt_of_lt_of_le hX hx1
  have h8x : 8 < x ^ 2 := lt_of_lt_of_le h8 (by nlinarith)
  have hpos3 : (0 : ℝ) < 2 / X ^ 3 := by positivity
  have hpos3' : (0 : ℝ) < 2 / x ^ 3 := by positivity
  have hbase : 1 / (4 * (X + 1)) ≤ 1 / (4 * x) := by
    apply one_div_le_one_div_of_le (by positivity)
    linarith
  rcases lt_or_gt_of_ne hne with hneg | hpos
  · refine ⟨1 / (4 * x), cbox_hasDerivAt_x_of_neg x y hx0 hneg, ?_, by linarith, ?_⟩
    · simpa using hpos3'.le
    · have : 0 < 1 / (4 * x) := by positivity
      linarith
  · refine ⟨1 / (4 * x) + (4 * y * (1 + y) / x ^ 5 + hbox x y / x ^ 3),
      cbox_hasDerivAt_x_of_pos x y hx0 hpos, ?_, ?_, ?_⟩
    · have habs := hbox_div_deriv_abs_le x y hx0 h8x hy0 hy1 hpos
      have heq : 1 / (4 * x) + (4 * y * (1 + y) / x ^ 5 + hbox x y / x ^ 3) - 1 / (4 * x)
          = -(-(4 * y * (1 + y) / x ^ 5) - hbox x y / x ^ 3) := by ring
      rw [heq, abs_neg]
      exact habs
    · have h1 : (0 : ℝ) ≤ 4 * y * (1 + y) / x ^ 5 := by positivity
      have h2 : (0 : ℝ) ≤ hbox x y / x ^ 3 := div_nonneg hpos.le (by positivity)
      linarith
    · have h1 : (0 : ℝ) ≤ 4 * y * (1 + y) / x ^ 5 := by positivity
      have h2 : (0 : ℝ) ≤ hbox x y / x ^ 3 := div_nonneg hpos.le (by positivity)
      have h3 : (0 : ℝ) < 1 / (4 * x) := by positivity
      linarith

/-! ## Lemma 2: the `A`-core `y`-slope gate -/

/-- The logarithmic upper-right `y`-derivative majorant
`η(x,t,n) = 0.02 - ½ log q(x) + t log N /(2(x-6)) + ½ log n`. -/
noncomputable def eta (x t n N : ℝ) : ℝ :=
  0.02 - (1 / 2) * Real.log (qbox x) + t * Real.log N / (2 * (x - 6)) + (1 / 2) * Real.log n

/-- **Lemma 2.** For `n ≤ N`, `x ≥ X > 6` and `0 ≤ t ≤ t₀`, the slope `η` is bounded by its
corner value. -/
theorem eta_le_corner (X x t t₀ n N : ℝ) (hX6 : 6 < X) (hxX : X ≤ x) (ht : 0 ≤ t)
    (htt₀ : t ≤ t₀) (hn1 : 1 ≤ n) (hnN : n ≤ N) (hN : 1 ≤ N) :
    eta x t n N ≤
      0.02 - (1 / 2) * Real.log (qbox X) + t₀ * Real.log N / (2 * (X - 6))
        + (1 / 2) * Real.log N := by
  have hlogN : 0 ≤ Real.log N := Real.log_nonneg hN
  have h1 : 0 < 2 * (X - 6) := by linarith
  have h2 : 0 ≤ t * Real.log N := mul_nonneg ht hlogN
  have hq := log_qbox_mono X x (by linarith) hxX
  have hn : Real.log n ≤ Real.log N := Real.log_le_log (by linarith) hnN
  have hmid : t * Real.log N / (2 * (x - 6)) ≤ t₀ * Real.log N / (2 * (X - 6)) := by
    gcongr
    exact mul_nonneg (ht.trans htt₀) hlogN
  simp only [eta]
  linarith

/-! ## Lemma 3: certified discrete-sum majorant -/

/-- **Head-plus-integral bound.** If `F` is nonincreasing on `[K, N]` then the full discrete sum
is bounded by the head sum up to `K` plus the integral over `[K, N]`. -/
theorem sum_le_head_add_integral (K N : ℕ) (F : ℝ → ℝ) (hKN : K ≤ N)
    (hanti : AntitoneOn F (Set.Icc (K : ℝ) (N : ℝ))) :
    ∑ n ∈ Finset.Icc 1 N, F n ≤ ∑ n ∈ Finset.Icc 1 K, F n + ∫ u in (K : ℝ)..(N : ℝ), F u := by
  have hcast : (K : ℝ) + ((N - K : ℕ) : ℝ) = (N : ℝ) := by
    rw [Nat.cast_sub hKN]; ring
  have hanti' : AntitoneOn F (Set.Icc (K : ℝ) ((K : ℝ) + ((N - K : ℕ) : ℝ))) := by
    rw [hcast]; exact hanti
  have key := hanti'.sum_le_integral
  rw [hcast] at key
  have hsplit : ∑ n ∈ Finset.Icc 1 N, F n
      = ∑ n ∈ Finset.Icc 1 K, F n + ∑ n ∈ Finset.Ioc K N, F n := by
    rw [← Finset.sum_union]
    · congr 1
      ext m
      simp only [Finset.mem_Icc, Finset.mem_Ioc, Finset.mem_union]
      omega
    · rw [Finset.disjoint_left]
      intro m hm hm'
      simp only [Finset.mem_Icc, Finset.mem_Ioc] at hm hm'
      omega
  have hIoc : ∑ n ∈ Finset.Ioc K N, (F n : ℝ)
      = ∑ i ∈ Finset.range (N - K), F ((K : ℝ) + ((i + 1 : ℕ) : ℝ)) := by
    have h : Finset.Ioc K N = Finset.Ico (K + 1) (N + 1) := by
      ext m; simp only [Finset.mem_Ioc, Finset.mem_Ico]; omega
    rw [h, Finset.sum_Ico_eq_sum_range]
    simp only [Nat.add_sub_add_right]
    refine Finset.sum_congr rfl fun i _ => ?_
    push_cast
    ring_nf
  rw [hsplit, hIoc]
  linarith

/-- The exponent slope `p(r) = -(1+y_min)/2 + t(r/2 - c₀)`. -/
noncomputable def pslope (ymin t c₀ r : ℝ) : ℝ := -(1 + ymin) / 2 + t * (r / 2 - c₀)

/-- The tail power `P(u) = u^{-(1+y_min)/2 + t(log u/4 - c₀)}`. -/
noncomputable def Pfun (ymin t c₀ u : ℝ) : ℝ :=
  u ^ (-(1 + ymin) / 2 + t * (Real.log u / 4 - c₀))

/-- The bracket `B(r) = r (C - r/4)` of the time derivative. -/
noncomputable def Bfun (C r : ℝ) : ℝ := r * (C - r / 4)

/-- First gate: `c₀ > ½ log N` and `t ≥ 0`, `r ≤ log N` give `p(r) ≤ -(1+y_min)/2`. -/
theorem pslope_le (ymin t c₀ r N : ℝ) (ht : 0 ≤ t) (hr : r ≤ Real.log N)
    (hc₀ : Real.log N / 2 < c₀) :
    pslope ymin t c₀ r ≤ -(1 + ymin) / 2 := by
  have h : r / 2 - c₀ ≤ 0 := by linarith
  have h' := mul_nonpos_of_nonneg_of_nonpos ht h
  simp only [pslope]; linarith

/-- Every logarithmic `r`-derivative occurring in the spatial sum, namely `p + 1/r`,
`p + y_min + 1/r` and `p + y_min`, is at most `(y_min - 1)/2 + 1/log K`. -/
theorem logderiv_le (ymin t c₀ r N K s : ℝ) (ht : 0 ≤ t) (hr : r ≤ Real.log N)
    (hc₀ : Real.log N / 2 < c₀) (hK : 0 < Real.log K) (hrK : Real.log K ≤ r)
    (hs : s ≤ ymin) :
    pslope ymin t c₀ r + s + 1 / r ≤ (ymin - 1) / 2 + 1 / Real.log K := by
  have h1 := pslope_le ymin t c₀ r N ht hr hc₀
  have h2 : 1 / r ≤ 1 / Real.log K := one_div_le_one_div_of_le hK hrK
  linarith

/-- Second gate: `(y_min - 1)/2 + 1/log K < 0` makes all those logarithmic derivatives strictly
negative. -/
theorem logderiv_neg (ymin t c₀ r N K s : ℝ) (ht : 0 ≤ t) (hr : r ≤ Real.log N)
    (hc₀ : Real.log N / 2 < c₀) (hK : 0 < Real.log K) (hrK : Real.log K ≤ r)
    (hs : s ≤ ymin) (hgate : (ymin - 1) / 2 + 1 / Real.log K < 0) :
    pslope ymin t c₀ r + s + 1 / r < 0 :=
  lt_of_le_of_lt (logderiv_le ymin t c₀ r N K s ht hr hc₀ hK hrK hs) hgate

/-- Under the gate `C > log N / 4`, the bracket `B` is positive on the tail. -/
theorem Bfun_pos (C r N : ℝ) (hr : 0 < r) (hrN : r ≤ Real.log N) (hC : Real.log N / 4 < C) :
    0 < Bfun C r := by
  have h : 0 < C - r / 4 := by linarith
  simp only [Bfun]
  positivity

/-- Derivative of `B`. -/
theorem Bfun_hasDerivAt (C r : ℝ) : HasDerivAt (Bfun C) (C - r / 2) r := by
  have h : HasDerivAt (fun u : ℝ => u * (C - u / 4)) (1 * (C - r / 4) + r * (-(1 / 4))) r :=
    (hasDerivAt_id r).mul (((hasDerivAt_id r).div_const 4).const_sub C)
  exact h.congr_deriv (by ring)

/-- The logarithmic derivative of `B` is at most `1/r`. -/
theorem Bfun_logDeriv_le (C r N : ℝ) (hr : 0 < r) (hrN : r ≤ Real.log N)
    (hC : Real.log N / 4 < C) :
    (C - r / 2) / Bfun C r ≤ 1 / r := by
  have hB : 0 < Bfun C r := Bfun_pos C r N hr hrN hC
  rw [div_le_div_iff₀ hB hr]
  simp only [Bfun]
  nlinarith

/-- A function with a nonpositive derivative on a closed interval is nonincreasing there. -/
theorem antitoneOn_Icc_of_hasDerivAt {f f' : ℝ → ℝ} {a b : ℝ}
    (hderiv : ∀ x ∈ Set.Icc a b, HasDerivAt f (f' x) x)
    (hnonpos : ∀ x ∈ Set.Icc a b, f' x ≤ 0) : AntitoneOn f (Set.Icc a b) := by
  refine antitoneOn_of_deriv_nonpos (convex_Icc a b)
    (fun x hx => (hderiv x hx).continuousAt.continuousWithinAt) ?_ ?_
  · intro x hx
    rw [interior_Icc] at hx
    exact ((hderiv x ⟨hx.1.le, hx.2.le⟩).differentiableAt).differentiableWithinAt
  · intro x hx
    rw [interior_Icc] at hx
    rw [(hderiv x ⟨hx.1.le, hx.2.le⟩).deriv]
    exact hnonpos x ⟨hx.1.le, hx.2.le⟩

/-- The `r`-derivative of the logarithm of `P(u) u^s`, written in the variable `r = log u`,
is `p(r) + s`. -/
theorem core_hasDerivAt (ymin t c₀ s r : ℝ) :
    HasDerivAt (fun z => (-(1 + ymin) / 2 + t * (z / 4 - c₀)) * z + s * z)
      (pslope ymin t c₀ r + s) r := by
  have h1 : HasDerivAt (fun z : ℝ => -(1 + ymin) / 2 + t * (z / 4 - c₀)) (t * (1 / 4)) r := by
    have h := (((hasDerivAt_id r).div_const 4).sub_const c₀).const_mul t
    simpa using h.const_add (-(1 + ymin) / 2)
  have h2 := (h1.mul (hasDerivAt_id r)).add ((hasDerivAt_id r).const_mul s)
  simp only [id] at h2
  refine h2.congr_deriv ?_
  simp only [pslope]
  ring

/-- Transfer of antitonicity in `r = log u` to antitonicity in `u`. -/
theorem antitoneOn_exp_comp_log {E : ℝ → ℝ} {K N : ℝ} (hK : 1 < K)
    (hE : AntitoneOn E (Set.Icc (Real.log K) (Real.log N))) :
    AntitoneOn (fun u => Real.exp (E (Real.log u))) (Set.Icc K N) := by
  intro u hu v hv huv
  have hu0 : (0 : ℝ) < u := lt_of_lt_of_le (by linarith) hu.1
  have hv0 : (0 : ℝ) < v := lt_of_lt_of_le (by linarith) hv.1
  have h1 : Real.log u ∈ Set.Icc (Real.log K) (Real.log N) :=
    ⟨Real.log_le_log (by linarith) hu.1, Real.log_le_log hu0 hu.2⟩
  have h2 : Real.log v ∈ Set.Icc (Real.log K) (Real.log N) :=
    ⟨Real.log_le_log (by linarith) hv.1, Real.log_le_log hv0 hv.2⟩
  exact Real.exp_le_exp.2 (hE h1 h2 (Real.log_le_log hu0 huv))

/-- **Decrease of the spatial summands.** For `s ≤ y_min`, the function
`u ↦ P(u) u^s log u` is nonincreasing on `[K, N]` under the two gates. -/
theorem Pfun_mul_log_antitoneOn (ymin t c₀ K N s : ℝ) (ht : 0 ≤ t) (hK : 1 < K)
    (hc₀ : Real.log N / 2 < c₀) (hs : s ≤ ymin)
    (hgate : (ymin - 1) / 2 + 1 / Real.log K < 0) :
    AntitoneOn (fun u => Pfun ymin t c₀ u * u ^ s * Real.log u) (Set.Icc K N) := by
  have hK0 : 0 < Real.log K := Real.log_pos hK
  have hE : AntitoneOn (fun r => (-(1 + ymin) / 2 + t * (r / 4 - c₀)) * r + s * r + Real.log r)
      (Set.Icc (Real.log K) (Real.log N)) := by
    refine antitoneOn_Icc_of_hasDerivAt (f' := fun r => pslope ymin t c₀ r + s + 1 / r) ?_ ?_
    · intro r hr
      have hr0 : 0 < r := lt_of_lt_of_le hK0 hr.1
      exact (core_hasDerivAt ymin t c₀ s r).add
        ((Real.hasDerivAt_log hr0.ne').congr_deriv (one_div r).symm)
    · intro r hr
      exact le_of_lt (logderiv_neg ymin t c₀ r N K s ht hr.2 hc₀ hK0 hr.1 hs hgate)
  refine (antitoneOn_exp_comp_log hK hE).congr ?_
  intro u hu
  have hu1 : 1 < u := lt_of_lt_of_le hK hu.1
  have hu0 : 0 < u := by linarith
  have hlu : 0 < Real.log u := Real.log_pos hu1
  simp only [Pfun, Real.exp_add, Real.exp_log hlu, Real.rpow_def_of_pos hu0]
  ring_nf

/-- **Decrease of the pure power summand** `u ↦ P(u) u^s` on `[K, N]`. -/
theorem Pfun_mul_rpow_antitoneOn (ymin t c₀ K N s : ℝ) (ht : 0 ≤ t) (hK : 1 < K)
    (hc₀ : Real.log N / 2 < c₀) (hs : s ≤ ymin)
    (hgate : (ymin - 1) / 2 + 1 / Real.log K < 0) :
    AntitoneOn (fun u => Pfun ymin t c₀ u * u ^ s) (Set.Icc K N) := by
  have hK0 : 0 < Real.log K := Real.log_pos hK
  have hE : AntitoneOn (fun r => (-(1 + ymin) / 2 + t * (r / 4 - c₀)) * r + s * r)
      (Set.Icc (Real.log K) (Real.log N)) := by
    refine antitoneOn_Icc_of_hasDerivAt (f' := fun r => pslope ymin t c₀ r + s) ?_ ?_
    · intro r _
      exact core_hasDerivAt ymin t c₀ s r
    · intro r hr
      have hr0 : 0 < r := lt_of_lt_of_le hK0 hr.1
      have hneg := logderiv_neg ymin t c₀ r N K s ht hr.2 hc₀ hK0 hr.1 hs hgate
      have : 0 < 1 / r := by positivity
      linarith
  refine (antitoneOn_exp_comp_log hK hE).congr ?_
  intro u hu
  have hu1 : 1 < u := lt_of_lt_of_le hK hu.1
  have hu0 : 0 < u := by linarith
  simp only [Pfun, Real.exp_add, Real.rpow_def_of_pos hu0]
  ring_nf

/-- **Decrease of the time-derivative summands** `u ↦ P(u) u^s B(log u)` on `[K, N]`. -/
theorem Pfun_mul_B_antitoneOn (ymin t c₀ C K N s : ℝ) (ht : 0 ≤ t) (hK : 1 < K)
    (hc₀ : Real.log N / 2 < c₀) (hs : s ≤ ymin)
    (hC : Real.log N / 4 < C) (hgate : (ymin - 1) / 2 + 1 / Real.log K < 0) :
    AntitoneOn (fun u => Pfun ymin t c₀ u * u ^ s * Bfun C (Real.log u)) (Set.Icc K N) := by
  have hK0 : 0 < Real.log K := Real.log_pos hK
  have hE : AntitoneOn
      (fun r => (-(1 + ymin) / 2 + t * (r / 4 - c₀)) * r + s * r + Real.log (Bfun C r))
      (Set.Icc (Real.log K) (Real.log N)) := by
    refine antitoneOn_Icc_of_hasDerivAt
      (f' := fun r => pslope ymin t c₀ r + s + (C - r / 2) / Bfun C r) ?_ ?_
    · intro r hr
      have hr0 : 0 < r := lt_of_lt_of_le hK0 hr.1
      have hB : 0 < Bfun C r := Bfun_pos C r N hr0 hr.2 hC
      have hlogB : HasDerivAt (fun z => Real.log (Bfun C z)) ((C - r / 2) / Bfun C r) r := by
        have h := (Real.hasDerivAt_log hB.ne').comp r (Bfun_hasDerivAt C r)
        exact h.congr_deriv (by field_simp)
      exact (core_hasDerivAt ymin t c₀ s r).add hlogB
    · intro r hr
      have hr0 : 0 < r := lt_of_lt_of_le hK0 hr.1
      have hneg := logderiv_neg ymin t c₀ r N K s ht hr.2 hc₀ hK0 hr.1 hs hgate
      have hBd := Bfun_logDeriv_le C r N hr0 hr.2 hC
      linarith
  refine (antitoneOn_exp_comp_log hK hE).congr ?_
  intro u hu
  have hu1 : 1 < u := lt_of_lt_of_le hK hu.1
  have hu0 : 0 < u := by linarith
  have hlu : 0 < Real.log u := Real.log_pos hu1
  have hB : 0 < Bfun C (Real.log u) := by
    refine Bfun_pos C (Real.log u) N hlu ?_ hC
    exact Real.log_le_log hu0 hu.2
  simp only [Pfun, Real.exp_add, Real.exp_log hB, Real.rpow_def_of_pos hu0]
  ring_nf

/-- A nonnegative multiple of a nonincreasing function is nonincreasing. -/
theorem antitoneOn_const_mul_nonneg {f : ℝ → ℝ} {S : Set ℝ} {c : ℝ} (hc : 0 ≤ c)
    (h : AntitoneOn f S) : AntitoneOn (fun x => c * f x) S :=
  fun _ ha _ hb hab => mul_le_mul_of_nonneg_left (h ha hb hab) hc

/-- **Lemma 3, packaged.** Under the two gates, a nonnegative linear combination of the three
spatial-derivative summands `P(u) log u`, `P(u) u^{y_min} log u`, `P(u) u^{y_min}` satisfies the
head-plus-integral bound. -/
theorem spatial_sum_le_head_add_integral (ymin t c₀ α β γ : ℝ) (K N : ℕ) (hK : 1 < (K : ℝ))
    (hKN : K ≤ N) (ht : 0 ≤ t) (hc₀ : Real.log N / 2 < c₀) (hymin : 0 ≤ ymin)
    (hgate : (ymin - 1) / 2 + 1 / Real.log K < 0)
    (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ) :
    ∑ n ∈ Finset.Icc 1 N,
        (α * (Pfun ymin t c₀ n * Real.log n) + β * (Pfun ymin t c₀ n * (n : ℝ) ^ ymin * Real.log n)
          + γ * (Pfun ymin t c₀ n * (n : ℝ) ^ ymin))
      ≤ ∑ n ∈ Finset.Icc 1 K,
          (α * (Pfun ymin t c₀ n * Real.log n)
            + β * (Pfun ymin t c₀ n * (n : ℝ) ^ ymin * Real.log n)
            + γ * (Pfun ymin t c₀ n * (n : ℝ) ^ ymin))
        + ∫ u in (K : ℝ)..(N : ℝ),
            (α * (Pfun ymin t c₀ u * Real.log u) + β * (Pfun ymin t c₀ u * u ^ ymin * Real.log u)
              + γ * (Pfun ymin t c₀ u * u ^ ymin)) := by
  refine sum_le_head_add_integral K N
    (fun u => α * (Pfun ymin t c₀ u * Real.log u) + β * (Pfun ymin t c₀ u * u ^ ymin * Real.log u)
      + γ * (Pfun ymin t c₀ u * u ^ ymin)) hKN ?_
  have h1 : AntitoneOn (fun u : ℝ => Pfun ymin t c₀ u * Real.log u) (Set.Icc (K : ℝ) (N : ℝ)) := by
    refine (Pfun_mul_log_antitoneOn ymin t c₀ K N 0 ht hK hc₀ hymin hgate).congr ?_
    intro u hu
    have hu0 : (0 : ℝ) < u := lt_of_lt_of_le (by linarith) hu.1
    simp [Real.rpow_zero]
  have h2 : AntitoneOn (fun u : ℝ => Pfun ymin t c₀ u * u ^ ymin * Real.log u)
      (Set.Icc (K : ℝ) (N : ℝ)) :=
    Pfun_mul_log_antitoneOn ymin t c₀ K N ymin ht hK hc₀ le_rfl hgate
  have h3 : AntitoneOn (fun u : ℝ => Pfun ymin t c₀ u * u ^ ymin) (Set.Icc (K : ℝ) (N : ℝ)) :=
    Pfun_mul_rpow_antitoneOn ymin t c₀ K N ymin ht hK hc₀ le_rfl hgate
  exact ((antitoneOn_const_mul_nonneg hα h1).add (antitoneOn_const_mul_nonneg hβ h2)).add
    (antitoneOn_const_mul_nonneg hγ h3)

/-! ## Lemma 4: holomorphic quadrature contract -/

/-- On a complex ball `B(u₀, ρ)` with `0 < u₀` real and `ρ ≤ u₀`, all points have positive
real part, hence `N z` avoids the branch cut `(-∞, 0]`.

The hypothesis `0 < u₀` is kept because it is part of the source statement; the proof only uses
`ρ ≤ u₀` (which, for a nonempty ball, already forces `0 < u₀`). -/
theorem mem_slitPlane_of_mem_ball (N u₀ ρ : ℝ) (hN : 0 < N) (hu₀ : 0 < u₀) (hρ : ρ ≤ u₀)
    (z : ℂ) (hz : z ∈ Metric.ball (u₀ : ℂ) ρ) : (N : ℂ) * z ∈ Complex.slitPlane := by
  have h1 : |z.re - u₀| ≤ ‖z - (u₀ : ℂ)‖ := by
    simpa using Complex.abs_re_le_norm (z - (u₀ : ℂ))
  have h2 : ‖z - (u₀ : ℂ)‖ < ρ := by
    simpa [Complex.dist_eq] using hz
  have h3 : 0 < z.re := by
    have h4 := abs_lt.mp (lt_of_le_of_lt h1 h2)
    linarith [h4.1]
  left
  simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  positivity

/-- `z ↦ log (N z)` is holomorphic on any ball `B(u₀, ρ)` with `0 < u₀` real, `ρ ≤ u₀`. -/
theorem clog_differentiableOn_ball (N u₀ ρ : ℝ) (hN : 0 < N) (hu₀ : 0 < u₀) (hρ : ρ ≤ u₀) :
    DifferentiableOn ℂ (fun z => Complex.log ((N : ℂ) * z)) (Metric.ball (u₀ : ℂ) ρ) := by
  intro z hz
  have hmem := mem_slitPlane_of_mem_ball N u₀ ρ hN hu₀ hρ z hz
  exact ((Complex.differentiableAt_log hmem).comp z
    (differentiableAt_id.const_mul _)).differentiableWithinAt

/-- `z ↦ (N z)^α` is holomorphic on any ball `B(u₀, ρ)` with `0 < u₀` real, `ρ ≤ u₀`. -/
theorem cpow_differentiableOn_ball (α : ℂ) (N u₀ ρ : ℝ) (hN : 0 < N) (hu₀ : 0 < u₀)
    (hρ : ρ ≤ u₀) :
    DifferentiableOn ℂ (fun z => ((N : ℂ) * z) ^ α) (Metric.ball (u₀ : ℂ) ρ) := by
  intro z hz
  have hmem := mem_slitPlane_of_mem_ball N u₀ ρ hN hu₀ hρ z hz
  have h1 : DifferentiableAt ℂ (fun w : ℂ => w ^ α) ((N : ℂ) * z) :=
    ((Complex.hasStrictDerivAt_cpow_const hmem).hasDerivAt).differentiableAt
  exact (h1.comp z (differentiableAt_id.const_mul _)).differentiableWithinAt

/-- The same functions are analytic (holomorphic in the strong sense) on the ball. -/
theorem clog_analyticOnNhd_ball (N u₀ ρ : ℝ) (hN : 0 < N) (hu₀ : 0 < u₀) (hρ : ρ ≤ u₀) :
    AnalyticOnNhd ℂ (fun z => Complex.log ((N : ℂ) * z)) (Metric.ball (u₀ : ℂ) ρ) :=
  (clog_differentiableOn_ball N u₀ ρ hN hu₀ hρ).analyticOnNhd Metric.isOpen_ball

/-- The implementation's change of variables: integrating from `K/N` to `1` and multiplying by
`N` reproduces `∫_K^N F`. -/
theorem integral_change_of_variables (K N : ℝ) (hN : 0 < N) (F : ℝ → ℝ) :
    (∫ v in (K / N)..(1 : ℝ), N * F (N * v)) = ∫ u in K..N, F u := by
  have h := intervalIntegral.smul_integral_comp_mul_left (a := K / N) (b := 1) F N
  simp only [smul_eq_mul] at h
  rw [mul_div_cancel₀ _ (ne_of_gt hN), mul_one] at h
  rw [← h, intervalIntegral.integral_const_mul]

/-! ## Lemma 5: convex-disk boundary homotopy -/

/-- **Left half of a subedge.** If the true image `F` is `D_z h`-Lipschitz on `[0,1]` then, for
`0 ≤ s ≤ 1/2`, both `F s` and the chord point `P s` lie in the closed disk of radius `D_z h / 2`
around `F 0`. -/
theorem chord_disk_left (F : ℝ → ℂ) (Dz hlen s : ℝ)
    (hlip : ∀ a ∈ Set.Icc (0 : ℝ) 1, ∀ b ∈ Set.Icc (0 : ℝ) 1, ‖F a - F b‖ ≤ Dz * hlen * |a - b|)
    (hs0 : 0 ≤ s) (hs : s ≤ 1 / 2) :
    F s ∈ Metric.closedBall (F 0) (Dz * hlen / 2) ∧
      ((1 - s) • F 0 + s • F 1) ∈ Metric.closedBall (F 0) (Dz * hlen / 2) := by
  have hs1 : s ≤ 1 := by linarith
  have hmem : s ∈ Set.Icc (0 : ℝ) 1 := ⟨hs0, hs1⟩
  have h0 : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨le_rfl, by norm_num⟩
  have h1 : (1 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨by norm_num, le_rfl⟩
  have hb := hlip 1 h1 0 h0
  rw [show |(1 : ℝ) - 0| = 1 by norm_num, mul_one] at hb
  have hD : 0 ≤ Dz * hlen := le_trans (norm_nonneg _) hb
  refine ⟨?_, ?_⟩
  · rw [Metric.mem_closedBall, Complex.dist_eq]
    have h := hlip s hmem 0 h0
    rw [show |s - 0| = s by rw [sub_zero, abs_of_nonneg hs0]] at h
    nlinarith
  · rw [Metric.mem_closedBall, Complex.dist_eq]
    have heq : (1 - s) • F 0 + s • F 1 - F 0 = s • (F 1 - F 0) := by
      simp [smul_sub, sub_smul]; ring
    rw [heq, norm_smul, Real.norm_eq_abs, abs_of_nonneg hs0]
    nlinarith [norm_nonneg (F 1 - F 0)]

/-- **Right half of a subedge**, symmetric statement about `F 1`. -/
theorem chord_disk_right (F : ℝ → ℂ) (Dz hlen s : ℝ)
    (hlip : ∀ a ∈ Set.Icc (0 : ℝ) 1, ∀ b ∈ Set.Icc (0 : ℝ) 1, ‖F a - F b‖ ≤ Dz * hlen * |a - b|)
    (hs : 1 / 2 ≤ s) (hs1 : s ≤ 1) :
    F s ∈ Metric.closedBall (F 1) (Dz * hlen / 2) ∧
      ((1 - s) • F 0 + s • F 1) ∈ Metric.closedBall (F 1) (Dz * hlen / 2) := by
  have hs0 : 0 ≤ s := by linarith
  have hmem : s ∈ Set.Icc (0 : ℝ) 1 := ⟨hs0, hs1⟩
  have h0 : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨le_rfl, by norm_num⟩
  have h1 : (1 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨by norm_num, le_rfl⟩
  have hb := hlip 0 h0 1 h1
  rw [show |(0 : ℝ) - 1| = 1 by norm_num, mul_one] at hb
  have hD : 0 ≤ Dz * hlen := le_trans (norm_nonneg _) hb
  refine ⟨?_, ?_⟩
  · rw [Metric.mem_closedBall, Complex.dist_eq]
    have h := hlip s hmem 1 h1
    rw [show |s - 1| = 1 - s by rw [abs_of_nonpos (by linarith)]; ring] at h
    nlinarith
  · rw [Metric.mem_closedBall, Complex.dist_eq]
    have heq : (1 - s) • F 0 + s • F 1 - F 1 = (1 - s) • (F 0 - F 1) := by
      simp [smul_sub, sub_smul]; ring
    rw [heq, norm_smul, Real.norm_eq_abs, abs_of_nonneg (by linarith : (0:ℝ) ≤ 1 - s)]
    nlinarith [norm_nonneg (F 0 - F 1)]

/-- **The straight-line homotopy stays in the disk** (convexity of a disk). -/
theorem homotopy_mem_disk (c z w : ℂ) (R θ : ℝ) (hz : z ∈ Metric.closedBall c R)
    (hw : w ∈ Metric.closedBall c R) (hθ0 : 0 ≤ θ) (hθ1 : θ ≤ 1) :
    (1 - θ) • z + θ • w ∈ Metric.closedBall c R :=
  (convex_closedBall c R) hz hw (by linarith) hθ0 (by ring)

/-- **Enlarged radius.** Adding the certified time motion `D_t (t_{i+1} - t_i)` and the
`H_t/B_t`-approximation error `0.00125 = 1/800` enlarges the disk radius accordingly. -/
theorem enlarged_disk (c z g : ℂ) (Dz hlen Dt t₁ t₂ : ℝ)
    (hz : z ∈ Metric.closedBall c (Dz * hlen / 2))
    (hg : ‖g - z‖ ≤ Dt * (t₂ - t₁) + 1 / 800) :
    g ∈ Metric.closedBall c (Dz * hlen / 2 + Dt * (t₂ - t₁) + 1 / 800) := by
  rw [Metric.mem_closedBall, Complex.dist_eq] at hz ⊢
  have h : ‖g - c‖ ≤ ‖g - z‖ + ‖z - c‖ := by
    simpa using norm_sub_le_norm_sub_add_norm_sub g z c
  linarith

/-- **Zero exclusion (strict prism predicate).** If the enlarged radius is smaller than the
modulus of the disk centre, the disk excludes zero. -/
theorem zero_not_mem_closedBall (c z : ℂ) (R : ℝ) (hR : R < ‖c‖)
    (hz : z ∈ Metric.closedBall c R) : z ≠ 0 := by
  rintro rfl
  rw [Metric.mem_closedBall, Complex.dist_eq, zero_sub, norm_neg] at hz
  linarith

/-- **Packaged prism statement.** Under the strict radius inequality, the whole spatial, time and
approximation homotopy is zero-avoiding on the left half of a subedge. -/
theorem prism_zero_free (F : ℝ → ℂ) (Dz hlen Dt t₁ t₂ : ℝ)
    (hlip : ∀ a ∈ Set.Icc (0 : ℝ) 1, ∀ b ∈ Set.Icc (0 : ℝ) 1, ‖F a - F b‖ ≤ Dz * hlen * |a - b|)
    (hstrict : Dz * hlen / 2 + Dt * (t₂ - t₁) + 1 / 800 < ‖F 0‖)
    (s θ : ℝ) (hs0 : 0 ≤ s) (hs : s ≤ 1 / 2) (hθ0 : 0 ≤ θ) (hθ1 : θ ≤ 1)
    (g : ℂ) (hg : ‖g - ((1 - θ) • F s + θ • ((1 - s) • F 0 + s • F 1))‖
      ≤ Dt * (t₂ - t₁) + 1 / 800) :
    g ≠ 0 := by
  obtain ⟨hF, hP⟩ := chord_disk_left F Dz hlen s hlip hs0 hs
  have hhom := homotopy_mem_disk (F 0) (F s) ((1 - s) • F 0 + s • F 1) (Dz * hlen / 2) θ hF hP hθ0 hθ1
  have hgb := enlarged_disk (F 0) _ g Dz hlen Dt t₁ t₂ hhom hg
  exact zero_not_mem_closedBall (F 0) g _ hstrict hgb

end DerivativeBox
