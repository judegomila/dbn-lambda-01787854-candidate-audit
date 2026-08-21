/-
Formalization of `job7_theorem12_weld.tex`:

  "Top-level weld: Polymath Theorem 1.2 instantiated at the 0.1787854 row".

The published inputs (Polymath15 Theorem 1.2, the Platt--Trudgian verified height,
the classical `ξ` functional-equation sign map, the analytic continuation of the
Dirichlet `η`-function) and the two certificate outputs (the final-time
nonvanishing `FT` and the barrier rectangle `BR`) all enter as explicit
hypotheses, exactly as in the source document.  Everything else is proved.
-/
import Mathlib

open Complex Filter Topology Set

open scoped Real

namespace Weld

noncomputable section

/-! ## Objects -/

/-- The Polymath15 kernel
`Φ(u) = ∑_{n ≥ 1} (2π²n⁴e^{9u} - 3πn²e^{5u}) exp(-πn²e^{4u})`. -/
def Phi (u : ℝ) : ℝ :=
  ∑' n : ℕ,
    (2 * π ^ 2 * ((n : ℝ) + 1) ^ 4 * Real.exp (9 * u)
      - 3 * π * ((n : ℝ) + 1) ^ 2 * Real.exp (5 * u))
      * Real.exp (-π * ((n : ℝ) + 1) ^ 2 * Real.exp (4 * u))

/-- `H t z = ∫_0^∞ e^{t u²} Φ(u) cos(z u) du` (the Polymath15 normalization). -/
def H (t : ℝ) (z : ℂ) : ℂ :=
  ∫ u in Ioi (0 : ℝ), ((Real.exp (t * u ^ 2) * Phi u : ℝ) : ℂ) * Complex.cos (z * u)

/-- The Riemann `ξ`-function `ξ(s) = s(s-1)/2 · π^{-s/2} Γ(s/2) ζ(s)`. -/
def xi (s : ℂ) : ℂ :=
  s * (s - 1) / 2 * (π : ℂ) ^ (-s / 2) * Complex.Gamma (s / 2) * riemannZeta s

/-- Characterization of the de Bruijn--Newman constant `Λ`: `H t` has only real
zeros if and only if `t ≥ Λ`. -/
def IsDeBruijnNewmanConstant (Lam : ℝ) : Prop :=
  ∀ t : ℝ, (∀ z : ℂ, H t z = 0 → z.im = 0) ↔ Lam ≤ t

/-! ## The exact row -/

/-- `X = 6000000185827`. -/
def X : ℝ := 6000000185827

/-- `t₀ = 129/800`. -/
def t0 : ℝ := 129 / 800

/-- `y₀² = 87677/2500000`. -/
def y0sq : ℝ := 87677 / 2500000

/-- `y₀`, the positive square root of `y₀²`. -/
def y0 : ℝ := Real.sqrt y0sq

/-- The Platt--Trudgian verified height `T_PT = 3000175332800`. -/
def TPT : ℝ := 3000175332800

/-! ## Lemma 1: exact rational identities -/

/-- Lemma 1, packaged as the pure rational arithmetic requested in the source
document: the five exact identities/inequalities of the `0.1787854` row. -/
theorem lemma1_rational_identities :
    ((129 : ℚ) / 800 + (1 / 2) * (87677 / 2500000) = 893927 / 5000000) ∧
    ((893927 : ℚ) / 2500000 < 1) ∧
    (1 - 2 * ((129 : ℚ) / 800) = 271 / 400) ∧
    ((87677 : ℚ) / 2500000 - (1809 / 10000) ^ 2 = 234599 / 100000000) ∧
    ((3000175332800 : ℚ) - 6000000185827 / 2 = 350479773 / 2) := by
  norm_num

theorem t0_pos : 0 < t0 := by norm_num [t0]

theorem t0_lt_half : t0 < 1 / 2 := by norm_num [t0]

theorem one_sub_two_t0 : 1 - 2 * t0 = 271 / 400 := by norm_num [t0]

theorem y0sq_pos : 0 < y0sq := by norm_num [y0sq]

theorem y0sq_lt_one_sub_two_t0 : y0sq < 1 - 2 * t0 := by norm_num [y0sq, t0]

theorem t0_add_half_y0sq : t0 + y0sq / 2 = 893927 / 5000000 := by norm_num [t0, y0sq]

