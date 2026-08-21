import RequestProject.Cap
import RequestProject.Convolution

/-!
# Lemma 3 : the contraction bound

Under Hypothesis H1 (the structure `f_t = F_B + γ F_A` with `Re s_* ≥ σ₁`, `|κ| ≤ k̂`,
`|γ| ≤ G`) one has `|M_λ(s_*) f_t - 1| ≤ D`.
-/

namespace Job2

open Finset

lemma bt_pos (t u : ℝ) : 0 < bt t u := Real.exp_pos _

/-- Termwise bound for the `B`-side. -/
lemma norm_bt_cpow_le {t s0 : ℝ} {s : ℂ} {k : ℕ} (hk : 1 ≤ k) (h : s0 ≤ s.re) :
    ‖(bt t k : ℂ) * (k:ℂ) ^ (-s)‖ ≤ bt t k * (k:ℝ) ^ (-s0) := by
  have hk0 : 0 < k := hk
  have hk1 : (1:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk
  rw [norm_mul, Complex.norm_natCast_cpow_of_pos hk0, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (bt_pos t k), Complex.neg_re]
  gcongr <;> first | exact (bt_pos t _).le | exact abs_nonneg _ | assumption

/-- Sum version of the `B`-side bound. -/
lemma norm_sum_bt_le {t s0 : ℝ} {s : ℂ} (T : Finset ℕ) (hT : ∀ k ∈ T, 1 ≤ k) (h : s0 ≤ s.re) :
    ‖∑ k ∈ T, (bt t k : ℂ) * (k:ℂ) ^ (-s)‖ ≤ ∑ k ∈ T, bt t k * (k:ℝ) ^ (-s0) :=
  le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun k hk => norm_bt_cpow_le (hT k hk) h)

/-- `‖M_λ(s_*)‖ ≤ M_max`. -/
lemma norm_Mlam_le {s0 : ℝ} {s : ℂ} (h : s0 ≤ s.re) : ‖Mlam s‖ ≤ Mmaxq s0 := by
  refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun d hd => ?_)
  have hd1 : 1 ≤ d := one_le_of_mem_S hd
  have hd0 : 0 < d := hd1
  have hd1' : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast hd1
  rw [norm_mul, Complex.norm_natCast_cpow_of_pos hd0, Complex.norm_real, Real.norm_eq_abs,
    Complex.neg_re]
  gcongr ; first | exact (bt_pos _ _).le | exact abs_nonneg _ | assumption

/-- `M_max ≥ 0`. -/
lemma Mmaxq_nonneg (s0 : ℝ) : 0 ≤ Mmaxq s0 :=
  Finset.sum_nonneg fun d _ => mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _)

/-- Caps are nonnegative as soon as `0 < a ≤ c`. -/
lemma Cap_nonneg {t s a c : ℝ} (ha : 0 < a) (hac : a ≤ c) : 0 ≤ Cap t a c s := by
  apply mul_nonneg
  · exact le_trans (Real.exp_nonneg _) (le_max_left _ _)
  · apply Real.log_nonneg
    rw [le_div_iff₀ ha]
    linarith

/-- The overlap padding `OV` is nonnegative. -/
lemma OVq_nonneg {t N s : ℝ} (hN : 0 < N) : 0 ≤ OVq t N s := by
  refine Finset.sum_nonneg fun d hd => ?_
  simp only [Finset.mem_filter] at hd
  have hd1 : (1:ℝ) < (d:ℝ) := by exact_mod_cast hd.2
  refine mul_nonneg (mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _)) ?_
  refine Cap_nonneg (by positivity) ?_
  rw [div_le_iff₀ (by linarith)]
  nlinarith

