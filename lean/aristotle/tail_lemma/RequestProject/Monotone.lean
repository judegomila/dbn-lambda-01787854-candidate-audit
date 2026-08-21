import RequestProject.Contraction

/-!
# Lemmas 4 and 5 : monotonicity in `N` and in `y`

Lemma 4 shows that all the contraction quantities decrease in `N` once the two gate
conditions hold at the cutoff, so that `D(N,t,y) ≤ D(N_*,t,y)` for all `N ≥ N_*`.
Lemma 5 shows that `D` decreases in `y` under the `YM` gate.
-/

namespace Job2

open Finset

lemma max_mul_nonneg (A B w : ℝ) (hw : 0 ≤ w) : max A B * w = max (A * w) (B * w) := by
  rcases le_total A B with h | h
  · rw [max_eq_right h, max_eq_right (mul_le_mul_of_nonneg_right h hw)]
  · rw [max_eq_left h, max_eq_left (mul_le_mul_of_nonneg_right h hw)]

lemma Ecap_pos (t s u : ℝ) : 0 < Ecap t s u := Real.exp_pos _

/-- `Cap` written with the width factored into both endpoint values. -/
lemma cap_eq_max_mul {t a c s : ℝ} (ha : 0 < a) (hac : a ≤ c) :
    Cap t a c s = max (Ecap t s a * (Real.log c - Real.log a))
      (Ecap t s c * (Real.log c - Real.log a)) := by
  have hc : 0 < c := lt_of_lt_of_le ha hac
  have hw : 0 ≤ Real.log c - Real.log a := sub_nonneg.2 (Real.log_le_log ha hac)
  rw [Cap, Real.log_div (ne_of_gt hc) (ne_of_gt ha), max_mul_nonneg _ _ _ hw]

/-- Elementary logarithm estimate: `log w₂ - log w₁ ≤ (w₂ - w₁)/w₁`. -/
lemma log_sub_log_le {w1 w2 : ℝ} (h1 : 0 < w1) (h2 : 0 < w2) :
    Real.log w2 - Real.log w1 ≤ (w2 - w1) / w1 := by
  have hkey := Real.log_le_sub_one_of_pos (div_pos h2 h1)
  rw [Real.log_div (ne_of_gt h2) (ne_of_gt h1)] at hkey
  have : w2 / w1 - 1 = (w2 - w1) / w1 := by field_simp
  linarith [hkey, this.le, this.ge]

