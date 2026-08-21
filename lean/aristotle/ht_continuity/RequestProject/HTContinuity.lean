import Mathlib

/-!
# Concrete instantiation lemmas for the de Bruijn–Newman heat-flow kernel

This file defines the Polymath15 heat-flow kernel
`Φ(u) = ∑_{n ≥ 1} (2 π² n⁴ e^{9u} - 3 π n² e^{5u}) exp(-π n² e^{4u})`
and proves:

* Lemma 1: the series converges for every `u ≥ 0`, uniformly on `[0, ∞)` (hence on
  compact subsets of `[0, ∞)`), and `Φ` is continuous on `[0, ∞)`.
* Lemma 2: `Φ` is a.e. strongly measurable for `volume.restrict (Ioi 0)`.
* Lemma 3: superexponential decay `|Φ u| ≤ C_A exp (-A e^{4u})` for `0 < A ≤ π/2`.
* Lemma 4: for `t₀, y₀ ≥ 0` the function `u ↦ exp (t₀ u² + y₀ u) ‖Φ u‖` is integrable
  on `(0, ∞)`.
-/

open Real Set MeasureTheory Filter
open scoped Topology

namespace HeatFlowKernel

/-- The `n`-th term of the Polymath15 heat-flow kernel series. -/
noncomputable def kernelTerm (n : ℕ) (u : ℝ) : ℝ :=
  (2 * π ^ 2 * (n : ℝ) ^ 4 * Real.exp (9 * u) - 3 * π * (n : ℝ) ^ 2 * Real.exp (5 * u)) *
    Real.exp (-(π * (n : ℝ) ^ 2 * Real.exp (4 * u)))

/-- The Polymath15 heat-flow kernel
`Φ(u) = ∑_{n ≥ 1} (2 π² n⁴ e^{9u} - 3 π n² e^{5u}) exp(-π n² e^{4u})`. -/
noncomputable def Phi (u : ℝ) : ℝ := ∑' n : ℕ, kernelTerm (n + 1) u

/-- The Weierstrass majorant used for the `M`-test. -/
noncomputable def kernelMajorant (n : ℕ) : ℝ :=
  Real.exp 81 * (2 * π ^ 2 * (n : ℝ) ^ 4 + 3 * π * (n : ℝ) ^ 2) *
    Real.exp (-(π / 4) * (n : ℝ) ^ 2)

/-! ### Elementary auxiliary estimates -/

lemma sq_le_exp_two_mul {u : ℝ} (hu : 0 ≤ u) : u ^ 2 ≤ Real.exp (2 * u) := by
  have h := Real.sum_le_exp_of_nonneg (x := 2 * u) (by linarith) 3
  simp [Finset.sum_range_succ] at h
  nlinarith

lemma self_le_exp_two_mul {u : ℝ} (hu : 0 ≤ u) : u ≤ Real.exp (2 * u) := by
  have h := Real.add_one_le_exp (2 * u)
  linarith

lemma nine_mul_sub_exp_le {u : ℝ} (hu : 0 ≤ u) :
    9 * u - (π / 4) * Real.exp (4 * u) ≤ 81 := by
  have hs : u ≤ Real.exp (2 * u) := self_le_exp_two_mul hu
  have hsq : Real.exp (4 * u) = Real.exp (2 * u) ^ 2 := by
    rw [← Real.exp_nat_mul]; ring_nf
  set s := Real.exp (2 * u) with hsdef
  have hs1 : (1 : ℝ) ≤ s := by
    rw [hsdef]; exact Real.one_le_exp (by linarith)
  have hpi : (3 : ℝ) < π := Real.pi_gt_three
  rw [hsq]
  nlinarith [sq_nonneg (s - 6)]

lemma quadratic_sub_exp_le {t₀ y₀ u : ℝ} (ht : 0 ≤ t₀) (hy : 0 ≤ y₀) (hu : 0 ≤ u) :
    t₀ * u ^ 2 + y₀ * u + u - (π / 2) * Real.exp (4 * u) ≤ (t₀ + y₀ + 1) ^ 2 := by
  have hsq : Real.exp (4 * u) = Real.exp (2 * u) ^ 2 := by
    rw [← Real.exp_nat_mul]; ring_nf
  have h1 : u ^ 2 ≤ Real.exp (2 * u) := sq_le_exp_two_mul hu
  have h2 : u ≤ Real.exp (2 * u) := self_le_exp_two_mul hu
  set s := Real.exp (2 * u) with hsdef
  have hs1 : (1 : ℝ) ≤ s := by rw [hsdef]; exact Real.one_le_exp (by linarith)
  have hpi : (3 : ℝ) < π := Real.pi_gt_three
  have hB : t₀ * u ^ 2 + y₀ * u + u ≤ (t₀ + y₀ + 1) * s := by nlinarith
  rw [hsq]
  nlinarith [sq_nonneg (s - (t₀ + y₀ + 1) / 3), sq_nonneg (t₀ + y₀ + 1)]

