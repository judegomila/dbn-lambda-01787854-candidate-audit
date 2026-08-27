import Mathlib

/-!
# A kernel-checked instance of the `e_{C,0}` error-budget certificate

Fixed exact parameters: `N₀ = 690988`, `t ∈ [t₀, t₁]` with `t₀ = 129/800` and
`t₁ = 161250001/10^9`, `y₀ = sqrt (87677/2500000)`, `y_max = sqrt (271/400)`.

For `t ∈ [t₀, t₁]` we set `x t = 4π (N₀² - t/16)` and `L t = log (x t / (4π)) = log (N₀² - t/16)`,
and

`e_{C,0}(t,y) = exp (-(1+y)/4 * L t - t/16 * (L t)^2
    + 31/25 * (3^y + 3^(-y)) / (N₀ - 1/8)
    + (3 * sqrt ((L t)^2 + π²/4) + 21/2) / (x t - 12))`.

The main results are

* `EC0.eC0_le_sharp` : `e_{C,0}(t,y) ≤ 233492848188649183/10^24` on the box;
* `EC0.eC0_le_weak`  : `e_{C,0}(t,y) ≤ 234/10^9` on the box.

All numeric steps are rigorous rational enclosures: two-sided rational bounds on `log`,
`exp`, `sqrt` and `π` obtained from mathlib's certified constants together with exact
integer arithmetic.

Remark on the informal proof guidance accompanying the statement: the suggested enclosure
`26.98 < L < 26.99` is not correct; in fact `L = log (690988² - t/16) = 26.8917554...`
on the box. The certified lower bound `L ≥ 2689175546/10^8` used below reflects the true
value. The bound is also genuinely tight: the maximum of `e_{C,0}` over the box is
`≈ 2.3349249936·10⁻⁷`, only a relative `1.5·10⁻⁶` below the target constant
`2.33492848188649183·10⁻⁷`, so the `y`-dependence has to be treated by an honest
monotonicity argument rather than by bounding the two `y`-dependent terms separately.
-/

namespace EC0

open Real

set_option exponentiation.threshold 40000
set_option maxRecDepth 20000

/-- The fixed parameter `N₀ = 690988`. -/
def N0 : ℝ := 690988

/-- Left endpoint of the `t`-interval. -/
noncomputable def t0 : ℝ := 129 / 800

/-- Right endpoint of the `t`-interval. -/
noncomputable def t1 : ℝ := 161250001 / 10 ^ 9

/-- Left endpoint of the `y`-interval, `y₀ = sqrt (87677/2500000)`. -/
noncomputable def y0 : ℝ := Real.sqrt (87677 / 2500000)

/-- Right endpoint of the `y`-interval, `y_max = sqrt (271/400)`. -/
noncomputable def ymax : ℝ := Real.sqrt (271 / 400)

/-- `x t = 4π (N₀² - t/16)`. -/
noncomputable def xf (t : ℝ) : ℝ := 4 * Real.pi * (N0 ^ 2 - t / 16)

/-- `L t = log (x t / (4π)) = log (N₀² - t/16)`. -/
noncomputable def Lf (t : ℝ) : ℝ := Real.log (N0 ^ 2 - t / 16)

/-- The error-budget quantity `e_{C,0}(t,y)`. -/
noncomputable def eC0 (t y : ℝ) : ℝ :=
  Real.exp (-((1 + y) / 4) * Lf t - (t / 16) * (Lf t) ^ 2
    + (31 / 25) * ((3 : ℝ) ^ y + (3 : ℝ) ^ (-y)) / (N0 - 1 / 8)
    + (3 * Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) + 21 / 2) / (xf t - 12))

/-- `L t` is indeed `log (x t / (4π))`. -/
lemma Lf_eq (t : ℝ) : Lf t = Real.log (xf t / (4 * Real.pi)) := by
  have hpi : (4 : ℝ) * Real.pi ≠ 0 := by positivity
  unfold Lf xf
  congr 1
  field_simp

/-! ### A general lower bound for `log` from an integer power certificate -/

