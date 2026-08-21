import RequestProject.WindowFreeze

/-!
# Lemma 2 (site bracketing) and Theorem 3 (exact half-open endpoint coverage)
-/

open scoped Real

set_option maxHeartbeats 1000000

namespace WindowFreeze

/-! ## Monotonicity of the grid `N ↦ x_N` -/

lemma qq_lt_qq {M N : ℤ} (hM : 0 ≤ M) (hMN : M < N) : qq M < qq N := by
  have h0 : (0 : ℝ) ≤ (M : ℝ) := by exact_mod_cast hM
  have h1 : (M : ℝ) < (N : ℝ) := by exact_mod_cast hMN
  have : (M : ℝ) ^ 2 < (N : ℝ) ^ 2 := by nlinarith
  simp only [qq]
  linarith

lemma xx_lt_xx {M N : ℤ} (hM : 0 ≤ M) (hMN : M < N) : xx M < xx N := by
  have hpi := Real.pi_pos
  have := qq_lt_qq hM hMN
  simp only [xx]
  have h4 : (0 : ℝ) < 4 * Real.pi := by positivity
  exact mul_lt_mul_of_pos_left this h4

lemma xx_le_xx {M N : ℤ} (hM : 0 ≤ M) (hMN : M ≤ N) : xx M ≤ xx N := by
  rcases eq_or_lt_of_le hMN with rfl | h
  · exact le_rfl
  · exact (xx_lt_xx hM h).le

/-- Each window is a nonempty half-open interval. -/
lemma window_nonempty {N : ℤ} (hN : 0 ≤ N) : (W N).Nonempty :=
  Set.nonempty_Ico.mpr (xx_lt_xx hN (by omega))

/-! ## Lemma 2 : site bracketing -/

lemma one_sub_y0sq : (1 : ℝ) - y0sq = 2412323 / 2500000 := by
  rw [y0sq]; norm_num

lemma sqrt_one_sub_y0sq_lower : (0.982308098 : ℝ) < Real.sqrt (1 - y0sq) := by
  rw [one_sub_y0sq]
  exact (Real.lt_sqrt (by norm_num)).mpr (by norm_num)

