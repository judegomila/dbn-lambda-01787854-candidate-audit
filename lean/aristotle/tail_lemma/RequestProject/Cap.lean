import RequestProject.Basic

/-!
# Lemma 1 : the endpoint cap

For `1 ≤ a < c`, `t ≥ 0` and `σ > (t/2) log c`, the sum of `b_t(n) n^{-σ}` over integers
`J < n ≤ K` with `a ≤ J < K ≤ c` is bounded by `Cap_t(a,c;σ)`.
-/

namespace Job2

open Finset Real MeasureTheory intervalIntegral

/-- `b_t(u) u^{-σ} = exp((t/4) log²u - σ log u)` for `u > 0`. -/
lemma bt_mul_rpow_eq_exp {t s u : ℝ} (hu : 0 < u) :
    bt t u * u ^ (-s) = Real.exp (t/4 * Real.log u ^ 2 - s * Real.log u) := by
  rw [bt, Real.rpow_def_of_pos hu, ← Real.exp_add]
  ring_nf

/-- `b_t(u) u^{-σ} = E_{t,σ}(u)/u` for `u > 0`. -/
lemma bt_mul_rpow_eq_Ecap_div {t s u : ℝ} (hu : 0 < u) :
    bt t u * u ^ (-s) = Ecap t s u / u := by
  rw [bt_mul_rpow_eq_exp hu, Ecap, eq_div_iff (ne_of_gt hu)]
  nth_rewrite 3 [← Real.exp_log hu]
  rw [← Real.exp_add]
  ring_nf

/-- The summand `u ↦ b_t(u) u^{-σ}` is antitone on `[a,c]` as soon as `σ > (t/2) log c`. -/
lemma bt_rpow_antitoneOn {t s a c : ℝ} (ht : 0 ≤ t) (ha : 0 < a)
    (hs : t/2 * Real.log c < s) :
    AntitoneOn (fun u : ℝ => bt t u * u ^ (-s)) (Set.Icc a c) := by
  intro u hu v hv huv
  have hu0 : 0 < u := lt_of_lt_of_le ha hu.1
  have hv0 : 0 < v := lt_of_lt_of_le hu0 huv
  have hlu : Real.log u ≤ Real.log v := Real.log_le_log hu0 huv
  have hlv : Real.log v ≤ Real.log c := Real.log_le_log hv0 hv.2
  show bt t v * v ^ (-s) ≤ bt t u * u ^ (-s)
  rw [bt_mul_rpow_eq_exp hu0, bt_mul_rpow_eq_exp hv0]
  apply Real.exp_le_exp.2
  nlinarith [mul_nonneg ht (sub_nonneg.2 hlu), sub_nonneg.2 hlu]