/-- If `ρ * 2 ^ b ≤ z ^ a` with `ρ > 0` and `a > 0`, then
`(b * log 2 + (1 - 1/ρ)) / a` is a lower bound for `log z`. -/
lemma log_lower_of_pow (z ρ : ℝ) (hρ : 0 < ρ) (a : ℕ) (ha : 0 < a) (b : ℤ)
    (h : ρ * (2 : ℝ) ^ b ≤ z ^ a) :
    ((b : ℝ) * Real.log 2 + (1 - 1 / ρ)) / a ≤ Real.log z := by
  have hpos : (0 : ℝ) < ρ * (2 : ℝ) ^ b := by positivity
  have h1 : Real.log (ρ * (2 : ℝ) ^ b) ≤ Real.log (z ^ a) := Real.log_le_log hpos h
  rw [Real.log_mul (ne_of_gt hρ) (by positivity), Real.log_zpow, Real.log_pow] at h1
  have h2 : 1 - 1 / ρ ≤ Real.log ρ := by
    have := Real.one_sub_inv_le_log_of_pos hρ
    rwa [one_div]
  have ha' : (0 : ℝ) < a := by exact_mod_cast ha
  rw [div_le_iff₀ ha']
  nlinarith [h1, h2]

/-- Rational lower bound for `log (4774644161439899/10^4)`, certified by
`(999676653/10^9) * 2^2289 ≤ (4774644161439899/10^4)^59`. -/
lemma log_A_lower : (2689175546 / 10 ^ 8 : ℝ) ≤ Real.log (4774644161439899 / 10 ^ 4) := by
  have key := log_lower_of_pow (4774644161439899 / 10 ^ 4) (999676653 / 10 ^ 9)
    (by norm_num) 59 (by norm_num) 2289 (by norm_num)
  have h2 := Real.log_two_gt_d9
  norm_num at key h2 ⊢
  linarith

/-- Rational lower bound for `log (233492848188649183/10^24)`, certified by
`(1000250757/10^9) * 2^(-3657) ≤ (233492848188649183/10^24)^166`. -/
lemma log_T_lower :
    (-152701143946 / 10 ^ 10 : ℝ) ≤ Real.log (233492848188649183 / 10 ^ 24) := by
  have key := log_lower_of_pow (233492848188649183 / 10 ^ 24) (1000250757 / 10 ^ 9)
    (by norm_num) 166 (by norm_num) (-3657) (by norm_num)
  have h2 := Real.log_two_lt_d9
  norm_num at key h2 ⊢
  linarith

/-! ### Bounds on `L` over the `t`-box -/

lemma M_lower {t : ℝ} (ht : t ≤ t1) : (4774644161439899 / 10 ^ 4 : ℝ) ≤ N0 ^ 2 - t / 16 := by
  unfold N0
  unfold t1 at ht
  norm_num at ht ⊢
  linarith

lemma M_upper {t : ℝ} (ht : t0 ≤ t) : N0 ^ 2 - t / 16 ≤ 477464416144 := by
  unfold N0
  unfold t0 at ht
  norm_num at ht ⊢
  linarith

lemma Lf_lower {t : ℝ} (ht : t ≤ t1) : (2689175546 / 10 ^ 8 : ℝ) ≤ Lf t :=
  le_trans log_A_lower (Real.log_le_log (by norm_num) (M_lower ht))

lemma Lf_upper {t : ℝ} (ht0 : t0 ≤ t) (ht1 : t ≤ t1) : Lf t ≤ 27 := by
  have hexp : (477464416144 : ℝ) ≤ Real.exp 27 := by
    have h1 : (2.7182818283 : ℝ) ^ (27 : ℕ) ≤ (Real.exp 1) ^ (27 : ℕ) :=
      pow_le_pow_left₀ (by norm_num) (le_of_lt Real.exp_one_gt_d9) 27
    have h2 : (Real.exp 1) ^ (27 : ℕ) = Real.exp 27 := by
      rw [Real.exp_one_pow]; norm_num
    rw [h2] at h1
    nlinarith [h1]
  have hM : N0 ^ 2 - t / 16 ≤ Real.exp 27 := le_trans (M_upper ht0) hexp
  have hpos : (0 : ℝ) < N0 ^ 2 - t / 16 := lt_of_lt_of_le (by norm_num) (M_lower ht1)
  unfold Lf
  calc Real.log (N0 ^ 2 - t / 16) ≤ Real.log (Real.exp 27) := Real.log_le_log hpos hM
    _ = 27 := Real.log_exp 27

/-! ### Bounds on the `y`-endpoints -/

lemma y0_nonneg : 0 ≤ y0 := Real.sqrt_nonneg _

lemma y0_lower : (187271994 / 10 ^ 9 : ℝ) ≤ y0 := by
  unfold y0
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 87677 / 2500000 by norm_num),
    Real.sqrt_nonneg (87677 / 2500000 : ℝ)]