/-- **Lemma 4, fixed-left caps.** With `σ(N) = s₀ + (t/2) log N`, a cap with fixed left endpoint
`a ≥ 1` and right endpoint `N` decreases in `N`, provided the two gate conditions hold at `N₁`. -/
lemma cap_fixed_left_antitone {t a s0 N1 N2 : ℝ} (ht : 0 ≤ t) (ha : 1 ≤ a)
    (haN1 : a < N1) (hN12 : N1 ≤ N2)
    (hg1 : 1 ≤ t/2 * Real.log a * (Real.log N1 - Real.log a))
    (hg2 : 1 ≤ (s0 + t/2 * Real.log N1 - 1) * (Real.log N1 - Real.log a)) :
    Cap t a N2 (s0 + t/2 * Real.log N2) ≤ Cap t a N1 (s0 + t/2 * Real.log N1) := by
  have ha0 : (0:ℝ) < a := lt_of_lt_of_le one_pos ha
  have hN10 : 0 < N1 := lt_trans ha0 haN1
  have hN20 : 0 < N2 := lt_of_lt_of_le hN10 hN12
  set la := Real.log a with hla
  set q1 := Real.log N1 with hq1
  set q2 := Real.log N2 with hq2
  have hla0 : 0 ≤ la := Real.log_nonneg ha
  have hlaq1 : la < q1 := Real.log_lt_log ha0 haN1
  have hq12 : q1 ≤ q2 := Real.log_le_log hN10 hN12
  have hw1 : 0 < q1 - la := by linarith
  have hw2 : 0 < q2 - la := by linarith
  have hd : 0 ≤ q2 - q1 := by linarith
  have hlogdiff : Real.log (q2 - la) - Real.log (q1 - la) ≤ (q2 - q1) / (q1 - la) := by
    have := log_sub_log_le hw1 hw2
    have heq : (q2 - la) - (q1 - la) = q2 - q1 := by ring
    rwa [heq] at this
  rw [cap_eq_max_mul ha0 (le_of_lt haN1), cap_eq_max_mul ha0 (le_of_lt (lt_of_lt_of_le haN1 hN12))]
  -- rewrite the products as exponentials
  have hrw : ∀ (s u w : ℝ), 0 < w →
      Ecap t s u * w = Real.exp ((1-s) * Real.log u + t/4 * Real.log u ^ 2 + Real.log w) := by
    intro s u w hwpos
    simp [Ecap, Real.exp_add, Real.exp_log hwpos]
  apply max_le
  · -- left endpoint
    refine le_trans ?_ (le_max_left _ _)
    rw [hrw _ _ _ hw2, hrw _ _ _ hw1, ← hla]
    apply Real.exp_le_exp.2
    have hinv : (q2 - q1) / (q1 - la) ≤ t/2 * la * (q2 - q1) := by
      rw [div_le_iff₀ hw1]
      nlinarith [hg1, hd]
    nlinarith [hlogdiff, hinv]
  · -- right endpoint
    refine le_trans ?_ (le_max_right _ _)
    rw [hrw _ _ _ hw2, hrw _ _ _ hw1, ← hq1, ← hq2]
    apply Real.exp_le_exp.2
    have hinv : (q2 - q1) / (q1 - la) ≤ (s0 + t/2 * q1 - 1) * (q2 - q1) := by
      rw [div_le_iff₀ hw1]
      nlinarith [hg2, hd]
    nlinarith [hlogdiff, hinv, mul_nonneg ht (mul_nonneg hd hd)]

/-- **Lemma 4, moving caps.** With `σ(N) = s₀ + (t/2) log N ≥ 1` at `N₁`, a cap whose two
endpoints are `N/r` and `N` (constant width `log r`) decreases in `N`. -/
lemma cap_moving_antitone {t r s0 N1 N2 : ℝ} (ht : 0 ≤ t) (hr : 1 ≤ r)
    (hN10 : 0 < N1) (hN12 : N1 ≤ N2)
    (hsig : 1 ≤ s0 + t/2 * Real.log N1) :
    Cap t (N2/r) N2 (s0 + t/2 * Real.log N2) ≤ Cap t (N1/r) N1 (s0 + t/2 * Real.log N1) := by
  have hr0 : 0 < r := lt_of_lt_of_le one_pos hr
  have hN20 : 0 < N2 := lt_of_lt_of_le hN10 hN12
  set q1 := Real.log N1 with hq1
  set q2 := Real.log N2 with hq2
  set Lr := Real.log r with hLr
  have hLr0 : 0 ≤ Lr := Real.log_nonneg hr
  have hq12 : q1 ≤ q2 := Real.log_le_log hN10 hN12
  have hdiv1 : Real.log (N1/r) = q1 - Lr := Real.log_div (ne_of_gt hN10) (ne_of_gt hr0)
  have hdiv2 : Real.log (N2/r) = q2 - Lr := Real.log_div (ne_of_gt hN20) (ne_of_gt hr0)
  have hle1 : N1/r ≤ N1 := div_le_self hN10.le hr
  have hle2 : N2/r ≤ N2 := div_le_self hN20.le hr
  have hpos1 : 0 < N1/r := div_pos hN10 hr0
  have hpos2 : 0 < N2/r := div_pos hN20 hr0
  rw [cap_eq_max_mul hpos1 hle1, cap_eq_max_mul hpos2 hle2, hdiv1, hdiv2]
  have hwidth : ∀ q : ℝ, q - (q - Lr) = Lr := by intro q; ring
  rw [hwidth, hwidth]
  apply max_le
  · refine le_trans ?_ (le_max_left _ _)
    refine mul_le_mul_of_nonneg_right ?_ hLr0
    simp only [Ecap, hdiv1, hdiv2]
    apply Real.exp_le_exp.2
    nlinarith [ht, hq12, hsig, mul_nonneg ht (sub_nonneg.2 hq12)]
  · refine le_trans ?_ (le_max_right _ _)
    refine mul_le_mul_of_nonneg_right ?_ hLr0
    simp only [Ecap]
    apply Real.exp_le_exp.2
    nlinarith [ht, hq12, hsig, mul_nonneg ht (sub_nonneg.2 hq12)]