/-- Maximum principle for `E_{t,σ}`: on `[a,c]` it is bounded by the maximum of its endpoint
values (`t ≥ 0`, `0 < a`). -/
lemma Ecap_le_max {t s a c u : ℝ} (ht : 0 ≤ t) (ha : 0 < a) (hau : a ≤ u) (huc : u ≤ c) :
    Ecap t s u ≤ max (Ecap t s a) (Ecap t s c) := by
  have hu0 : 0 < u := lt_of_lt_of_le ha hau
  have hla : Real.log a ≤ Real.log u := Real.log_le_log ha hau
  have hlc : Real.log u ≤ Real.log c := Real.log_le_log hu0 huc
  set la := Real.log a with hla'
  set l := Real.log u with hl'
  set lc := Real.log c with hlc'
  have key : (1-s) * l + t/4 * l ^ 2 ≤
      max ((1-s) * la + t/4 * la ^ 2) ((1-s) * lc + t/4 * lc ^ 2) := by
    rcases le_total ((1-s) * la + t/4 * la ^ 2) ((1-s) * lc + t/4 * lc ^ 2) with h | h
    · refine le_trans ?_ (le_max_right _ _)
      rcases eq_or_lt_of_le (hla.trans hlc) with hEq | hlt
      · have hlle : l = lc := le_antisymm hlc (by linarith)
        rw [hlle]
      · have hb : 0 ≤ (1-s) + t/4*(la+lc) := by
          by_contra hcon
          push_neg at hcon
          nlinarith
        have hb2 : 0 ≤ (1-s) + t/4*(l+lc) := by nlinarith [mul_nonneg ht (sub_nonneg.2 hla)]
        nlinarith [mul_nonneg (sub_nonneg.2 hlc) hb2]
    · refine le_trans ?_ (le_max_left _ _)
      rcases eq_or_lt_of_le (hla.trans hlc) with hEq | hlt
      · have hlle : l = la := le_antisymm (by linarith) hla
        rw [hlle]
      · have hb : (1-s) + t/4*(la+lc) ≤ 0 := by
          by_contra hcon
          push_neg at hcon
          nlinarith
        have hb2 : (1-s) + t/4*(l+la) ≤ 0 := by nlinarith [mul_nonneg ht (sub_nonneg.2 hlc)]
        nlinarith [mul_nonneg (sub_nonneg.2 hla) (neg_nonneg.2 hb2)]
  simp only [Ecap, ← hla', ← hl', ← hlc']
  rcases le_max_iff.1 key with h | h
  · exact le_max_of_le_left (Real.exp_le_exp.2 h)
  · exact le_max_of_le_right (Real.exp_le_exp.2 h)

/-- **Lemma 1 (endpoint cap).** For `t ≥ 0`, real `σ` with `σ > (t/2) log c`, and integers
`a ≤ J < K ≤ c` with `1 ≤ a < c`,
`∑_{J < n ≤ K} b_t(n) n^{-σ} ≤ Cap_t(a,c;σ)`. -/
theorem lemma1_cap {t s a c : ℝ} (ht : 0 ≤ t) (ha : 1 ≤ a) (hac : a < c)
    (hs : t/2 * Real.log c < s) {J K : ℕ} (haJ : a ≤ (J:ℝ)) (hJK : J < K) (hKc : (K:ℝ) ≤ c) :
    ∑ n ∈ Finset.Ioc J K, bt t n * (n:ℝ) ^ (-s) ≤ Cap t a c s := by
  have ha0 : (0:ℝ) < a := lt_of_lt_of_le one_pos ha
  have hJ0 : (0:ℝ) < (J:ℝ) := lt_of_lt_of_le ha0 haJ
  have hJK' : (J:ℝ) ≤ (K:ℝ) := by exact_mod_cast hJK.le
  have hIcc : Set.Icc (J:ℝ) (K:ℝ) ⊆ Set.Icc a c := Set.Icc_subset_Icc haJ hKc
  set f : ℝ → ℝ := fun u => bt t u * u ^ (-s) with hf
  have hanti : AntitoneOn f (Set.Icc a c) := bt_rpow_antitoneOn ht ha0 hs
  have hantiJK : AntitoneOn f (Set.Icc (J:ℝ) (K:ℝ)) := hanti.mono hIcc
  -- step 1 : sum ≤ integral
  have hsum : ∑ n ∈ Finset.Ioc J K, f n ≤ ∫ x in (J:ℝ)..(K:ℝ), f x := by
    have himg : Finset.Ioc J K = (Finset.Ico J K).image (· + 1) := by
      ext n
      simp only [Finset.mem_Ioc, Finset.mem_image, Finset.mem_Ico]
      constructor
      · rintro ⟨h1, h2⟩
        exact ⟨n - 1, by omega, by omega⟩
      · rintro ⟨m, ⟨h1, h2⟩, rfl⟩
        omega
    rw [himg, Finset.sum_image (by intro x _ y _ h; simpa using h)]
    exact hantiJK.sum_le_integral_Ico hJK.le
  -- step 2 : integral ≤ Mx * log (K/J)
  set Mx : ℝ := max (Ecap t s a) (Ecap t s c) with hMx
  have hMx0 : 0 ≤ Mx := le_trans (Real.exp_nonneg _) (le_max_left _ _)
  have huIcc : Set.uIcc (J:ℝ) (K:ℝ) = Set.Icc (J:ℝ) (K:ℝ) := Set.uIcc_of_le hJK'
  have hcont : ContinuousOn f (Set.uIcc (J:ℝ) (K:ℝ)) := by
    rw [huIcc, hf]
    apply ContinuousOn.mul
    · apply Real.continuous_exp.comp_continuousOn
      apply ContinuousOn.mul continuousOn_const
      apply ContinuousOn.pow
      apply Real.continuousOn_log.mono
      intro x hx
      exact ne_of_gt (lt_of_lt_of_le hJ0 hx.1)
    · apply ContinuousOn.rpow_const continuousOn_id
      intro x hx
      exact Or.inl (ne_of_gt (lt_of_lt_of_le hJ0 hx.1))
  have hint1 : IntervalIntegrable f volume (J:ℝ) (K:ℝ) := hcont.intervalIntegrable
  have hcont2 : ContinuousOn (fun u : ℝ => Mx / u) (Set.uIcc (J:ℝ) (K:ℝ)) := by
    rw [huIcc]
    apply ContinuousOn.div continuousOn_const continuousOn_id
    intro x hx
    exact ne_of_gt (lt_of_lt_of_le hJ0 hx.1)
  have hint2 : IntervalIntegrable (fun u : ℝ => Mx / u) volume (J:ℝ) (K:ℝ) :=
    hcont2.intervalIntegrable
  have hmono : (∫ x in (J:ℝ)..(K:ℝ), f x) ≤ ∫ x in (J:ℝ)..(K:ℝ), Mx / x := by
    apply intervalIntegral.integral_mono_on hJK' hint1 hint2
    intro x hx
    have hx0 : 0 < x := lt_of_lt_of_le hJ0 hx.1
    show bt t x * x ^ (-s) ≤ Mx / x
    rw [bt_mul_rpow_eq_Ecap_div hx0]
    gcongr
    exact Ecap_le_max ht ha0 (le_trans haJ hx.1) (le_trans hx.2 hKc)
  have h0 : (0:ℝ) ∉ Set.uIcc (J:ℝ) (K:ℝ) := by
    rw [huIcc]
    intro hmem
    exact absurd hmem.1 (not_le.2 hJ0)
  have hlog : (∫ x in (J:ℝ)..(K:ℝ), Mx / x) = Mx * Real.log ((K:ℝ)/(J:ℝ)) := by
    simp_rw [div_eq_mul_inv]
    rw [intervalIntegral.integral_const_mul, integral_inv h0, div_eq_mul_inv]
  -- step 3 : compare the logs
  have hK0 : (0:ℝ) < (K:ℝ) := lt_of_lt_of_le hJ0 hJK'
  have hlogle : Real.log ((K:ℝ)/(J:ℝ)) ≤ Real.log (c/a) := by
    apply Real.log_le_log (div_pos hK0 hJ0)
    have hc0 : (0:ℝ) ≤ c := le_of_lt (ha0.trans hac)
    calc (K:ℝ)/(J:ℝ) ≤ c/(J:ℝ) := by gcongr
      _ ≤ c/a := by gcongr
  calc ∑ n ∈ Finset.Ioc J K, bt t n * (n:ℝ) ^ (-s) = ∑ n ∈ Finset.Ioc J K, f n := rfl
    _ ≤ ∫ x in (J:ℝ)..(K:ℝ), f x := hsum
    _ ≤ ∫ x in (J:ℝ)..(K:ℝ), Mx / x := hmono
    _ = Mx * Real.log ((K:ℝ)/(J:ℝ)) := hlog
    _ ≤ Mx * Real.log (c/a) := mul_le_mul_of_nonneg_left hlogle hMx0
    _ = Cap t a c s := rfl

end Job2