lemma sqrt_one_sub_y0sq_upper : Real.sqrt (1 - y0sq) < (0.982308099 : ℝ) := by
  rw [one_sub_y0sq]
  exact (Real.sqrt_lt' (by norm_num)).mpr (by norm_num)

lemma qq_690988 : qq 690988 = 6111544526643071 / 12800 := by
  rw [qq, t0]; norm_num

lemma qq_690989 : qq 690989 = 6111562215948671 / 12800 := by
  rw [qq, t0]; norm_num

/-- **Lemma 2, lower margin.** `x_* - x_{690988} > 5377393.9878`. -/
theorem site_margin_left : (5377393.9878 : ℝ) < xstar - xx 690988 := by
  have hpi : Real.pi < 3.14159265358979323847 := Real.pi_lt_d20
  have hs := sqrt_one_sub_y0sq_lower
  have hq : (0 : ℝ) < 6111544526643071 / 12800 := by norm_num
  have hx : xx 690988 < 4 * 3.14159265358979323847 * (6111544526643071 / 12800) := by
    rw [xx, qq_690988]
    have : Real.pi * (6111544526643071 / 12800) <
        3.14159265358979323847 * (6111544526643071 / 12800) :=
      mul_lt_mul_of_pos_right hpi hq
    linarith
  have hnum : 4 * (3.14159265358979323847 : ℝ) * (6111544526643071 / 12800) <
      6000000185827 + 0.982308098 - 5377393.9878 := by norm_num
  simp only [xstar, Xsite]
  linarith

/-- **Lemma 2, upper margin.** `x_{690989} - x_* > 11989041.1746`. -/
theorem site_margin_right : (11989041.1746 : ℝ) < xx 690989 - xstar := by
  have hpi : (3.14159265358979323846 : ℝ) < Real.pi := Real.pi_gt_d20
  have hs := sqrt_one_sub_y0sq_upper
  have hq : (0 : ℝ) < 6111562215948671 / 12800 := by norm_num
  have hx : 4 * (3.14159265358979323846 : ℝ) * (6111562215948671 / 12800) < xx 690989 := by
    rw [xx, qq_690989]
    have : (3.14159265358979323846 : ℝ) * (6111562215948671 / 12800) <
        Real.pi * (6111562215948671 / 12800) :=
      mul_lt_mul_of_pos_right hpi hq
    linarith
  have hnum : 6000000185827 + 0.982308099 + 11989041.1746 <
      4 * (3.14159265358979323846 : ℝ) * (6111562215948671 / 12800) := by norm_num
  simp only [xstar, Xsite]
  linarith

/-- **Lemma 2 (site bracketing).** `x_{690988} < x_* < x_{690989}`. -/
theorem site_bracket : xx 690988 < xstar ∧ xstar < xx 690989 := by
  constructor
  · have := site_margin_left; linarith
  · have := site_margin_right; linarith

/-! ## Theorem 3 : exact half-open endpoint coverage -/

/-- The union of consecutive half-open windows over an integer range is the single
half-open interval spanning the range. -/
lemma iUnion_window_Icc {a : ℤ} (ha : 0 ≤ a) (b : ℤ) (hab : a ≤ b) :
    (⋃ N ∈ Finset.Icc a b, Set.Ico (xx N) (xx (N + 1))) = Set.Ico (xx a) (xx (b + 1)) := by
  induction b, hab using Int.le_induction with
  | base => simp
  | succ b hb ih =>
      have hins : Finset.Icc a (b + 1) = insert (b + 1) (Finset.Icc a b) := by
        ext n; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
      rw [hins, Finset.set_biUnion_insert, ih, Set.union_comm]
      exact Set.Ico_union_Ico_eq_Ico (xx_le_xx ha (by omega)) (xx_le_xx (by omega) (by omega))

/-- **Theorem 3 (exact half-open endpoint coverage).**
`[x_*, x_{690989}) ∪ ⋃_{N=690989}^{3840000} [x_N, x_{N+1}) = [x_*, x_{3840001})`. -/
theorem window_cover :
    Set.Ico xstar (xx 690989) ∪
        (⋃ N ∈ Finset.Icc (690989 : ℤ) 3840000, Set.Ico (xx N) (xx (N + 1)))
      = Set.Ico xstar (xx 3840001) := by
  rw [iUnion_window_Icc (by norm_num) 3840000 (by norm_num)]
  norm_num
  exact Set.Ico_union_Ico_eq_Ico site_bracket.2.le (xx_le_xx (by norm_num) (by norm_num))

/-- Distinct windows are disjoint: at `x = x_{N+1}` the point belongs to `W_{N+1}`,
not to `W_N`. -/
theorem window_pairwise_disjoint {M N : ℤ} (hM : 0 ≤ M) (hN : 0 ≤ N) (hMN : M ≠ N) :
    Disjoint (W M) (W N) := by
  wlog h : M < N generalizing M N
  · exact (this hN hM hMN.symm (by omega)).symm
  have h1 : xx (M + 1) ≤ xx N := xx_le_xx (by omega) (by omega)
  simp only [W, Set.disjoint_left, Set.mem_Ico]
  rintro x ⟨-, hx2⟩ ⟨hx3, -⟩
  linarith

/-- The initial piece `[x_*, x_{690989})` is disjoint from every window with
`N ≥ 690989`. -/
theorem first_piece_disjoint {N : ℤ} (hN : 690989 ≤ N) :
    Disjoint (Set.Ico xstar (xx 690989)) (W N) := by
  have h1 : xx 690989 ≤ xx N := xx_le_xx (by norm_num) hN
  simp only [W, Set.disjoint_left, Set.mem_Ico]
  rintro x ⟨-, hx2⟩ ⟨hx3, -⟩
  linarith

end WindowFreeze