/-- **Lemma 3 (contraction bound).** Under Hypothesis H1 at a window with index `N ≥ N_*`
(here only `M < N` is needed) and the cap-validity gates, `|M_λ(s_*) f_t - 1| ≤ D`. -/
theorem lemma3_contraction {t y dh kh : ℝ} {N : ℕ} {sstar gam kap f FA FB : ℂ}
    (ht : 0 ≤ t) (hMN : Mcut < N)
    (hFB : FB = ∑ k ∈ Finset.Icc 1 N, (bt t k : ℂ) * (k:ℂ) ^ (-sstar))
    (hFA : FA = ∑ k ∈ Finset.Icc 1 N, (((k:ℝ) ^ y : ℝ) : ℂ) * (bt t k : ℂ) *
        (k:ℂ) ^ (-(starRingEnd ℂ) sstar - kap))
    (hf : f = FB + gam * FA)
    (hRe : sig1 dh N t y ≤ sstar.re)
    (hkap : ‖kap‖ ≤ kh)
    (hgam : ‖gam‖ ≤ Gval N t y)
    (hG0 : 0 ≤ Gval N t y)
    (hcap1 : t/2 * Real.log N < sig1 dh (N:ℝ) t y)
    (hcap2 : t/2 * Real.log N < sig2 dh kh (N:ℝ) t y) :
    ‖Mlam sstar * f - 1‖ ≤ Dq dh kh (N:ℝ) t y := by
  set s1 : ℝ := sig1 dh (N:ℝ) t y with hs1def
  set s2 : ℝ := sig2 dh kh (N:ℝ) t y with hs2def
  have hN1 : 1 ≤ N := le_trans (by norm_num [Mcut]) hMN.le
  have hNR : (1:ℝ) ≤ (N:ℝ) := by exact_mod_cast hN1
  have hMcutN : ((Mcut : ℕ) : ℝ) < (N:ℝ) := by exact_mod_cast hMN
  -- the `B`-side
  have hBbound : ‖Mlam sstar * FB - 1‖ ≤ Pq t s1 + TRq t (N:ℝ) s1 := by
    rw [hFB, lemma2_convolution t sstar hMN]
    refine le_trans (norm_add_le _ _) (add_le_add ?_ ?_)
    · refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun m hm => ?_)
      simp only [Finset.mem_Icc] at hm
      have hm1 : 1 ≤ m := le_trans (by norm_num) hm.1
      have hm0 : 0 < m := hm1
      have hm1' : (1:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm1
      rw [norm_mul, Complex.norm_natCast_cpow_of_pos hm0, Complex.norm_real, Real.norm_eq_abs,
        Complex.neg_re]
      gcongr ; first | exact (bt_pos t _).le | exact abs_nonneg _ | assumption
    · refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun d hd => ?_)
      have hd1 : 1 ≤ d := one_le_of_mem_S hd
      have hd0 : 0 < d := hd1
      have hd1' : (1:ℝ) ≤ (d:ℝ) := by exact_mod_cast hd1
      have hdM : 1 ≤ Mcut / d := by
        refine (Nat.one_le_div_iff hd0).2 ?_
        have hd14 : d ≤ 14 := by fin_cases hd <;> norm_num
        simp only [Mcut]
        omega
      have hdMN : Mcut / d < N := lt_of_le_of_lt (Nat.div_le_self _ _) hMN
      have htail : ‖∑ k ∈ Finset.Ioc (Mcut / d) N, (bt t k : ℂ) * (k:ℂ) ^ (-sstar)‖
          ≤ Cap t ((Mcut / d : ℕ) : ℝ) (N:ℝ) s1 := by
        refine le_trans (norm_sum_bt_le _ (fun k hk => ?_) hRe) ?_
        · simp only [Finset.mem_Ioc] at hk
          exact Nat.lt_of_le_of_lt (Nat.zero_le _) hk.1
        · refine lemma1_cap ht (by exact_mod_cast hdM) (by exact_mod_cast hdMN) hcap1
            (le_refl _) hdMN (le_refl _)
      rw [norm_mul, norm_mul, Complex.norm_natCast_cpow_of_pos hd0, Complex.norm_real,
        Real.norm_eq_abs, Complex.neg_re]
      have hstep : |lam d| * (d:ℝ) ^ (-sstar.re) ≤ |lam d| * (d:ℝ) ^ (-s1) := by
        gcongr ; first | exact (bt_pos t _).le | exact abs_nonneg _ | assumption
      exact mul_le_mul hstep htail (norm_nonneg _)
        (mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _))
  -- the `A`-side
  have hABnonneg : 0 ≤ ABq t (N:ℝ) s2 (Gval (N:ℝ) t y) := by
    refine mul_nonneg hG0 (add_nonneg ?_ ?_)
    · exact Finset.sum_nonneg fun k _ =>
        mul_nonneg (bt_pos t k).le (Real.rpow_nonneg (by positivity) _)
    · exact Cap_nonneg (by norm_num [Mcut]) (le_of_lt hMcutN)
  have hAbound : ‖gam * FA‖ ≤ ABq t (N:ℝ) s2 (Gval (N:ℝ) t y) := by
    have hFAbound : ‖FA‖ ≤ (∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s2))
        + Cap t ((Mcut : ℕ) : ℝ) (N:ℝ) s2 := by
      have hterm : ∀ k ∈ Finset.Icc 1 N,
          ‖(((k:ℝ) ^ y : ℝ) : ℂ) * (bt t k : ℂ) * (k:ℂ) ^ (-(starRingEnd ℂ) sstar - kap)‖
            ≤ bt t k * (k:ℝ) ^ (-s2) := by
        intro k hk
        simp only [Finset.mem_Icc] at hk
        have hk0 : 0 < k := hk.1
        have hk1 : (1:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk.1
        have hk0' : (0:ℝ) < (k:ℝ) := by positivity
        rw [norm_mul, norm_mul, Complex.norm_natCast_cpow_of_pos hk0, Complex.norm_real,
          Real.norm_eq_abs, Complex.norm_real, Real.norm_eq_abs,
          abs_of_pos (bt_pos t k), abs_of_pos (Real.rpow_pos_of_pos hk0' y)]
        have hre : (-(starRingEnd ℂ) sstar - kap).re = -sstar.re - kap.re := by
          simp [Complex.sub_re, Complex.neg_re, Complex.conj_re]
        rw [hre, mul_comm ((k:ℝ) ^ y) (bt t k), mul_assoc, ← Real.rpow_add hk0']
        have hkapre : -kap.re ≤ kh :=
          le_trans (le_trans (neg_le_abs _) (Complex.abs_re_le_norm kap)) hkap
        have hs21 : s2 = s1 - y - kh := by
          simp only [hs1def, hs2def, sig1, sig2]; ring
        gcongr <;>
          first
            | exact (bt_pos t _).le
            | exact abs_nonneg _
            | assumption
            | (rw [hs21]; linarith)
      rw [hFA]
      refine le_trans (le_trans (norm_sum_le _ _) (Finset.sum_le_sum hterm)) ?_
      have hsplit : ∑ k ∈ Finset.Icc 1 N, bt t k * (k:ℝ) ^ (-s2)
          = (∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s2))
            + ∑ k ∈ Finset.Ioc Mcut N, bt t k * (k:ℝ) ^ (-s2) := by
        have hIcc : ∀ n : ℕ, Finset.Icc 1 n = Finset.Ioc 0 n := by
          intro n; ext k; simp only [Finset.mem_Icc, Finset.mem_Ioc]; omega
        rw [hIcc, hIcc]
        exact (Finset.sum_Ioc_consecutive _ (Nat.zero_le _) hMN.le).symm
      rw [hsplit]
      gcongr
      exact lemma1_cap ht (by norm_num [Mcut]) hMcutN hcap2 (le_refl _) hMN (le_refl _)
    calc ‖gam * FA‖ = ‖gam‖ * ‖FA‖ := norm_mul _ _
      _ ≤ Gval (N:ℝ) t y * ((∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s2))
            + Cap t ((Mcut : ℕ) : ℝ) (N:ℝ) s2) := by
          refine mul_le_mul hgam hFAbound (norm_nonneg _) hG0
      _ = ABq t (N:ℝ) s2 (Gval (N:ℝ) t y) := rfl
  -- combine
  have hsplitf : Mlam sstar * f - 1 = (Mlam sstar * FB - 1) + Mlam sstar * (gam * FA) := by
    rw [hf]; ring
  have hOV : 0 ≤ OVq t (N:ℝ) s1 := OVq_nonneg (by linarith)
  calc ‖Mlam sstar * f - 1‖ ≤ ‖Mlam sstar * FB - 1‖ + ‖Mlam sstar * (gam * FA)‖ := by
        rw [hsplitf]; exact norm_add_le _ _
    _ ≤ (Pq t s1 + TRq t (N:ℝ) s1) + Mmaxq s1 * ABq t (N:ℝ) s2 (Gval (N:ℝ) t y) := by
        refine add_le_add hBbound ?_
        rw [norm_mul]
        exact mul_le_mul (norm_Mlam_le hRe) hAbound (norm_nonneg _) (Mmaxq_nonneg s1)
    _ ≤ Dq dh kh (N:ℝ) t y := by
        rw [Dq]
        linarith

end Job2