/-! ### Monotonicity of the individual contraction quantities -/

lemma sig1_eq (dh N t y : ℝ) : sig1 dh N t y = ((1+y)/2 - dh) + t/2 * Real.log N := by
  rw [sig1]; ring

lemma sig2_eq (dh kh N t y : ℝ) :
    sig2 dh kh N t y = ((1-y)/2 - dh - kh) + t/2 * Real.log N := by
  rw [sig2]; ring

lemma sig1_mono_N {dh t y N1 N2 : ℝ} (ht : 0 ≤ t) (hN10 : 0 < N1) (hN12 : N1 ≤ N2) :
    sig1 dh N1 t y ≤ sig1 dh N2 t y := by
  rw [sig1, sig1]
  have := Real.log_le_log hN10 hN12
  nlinarith

lemma sig2_mono_N {dh kh t y N1 N2 : ℝ} (ht : 0 ≤ t) (hN10 : 0 < N1) (hN12 : N1 ≤ N2) :
    sig2 dh kh N1 t y ≤ sig2 dh kh N2 t y := by
  rw [sig2, sig2]
  have := Real.log_le_log hN10 hN12
  nlinarith

/-- `P` decreases when `σ₁` increases. -/
lemma Pq_antitone {t s1 s2 : ℝ} (h : s1 ≤ s2) : Pq t s2 ≤ Pq t s1 := by
  refine Finset.sum_le_sum fun m hm => ?_
  simp only [Finset.mem_Icc] at hm
  have hm1 : (1:ℝ) ≤ (m:ℝ) := by exact_mod_cast le_trans (by norm_num) hm.1
  gcongr ; first | exact abs_nonneg _ | assumption

/-- `M_max` decreases when `σ₁` increases. -/
lemma Mmaxq_antitone {s1 s2 : ℝ} (h : s1 ≤ s2) : Mmaxq s2 ≤ Mmaxq s1 := by
  refine Finset.sum_le_sum fun d hd => ?_
  have hd1 : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast one_le_of_mem_S hd
  gcongr ; first | exact abs_nonneg _ | assumption

/-- The finite `A`-head decreases when `σ₂` increases. -/
lemma headM_antitone {t s1 s2 : ℝ} (h : s1 ≤ s2) :
    (∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s2))
      ≤ ∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s1) := by
  refine Finset.sum_le_sum fun k hk => ?_
  simp only [Finset.mem_Icc] at hk
  have hk1 : (1:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk.1
  gcongr <;> first | exact (bt_pos t k).le | assumption

lemma headM_nonneg (t s : ℝ) : 0 ≤ ∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s) :=
  Finset.sum_nonneg fun k _ => mul_nonneg (bt_pos t k).le (Real.rpow_nonneg (by positivity) _)

lemma Gval_pos {N t y : ℝ} (hNt : 0 < N^2 - t/16) : 0 < Gval N t y :=
  mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos hNt _)

/-- `G` decreases in `N` (for `y ≥ 0`). -/
lemma Gval_antitone_N {t y N1 N2 : ℝ} (hy : 0 ≤ y) (hN10 : 0 ≤ N1) (hN12 : N1 ≤ N2)
    (hNt : 0 < N1^2 - t/16) : Gval N2 t y ≤ Gval N1 t y := by
  rw [Gval, Gval]
  refine mul_le_mul_of_nonneg_left ?_ (Real.exp_nonneg _)
  refine Real.rpow_le_rpow_of_nonpos hNt ?_ (by linarith)
  nlinarith