/-! ### The Weierstrass majorant -/

lemma kernelMajorant_nonneg (n : ℕ) : 0 ≤ kernelMajorant n := by
  unfold kernelMajorant
  have := Real.pi_pos
  positivity

lemma summable_kernelMajorant : Summable fun n : ℕ => kernelMajorant (n + 1) := by
  have hpi := Real.pi_pos
  have h4 : Summable (fun n : ℕ => ((n : ℝ)) ^ 4 * Real.exp (-(π / 4) * (n : ℝ))) :=
    Real.summable_pow_mul_exp_neg_nat_mul 4 (by positivity)
  have hshift : Summable
      (fun n : ℕ => (((n + 1 : ℕ) : ℝ)) ^ 4 * Real.exp (-(π / 4) * ((n + 1 : ℕ) : ℝ))) :=
    (summable_nat_add_iff 1).2 h4
  have hmul : Summable (fun n : ℕ => (Real.exp 81 * (2 * π ^ 2 + 3 * π)) *
      ((((n + 1 : ℕ) : ℝ)) ^ 4 * Real.exp (-(π / 4) * ((n + 1 : ℕ) : ℝ)))) := hshift.mul_left _
  refine Summable.of_nonneg_of_le (fun n => kernelMajorant_nonneg _) (fun n => ?_) hmul
  simp only [kernelMajorant]
  push_cast
  set x : ℝ := (n : ℝ) + 1 with hx
  have hx1 : (1 : ℝ) ≤ x := by simp [hx]
  have hpoly : 2 * π ^ 2 * x ^ 4 + 3 * π * x ^ 2 ≤ (2 * π ^ 2 + 3 * π) * x ^ 4 := by
    nlinarith [sq_nonneg x, pow_le_pow_right₀ hx1 (show 2 ≤ 4 by norm_num)]
  have hexp : Real.exp (-(π / 4) * x ^ 2) ≤ Real.exp (-(π / 4) * x) :=
    Real.exp_le_exp.2 (by nlinarith)
  calc Real.exp 81 * (2 * π ^ 2 * x ^ 4 + 3 * π * x ^ 2) * Real.exp (-(π / 4) * x ^ 2)
      ≤ Real.exp 81 * ((2 * π ^ 2 + 3 * π) * x ^ 4) * Real.exp (-(π / 4) * x) :=
        mul_le_mul (by nlinarith [Real.exp_pos (81 : ℝ)]) hexp (Real.exp_pos _).le (by positivity)
    _ = Real.exp 81 * (2 * π ^ 2 + 3 * π) * (x ^ 4 * Real.exp (-(π / 4) * x)) := by ring