theorem y0sq_add_two_t0 : y0sq + 2 * t0 = 893927 / 2500000 := by norm_num [y0sq, t0]

theorem y0sq_add_two_t0_lt_one : y0sq + 2 * t0 < 1 := by norm_num [y0sq, t0]

theorem y0sq_sub_barrier_sq : y0sq - (1809 / 10000) ^ 2 = 234599 / 100000000 := by
  norm_num [y0sq]

theorem barrier_sq_lt_y0sq : ((1809 : ℝ) / 10000) ^ 2 < y0sq := by norm_num [y0sq]

theorem TPT_sub_half_X : TPT - X / 2 = 350479773 / 2 := by norm_num [TPT, X]

theorem half_X_lt_TPT : X / 2 < TPT := by norm_num [X, TPT]

/-! ## Basic consequences for `y₀` -/

theorem y0_sq : y0 ^ 2 = y0sq := Real.sq_sqrt y0sq_pos.le

theorem y0_pos : 0 < y0 := Real.sqrt_pos.mpr y0sq_pos

theorem barrier_lt_y0 : (1809 : ℝ) / 10000 < y0 := by
  have h : Real.sqrt (((1809 : ℝ) / 10000) ^ 2) < Real.sqrt y0sq :=
    Real.sqrt_lt_sqrt (by positivity) barrier_sq_lt_y0sq
  rwa [Real.sqrt_sq (by norm_num)] at h

theorem half_lt_half_one_add_y0 : (1 : ℝ) / 2 < (1 + y0) / 2 := by
  have := y0_pos; linarith

/-! ## The Dirichlet eta function `η(σ) = ∑_{n ≥ 1} (-1)^{n-1} n^{-σ}` -/

/-- The `N`-th partial sum of `η(σ) = ∑_{n≥1} (-1)^{n-1} n^{-σ}`. -/
def etaPartial (σ : ℝ) (N : ℕ) : ℝ :=
  ∑ i ∈ Finset.range N, (-1) ^ i * (((i : ℝ) + 1) ^ (-σ))

/-- `HasEtaSum σ L` says that the (conditionally convergent) alternating series
defining `η(σ)` converges to `L`. -/
def HasEtaSum (σ L : ℝ) : Prop :=
  Tendsto (etaPartial σ) atTop (𝓝 L)

private theorem eta_terms_antitone {σ : ℝ} (hσ : 0 < σ) :
    Antitone fun i : ℕ => ((i : ℝ) + 1) ^ (-σ) := by
  intro a b hab
  refine Real.rpow_le_rpow_of_nonpos (by positivity) ?_ (neg_nonpos.mpr hσ.le)
  have : (a : ℝ) ≤ (b : ℝ) := Nat.cast_le.mpr hab
  linarith

private theorem eta_terms_tendsto_zero {σ : ℝ} (hσ : 0 < σ) :
    Tendsto (fun i : ℕ => ((i : ℝ) + 1) ^ (-σ)) atTop (𝓝 0) := by
  have h : Tendsto (fun x : ℝ => x ^ (-σ)) atTop (𝓝 0) :=
    tendsto_rpow_neg_atTop hσ
  exact h.comp (tendsto_atTop_add_const_right _ 1 tendsto_natCast_atTop_atTop)

/-- The alternating series defining `η(σ)` converges for every `σ > 0`. -/
theorem exists_hasEtaSum {σ : ℝ} (hσ : 0 < σ) : ∃ L, HasEtaSum σ L :=
  (eta_terms_antitone hσ).tendsto_alternating_series_of_tendsto_zero
    (eta_terms_tendsto_zero hσ)

/-- **Grouping argument**: `η(σ) > 0` for `σ > 0`.  Pairing consecutive terms,
the limit is at least the first pair `1 - 2^{-σ} > 0`. -/
theorem hasEtaSum_pos {σ L : ℝ} (hσ : 0 < σ) (hL : HasEtaSum σ L) : 0 < L := by
  have key := (eta_terms_antitone hσ).alternating_series_le_tendsto (l := L)
    (by simpa [etaPartial] using hL) 1
  have h1 : ∑ i ∈ Finset.range (2 * 1), (-1 : ℝ) ^ i * (((i : ℝ) + 1) ^ (-σ))
      = 1 - (2 : ℝ) ^ (-σ) := by
    norm_num [Finset.sum_range_succ, Real.one_rpow]
    ring
  rw [h1] at key
  have h2 : (2 : ℝ) ^ (-σ) < 1 :=
    Real.rpow_lt_one_of_one_lt_of_neg (by norm_num) (neg_neg_iff_pos.mpr hσ)
  linarith