/-- **Lemma 4 (reduction of all `N ≥ N_*` to the cutoff).**  If the two gate conditions hold at
`N₁` for every fixed left cap endpoint used in `D`, and `σ₁ ≥ 1` there, then `D` decreases in
`N`, i.e. `D(N₂,t,y) ≤ D(N₁,t,y)` for all `N₂ ≥ N₁`. -/
theorem lemma4_reduction {t y dh kh N1 N2 : ℝ}
    (ht : 0 ≤ t) (hy : 0 ≤ y) (hN10 : 0 < N1) (hN12 : N1 ≤ N2)
    (hNt : 0 < N1^2 - t/16)
    (hsig1 : 1 ≤ sig1 dh N1 t y)
    (hTR : ∀ d ∈ S, 1 ≤ ((Mcut/d : ℕ):ℝ) ∧ ((Mcut/d : ℕ):ℝ) < N1 ∧
      1 ≤ t/2 * Real.log ((Mcut/d : ℕ):ℝ) * (Real.log N1 - Real.log ((Mcut/d : ℕ):ℝ)) ∧
      1 ≤ (sig1 dh N1 t y - 1) * (Real.log N1 - Real.log ((Mcut/d : ℕ):ℝ)))
    (hABa : (Mcut:ℝ) < N1)
    (hABg1 : 1 ≤ t/2 * Real.log (Mcut:ℝ) * (Real.log N1 - Real.log (Mcut:ℝ)))
    (hABg2 : 1 ≤ (sig2 dh kh N1 t y - 1) * (Real.log N1 - Real.log (Mcut:ℝ))) :
    Dq dh kh N2 t y ≤ Dq dh kh N1 t y := by
  have hN20 : 0 < N2 := lt_of_lt_of_le hN10 hN12
  have hs1 : sig1 dh N1 t y ≤ sig1 dh N2 t y := sig1_mono_N ht hN10 hN12
  have hs2 : sig2 dh kh N1 t y ≤ sig2 dh kh N2 t y := sig2_mono_N ht hN10 hN12
  -- `TR`
  have hTRle : TRq t N2 (sig1 dh N2 t y) ≤ TRq t N1 (sig1 dh N1 t y) := by
    refine Finset.sum_le_sum fun d hd => ?_
    obtain ⟨ha1, haN1, hg1, hg2⟩ := hTR d hd
    have hd1 : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast one_le_of_mem_S hd
    have hcap : Cap t ((Mcut/d : ℕ):ℝ) N2 (sig1 dh N2 t y)
        ≤ Cap t ((Mcut/d : ℕ):ℝ) N1 (sig1 dh N1 t y) := by
      rw [sig1_eq dh N1 t y, sig1_eq dh N2 t y]
      refine cap_fixed_left_antitone ht ha1 haN1 hN12 hg1 ?_
      rw [← sig1_eq dh N1 t y]
      exact hg2
    have hfac : |lam d| * (d:ℝ) ^ (-sig1 dh N2 t y) ≤ |lam d| * (d:ℝ) ^ (-sig1 dh N1 t y) := by
      gcongr ; first | exact abs_nonneg _ | assumption
    refine mul_le_mul hfac hcap (Cap_nonneg (by linarith) ?_) ?_
    · exact le_trans (le_of_lt haN1) hN12
    · exact mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _)
  -- `OV`
  have hOVle : OVq t N2 (sig1 dh N2 t y) ≤ OVq t N1 (sig1 dh N1 t y) := by
    refine Finset.sum_le_sum fun d hd => ?_
    simp only [Finset.mem_filter] at hd
    have hd1 : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast one_le_of_mem_S hd.1
    have hr : (1:ℝ) ≤ (d:ℝ) + 1 := by linarith
    have hcap : Cap t (N2/((d:ℝ)+1)) N2 (sig1 dh N2 t y)
        ≤ Cap t (N1/((d:ℝ)+1)) N1 (sig1 dh N1 t y) := by
      rw [sig1_eq dh N1 t y, sig1_eq dh N2 t y]
      refine cap_moving_antitone ht hr hN10 hN12 ?_
      rw [← sig1_eq dh N1 t y]
      exact hsig1
    have hfac : |lam d| * (d:ℝ) ^ (-sig1 dh N2 t y) ≤ |lam d| * (d:ℝ) ^ (-sig1 dh N1 t y) := by
      gcongr ; first | exact abs_nonneg _ | assumption
    refine mul_le_mul hfac hcap (Cap_nonneg (by positivity) ?_) ?_
    · exact div_le_self hN20.le hr
    · exact mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _)
  -- `AB`
  have hABle : ABq t N2 (sig2 dh kh N2 t y) (Gval N2 t y)
      ≤ ABq t N1 (sig2 dh kh N1 t y) (Gval N1 t y) := by
    have hcap : Cap t (Mcut:ℝ) N2 (sig2 dh kh N2 t y) ≤ Cap t (Mcut:ℝ) N1 (sig2 dh kh N1 t y) := by
      rw [sig2_eq dh kh N1 t y, sig2_eq dh kh N2 t y]
      refine cap_fixed_left_antitone ht (by norm_num [Mcut]) hABa hN12 hABg1 ?_
      rw [← sig2_eq dh kh N1 t y]
      exact hABg2
    have hbracket : (∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-sig2 dh kh N2 t y))
          + Cap t (Mcut:ℝ) N2 (sig2 dh kh N2 t y)
        ≤ (∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-sig2 dh kh N1 t y))
          + Cap t (Mcut:ℝ) N1 (sig2 dh kh N1 t y) :=
      add_le_add (headM_antitone hs2) hcap
    refine mul_le_mul (Gval_antitone_N hy hN10.le hN12 hNt) hbracket ?_ (Gval_pos hNt).le
    exact add_nonneg (headM_nonneg _ _)
      (Cap_nonneg (by norm_num [Mcut]) (le_trans hABa.le hN12))
  have hMmax : Mmaxq (sig1 dh N2 t y) ≤ Mmaxq (sig1 dh N1 t y) := Mmaxq_antitone hs1
  have hABnonneg : 0 ≤ ABq t N2 (sig2 dh kh N2 t y) (Gval N2 t y) := by
    refine mul_nonneg (Gval_pos ?_).le (add_nonneg (headM_nonneg _ _)
      (Cap_nonneg (by norm_num [Mcut]) (le_trans hABa.le hN12)))
    nlinarith
  rw [Dq, Dq]
  refine add_le_add (add_le_add (add_le_add (Pq_antitone hs1) hTRle) hOVle) ?_
  exact mul_le_mul hMmax hABle hABnonneg (Mmaxq_nonneg _)

