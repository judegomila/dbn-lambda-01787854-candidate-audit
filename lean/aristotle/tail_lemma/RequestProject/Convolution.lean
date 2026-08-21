import RequestProject.Basic

/-!
# Lemma 2 : the exact convolution identity

`M_λ(s) F_B - 1` splits as the short convolution sum `∑_{m=2}^{M} c_m(t) m^{-s}` plus the
eleven tails `∑_{⌊M/d⌋ < k ≤ N} b_t(k) k^{-s}` weighted by `λ_d d^{-s}`.
-/

namespace Job2

open Finset

lemma one_le_of_mem_S {d : ℕ} (hd : d ∈ S) : 1 ≤ d := by
  fin_cases hd <;> norm_num

/-- `c_1(t) = 1`. -/
@[simp] lemma cconv_one (t : ℝ) : cconv t 1 = 1 := by
  have h : S.filter (· ∣ 1) = {1} := by decide +kernel
  rw [cconv, h]
  simp [lam, bt]

/-- The pairs `(d,k)` with `d ∈ 𝒮`, `k ≥ 1` and `dk ≤ M`. -/
private def pairs : Finset (ℕ × ℕ) :=
  (S ×ˢ Finset.Icc 1 Mcut).filter (fun p => p.1 * p.2 ≤ Mcut)

private noncomputable def Fterm (t : ℝ) (s : ℂ) (d k : ℕ) : ℂ :=
  (lam d : ℂ) * (bt t k : ℂ) * ((d * k : ℕ) : ℂ) ^ (-s)

private lemma mem_pairs {p : ℕ × ℕ} :
    p ∈ pairs ↔ p.1 ∈ S ∧ 1 ≤ p.2 ∧ p.2 ≤ Mcut ∧ p.1 * p.2 ≤ Mcut := by
  simp [pairs, Finset.mem_filter, Finset.mem_product, Finset.mem_Icc, and_assoc]

private lemma sum_pairs_eq (t : ℝ) (s : ℂ) :
    ∑ d ∈ S, ∑ k ∈ Finset.Icc 1 (Mcut / d), Fterm t s d k
      = ∑ p ∈ pairs, Fterm t s p.1 p.2 := by
  rw [pairs, Finset.sum_filter, Finset.sum_product]
  refine Finset.sum_congr rfl (fun d hd => ?_)
  have hd1 : 1 ≤ d := one_le_of_mem_S hd
  rw [← Finset.sum_filter]
  refine Finset.sum_congr ?_ (fun k _ => rfl)
  ext k
  simp only [Finset.mem_Icc, Finset.mem_filter]
  rw [Nat.le_div_iff_mul_le (by omega : 0 < d)]
  constructor
  · rintro ⟨h1, h2⟩
    have hkm : k ≤ Mcut := le_trans (Nat.le_mul_of_pos_right k (by omega)) h2
    exact ⟨⟨h1, hkm⟩, by rwa [Nat.mul_comm]⟩
  · rintro ⟨⟨h1, _⟩, h3⟩
    exact ⟨h1, by rwa [Nat.mul_comm] at h3⟩

private lemma fiber_sum (t : ℝ) (s : ℂ) {m : ℕ} (hm : m ∈ Finset.Icc 1 Mcut) :
    ∑ p ∈ pairs with p.1 * p.2 = m, Fterm t s p.1 p.2 = (cconv t m : ℂ) * (m : ℂ) ^ (-s) := by
  simp only [Finset.mem_Icc] at hm
  rw [cconv]
  push_cast
  rw [Finset.sum_mul]
  refine Finset.sum_nbij' (fun p => p.1) (fun d => (d, m / d)) ?_ ?_ ?_ ?_ ?_
  · rintro ⟨d, k⟩ hp
    simp only [Finset.mem_filter, mem_pairs] at hp
    simp only [Finset.mem_filter]
    exact ⟨hp.1.1, ⟨k, hp.2.symm⟩⟩
  · intro d hd
    simp only [Finset.mem_filter] at hd
    obtain ⟨hdS, hdvd⟩ := hd
    have hd1 : 1 ≤ d := one_le_of_mem_S hdS
    have hdm : d * (m / d) = m := Nat.mul_div_cancel' hdvd
    have hmd1 : 1 ≤ m / d :=
      (Nat.one_le_div_iff (by omega)).2 (Nat.le_of_dvd (by omega) hdvd)
    rw [Finset.mem_filter]
    exact ⟨mem_pairs.2 ⟨hdS, hmd1, le_trans (Nat.div_le_self _ _) hm.2,
      by rw [hdm]; exact hm.2⟩, hdm⟩
  · rintro ⟨d, k⟩ hp
    simp only [Finset.mem_filter, mem_pairs] at hp
    have hd1 : 1 ≤ d := one_le_of_mem_S hp.1.1
    have hk : m / d = k := by
      rw [← hp.2, Nat.mul_div_cancel_left _ (by omega)]
    simp [hk]
  · intro d hd
    simp
  · rintro ⟨d, k⟩ hp
    simp only [Finset.mem_filter, mem_pairs] at hp
    have hd1 : 1 ≤ d := one_le_of_mem_S hp.1.1
    have hk : m / d = k := by
      rw [← hp.2, Nat.mul_div_cancel_left _ (by omega)]
    simp only [Fterm, hp.2, hk]