lemma y0_upper : y0 ≤ 3 / 16 := by
  unfold y0
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 87677 / 2500000 by norm_num),
    Real.sqrt_nonneg (87677 / 2500000 : ℝ)]

lemma ymax_le_one : ymax ≤ 1 := by
  unfold ymax
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 271 / 400 by norm_num),
    Real.sqrt_nonneg (271 / 400 : ℝ)]

/-! ### Elementary bounds on real powers of `3` -/

/-- A crude Lipschitz bound for `y ↦ 3^y` on `[0,1]`. -/
lemma three_rpow_sub_le {u v : ℝ} (huv : u ≤ v) (hv : v ≤ 1) :
    (3 : ℝ) ^ v - (3 : ℝ) ^ u ≤ 6 * (v - u) := by
  set d : ℝ := v - u with hd
  have hd0 : 0 ≤ d := by simp only [hd, sub_nonneg]; exact huv
  have hlog3 : Real.log 3 ≤ 2 := by
    have := Real.log_le_sub_one_of_pos (show (0:ℝ) < 3 by norm_num)
    linarith
  have hlog3nn : 0 ≤ Real.log 3 := Real.log_nonneg (by norm_num)
  have hsplit : (3 : ℝ) ^ v = (3 : ℝ) ^ u * (3 : ℝ) ^ d := by
    rw [← Real.rpow_add (by norm_num)]
    congr 1
    simp [hd]
  have hexp : (3 : ℝ) ^ d = Real.exp (d * Real.log 3) := by
    rw [Real.rpow_def_of_pos (by norm_num), mul_comm]
  have hkey : Real.exp (d * Real.log 3) - 1 ≤ (d * Real.log 3) * Real.exp (d * Real.log 3) := by
    have h1 : -(d * Real.log 3) + 1 ≤ Real.exp (-(d * Real.log 3)) := Real.add_one_le_exp _
    have h2 : (0 : ℝ) < Real.exp (d * Real.log 3) := Real.exp_pos _
    have h3 : Real.exp (-(d * Real.log 3)) * Real.exp (d * Real.log 3) = 1 := by
      rw [← Real.exp_add]; simp
    nlinarith [h1, h2, h3]
  have h3u : (0 : ℝ) < (3 : ℝ) ^ u := Real.rpow_pos_of_pos (by norm_num) u
  have hv3 : (3 : ℝ) ^ v ≤ 3 := by
    calc (3 : ℝ) ^ v ≤ (3 : ℝ) ^ (1 : ℝ) :=
          Real.rpow_le_rpow_of_exponent_le (by norm_num) hv
      _ = 3 := by norm_num
  have h4 := mul_le_mul_of_nonneg_left hkey (le_of_lt h3u)
  have hstep : (3 : ℝ) ^ v - (3 : ℝ) ^ u ≤ d * Real.log 3 * (3 : ℝ) ^ v := by
    calc (3 : ℝ) ^ v - (3 : ℝ) ^ u = (3 : ℝ) ^ u * ((3 : ℝ) ^ d - 1) := by rw [hsplit]; ring
      _ = (3 : ℝ) ^ u * (Real.exp (d * Real.log 3) - 1) := by rw [hexp]
      _ ≤ (3 : ℝ) ^ u * ((d * Real.log 3) * Real.exp (d * Real.log 3)) := h4
      _ = d * Real.log 3 * ((3 : ℝ) ^ u * (3 : ℝ) ^ d) := by rw [← hexp]; ring
      _ = d * Real.log 3 * (3 : ℝ) ^ v := by rw [hsplit]
  have hc1 : 0 ≤ d * Real.log 3 := mul_nonneg hd0 hlog3nn
  have hc2 : d * Real.log 3 * (3 : ℝ) ^ v ≤ d * Real.log 3 * 3 :=
    mul_le_mul_of_nonneg_left hv3 hc1
  have hc3 : d * Real.log 3 * 3 ≤ d * 2 * 3 := by
    have := mul_le_mul_of_nonneg_left hlog3 hd0
    linarith
  linarith [hstep, hc2, hc3]