/-! ### Lemma 5 : monotonicity in `y` -/

lemma mul_max_nonneg (c A B : ℝ) (hc : 0 ≤ c) : c * max A B = max (c * A) (c * B) := by
  rcases le_total A B with h | h
  · rw [max_eq_right h, max_eq_right (mul_le_mul_of_nonneg_left h hc)]
  · rw [max_eq_left h, max_eq_left (mul_le_mul_of_nonneg_left h hc)]

lemma sig1_mono_y {dh t N y1 y2 : ℝ} (h : y1 ≤ y2) : sig1 dh N t y1 ≤ sig1 dh N t y2 := by
  rw [sig1, sig1]; linarith

lemma sig2_anti_y {dh kh t N y1 y2 : ℝ} (h : y1 ≤ y2) : sig2 dh kh N t y2 ≤ sig2 dh kh N t y1 := by
  rw [sig2, sig2]; linarith

/-- `E_{t,σ}(u)` decreases when `σ` increases, for `u ≥ 1`. -/
lemma Ecap_antitone_sigma {t u s1 s2 : ℝ} (hu : 1 ≤ u) (h : s1 ≤ s2) :
    Ecap t s2 u ≤ Ecap t s1 u := by
  have hlu : 0 ≤ Real.log u := Real.log_nonneg hu
  rw [Ecap, Ecap]
  apply Real.exp_le_exp.2
  nlinarith