/-- The key pointwise bound: for `n ≥ 1` and `u ≥ 0` the `n`-th term is dominated by
the majorant times the superexponentially small factor `exp (-(π/2) e^{4u})`. -/
lemma abs_kernelTerm_le {n : ℕ} (hn : 1 ≤ n) {u : ℝ} (hu : 0 ≤ u) :
    |kernelTerm n u| ≤ kernelMajorant n * Real.exp (-(π / 2) * Real.exp (4 * u)) := by
  have hpi := Real.pi_pos
  have h9 : 9 * u - (π / 4) * Real.exp (4 * u) ≤ 81 := nine_mul_sub_exp_le hu
  have hN1' : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  set N : ℝ := (n : ℝ) with hN
  set E : ℝ := Real.exp (4 * u) with hE
  have hE1 : (1 : ℝ) ≤ E := Real.one_le_exp (by linarith)
  have h59 : Real.exp (5 * u) ≤ Real.exp (9 * u) := Real.exp_le_exp.2 (by linarith)
  have hbase : (3 / 4) * E + (1 / 4) * N ^ 2 ≤ N ^ 2 * E := by
    nlinarith [mul_nonneg (by nlinarith : (0 : ℝ) ≤ N ^ 2 - 3 / 4) (by linarith : (0 : ℝ) ≤ E - 1)]
  have hsplit : (π / 2) * E + (π / 4) * E + (π / 4) * N ^ 2 ≤ π * N ^ 2 * E := by
    nlinarith [mul_le_mul_of_nonneg_left hbase hpi.le]
  have hkey : 9 * u + -(π * N ^ 2 * E) ≤ 81 + (-(π / 4) * N ^ 2) + (-(π / 2) * E) := by linarith
  have hcoef : (0 : ℝ) ≤ 2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2 := by positivity
  have habs : |2 * π ^ 2 * N ^ 4 * Real.exp (9 * u) - 3 * π * N ^ 2 * Real.exp (5 * u)| ≤
      (2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2) * Real.exp (9 * u) := by
    rw [abs_sub_le_iff]
    constructor <;>
      nlinarith [Real.exp_pos (9 * u), Real.exp_pos (5 * u), sq_nonneg N,
        mul_nonneg (mul_nonneg (by positivity : (0 : ℝ) ≤ 3 * π) (sq_nonneg N))
          (Real.exp_pos (5 * u)).le,
        mul_nonneg (mul_nonneg (by positivity : (0 : ℝ) ≤ 2 * π ^ 2)
          (pow_nonneg (by linarith : (0 : ℝ) ≤ N) 4)) (Real.exp_pos (9 * u)).le]
  have h1 : |kernelTerm n u| ≤ (2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2) *
      Real.exp (9 * u + -(π * N ^ 2 * E)) := by
    rw [kernelTerm, abs_mul, abs_of_pos (Real.exp_pos _), Real.exp_add, ← hN, ← hE]
    calc |2 * π ^ 2 * N ^ 4 * Real.exp (9 * u) - 3 * π * N ^ 2 * Real.exp (5 * u)| *
          Real.exp (-(π * N ^ 2 * E))
        ≤ ((2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2) * Real.exp (9 * u)) *
            Real.exp (-(π * N ^ 2 * E)) :=
          mul_le_mul_of_nonneg_right habs (Real.exp_pos _).le
      _ = (2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2) *
            (Real.exp (9 * u) * Real.exp (-(π * N ^ 2 * E))) := by ring
  refine h1.trans ?_
  rw [kernelMajorant, ← hN]
  have hRHS : Real.exp 81 * (2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2) * Real.exp (-(π / 4) * N ^ 2) *
      Real.exp (-(π / 2) * E)
      = (2 * π ^ 2 * N ^ 4 + 3 * π * N ^ 2) *
        Real.exp (81 + (-(π / 4) * N ^ 2) + (-(π / 2) * E)) := by
    rw [Real.exp_add, Real.exp_add]; ring
  rw [hRHS]
  exact mul_le_mul_of_nonneg_left (Real.exp_le_exp.2 hkey) hcoef

lemma abs_kernelTerm_le_majorant {n : ℕ} (hn : 1 ≤ n) {u : ℝ} (hu : 0 ≤ u) :
    |kernelTerm n u| ≤ kernelMajorant n := by
  refine (abs_kernelTerm_le hn hu).trans ?_
  have h1 : Real.exp (-(π / 2) * Real.exp (4 * u)) ≤ 1 := by
    rw [Real.exp_le_one_iff]
    have := Real.pi_pos
    have : (0 : ℝ) < Real.exp (4 * u) := Real.exp_pos _
    nlinarith
  nlinarith [kernelMajorant_nonneg n, Real.exp_pos (-(π / 2) * Real.exp (4 * u))]


/-! ### Lemma 1: convergence, uniform convergence and continuity -/

/-- **Lemma 1a.** The defining series of `Φ` converges for every `u ≥ 0`. -/
theorem summable_kernelTerm {u : ℝ} (hu : 0 ≤ u) :
    Summable fun n : ℕ => kernelTerm (n + 1) u := by
  refine Summable.of_norm_bounded summable_kernelMajorant (fun n => ?_)
  simpa [Real.norm_eq_abs] using abs_kernelTerm_le_majorant (n := n + 1) (by omega) hu

lemma summable_abs_kernelTerm {u : ℝ} (hu : 0 ≤ u) :
    Summable fun n : ℕ => |kernelTerm (n + 1) u| :=
  Summable.of_nonneg_of_le (fun n => abs_nonneg _)
    (fun n => abs_kernelTerm_le_majorant (n := n + 1) (by omega) hu) summable_kernelMajorant

/-- **Lemma 1b.** The partial sums converge uniformly on all of `[0, ∞)`. -/
theorem tendstoUniformlyOn_Phi :
    TendstoUniformlyOn (fun N : ℕ => fun u : ℝ => ∑ n ∈ Finset.range N, kernelTerm (n + 1) u)
      Phi atTop (Ici 0) := by
  have hPhi : Phi = fun u : ℝ => ∑' n : ℕ, kernelTerm (n + 1) u := rfl
  rw [hPhi]
  refine tendstoUniformlyOn_tsum_nat (f := fun n u => kernelTerm (n + 1) u)
    summable_kernelMajorant (fun n u hu => ?_)
  simpa [Real.norm_eq_abs] using abs_kernelTerm_le_majorant (n := n + 1) (by omega) hu