lemma three_rpow_y0_le : (3 : ℝ) ^ y0 ≤ 1236 / 1000 := by
  have h1 : (3 : ℝ) ^ y0 ≤ (3 : ℝ) ^ ((3 : ℝ) / 16) :=
    Real.rpow_le_rpow_of_exponent_le (by norm_num) y0_upper
  have h2 : (3 : ℝ) ^ ((3 : ℝ) / 16) ≤ 1236 / 1000 := by
    have hpow : ((3 : ℝ) ^ ((3 : ℝ) / 16)) ^ (16 : ℕ) ≤ ((1236 / 1000 : ℝ)) ^ (16 : ℕ) := by
      rw [← Real.rpow_natCast ((3 : ℝ) ^ ((3 : ℝ) / 16)) 16, ← Real.rpow_mul (by norm_num)]
      norm_num
    exact le_of_pow_le_pow_left₀ (by norm_num) (by norm_num) hpow
  linarith

lemma three_rpow_neg_y0_le : (3 : ℝ) ^ (-y0) ≤ 1 := by
  have : (3 : ℝ) ^ (-y0) ≤ (3 : ℝ) ^ (0 : ℝ) :=
    Real.rpow_le_rpow_of_exponent_le (by norm_num) (by linarith [y0_nonneg])
  simpa using this

/-! ### The tail term -/

lemma tail_le {t : ℝ} (ht0 : t0 ≤ t) (ht1 : t ≤ t1) :
    (3 * Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) + 21 / 2) / (xf t - 12) ≤ 2 / 10 ^ 11 := by
  have hL1 : (2689175546 / 10 ^ 8 : ℝ) ≤ Lf t := Lf_lower ht1
  have hL2 : Lf t ≤ 27 := Lf_upper ht0 ht1
  have hpi1 : (3.14 : ℝ) < Real.pi := Real.pi_gt_d2
  have hpi2 : Real.pi < 3.15 := Real.pi_lt_d2
  have hsqrt : Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) ≤ 27.05 := by
    have harg : (Lf t) ^ 2 + Real.pi ^ 2 / 4 ≤ (27.05 : ℝ) ^ 2 := by nlinarith
    calc Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) ≤ Real.sqrt ((27.05 : ℝ) ^ 2) :=
          Real.sqrt_le_sqrt harg
      _ = 27.05 := Real.sqrt_sq (by norm_num)
  have hM : (4774644161439899 / 10 ^ 4 : ℝ) ≤ N0 ^ 2 - t / 16 := M_lower ht1
  have hx : (5990000000000 : ℝ) ≤ xf t - 12 := by
    unfold xf
    nlinarith [hM, hpi1]
  have hnum : 3 * Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) + 21 / 2 ≤ 92 := by linarith
  calc (3 * Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) + 21 / 2) / (xf t - 12)
      ≤ 92 / 5990000000000 := div_le_div₀ (by norm_num) hnum (by norm_num) hx
    _ ≤ 2 / 10 ^ 11 := by norm_num

/-! ### The main exponent bound -/