/-- A cap decreases when `σ` increases, provided both endpoints are `≥ 1`. -/
lemma Cap_antitone_sigma {t a c s1 s2 : ℝ} (ha : 1 ≤ a) (hac : a ≤ c) (h : s1 ≤ s2) :
    Cap t a c s2 ≤ Cap t a c s1 := by
  have ha0 : (0:ℝ) < a := lt_of_lt_of_le one_pos ha
  have hw : 0 ≤ Real.log (c/a) := Real.log_nonneg (by rw [le_div_iff₀ ha0]; linarith)
  refine mul_le_mul_of_nonneg_right ?_ hw
  exact max_le_max (Ecap_antitone_sigma ha h) (Ecap_antitone_sigma (le_trans ha hac) h)

lemma Gval_eq_exp {N t y : ℝ} (hNt : 0 < N^2 - t/16) :
    Gval N t y = Real.exp (y/50 - y/2 * Lwin N t) := by
  rw [Gval, Lwin, Real.rpow_def_of_pos hNt, ← Real.exp_add]
  ring_nf

/-- **The `YM` gate at work.**  `G · E_{t,σ₂}(u)` decreases in `y` for every `u ≤ N`. -/
lemma G_mul_Ecap_antitone_y {t dh kh N u y1 y2 : ℝ} (hNt : 0 < N^2 - t/16)
    (hu1 : 1 ≤ u) (huN : u ≤ N) (hy12 : y1 ≤ y2)
    (hYM : 1/50 - Lwin N t / 2 + Real.log N / 2 ≤ 0) :
    Gval N t y2 * Ecap t (sig2 dh kh N t y2) u ≤ Gval N t y1 * Ecap t (sig2 dh kh N t y1) u := by
  have hu0 : 0 < u := lt_of_lt_of_le one_pos hu1
  have hlu : Real.log u ≤ Real.log N := Real.log_le_log hu0 huN
  have hcoef : 1/50 - Lwin N t / 2 + Real.log u / 2 ≤ 0 := by linarith
  rw [Gval_eq_exp hNt, Gval_eq_exp hNt, Ecap, Ecap, ← Real.exp_add, ← Real.exp_add]
  apply Real.exp_le_exp.2
  rw [sig2, sig2]
  nlinarith [mul_nonneg (sub_nonneg.2 hy12) (neg_nonneg.2 hcoef)]

