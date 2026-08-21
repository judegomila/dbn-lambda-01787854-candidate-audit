import Mathlib

/-!
# Native Triangle binding: stored floors lower-bound the normalized `|f_t|`

This file formalizes the statements requested in `job4_native_binding.tex`.

## Setup

For a real parameter `t` we put `b_t(u) = exp((t/4) log² u)` (`NativeBinding.bt`).
For a finite set `P` of primes with `D = ∏_{p ∈ P} p` and each divisor `d ∣ D` we put
`λ_d = ∏_{p ∣ d} (-b_t(p))` (`NativeBinding.lam`), so that the mollifier
`E(z) = ∏_{p ∈ P} (1 - b_t(p) p^{-z})` equals the Dirichlet polynomial
`∑_{d ∣ D} λ_d d^{-z}`.

## Main results

* `NativeBinding.eulerFactorProd_eq_dirichletSum` : the Euler expansion
  `E(z) = ∑_{d ∣ D} λ_d d^{-z}`.
* `NativeBinding.eulerFactorProd_mul_Asum` and `NativeBinding.conj_eulerFactorProd_mul_Csum` :
  the two exact Dirichlet-convolution identities (target (a)), together with
  `NativeBinding.Bcoef_one` and `NativeBinding.Acoef_one` (`B_{N,1} = A_{N,1} = 1`).
* `NativeBinding.norm_cpow_neg_sub_one_le` : the elementary estimate `|m^{-κ} - 1| ≤ m^{k} - 1`
  (target (b)).
* `NativeBinding.native_triangle` : the Native Triangle lemma (target (c)).
-/

namespace NativeBinding

open Finset

/-! ### Definitions -/

/-- `b_t(u) = exp((t/4) log² u)`, evaluated at natural numbers. -/
noncomputable def bt (t : ℝ) (m : ℕ) : ℝ := Real.exp (t / 4 * (Real.log m) ^ 2)

/-- `λ_d = ∏_{p ∣ d} (-b_t(p))`. -/
noncomputable def lam (t : ℝ) (d : ℕ) : ℝ := ∏ p ∈ d.primeFactors, (-(bt t p))

/-- The mollifier `E(z) = ∏_{p ∈ P} (1 - b_t(p) p^{-z})`. -/
noncomputable def eulerFactorProd (t : ℝ) (P : Finset ℕ) (z : ℂ) : ℂ :=
  ∏ p ∈ P, (1 - (bt t p : ℂ) * (p : ℂ) ^ (-z))

/-- The Dirichlet polynomial `∑_{d ∣ D} λ_d d^{-z}`. -/
noncomputable def dirichletSum (t : ℝ) (D : ℕ) (z : ℂ) : ℂ :=
  ∑ d ∈ D.divisors, (lam t d : ℂ) * (d : ℂ) ^ (-z)

/-- The generic convolution coefficient `∑_{d ∣ D, d ∣ n, n/d ≤ N} λ_d w(n/d)`. -/
noncomputable def coeff (t : ℝ) (D N : ℕ) (w : ℕ → ℝ) (n : ℕ) : ℝ :=
  ∑ d ∈ D.divisors with (d ∣ n ∧ n / d ≤ N), lam t d * w (n / d)

/-- `B_{N,n} = ∑_{d ∣ D, d ∣ n, n/d ≤ N} λ_d b_t(n/d)`. -/
noncomputable def Bcoef (t : ℝ) (D N n : ℕ) : ℝ := coeff t D N (bt t) n

/-- `A_{N,n} = ∑_{d ∣ D, d ∣ n, n/d ≤ N} λ_d b_t(n/d) (n/d)^y`. -/
noncomputable def Acoef (t y : ℝ) (D N n : ℕ) : ℝ :=
  coeff t D N (fun m => bt t m * (m : ℝ) ^ y) n

/-- `A = ∑_{m=1}^N b_t(m) m^{-s}`. -/
noncomputable def Asum (t : ℝ) (N : ℕ) (s : ℂ) : ℂ :=
  ∑ m ∈ Icc 1 N, (bt t m : ℂ) * (m : ℂ) ^ (-s)

/-- `C_κ = ∑_{m=1}^N m^y b_t(m) m^{-conj s - κ}`. -/
noncomputable def Csum (t y : ℝ) (N : ℕ) (s kappa : ℂ) : ℂ :=
  ∑ m ∈ Icc 1 N, (((m : ℝ) ^ y * bt t m : ℝ) : ℂ) * (m : ℂ) ^ (-(starRingEnd ℂ) s - kappa)

/-- `M_N = ∑_{d ∣ D} |λ_d| d^{-σ_N}`. -/
noncomputable def MN (t : ℝ) (D : ℕ) (sig : ℝ) : ℝ :=
  ∑ d ∈ D.divisors, |lam t d| * (d : ℝ) ^ (-sig)

/-- `C_N = ∑_{m=2}^N b_t(m) (m^{k_N} - 1) m^{y - σ_N}`. -/
noncomputable def CN (t y : ℝ) (N : ℕ) (sig k : ℝ) : ℝ :=
  ∑ m ∈ Icc 2 N, bt t m * ((m : ℝ) ^ k - 1) * (m : ℝ) ^ (y - sig)