/-- **Lemma 1b'.** In particular, the convergence is uniform on every subset of `[0, ∞)`,
in particular on every compact subset. -/
theorem tendstoUniformlyOn_Phi_subset {s : Set ℝ} (hs : s ⊆ Ici 0) :
    TendstoUniformlyOn (fun N : ℕ => fun u : ℝ => ∑ n ∈ Finset.range N, kernelTerm (n + 1) u)
      Phi atTop s :=
  tendstoUniformlyOn_Phi.mono hs

/-- **Lemma 1c.** `Φ` is continuous on `[0, ∞)`. -/
theorem continuousOn_Phi : ContinuousOn Phi (Ici 0) := by
  have hPhi : Phi = fun u : ℝ => ∑' n : ℕ, kernelTerm (n + 1) u := rfl
  rw [hPhi]
  refine continuousOn_tsum (u := fun n : ℕ => kernelMajorant (n + 1)) (fun n => ?_)
    summable_kernelMajorant (fun n u hu => ?_)
  · apply Continuous.continuousOn
    unfold kernelTerm
    fun_prop
  · simpa [Real.norm_eq_abs] using abs_kernelTerm_le_majorant (n := n + 1) (by omega) hu

/-! ### Lemma 2: measurability -/

/-- **Lemma 2.** `Φ` is a.e. strongly measurable on `(0, ∞)`. -/
theorem aestronglyMeasurable_Phi :
    AEStronglyMeasurable Phi (volume.restrict (Ioi (0 : ℝ))) :=
  (continuousOn_Phi.mono Ioi_subset_Ici_self).aestronglyMeasurable measurableSet_Ioi

/-! ### Lemma 3: superexponential decay -/