/-- **Lemma 5 (complete `y`-range).**  Under the `YM` gate, `D` decreases in `y`. -/
theorem lemma5_y_monotone {t dh kh N y1 y2 : ℝ}
    (hN15 : (15:ℝ) ≤ N) (hNt : 0 < N^2 - t/16) (hMN : (Mcut:ℝ) < N) (hy12 : y1 ≤ y2)
    (hYM : 1/50 - Lwin N t / 2 + Real.log N / 2 ≤ 0) :
    Dq dh kh N t y2 ≤ Dq dh kh N t y1 := by
  have hN0 : (0:ℝ) < N := by linarith
  have hs1 : sig1 dh N t y1 ≤ sig1 dh N t y2 := sig1_mono_y hy12
  -- `TR`
  have hTRle : TRq t N (sig1 dh N t y2) ≤ TRq t N (sig1 dh N t y1) := by
    refine Finset.sum_le_sum fun d hd => ?_
    have hd1 : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast one_le_of_mem_S hd
    have hd0 : 0 < d := one_le_of_mem_S hd
    have hdM : 1 ≤ Mcut / d := by
      refine (Nat.one_le_div_iff hd0).2 ?_
      have hd14 : d ≤ 14 := by fin_cases hd <;> norm_num
      simp only [Mcut]
      omega
    have ha1 : (1:ℝ) ≤ ((Mcut/d : ℕ):ℝ) := by exact_mod_cast hdM
    have haN : ((Mcut/d : ℕ):ℝ) ≤ N := by
      refine le_trans ?_ hMN.le
      exact_mod_cast Nat.div_le_self Mcut d
    have hcap : Cap t ((Mcut/d : ℕ):ℝ) N (sig1 dh N t y2)
        ≤ Cap t ((Mcut/d : ℕ):ℝ) N (sig1 dh N t y1) := Cap_antitone_sigma ha1 haN hs1
    have hfac : |lam d| * (d:ℝ) ^ (-sig1 dh N t y2) ≤ |lam d| * (d:ℝ) ^ (-sig1 dh N t y1) := by
      gcongr ; first | exact abs_nonneg _ | assumption
    exact mul_le_mul hfac hcap (Cap_nonneg (by linarith) haN)
      (mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _))
  -- `OV`
  have hOVle : OVq t N (sig1 dh N t y2) ≤ OVq t N (sig1 dh N t y1) := by
    refine Finset.sum_le_sum fun d hd => ?_
    simp only [Finset.mem_filter] at hd
    have hd1 : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast one_le_of_mem_S hd.1
    have hd14 : (d:ℝ) ≤ 14 := by
      have hdS := hd.1
      have hdle : d ≤ 14 := by fin_cases hdS <;> norm_num
      exact_mod_cast hdle
    have hr : (0:ℝ) < (d:ℝ) + 1 := by linarith
    have ha1 : (1:ℝ) ≤ N/((d:ℝ)+1) := by
      rw [le_div_iff₀ hr]; linarith
    have haN : N/((d:ℝ)+1) ≤ N := div_le_self hN0.le (by linarith)
    have hcap : Cap t (N/((d:ℝ)+1)) N (sig1 dh N t y2)
        ≤ Cap t (N/((d:ℝ)+1)) N (sig1 dh N t y1) := Cap_antitone_sigma ha1 haN hs1
    have hfac : |lam d| * (d:ℝ) ^ (-sig1 dh N t y2) ≤ |lam d| * (d:ℝ) ^ (-sig1 dh N t y1) := by
      gcongr ; first | exact abs_nonneg _ | assumption
    exact mul_le_mul hfac hcap (Cap_nonneg (by linarith) haN)
      (mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _))
  -- `AB`
  have hMcut1 : (1:ℝ) ≤ (Mcut:ℝ) := by norm_num [Mcut]
  have hABle : ABq t N (sig2 dh kh N t y2) (Gval N t y2)
      ≤ ABq t N (sig2 dh kh N t y1) (Gval N t y1) := by
    rw [ABq, ABq, mul_add, mul_add, Finset.mul_sum, Finset.mul_sum]
    refine add_le_add (Finset.sum_le_sum fun k hk => ?_) ?_
    · simp only [Finset.mem_Icc] at hk
      have hk1 : (1:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk.1
      have hkM : (k:ℝ) ≤ (Mcut:ℝ) := by exact_mod_cast hk.2
      have hkN : (k:ℝ) ≤ N := le_trans hkM hMN.le
      have hk0 : (0:ℝ) < (k:ℝ) := by linarith
      rw [bt_mul_rpow_eq_Ecap_div hk0, bt_mul_rpow_eq_Ecap_div hk0, mul_div_assoc',
        mul_div_assoc']
      exact (div_le_div_iff_of_pos_right hk0).2
        (G_mul_Ecap_antitone_y (dh := dh) (kh := kh) hNt hk1 hkN hy12 hYM)
    · rw [Cap, Cap, ← mul_assoc, ← mul_assoc, mul_max_nonneg _ _ _ (Gval_pos hNt).le,
        mul_max_nonneg _ _ _ (Gval_pos hNt).le]
      refine mul_le_mul_of_nonneg_right (max_le_max ?_ ?_) ?_
      · exact G_mul_Ecap_antitone_y hNt hMcut1 hMN.le hy12 hYM
      · exact G_mul_Ecap_antitone_y hNt (by linarith) (le_refl _) hy12 hYM
      · exact Real.log_nonneg (by rw [le_div_iff₀ (by linarith)]; linarith)
  have hABnonneg : 0 ≤ ABq t N (sig2 dh kh N t y2) (Gval N t y2) :=
    mul_nonneg (Gval_pos hNt).le
      (add_nonneg (headM_nonneg _ _) (Cap_nonneg (by linarith) hMN.le))
  rw [Dq, Dq]
  refine add_le_add (add_le_add (add_le_add (Pq_antitone hs1) hTRle) hOVle) ?_
  exact mul_le_mul (Mmaxq_antitone hs1) hABle hABnonneg (Mmaxq_nonneg _)

end Job2