lemma exponent_le {t y : ℝ} (ht0 : t0 ≤ t) (ht1 : t ≤ t1) (hy0 : y0 ≤ y) (hy1 : y ≤ ymax) :
    -((1 + y) / 4) * Lf t - (t / 16) * (Lf t) ^ 2
      + (31 / 25) * ((3 : ℝ) ^ y + (3 : ℝ) ^ (-y)) / (N0 - 1 / 8)
      + (3 * Real.sqrt ((Lf t) ^ 2 + Real.pi ^ 2 / 4) + 21 / 2) / (xf t - 12)
      ≤ Real.log (233492848188649183 / 10 ^ 24) := by
  set L := Lf t with hLdef
  have hL1 : (2689175546 / 10 ^ 8 : ℝ) ≤ L := Lf_lower ht1
  have hLpos : (0 : ℝ) < L := by linarith
  have hy0nn : 0 ≤ y0 := y0_nonneg
  have hy0lo : (187271994 / 10 ^ 9 : ℝ) ≤ y0 := y0_lower
  have hyle1 : y ≤ 1 := le_trans hy1 ymax_le_one
  have hg1 : (3 : ℝ) ^ y - (3 : ℝ) ^ y0 ≤ 6 * (y - y0) :=
    three_rpow_sub_le hy0 hyle1
  have hg2 : (3 : ℝ) ^ (-y) ≤ (3 : ℝ) ^ (-y0) :=
    Real.rpow_le_rpow_of_exponent_le (by norm_num) (by linarith)
  have hydiff : 0 ≤ y - y0 := by linarith
  have hN : N0 - 1 / 8 = (5527903 / 8) := by unfold N0; norm_num
  -- reduce the `y`-dependence to the endpoint `y = y₀`
  have hprod : 0 ≤ (y - y0) * (L - 2689175546 / 10 ^ 8) :=
    mul_nonneg hydiff (by linarith)
  have hlip : (31 / 25 : ℝ) * (6 * (y - y0)) / (5527903 / 8) ≤ (y - y0) / 4 * L := by
    nlinarith [hprod, hydiff]
  have hid : -((1 + y) / 4) * L + (y - y0) / 4 * L = -((1 + y0) / 4) * L := by ring
  have hstep1 : -((1 + y) / 4) * L
        + (31 / 25) * ((3 : ℝ) ^ y + (3 : ℝ) ^ (-y)) / (N0 - 1 / 8)
      ≤ -((1 + y0) / 4) * L
        + (31 / 25) * ((3 : ℝ) ^ y0 + (3 : ℝ) ^ (-y0)) / (N0 - 1 / 8) := by
    rw [hN]
    linarith [hg1, hg2, hlip, hid]
  -- the middle term at `y = y₀`
  have hmid : (31 / 25 : ℝ) * ((3 : ℝ) ^ y0 + (3 : ℝ) ^ (-y0)) / (N0 - 1 / 8)
      ≤ (31 / 25 : ℝ) * (2236 / 1000) / (5527903 / 8) := by
    rw [hN]
    linarith [three_rpow_y0_le, three_rpow_neg_y0_le]
  -- the main term at `y = y₀`
  have hmain : -((1 + y0) / 4) * L ≤ -((1 + 187271994 / 10 ^ 9) / 4) * (2689175546 / 10 ^ 8) := by
    have : ((1 + 187271994 / 10 ^ 9) / 4 : ℝ) * (2689175546 / 10 ^ 8) ≤ ((1 + y0) / 4) * L :=
      mul_le_mul (by linarith) hL1 (by norm_num) (by linarith)
    linarith
  -- the quadratic term
  have hquad : -(t / 16) * L ^ 2 ≤ -(129 / 800 / 16) * (2689175546 / 10 ^ 8 : ℝ) ^ 2 := by
    have ht0' : (129 / 800 : ℝ) ≤ t := by unfold t0 at ht0; linarith
    have hsq : ((2689175546 / 10 ^ 8 : ℝ)) ^ 2 ≤ L ^ 2 := by nlinarith [hL1]
    have : (129 / 800 / 16 : ℝ) * (2689175546 / 10 ^ 8) ^ 2 ≤ (t / 16) * L ^ 2 :=
      mul_le_mul (by linarith) hsq (by positivity) (by linarith)
    linarith
  have htail := tail_le ht0 ht1
  have hT := log_T_lower
  have hfinal : -((1 + 187271994 / 10 ^ 9) / 4) * (2689175546 / 10 ^ 8 : ℝ)
      + -(129 / 800 / 16) * (2689175546 / 10 ^ 8) ^ 2
      + (31 / 25 : ℝ) * (2236 / 1000) / (5527903 / 8) + 2 / 10 ^ 11
      ≤ -152701143946 / 10 ^ 10 := by norm_num
  linarith [hstep1, hmid, hmain, hquad, htail, hT, hfinal]

/-! ### Main results -/

/-- **Primary target.** For all `t ∈ [t₀, t₁]` and all `y ∈ [y₀, y_max]`,
`e_{C,0}(t,y) ≤ 233492848188649183/10^24`. -/
theorem eC0_le_sharp {t y : ℝ} (ht0 : t0 ≤ t) (ht1 : t ≤ t1) (hy0 : y0 ≤ y) (hy1 : y ≤ ymax) :
    eC0 t y ≤ 233492848188649183 / 10 ^ 24 := by
  have h := exponent_le ht0 ht1 hy0 hy1
  have h2 := Real.exp_le_exp.2 h
  rwa [Real.exp_log (by norm_num)] at h2

/-- The box `[t₀,t₁] × [y₀,y_max]` is nonempty, so the two bounds above are not vacuous. -/
lemma box_nonempty : t0 < t1 ∧ y0 < ymax := by
  constructor
  · unfold t0 t1; norm_num
  · unfold y0 ymax
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)

/-- **Weaker fallback.** Under the same hypotheses, `e_{C,0}(t,y) ≤ 234/10^9`. -/
theorem eC0_le_weak {t y : ℝ} (ht0 : t0 ≤ t) (ht1 : t ≤ t1) (hy0 : y0 ≤ y) (hy1 : y ≤ ymax) :
    eC0 t y ≤ 234 / 10 ^ 9 := by
  have h := eC0_le_sharp ht0 ht1 hy0 hy1
  norm_num at h ⊢
  linarith

end EC0