/-- **Lemma 3.** `|Φ u| ≤ C exp (-(π/2) e^{4u})` for all `u ≥ 0`. -/
theorem abs_Phi_le : ∃ C : ℝ, 0 < C ∧ ∀ u : ℝ, 0 ≤ u →
    |Phi u| ≤ C * Real.exp (-(π / 2) * Real.exp (4 * u)) := by
  set S : ℝ := ∑' n : ℕ, kernelMajorant (n + 1) with hS
  have hS0 : 0 ≤ S := tsum_nonneg fun n => kernelMajorant_nonneg _
  refine ⟨S + 1, by linarith, fun u hu => ?_⟩
  have hsum1 : Summable fun n : ℕ => |kernelTerm (n + 1) u| := summable_abs_kernelTerm hu
  have hsum2 : Summable fun n : ℕ =>
      kernelMajorant (n + 1) * Real.exp (-(π / 2) * Real.exp (4 * u)) :=
    summable_kernelMajorant.mul_right _
  have hstep1 : |Phi u| ≤ ∑' n : ℕ, |kernelTerm (n + 1) u| := by
    simpa [Phi, Real.norm_eq_abs] using
      norm_tsum_le_tsum_norm (f := fun n : ℕ => kernelTerm (n + 1) u)
        (by simpa [Real.norm_eq_abs] using hsum1)
  have hstep2 : (∑' n : ℕ, |kernelTerm (n + 1) u|) ≤
      ∑' n : ℕ, kernelMajorant (n + 1) * Real.exp (-(π / 2) * Real.exp (4 * u)) :=
    hsum1.tsum_mono hsum2 fun n => abs_kernelTerm_le (n := n + 1) (by omega) hu
  have hstep3 : (∑' n : ℕ, kernelMajorant (n + 1) * Real.exp (-(π / 2) * Real.exp (4 * u)))
      = S * Real.exp (-(π / 2) * Real.exp (4 * u)) :=
    summable_kernelMajorant.tsum_mul_right _
  have hexp : (0 : ℝ) < Real.exp (-(π / 2) * Real.exp (4 * u)) := Real.exp_pos _
  calc |Phi u| ≤ S * Real.exp (-(π / 2) * Real.exp (4 * u)) := by
        rw [← hstep3]; exact hstep1.trans hstep2
    _ ≤ (S + 1) * Real.exp (-(π / 2) * Real.exp (4 * u)) := by nlinarith

/-- **Lemma 3'.** For every `A` with `0 < A ≤ π/2` there is `C_A > 0` with
`|Φ u| ≤ C_A exp (-A e^{4u})` for all `u ≥ 0`.

(The hypothesis `0 < A` is stated as in the source text, but the proof only uses
`A ≤ π/2`.) -/
theorem abs_Phi_le_of_le_pi_div_two {A : ℝ} (hA : 0 < A) (hA' : A ≤ π / 2) :
    ∃ C : ℝ, 0 < C ∧ ∀ u : ℝ, 0 ≤ u → |Phi u| ≤ C * Real.exp (-A * Real.exp (4 * u)) := by
  obtain ⟨C, hC, hCbound⟩ := abs_Phi_le
  refine ⟨C, hC, fun u hu => ?_⟩
  refine (hCbound u hu).trans ?_
  have hE : (0 : ℝ) < Real.exp (4 * u) := Real.exp_pos _
  have : Real.exp (-(π / 2) * Real.exp (4 * u)) ≤ Real.exp (-A * Real.exp (4 * u)) :=
    Real.exp_le_exp.2 (by nlinarith)
  exact mul_le_mul_of_nonneg_left this hC.le

/-! ### Lemma 4: integrability of the dominating function -/

/-- **Lemma 4.** For all `t₀, y₀ ≥ 0`, the function `u ↦ exp (t₀ u² + y₀ u) ‖Φ u‖` is
integrable on `(0, ∞)`. -/
theorem integrable_exp_mul_norm_Phi {t₀ y₀ : ℝ} (ht : 0 ≤ t₀) (hy : 0 ≤ y₀) :
    Integrable (fun u : ℝ => Real.exp (t₀ * u ^ 2 + y₀ * u) * ‖Phi u‖)
      (volume.restrict (Ioi (0 : ℝ))) := by
  obtain ⟨C, hC, hCbound⟩ := abs_Phi_le
  have hg : Integrable
      (fun u : ℝ => (C * Real.exp ((t₀ + y₀ + 1) ^ 2)) * Real.exp (-1 * u))
      (volume.restrict (Ioi (0 : ℝ))) :=
    (exp_neg_integrableOn_Ioi 0 one_pos).const_mul _
  have hmeas : AEStronglyMeasurable
      (fun u : ℝ => Real.exp (t₀ * u ^ 2 + y₀ * u) * ‖Phi u‖)
      (volume.restrict (Ioi (0 : ℝ))) := by
    refine ContinuousOn.aestronglyMeasurable ?_ measurableSet_Ioi
    exact (Continuous.continuousOn (by fun_prop)).mul
      ((continuousOn_Phi.mono Ioi_subset_Ici_self).norm)
  refine hg.mono' hmeas ?_
  filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
  have hu0 : (0 : ℝ) ≤ u := le_of_lt hu
  have h1 : ‖Real.exp (t₀ * u ^ 2 + y₀ * u) * ‖Phi u‖‖
      = Real.exp (t₀ * u ^ 2 + y₀ * u) * |Phi u| := by
    rw [Real.norm_eq_abs, abs_mul, abs_of_pos (Real.exp_pos _), Real.norm_eq_abs, abs_abs]
  rw [h1]
  have h2 : Real.exp (t₀ * u ^ 2 + y₀ * u) * |Phi u|
      ≤ Real.exp (t₀ * u ^ 2 + y₀ * u) * (C * Real.exp (-(π / 2) * Real.exp (4 * u))) :=
    mul_le_mul_of_nonneg_left (hCbound u hu0) (Real.exp_pos _).le
  refine h2.trans ?_
  have h3 : Real.exp (t₀ * u ^ 2 + y₀ * u) * (C * Real.exp (-(π / 2) * Real.exp (4 * u)))
      = C * Real.exp (t₀ * u ^ 2 + y₀ * u + -(π / 2) * Real.exp (4 * u)) := by
    rw [Real.exp_add (t₀ * u ^ 2 + y₀ * u) (-(π / 2) * Real.exp (4 * u))]; ring
  have h4 : (C * Real.exp ((t₀ + y₀ + 1) ^ 2)) * Real.exp (-1 * u)
      = C * Real.exp ((t₀ + y₀ + 1) ^ 2 + -u) := by
    rw [Real.exp_add ((t₀ + y₀ + 1) ^ 2) (-u), neg_one_mul]; ring
  rw [h3, h4]
  have h5 : t₀ * u ^ 2 + y₀ * u + -(π / 2) * Real.exp (4 * u) ≤ (t₀ + y₀ + 1) ^ 2 + -u := by
    have := quadratic_sub_exp_le ht hy hu0
    linarith
  exact mul_le_mul_of_nonneg_left (Real.exp_le_exp.2 h5) hC.le

end HeatFlowKernel