/-! ## Hypotheses -/

/-- **Hypothesis EZ** (classical input): for `0 < σ < 1` the analytic
continuation of `ζ` satisfies `η(σ) = (1 - 2^{1-σ}) ζ(σ)`. -/
def EtaZetaHyp : Prop :=
  ∀ σ L : ℝ, 0 < σ → σ < 1 → HasEtaSum σ L →
    (L : ℂ) = (1 - (2 : ℂ) ^ (1 - (σ : ℂ))) * riemannZeta (σ : ℂ)

/-- **Hypothesis PT** (Platt--Trudgian): every nontrivial zero `ζ(σ + iT) = 0`
with `0 < T ≤ T_PT` has `σ = 1/2`. -/
def PTHyp : Prop :=
  ∀ σ T : ℝ, 0 < σ → σ < 1 → 0 < T → T ≤ TPT →
    riemannZeta ((σ : ℂ) + (T : ℂ) * I) = 0 → σ = 1 / 2

/-- The classical `ξ` functional-equation sign map: a zero `H₀(x + iy) = 0`
produces the zeros `ξ((1 - y + ix)/2) = 0` and `ξ((1 + y + ix)/2) = 0`. -/
def SignMapHyp : Prop :=
  ∀ x y : ℝ, H 0 ((x : ℂ) + (y : ℂ) * I) = 0 →
    xi ((1 - (y : ℂ) + (x : ℂ) * I) / 2) = 0 ∧ xi ((1 + (y : ℂ) + (x : ℂ) * I) / 2) = 0

/-- Condition (i) of Polymath Theorem 1.2 for the present row. -/
def CondI : Prop :=
  ∀ σ T : ℝ, (1 + y0) / 2 ≤ σ → σ ≤ 1 → 0 ≤ T → T ≤ X / 2 →
    riemannZeta ((σ : ℂ) + (T : ℂ) * I) ≠ 0

/-- Condition (ii) of Polymath Theorem 1.2 for the present row; this is also
exactly **Hypothesis FT** (final-time nonvanishing). -/
def CondII : Prop :=
  ∀ x y : ℝ, X + Real.sqrt (1 - y0sq) ≤ x → y0 ≤ y → y ≤ Real.sqrt (1 - 2 * t0) →
    H t0 ((x : ℂ) + (y : ℂ) * I) ≠ 0

/-- Condition (iii) of Polymath Theorem 1.2 for the present row. -/
def CondIII : Prop :=
  ∀ t x y : ℝ, 0 ≤ t → t ≤ t0 → X ≤ x → x ≤ X + Real.sqrt (1 - y0sq) →
    Real.sqrt (y0sq + 2 * (t0 - t)) ≤ y → y ≤ Real.sqrt (1 - 2 * t) →
    H t ((x : ℂ) + (y : ℂ) * I) ≠ 0

/-- **Hypothesis BR** (barrier rectangle): `H t` does not vanish on
`R = [X, X+1] + i[1809/10000, 1]` for `0 ≤ t ≤ t₀`. -/
def BRHyp : Prop :=
  ∀ t x y : ℝ, 0 ≤ t → t ≤ t0 → X ≤ x → x ≤ X + 1 → 1809 / 10000 ≤ y → y ≤ 1 →
    H t ((x : ℂ) + (y : ℂ) * I) ≠ 0

/-- **Hypothesis T12** (Polymath Theorem 1.2, arXiv:1904.12438v2) instantiated at
the present row: conditions (i), (ii), (iii) imply `Λ ≤ t₀ + y₀²/2`. -/
def T12Hyp (Lam : ℝ) : Prop :=
  CondI → CondII → CondIII → Lam ≤ t0 + y0sq / 2

/-! ## The endpoint `T = 0`: `ζ(σ) < 0` on `0 < σ < 1` -/