/-- `Q_N = 1 - g_N - ∑_{n=2}^{DN} (|B_{N,n}| + g_N |A_{N,n}|) n^{-σ_N}`. -/
noncomputable def QN (t y : ℝ) (D N : ℕ) (sig g : ℝ) : ℝ :=
  1 - g - ∑ n ∈ Icc 2 (D * N), (|Bcoef t D N n| + g * |Acoef t y D N n|) * (n : ℝ) ^ (-sig)

/-- `L_N = Q_N / M_N - g_N C_N`. -/
noncomputable def LN (t y : ℝ) (D N : ℕ) (sig g k : ℝ) : ℝ :=
  QN t y D N sig g / MN t D sig - g * CN t y N sig k

/-! ### Elementary facts -/

lemma bt_pos (t : ℝ) (m : ℕ) : 0 < bt t m := Real.exp_pos _

lemma bt_one (t : ℝ) : bt t 1 = 1 := by simp [bt]

lemma lam_one (t : ℝ) : lam t 1 = 1 := by simp [lam]

lemma lam_prime (t : ℝ) {p : ℕ} (hp : p.Prime) : lam t p = -(bt t p) := by
  simp [lam, hp.primeFactors]

lemma lam_mul_coprime (t : ℝ) {m n : ℕ} (hm : m ≠ 0) (hn : n ≠ 0) (h : Nat.Coprime m n) :
    lam t (m * n) = lam t m * lam t n := by
  rw [lam, lam, lam, Nat.primeFactors_mul hm hn,
    Finset.prod_union (Nat.Coprime.disjoint_primeFactors h)]

lemma cpow_natCast_mul (a b : ℕ) (z : ℂ) :
    ((a * b : ℕ) : ℂ) ^ z = (a : ℂ) ^ z * (b : ℂ) ^ z := by
  rw [show ((a * b : ℕ) : ℂ) = ((a : ℝ) : ℂ) * ((b : ℝ) : ℂ) by push_cast; ring,
    Complex.mul_cpow_ofReal_nonneg (Nat.cast_nonneg a) (Nat.cast_nonneg b)]
  norm_num

lemma conj_natCast_cpow (d : ℕ) (w : ℂ) :
    (starRingEnd ℂ) ((d : ℂ) ^ w) = (d : ℂ) ^ ((starRingEnd ℂ) w) := by
  have harg : ((d : ℂ)).arg ≠ Real.pi := by
    simp only [Complex.natCast_arg]
    exact fun h => Real.pi_ne_zero h.symm
  rw [Complex.cpow_conj (d : ℂ) w harg]
  simp

/-- Splitting off the `n = 1` term of a sum over `Icc 1 M`. -/
lemma sum_Icc_one_split {M : ℕ} (hM : 1 ≤ M) {A : Type*} [AddCommMonoid A] (F : ℕ → A) :
    ∑ n ∈ Icc 1 M, F n = F 1 + ∑ n ∈ Icc 2 M, F n := by
  rw [show (2 : ℕ) = 1 + 1 from rfl, Finset.Icc_add_one_left_eq_Ioc,
    Finset.Icc_eq_cons_Ioc hM, Finset.sum_cons]

/-- The norm of `n^{-s}` is bounded by `n^{-σ}` whenever `σ ≤ Re s` and `n ≥ 1`. -/
lemma norm_cpow_neg_le (n : ℕ) (hn : 1 ≤ n) (s : ℂ) (sig : ℝ) (hs : sig ≤ s.re) :
    ‖(n : ℂ) ^ (-s)‖ ≤ (n : ℝ) ^ (-sig) := by
  have hn0 : (0 : ℝ) < n := by exact_mod_cast hn
  have hn1 : (1 : ℝ) ≤ n := by exact_mod_cast hn
  rw [show ((n : ℂ)) = (((n : ℝ)) : ℂ) by push_cast; ring,
    Complex.norm_cpow_eq_rpow_re_of_pos hn0]
  simpa using Real.rpow_le_rpow_of_exponent_le hn1 (by simpa using hs)

/-! ### The Euler expansion -/