/-- The head part of the convolution: `∑_{d ∈ 𝒮} λ_d d^{-s} ∑_{k ≤ ⌊M/d⌋} b_t(k) k^{-s}
= ∑_{m ≤ M} c_m(t) m^{-s}`. -/
lemma conv_head (t : ℝ) (s : ℂ) :
    ∑ d ∈ S, (lam d : ℂ) * (d:ℂ) ^ (-s) *
        ∑ k ∈ Finset.Icc 1 (Mcut / d), (bt t k : ℂ) * (k:ℂ) ^ (-s)
      = ∑ m ∈ Finset.Icc 1 Mcut, (cconv t m : ℂ) * (m:ℂ) ^ (-s) := by
  have hstep : ∀ d ∈ S, (lam d : ℂ) * (d:ℂ) ^ (-s) *
      (∑ k ∈ Finset.Icc 1 (Mcut / d), (bt t k : ℂ) * (k:ℂ) ^ (-s))
      = ∑ k ∈ Finset.Icc 1 (Mcut / d), Fterm t s d k := by
    intro d _
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun k _ => ?_)
    simp only [Fterm]
    push_cast
    rw [Complex.natCast_mul_natCast_cpow]
    ring
  rw [Finset.sum_congr rfl hstep, sum_pairs_eq]
  have hmaps : ∀ p ∈ pairs, p.1 * p.2 ∈ Finset.Icc 1 Mcut := by
    rintro ⟨d, k⟩ hp
    rw [mem_pairs] at hp
    simp only [Finset.mem_Icc]
    have hd1 : 1 ≤ d := one_le_of_mem_S hp.1
    have hk1 : 1 ≤ k := hp.2.1
    exact ⟨Nat.one_le_iff_ne_zero.2 (Nat.mul_ne_zero (by omega) (by omega)), hp.2.2.2⟩
  rw [← Finset.sum_fiberwise_of_maps_to hmaps (fun p => Fterm t s p.1 p.2)]
  exact Finset.sum_congr rfl (fun m hm => fiber_sum t s hm)

/-- **Lemma 2 (exact convolution).** With `M < N`,
`M_λ(s) F_B - 1 = ∑_{m=2}^{M} c_m(t) m^{-s} + ∑_{d ∈ 𝒮} λ_d d^{-s} ∑_{⌊M/d⌋ < k ≤ N} b_t(k) k^{-s}`.
-/
theorem lemma2_convolution (t : ℝ) (s : ℂ) {N : ℕ} (hMN : Mcut < N) :
    Mlam s * (∑ k ∈ Finset.Icc 1 N, (bt t k : ℂ) * (k:ℂ) ^ (-s)) - 1
      = (∑ m ∈ Finset.Icc 2 Mcut, (cconv t m : ℂ) * (m:ℂ) ^ (-s))
        + ∑ d ∈ S, (lam d : ℂ) * (d:ℂ) ^ (-s) *
            ∑ k ∈ Finset.Ioc (Mcut / d) N, (bt t k : ℂ) * (k:ℂ) ^ (-s) := by
  have hIcc : ∀ n : ℕ, Finset.Icc 1 n = Finset.Ioc 0 n := by
    intro n; ext k; simp only [Finset.mem_Icc, Finset.mem_Ioc]; omega
  -- split each inner sum at ⌊M/d⌋
  have hsplit : ∀ d ∈ S, (∑ k ∈ Finset.Icc 1 N, (bt t k : ℂ) * (k:ℂ) ^ (-s))
      = (∑ k ∈ Finset.Icc 1 (Mcut / d), (bt t k : ℂ) * (k:ℂ) ^ (-s))
        + ∑ k ∈ Finset.Ioc (Mcut / d) N, (bt t k : ℂ) * (k:ℂ) ^ (-s) := by
    intro d hd
    have hdN : Mcut / d ≤ N := le_trans (Nat.div_le_self _ _) hMN.le
    rw [hIcc, hIcc]
    exact (Finset.sum_Ioc_consecutive _ (Nat.zero_le _) hdN).symm
  have hLHS : Mlam s * (∑ k ∈ Finset.Icc 1 N, (bt t k : ℂ) * (k:ℂ) ^ (-s))
      = (∑ d ∈ S, (lam d : ℂ) * (d:ℂ) ^ (-s) *
            ∑ k ∈ Finset.Icc 1 (Mcut / d), (bt t k : ℂ) * (k:ℂ) ^ (-s))
        + ∑ d ∈ S, (lam d : ℂ) * (d:ℂ) ^ (-s) *
            ∑ k ∈ Finset.Ioc (Mcut / d) N, (bt t k : ℂ) * (k:ℂ) ^ (-s) := by
    rw [Mlam, Finset.sum_mul, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun d hd => ?_)
    rw [hsplit d hd, mul_add]
  rw [hLHS, conv_head]
  have hone : Finset.Icc 1 Mcut = insert 1 (Finset.Icc 2 Mcut) := by
    ext k
    simp only [Finset.mem_Icc, Finset.mem_insert]
    constructor
    · rintro ⟨h1, h2⟩
      rcases Nat.eq_or_lt_of_le h1 with h | h
      · exact Or.inl h.symm
      · exact Or.inr ⟨h, h2⟩
    · rintro (rfl | ⟨h1, h2⟩)
      · exact ⟨le_refl _, by norm_num [Mcut]⟩
      · omega
  rw [hone, Finset.sum_insert (by simp)]
  simp [cconv_one]
  ring

end Job2