/-- Assuming the classical `η`-`ζ` identity, `ζ(σ)` is a negative real number for
real `σ ∈ (0,1)`; the positivity of `η(σ)` is proved (grouping argument) and
`1 - 2^{1-σ} < 0`. -/
theorem zeta_lt_zero_of_mem_Ioo (hEZ : EtaZetaHyp) {σ : ℝ} (h0 : 0 < σ) (h1 : σ < 1) :
    ∃ r : ℝ, r < 0 ∧ riemannZeta (σ : ℂ) = (r : ℂ) := by
  obtain ⟨L, hL⟩ := exists_hasEtaSum h0
  have hLpos : 0 < L := hasEtaSum_pos h0 hL
  set c : ℝ := 1 - (2 : ℝ) ^ (1 - σ) with hc
  have hgt : (1 : ℝ) < (2 : ℝ) ^ (1 - σ) :=
    Real.one_lt_rpow_iff_of_pos (by norm_num) |>.mpr (Or.inl ⟨by norm_num, by linarith⟩)
  have hcneg : c < 0 := by simp only [hc]; linarith
  have hcast : ((c : ℝ) : ℂ) = 1 - (2 : ℂ) ^ (1 - (σ : ℂ)) := by
    have : (((2 : ℝ) ^ (1 - σ) : ℝ) : ℂ) = (2 : ℂ) ^ ((1 - σ : ℝ) : ℂ) :=
      Complex.ofReal_cpow (by norm_num) _
    push_cast [hc] at this ⊢
    rw [this]
  have hEq := hEZ σ L h0 h1 hL
  rw [← hcast] at hEq
  have hcne : ((c : ℝ) : ℂ) ≠ 0 := by
    simpa using (ne_of_lt hcneg)
  refine ⟨L / c, div_neg_of_pos_of_neg hLpos hcneg, ?_⟩
  have hpc : ((L / c : ℝ) : ℂ) = (L : ℂ) / (c : ℂ) := by push_cast; ring
  rw [hpc, hEq, mul_comm, mul_div_assoc, div_self hcne, mul_one]

theorem zeta_ne_zero_of_mem_Ioo (hEZ : EtaZetaHyp) {σ : ℝ} (h0 : 0 < σ) (h1 : σ < 1) :
    riemannZeta (σ : ℂ) ≠ 0 := by
  obtain ⟨r, hr, hEq⟩ := zeta_lt_zero_of_mem_Ioo hEZ h0 h1
  rw [hEq]
  simpa using ne_of_lt hr

/-! ## Lemma 2: condition (i) from PT -/

/-- **Lemma 2.** Assuming the Platt--Trudgian verified height `PT` (together with
the classical `η`-`ζ` identity, used only at the endpoint `T = 0`), condition (i)
of Theorem 1.2 holds for the present row.

As formalized, condition (i) is a statement about `ζ` alone, so the `ξ`
functional-equation sign map of the source document is not needed here; its role
(producing the representative zero occurring in (i) from a zero of `H₀`) is
recorded separately in `Weld.xi_zero_of_H0_zero`. -/
theorem lemma2 (hEZ : EtaZetaHyp) (hPT : PTHyp) : CondI := by
  intro σ T hσ1 hσ2 hT1 hT2 hzero
  have hhalf : (1 : ℝ) / 2 < σ := lt_of_lt_of_le half_lt_half_one_add_y0 hσ1
  rcases eq_or_lt_of_le hσ2 with hσeq | hσlt
  · -- `σ = 1`: `ζ` does not vanish on `Re s ≥ 1`.
    refine riemannZeta_ne_zero_of_one_le_re (s := (σ : ℂ) + (T : ℂ) * I) ?_ hzero
    simp [hσeq]
  · rcases eq_or_lt_of_le hT1 with hTeq | hTpos
    · -- Endpoint `T = 0`: `ζ(σ) < 0`.
      refine zeta_ne_zero_of_mem_Ioo hEZ (by linarith) hσlt ?_
      rw [← hzero, ← hTeq]
      simp
    · -- `0 < T ≤ X/2 < T_PT`: Platt--Trudgian forces `σ = 1/2`.
      have hTle : T ≤ TPT := le_trans hT2 half_X_lt_TPT.le
      have := hPT σ T (by linarith) hσlt hTpos hTle hzero
      linarith

/-- The sign map of the source document: a zero `H₀(x + iy) = 0` produces the
`ξ`-zero at `(1 + y + ix)/2`, which is exactly the representative appearing in
condition (i). -/
theorem xi_zero_of_H0_zero (hSign : SignMapHyp) (x y : ℝ)
    (hz : H 0 ((x : ℂ) + (y : ℂ) * I) = 0) :
    xi ((1 + (y : ℂ) + (x : ℂ) * I) / 2) = 0 :=
  (hSign x y hz).2