theorem eulerFactorProd_eq_dirichletSum (t : ℝ) (P : Finset ℕ) (hP : ∀ p ∈ P, p.Prime)
    (z : ℂ) : eulerFactorProd t P z = dirichletSum t (∏ p ∈ P, p) z := by
  set D := ∏ p ∈ P, p with hDdef
  have hsq : Squarefree D := by
    refine Finset.squarefree_prod_of_pairwise_isCoprime ?_ (fun i hi => (hP i hi).squarefree)
    intro p hp q hq hpq
    exact Nat.coprime_iff_isRelPrime.1 (((hP p hp).coprime_iff_not_dvd).2
      (fun hd => hpq ((Nat.prime_dvd_prime_iff_eq (hP p hp) (hP q hq)).1 hd)))
  have hpf : D.primeFactors = P := Nat.primeFactors_prod hP
  let F : ArithmeticFunction ℂ :=
    ⟨fun d => if d = 0 then 0 else (lam t d : ℂ) * (d : ℂ) ^ (-z), by simp⟩
  have hFval : ∀ d : ℕ, d ≠ 0 → F d = (lam t d : ℂ) * (d : ℂ) ^ (-z) := by
    intro d hd; simp [F, hd]
  have hmul : F.IsMultiplicative := by
    constructor
    · rw [hFval 1 one_ne_zero, lam_one]; simp
    · intro m n hco
      rcases eq_or_ne m 0 with rfl | hm
      · simp [F]
      rcases eq_or_ne n 0 with rfl | hn
      · simp [F]
      rw [hFval _ (Nat.mul_ne_zero hm hn), hFval _ hm, hFval _ hn,
        lam_mul_coprime t hm hn hco, cpow_natCast_mul]
      push_cast
      ring
  have hkey := hmul.prodPrimeFactors_one_add_of_squarefree hsq
  rw [hpf] at hkey
  have hrhs : ∑ d ∈ D.divisors, F d = ∑ d ∈ D.divisors, (lam t d : ℂ) * (d : ℂ) ^ (-z) :=
    Finset.sum_congr rfl (fun d hd => hFval d (Nat.pos_of_mem_divisors hd).ne')
  rw [eulerFactorProd, dirichletSum, ← hrhs, ← hkey]
  refine Finset.prod_congr rfl (fun p hp => ?_)
  rw [hFval p (hP p hp).ne_zero, lam_prime t (hP p hp)]
  push_cast
  ring

/-! ### The exact Dirichlet convolution -/

/-- The general convolution identity: `(∑_{d ∣ D} λ_d d^{-z}) (∑_{m ≤ N} w(m) m^{-z})`
equals `∑_{n ≤ DN} (∑_{d ∣ D, d ∣ n, n/d ≤ N} λ_d w(n/d)) n^{-z}`. -/
theorem dirichletSum_mul_sum (t : ℝ) (D N : ℕ) (hD : D ≠ 0) (w : ℕ → ℝ) (z : ℂ) :
    dirichletSum t D z * (∑ m ∈ Icc 1 N, ((w m : ℝ) : ℂ) * (m : ℂ) ^ (-z))
      = ∑ n ∈ Icc 1 (D * N), ((coeff t D N w n : ℝ) : ℂ) * (n : ℂ) ^ (-z) := by
  have hD0 : 0 < D := Nat.pos_of_ne_zero hD
  have key : dirichletSum t D z * (∑ m ∈ Icc 1 N, ((w m : ℝ) : ℂ) * (m : ℂ) ^ (-z))
      = ∑ x ∈ D.divisors ×ˢ Icc 1 N,
          ((lam t x.1 * w x.2 : ℝ) : ℂ) * ((x.1 * x.2 : ℕ) : ℂ) ^ (-z) := by
    rw [dirichletSum, Finset.sum_mul_sum, Finset.sum_product]
    refine Finset.sum_congr rfl (fun d _ => Finset.sum_congr rfl (fun m _ => ?_))
    rw [cpow_natCast_mul]
    push_cast
    ring
  rw [key]
  have hmaps : ∀ x ∈ D.divisors ×ˢ Icc 1 N, x.1 * x.2 ∈ Icc 1 (D * N) := by
    rintro ⟨d, m⟩ hx
    simp only [Finset.mem_product, Nat.mem_divisors, Finset.mem_Icc] at hx
    obtain ⟨⟨hdvd, -⟩, hm1, hmN⟩ := hx
    have hd1 : 1 ≤ d := Nat.pos_of_dvd_of_pos hdvd hD0
    have hdD : d ≤ D := Nat.le_of_dvd hD0 hdvd
    exact Finset.mem_Icc.2 ⟨Nat.one_le_iff_ne_zero.2 (by positivity), Nat.mul_le_mul hdD hmN⟩
  rw [← Finset.sum_fiberwise_of_maps_to hmaps]
  refine Finset.sum_congr rfl (fun n hn => ?_)
  have hn1 : 1 ≤ n := (Finset.mem_Icc.1 hn).1
  rw [coeff]
  push_cast
  rw [Finset.sum_mul]
  refine Finset.sum_nbij' (i := fun x => x.1) (j := fun d => (d, n / d)) ?_ ?_ ?_ ?_ ?_
  · rintro ⟨d, m⟩ hx
    simp only [Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hx ⊢
    obtain ⟨⟨hd, hm1, hmN⟩, hprod⟩ := hx
    have hdpos : 0 < d := Nat.pos_of_dvd_of_pos (Nat.mem_divisors.1 hd).1 hD0
    have hnd : n / d = m := by rw [← hprod, Nat.mul_div_cancel_left m hdpos]
    exact ⟨hd, ⟨m, hprod.symm⟩, by rw [hnd]; exact hmN⟩
  · intro d hd
    simp only [Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hd ⊢
    obtain ⟨hdD, hdvd, hle⟩ := hd
    have hdpos : 0 < d := Nat.pos_of_dvd_of_pos (Nat.mem_divisors.1 hdD).1 hD0
    exact ⟨⟨hdD, (Nat.one_le_div_iff hdpos).2 (Nat.le_of_dvd hn1 hdvd), hle⟩,
      Nat.mul_div_cancel' hdvd⟩
  · rintro ⟨d, m⟩ hx
    simp only [Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hx
    obtain ⟨⟨hd, -, -⟩, hprod⟩ := hx
    have hdpos : 0 < d := Nat.pos_of_dvd_of_pos (Nat.mem_divisors.1 hd).1 hD0
    simp only [Prod.mk.injEq, true_and]
    rw [← hprod, Nat.mul_div_cancel_left m hdpos]
  · intro d _; rfl
  · rintro ⟨d, m⟩ hx
    simp only [Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hx
    obtain ⟨⟨hd, -, -⟩, hprod⟩ := hx
    have hdpos : 0 < d := Nat.pos_of_dvd_of_pos (Nat.mem_divisors.1 hd).1 hD0
    have hnd : n / d = m := by rw [← hprod, Nat.mul_div_cancel_left m hdpos]
    simp only [hnd]
    rw [show ((d : ℂ) * (m : ℂ)) = ((n : ℕ) : ℂ) by rw [← hprod]; push_cast; ring]

theorem coeff_one (t : ℝ) (D N : ℕ) (hD : D ≠ 0) (hN : 1 ≤ N) (w : ℕ → ℝ) :
    coeff t D N w 1 = w 1 := by
  have hfil : {d ∈ D.divisors | d ∣ 1 ∧ 1 / d ≤ N} = {1} := by
    ext d
    simp only [Finset.mem_filter, Finset.mem_singleton, Nat.mem_divisors, Nat.dvd_one]
    constructor
    · rintro ⟨-, h, -⟩; exact h
    · rintro rfl; exact ⟨⟨one_dvd _, hD⟩, rfl, by simpa using hN⟩
  rw [coeff, hfil]
  simp [lam]

theorem Bcoef_one (t : ℝ) (D N : ℕ) (hD : D ≠ 0) (hN : 1 ≤ N) : Bcoef t D N 1 = 1 := by
  rw [Bcoef, coeff_one t D N hD hN, bt_one]

theorem Acoef_one (t y : ℝ) (D N : ℕ) (hD : D ≠ 0) (hN : 1 ≤ N) : Acoef t y D N 1 = 1 := by
  rw [Acoef, coeff_one t D N hD hN]
  simp [bt_one]

lemma prod_primes_ne_zero {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) : (∏ p ∈ P, p) ≠ 0 :=
  Finset.prod_ne_zero_iff.2 (fun p hp => (hP p hp).ne_zero)

/-- Target (a), first identity: `E(s) A = ∑_{n ≤ DN} B_{N,n} n^{-s}`. -/
theorem eulerFactorProd_mul_Asum (t : ℝ) (N : ℕ) (P : Finset ℕ) (hP : ∀ p ∈ P, p.Prime)
    (D : ℕ) (hD : D = ∏ p ∈ P, p) (s : ℂ) :
    eulerFactorProd t P s * Asum t N s
      = ∑ n ∈ Icc 1 (D * N), ((Bcoef t D N n : ℝ) : ℂ) * (n : ℂ) ^ (-s) := by
  subst hD
  rw [eulerFactorProd_eq_dirichletSum t P hP, Asum]
  exact dirichletSum_mul_sum t _ N (prod_primes_ne_zero hP) (bt t) s

/-- Target (a), second identity: `conj (E(s)) C_0 = ∑_{n ≤ DN} A_{N,n} n^{-conj s}`. -/
theorem conj_eulerFactorProd_mul_Csum (t y : ℝ) (N : ℕ) (P : Finset ℕ) (hP : ∀ p ∈ P, p.Prime)
    (D : ℕ) (hD : D = ∏ p ∈ P, p) (s : ℂ) :
    (starRingEnd ℂ) (eulerFactorProd t P s) * Csum t y N s 0
      = ∑ n ∈ Icc 1 (D * N), ((Acoef t y D N n : ℝ) : ℂ) * (n : ℂ) ^ (-(starRingEnd ℂ) s) := by
  subst hD
  have hconj : (starRingEnd ℂ) (eulerFactorProd t P s)
      = dirichletSum t (∏ p ∈ P, p) ((starRingEnd ℂ) s) := by
    rw [eulerFactorProd_eq_dirichletSum t P hP, dirichletSum, dirichletSum, map_sum]
    refine Finset.sum_congr rfl (fun d _ => ?_)
    rw [map_mul, conj_natCast_cpow, Complex.conj_ofReal, map_neg]
  rw [hconj]
  have hC : Csum t y N s 0
      = ∑ m ∈ Icc 1 N, (((bt t m * (m : ℝ) ^ y : ℝ)) : ℂ) * (m : ℂ) ^ (-(starRingEnd ℂ) s) := by
    rw [Csum]
    refine Finset.sum_congr rfl (fun m _ => ?_)
    rw [sub_zero]
    push_cast
    ring
  rw [hC]
  exact dirichletSum_mul_sum t _ N (prod_primes_ne_zero hP) _ _

/-! ### The elementary estimate (target (b)) -/

theorem norm_cexp_sub_one_le (z : ℂ) : ‖Complex.exp z - 1‖ ≤ Real.exp ‖z‖ - 1 := by
  have hsC : Summable (fun n : ℕ => z ^ n / (n.factorial : ℂ)) :=
    NormedSpace.expSeries_div_summable z
  have hsR : Summable (fun n : ℕ => ‖z‖ ^ n / (n.factorial : ℝ)) :=
    Real.summable_pow_div_factorial _
  have hexpC : Complex.exp z = ∑' n : ℕ, z ^ n / (n.factorial : ℂ) := by
    rw [Complex.exp_eq_exp_ℂ, NormedSpace.exp_eq_tsum_div]
  have hexpR : Real.exp ‖z‖ = ∑' n : ℕ, ‖z‖ ^ n / (n.factorial : ℝ) := by
    rw [Real.exp_eq_exp_ℝ, NormedSpace.exp_eq_tsum_div]
  have h1 : Complex.exp z - 1 = ∑' n : ℕ, z ^ (n + 1) / (((n + 1).factorial : ℕ) : ℂ) := by
    rw [hexpC, hsC.tsum_eq_zero_add]; simp
  have h2 : Real.exp ‖z‖ - 1 = ∑' n : ℕ, ‖z‖ ^ (n + 1) / (((n + 1).factorial : ℕ) : ℝ) := by
    rw [hexpR, hsR.tsum_eq_zero_add]; simp
  rw [h1, h2]
  refine norm_tsum_le_tsum_norm ?_ |>.trans (le_of_eq ?_)
  · refine Summable.of_nonneg_of_le (fun n => norm_nonneg _) (fun n => le_of_eq ?_)
      ((summable_nat_add_iff 1).2 hsR)
    simp [norm_pow]
  · exact tsum_congr (fun n => by simp [norm_pow])

/-- Target (b): `|m^{-κ} - 1| ≤ m^{k} - 1` for `|κ| ≤ k` and `m ≥ 1`. -/
theorem norm_cpow_neg_sub_one_le (m : ℕ) (hm : 1 ≤ m) (kappa : ℂ) (k : ℝ) (hk : ‖kappa‖ ≤ k) :
    ‖(m : ℂ) ^ (-kappa) - 1‖ ≤ (m : ℝ) ^ k - 1 := by
  have hm0 : (0 : ℝ) < m := by exact_mod_cast hm
  have hlog : 0 ≤ Real.log m := Real.log_natCast_nonneg m
  have hcpow : (m : ℂ) ^ (-kappa) = Complex.exp ((-kappa) * ((Real.log m : ℝ) : ℂ)) := by
    rw [Complex.cpow_def_of_ne_zero (by exact_mod_cast Nat.one_le_iff_ne_zero.mp hm)]
    congr 1
    rw [← Complex.natCast_log]
    ring
  have hnorm : ‖(-kappa) * ((Real.log m : ℝ) : ℂ)‖ ≤ k * Real.log m := by
    rw [norm_mul, norm_neg, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hlog]
    exact mul_le_mul_of_nonneg_right hk hlog
  calc ‖(m : ℂ) ^ (-kappa) - 1‖ ≤ Real.exp ‖(-kappa) * ((Real.log m : ℝ) : ℂ)‖ - 1 := by
        rw [hcpow]; exact norm_cexp_sub_one_le _
    _ ≤ Real.exp (k * Real.log m) - 1 := by gcongr
    _ = (m : ℝ) ^ k - 1 := by rw [Real.rpow_def_of_pos hm0, mul_comm]

/-! ### Auxiliary bounds for the Native Triangle lemma -/

/-- The mollifier triangle bound `|E(s)| ≤ M_N`. -/
lemma norm_dirichletSum_le (t : ℝ) (D : ℕ) (sig : ℝ) (s : ℂ) (hs : sig ≤ s.re) :
    ‖dirichletSum t D s‖ ≤ MN t D sig := by
  refine (norm_sum_le _ _).trans ?_
  refine Finset.sum_le_sum (fun d hd => ?_)
  have hd1 : 1 ≤ d := Nat.pos_of_mem_divisors hd
  rw [norm_mul, Complex.norm_real, Real.norm_eq_abs]
  exact mul_le_mul_of_nonneg_left (norm_cpow_neg_le d hd1 s sig hs) (abs_nonneg _)

lemma MN_ge_one (t : ℝ) (D : ℕ) (hD : D ≠ 0) (sig : ℝ) : 1 ≤ MN t D sig := by
  have h1 : (1 : ℕ) ∈ D.divisors := Nat.one_mem_divisors.2 hD
  have hnn : ∀ d ∈ D.divisors, 0 ≤ |lam t d| * (d : ℝ) ^ (-sig) := by
    intro d hd
    have : (0 : ℝ) ≤ (d : ℝ) ^ (-sig) := Real.rpow_nonneg (Nat.cast_nonneg d) _
    positivity
  have := Finset.single_le_sum hnn h1
  simpa [lam_one] using this

lemma CN_nonneg (t y : ℝ) (N : ℕ) (sig k : ℝ) (hk : 0 ≤ k) : 0 ≤ CN t y N sig k := by
  refine Finset.sum_nonneg (fun m hm => ?_)
  have hm2 : 2 ≤ m := (Finset.mem_Icc.1 hm).1
  have hm1 : (1 : ℝ) ≤ m := by exact_mod_cast Nat.one_le_of_lt hm2
  have h1 : (1 : ℝ) ≤ (m : ℝ) ^ k := Real.one_le_rpow hm1 hk
  have h2 : (0 : ℝ) ≤ (m : ℝ) ^ (y - sig) := Real.rpow_nonneg (by positivity) _
  have h3 : 0 < bt t m := bt_pos t m
  exact mul_nonneg (mul_nonneg h3.le (by linarith)) h2

/-- The `κ`-perturbation bound: `|C_κ - C_0| ≤ C_N`. -/
lemma norm_Csum_sub_le (t y : ℝ) (N : ℕ) (hN : 1 ≤ N) (sig k : ℝ) (s kappa : ℂ)
    (hs : sig ≤ s.re) (hk : ‖kappa‖ ≤ k) :
    ‖Csum t y N s kappa - Csum t y N s 0‖ ≤ CN t y N sig k := by
  have hterm : ∀ m : ℕ, 1 ≤ m →
      (((m : ℝ) ^ y * bt t m : ℝ) : ℂ) * (m : ℂ) ^ (-(starRingEnd ℂ) s - kappa)
        - (((m : ℝ) ^ y * bt t m : ℝ) : ℂ) * (m : ℂ) ^ (-(starRingEnd ℂ) s - 0)
        = (((m : ℝ) ^ y * bt t m : ℝ) : ℂ) * (m : ℂ) ^ (-(starRingEnd ℂ) s)
            * ((m : ℂ) ^ (-kappa) - 1) := by
    intro m hm
    have hm0 : (m : ℂ) ≠ 0 := by
      exact_mod_cast Nat.one_le_iff_ne_zero.mp hm
    rw [show -(starRingEnd ℂ) s - kappa = (-(starRingEnd ℂ) s) + (-kappa) by ring,
      Complex.cpow_add _ _ hm0, sub_zero]
    ring
  have hsplit : Csum t y N s kappa - Csum t y N s 0
      = ∑ m ∈ Icc 2 N, (((m : ℝ) ^ y * bt t m : ℝ) : ℂ) * (m : ℂ) ^ (-(starRingEnd ℂ) s)
          * ((m : ℂ) ^ (-kappa) - 1) := by
    rw [Csum, Csum, ← Finset.sum_sub_distrib]
    rw [sum_Icc_one_split hN]
    have : (((1 : ℕ) : ℝ) ^ y * bt t 1 : ℝ) = 1 := by simp [bt_one]
    simp only [Nat.cast_one, Complex.one_cpow]
    rw [Finset.sum_congr rfl (fun m hm => hterm m (le_trans (by norm_num)
      (Finset.mem_Icc.1 hm).1))]
    simp
  rw [hsplit, CN]
  refine (norm_sum_le _ _).trans (Finset.sum_le_sum (fun m hm => ?_))
  have hm2 : 2 ≤ m := (Finset.mem_Icc.1 hm).1
  have hm1 : 1 ≤ m := le_trans (by norm_num) hm2
  have hmR : (1 : ℝ) ≤ (m : ℝ) := by exact_mod_cast hm1
  have hmR0 : (0 : ℝ) < (m : ℝ) := by linarith
  have hy : (0 : ℝ) ≤ (m : ℝ) ^ y := Real.rpow_nonneg hmR0.le _
  have hprod0 : (0 : ℝ) ≤ (m : ℝ) ^ y * bt t m := mul_nonneg hy (bt_pos t m).le
  have hb1 : ‖(((m : ℝ) ^ y * bt t m : ℝ) : ℂ)‖ = (m : ℝ) ^ y * bt t m := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hprod0]
  have hb2 : ‖(m : ℂ) ^ (-(starRingEnd ℂ) s)‖ ≤ (m : ℝ) ^ (-sig) :=
    norm_cpow_neg_le m hm1 _ sig (by simpa using hs)
  have hb3 : ‖(m : ℂ) ^ (-kappa) - 1‖ ≤ (m : ℝ) ^ k - 1 :=
    norm_cpow_neg_sub_one_le m hm1 kappa k hk
  have hk0 : 0 ≤ k := le_trans (norm_nonneg _) hk
  have hpow : (0 : ℝ) ≤ (m : ℝ) ^ k - 1 := by
    have := Real.one_le_rpow hmR hk0
    linarith
  rw [norm_mul, norm_mul, hb1]
  have hstep : (m : ℝ) ^ y * bt t m * ‖(m : ℂ) ^ (-(starRingEnd ℂ) s)‖
      ≤ (m : ℝ) ^ y * bt t m * (m : ℝ) ^ (-sig) :=
    mul_le_mul_of_nonneg_left hb2 hprod0
  calc (m : ℝ) ^ y * bt t m * ‖(m : ℂ) ^ (-(starRingEnd ℂ) s)‖ * ‖(m : ℂ) ^ (-kappa) - 1‖
      ≤ (m : ℝ) ^ y * bt t m * (m : ℝ) ^ (-sig) * ((m : ℝ) ^ k - 1) :=
        mul_le_mul hstep hb3 (norm_nonneg _)
          (mul_nonneg hprod0 (Real.rpow_nonneg hmR0.le _))
    _ = bt t m * ((m : ℝ) ^ k - 1) * (m : ℝ) ^ (y - sig) := by
        rw [Real.rpow_sub hmR0, Real.rpow_neg hmR0.le]
        field_simp

/-- Termwise triangle bound for the tail `∑_{n=2}^M c_n n^{-s}`. -/
lemma norm_tail_le (co : ℕ → ℝ) (M : ℕ) (sig : ℝ) (s : ℂ) (hs : sig ≤ s.re) :
    ‖∑ n ∈ Icc 2 M, ((co n : ℝ) : ℂ) * (n : ℂ) ^ (-s)‖
      ≤ ∑ n ∈ Icc 2 M, |co n| * (n : ℝ) ^ (-sig) := by
  refine (norm_sum_le _ _).trans (Finset.sum_le_sum (fun n hn => ?_))
  have hn1 : 1 ≤ n := le_trans (by norm_num) (Finset.mem_Icc.1 hn).1
  rw [norm_mul, Complex.norm_real, Real.norm_eq_abs]
  exact mul_le_mul_of_nonneg_left (norm_cpow_neg_le n hn1 s sig hs) (abs_nonneg _)

/-- Lower bound `|E(s) A| ≥ 1 - ∑_{n=2}^{DN} |B_{N,n}| n^{-σ_N}`. -/
lemma norm_eulerFactorProd_mul_Asum_ge (t : ℝ) (N : ℕ) (hN : 1 ≤ N) (P : Finset ℕ)
    (hP : ∀ p ∈ P, p.Prime) (D : ℕ) (hD : D = ∏ p ∈ P, p) (sig : ℝ) (s : ℂ)
    (hs : sig ≤ s.re) :
    1 - ∑ n ∈ Icc 2 (D * N), |Bcoef t D N n| * (n : ℝ) ^ (-sig)
      ≤ ‖eulerFactorProd t P s * Asum t N s‖ := by
  have hD0 : D ≠ 0 := by rw [hD]; exact prod_primes_ne_zero hP
  have hDN : 1 ≤ D * N := Nat.one_le_iff_ne_zero.2
    (Nat.mul_ne_zero hD0 (Nat.one_le_iff_ne_zero.1 hN))
  rw [eulerFactorProd_mul_Asum t N P hP D hD s, sum_Icc_one_split hDN,
    Bcoef_one t D N hD0 hN]
  simp only [Nat.cast_one, Complex.ofReal_one, Complex.one_cpow, one_mul]
  have htail := norm_tail_le (fun n => Bcoef t D N n) (D * N) sig s hs
  have h := norm_sub_norm_le (1 : ℂ)
    (-(∑ n ∈ Icc 2 (D * N), ((Bcoef t D N n : ℝ) : ℂ) * (n : ℂ) ^ (-s)))
  rw [norm_neg, sub_neg_eq_add, norm_one] at h
  linarith

/-- Upper bound `|conj(E(s)) C_0| ≤ 1 + ∑_{n=2}^{DN} |A_{N,n}| n^{-σ_N}`. -/
lemma norm_conj_eulerFactorProd_mul_Csum_le (t y : ℝ) (N : ℕ) (hN : 1 ≤ N) (P : Finset ℕ)
    (hP : ∀ p ∈ P, p.Prime) (D : ℕ) (hD : D = ∏ p ∈ P, p) (sig : ℝ) (s : ℂ)
    (hs : sig ≤ s.re) :
    ‖(starRingEnd ℂ) (eulerFactorProd t P s) * Csum t y N s 0‖
      ≤ 1 + ∑ n ∈ Icc 2 (D * N), |Acoef t y D N n| * (n : ℝ) ^ (-sig) := by
  have hD0 : D ≠ 0 := by rw [hD]; exact prod_primes_ne_zero hP
  have hDN : 1 ≤ D * N := Nat.one_le_iff_ne_zero.2
    (Nat.mul_ne_zero hD0 (Nat.one_le_iff_ne_zero.1 hN))
  rw [conj_eulerFactorProd_mul_Csum t y N P hP D hD s, sum_Icc_one_split hDN,
    Acoef_one t y D N hD0 hN]
  simp only [Nat.cast_one, Complex.ofReal_one, Complex.one_cpow, one_mul]
  have htail := norm_tail_le (fun n => Acoef t y D N n) (D * N) sig
    ((starRingEnd ℂ) s) (by simpa using hs)
  have h := norm_add_le (1 : ℂ)
    (∑ n ∈ Icc 2 (D * N), ((Acoef t y D N n : ℝ) : ℂ) * (n : ℂ) ^ (-(starRingEnd ℂ) s))
  rw [norm_one] at h
  linarith

/-! ### The Native Triangle lemma (target (c)) -/

/-- Target (c): the Native Triangle lemma.  Under Hypothesis H — i.e. the representation
`f = A + γ C_κ` with `|γ| ≤ g_N`, `Re s ≥ σ_N`, `|κ| ≤ k_N` — and `L_N > 0`,
one has `|f| ≥ L_N`. -/
theorem native_triangle (t y : ℝ) (N : ℕ) (hN : 1 ≤ N) (P : Finset ℕ) (hP : ∀ p ∈ P, p.Prime)
    (D : ℕ) (hD : D = ∏ p ∈ P, p) (sig g k : ℝ) (gamma s kappa : ℂ) (f : ℂ)
    (hgamma : ‖gamma‖ ≤ g) (hs : sig ≤ s.re) (hkappa : ‖kappa‖ ≤ k)
    (hf : f = Asum t N s + gamma * Csum t y N s kappa)
    (hL : 0 < LN t y D N sig g k) :
    LN t y D N sig g k ≤ ‖f‖ := by
  have hD0 : D ≠ 0 := by rw [hD]; exact prod_primes_ne_zero hP
  have hg0 : 0 ≤ g := le_trans (norm_nonneg _) hgamma
  have hk0 : 0 ≤ k := le_trans (norm_nonneg _) hkappa
  set SB := ∑ n ∈ Icc 2 (D * N), |Bcoef t D N n| * (n : ℝ) ^ (-sig) with hSB
  set SA := ∑ n ∈ Icc 2 (D * N), |Acoef t y D N n| * (n : ℝ) ^ (-sig) with hSA
  set E := eulerFactorProd t P s with hEdef
  -- rewriting `Q_N`
  have hsum : ∑ n ∈ Icc 2 (D * N),
      (|Bcoef t D N n| + g * |Acoef t y D N n|) * (n : ℝ) ^ (-sig) = SB + g * SA := by
    rw [hSB, hSA, Finset.mul_sum, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl (fun n _ => by ring)
  have hQ : QN t y D N sig g = 1 - SB - g * (1 + SA) := by rw [QN, hsum]; ring
  -- the mollifier triangle bound
  have hEeq : E = dirichletSum t D s := by
    rw [hEdef, hD, eulerFactorProd_eq_dirichletSum t P hP]
  have hEnorm : ‖E‖ ≤ MN t D sig := hEeq ▸ norm_dirichletSum_le t D sig s hs
  have hM1 : 1 ≤ MN t D sig := MN_ge_one t D hD0 sig
  have hM0 : 0 < MN t D sig := lt_of_lt_of_le one_pos hM1
  have hCN0 : 0 ≤ CN t y N sig k := CN_nonneg t y N sig k hk0
  -- the two convolution bounds
  have hEA : 1 - SB ≤ ‖E * Asum t N s‖ :=
    norm_eulerFactorProd_mul_Asum_ge t N hN P hP D hD sig s hs
  have hC0 : ‖E‖ * ‖Csum t y N s 0‖ ≤ 1 + SA := by
    have h := norm_conj_eulerFactorProd_mul_Csum_le t y N hN P hP D hD sig s hs
    rwa [norm_mul, Complex.norm_conj] at h
  -- the `κ`-perturbation
  have hCk : ‖Csum t y N s kappa‖ ≤ ‖Csum t y N s 0‖ + CN t y N sig k := by
    have h := norm_Csum_sub_le t y N hN sig k s kappa hs hkappa
    calc ‖Csum t y N s kappa‖
        = ‖(Csum t y N s kappa - Csum t y N s 0) + Csum t y N s 0‖ := by congr 1; ring
      _ ≤ ‖Csum t y N s kappa - Csum t y N s 0‖ + ‖Csum t y N s 0‖ := norm_add_le _ _
      _ ≤ ‖Csum t y N s 0‖ + CN t y N sig k := by linarith
  -- combining
  have hEf : E * f = E * Asum t N s + gamma * (E * Csum t y N s kappa) := by rw [hf]; ring
  have htri : ‖E * Asum t N s‖ - ‖gamma * (E * Csum t y N s kappa)‖ ≤ ‖E * f‖ := by
    rw [hEf]
    have h := norm_sub_norm_le (E * Asum t N s) (-(gamma * (E * Csum t y N s kappa)))
    rwa [norm_neg, sub_neg_eq_add] at h
  have hgb : ‖gamma * (E * Csum t y N s kappa)‖
      ≤ g * ((1 + SA) + ‖E‖ * CN t y N sig k) := by
    have hX : ‖E‖ * ‖Csum t y N s kappa‖ ≤ (1 + SA) + ‖E‖ * CN t y N sig k := by
      have h := mul_le_mul_of_nonneg_left hCk (norm_nonneg E)
      nlinarith [hC0]
    rw [norm_mul, norm_mul]
    calc ‖gamma‖ * (‖E‖ * ‖Csum t y N s kappa‖)
        ≤ g * (‖E‖ * ‖Csum t y N s kappa‖) :=
          mul_le_mul_of_nonneg_right hgamma (by positivity)
      _ ≤ g * ((1 + SA) + ‖E‖ * CN t y N sig k) := mul_le_mul_of_nonneg_left hX hg0
  have hmain : QN t y D N sig g - g * ‖E‖ * CN t y N sig k ≤ ‖E‖ * ‖f‖ := by
    rw [hQ, ← norm_mul]
    nlinarith [htri, hEA, hgb]
  -- positivity of `Q_N`
  have hQpos : 0 < QN t y D N sig g := by
    rw [LN] at hL
    have h1 : 0 ≤ g * CN t y N sig k := mul_nonneg hg0 hCN0
    have h2 : 0 < QN t y D N sig g / MN t D sig := by linarith
    have h3 := mul_pos h2 hM0
    rwa [div_mul_cancel₀ _ hM0.ne'] at h3
  -- hence `E(s) ≠ 0`
  have hEpos : 0 < ‖E‖ := by
    rcases eq_or_lt_of_le (norm_nonneg E) with h | h
    · exfalso
      rw [← h] at hmain
      simp only [zero_mul, mul_zero, sub_zero] at hmain
      linarith
    · exact h
  -- and division is legitimate
  have h5 : QN t y D N sig g / ‖E‖ ≤ ‖f‖ + g * CN t y N sig k := by
    rw [div_le_iff₀ hEpos]
    nlinarith [hmain]
  have h6 : QN t y D N sig g / MN t D sig ≤ QN t y D N sig g / ‖E‖ :=
    div_le_div_of_nonneg_left hQpos.le hEpos hEnorm
  rw [LN]
  linarith

/-- The hypothesis `L_N > 0` of the Native Triangle lemma is satisfiable: for the empty prime
set (`D = 1`), `N = 1`, `σ_N = 0`, `g_N = 1/2` and `k_N = 0` one has `L_N = 1/2 > 0`. -/
example : 0 < LN 0 0 1 1 0 (1 / 2) 0 := by
  norm_num [LN, QN, MN, CN, lam, bt, Nat.divisors]
  decide

/-! ### The numerical remark -/

theorem sealed_margin_pos :
    (0.000000791366 : ℝ) - 0.000000233494905213 ≥ 0.000000557871094787 ∧
      (0.000000557871094787 : ℝ) > 0 := by
  norm_num

end NativeBinding