/-! ## Lemma 3: barrier containment -/

/-- The region of condition (iii), as a set of triples `(t, x, y)`. -/
def regionIII : Set (ℝ × ℝ × ℝ) :=
  {p | 0 ≤ p.1 ∧ p.1 ≤ t0 ∧ X ≤ p.2.1 ∧ p.2.1 ≤ X + Real.sqrt (1 - y0sq) ∧
    Real.sqrt (y0sq + 2 * (t0 - p.1)) ≤ p.2.2 ∧ p.2.2 ≤ Real.sqrt (1 - 2 * p.1)}

/-- The barrier prism `R × [0, t₀]` with `R = [X, X+1] + i[1809/10000, 1]`, as a
set of triples `(t, x, y)`. -/
def barrierPrism : Set (ℝ × ℝ × ℝ) :=
  {p | 0 ≤ p.1 ∧ p.1 ≤ t0 ∧ X ≤ p.2.1 ∧ p.2.1 ≤ X + 1 ∧ 1809 / 10000 ≤ p.2.2 ∧ p.2.2 ≤ 1}

/-- **Lemma 3** as a pure set-containment statement over the reals: the region of
condition (iii) is contained in the barrier prism. -/
theorem lemma3_subset : regionIII ⊆ barrierPrism := by
  rintro ⟨t, x, y⟩ hp
  simp only [regionIII, Set.mem_setOf_eq] at hp
  obtain ⟨ht0, htt, hx1, hx2, hy1, hy2⟩ := hp
  simp only [barrierPrism, Set.mem_setOf_eq]
  refine ⟨ht0, htt, hx1, ?_, ?_, ?_⟩
  · -- `√(1 - y₀²) ≤ 1`
    have h : Real.sqrt (1 - y0sq) ≤ 1 := by
      have := y0sq_pos
      simpa using Real.sqrt_le_sqrt (show 1 - y0sq ≤ (1 : ℝ) by linarith)
    linarith
  · -- lower height: `y ≥ √(y₀² + 2(t₀ - t)) ≥ y₀ > 1809/10000`
    have h1 : y0 ≤ Real.sqrt (y0sq + 2 * (t0 - t)) := by
      rw [y0]
      exact Real.sqrt_le_sqrt (by linarith)
    have := barrier_lt_y0
    linarith
  · -- upper height: `y ≤ √(1 - 2t) ≤ 1`
    have h : Real.sqrt (1 - 2 * t) ≤ 1 := by
      simpa using Real.sqrt_le_sqrt (show 1 - 2 * t ≤ (1 : ℝ) by linarith)
    linarith

/-- **Lemma 3.** Assuming `BR`, condition (iii) of Theorem 1.2 holds. -/
theorem lemma3 (hBR : BRHyp) : CondIII := by
  intro t x y ht0 htt hx1 hx2 hy1 hy2
  have hmem : (t, x, y) ∈ regionIII := ⟨ht0, htt, hx1, hx2, hy1, hy2⟩
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := lemma3_subset hmem
  exact hBR t x y h1 h2 h3 h4 h5 h6

/-! ## The weld theorem -/

/-- **Theorem (weld).**  Assume Hypotheses T12, PT, FT and BR (together with the
classical `η`-`ζ` identity, which is used only at the endpoint `T = 0`).  Then
the de Bruijn--Newman constant satisfies
`Λ ≤ t₀ + y₀²/2 = 893927/5000000 = 0.1787854`.

Here `Lam` stands for the de Bruijn--Newman constant `Λ`, i.e. any real number
with `IsDeBruijnNewmanConstant Lam`; no property of `Lam` beyond the one supplied
by Hypothesis T12 is used. -/
theorem weld (Lam : ℝ) (hT12 : T12Hyp Lam) (hPT : PTHyp) (hFT : CondII) (hBR : BRHyp)
    (hEZ : EtaZetaHyp) :
    Lam ≤ 893927 / 5000000 := by
  have h := hT12 (lemma2 hEZ hPT) hFT (lemma3 hBR)
  rwa [t0_add_half_y0sq] at h

end

end Weld
