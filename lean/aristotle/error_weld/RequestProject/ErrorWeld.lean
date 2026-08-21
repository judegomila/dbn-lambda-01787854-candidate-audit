import Mathlib

open scoped Real

namespace ErrorWeld

/-- The real-valued modulus `|log (x/(4π)) + iπ/2| = sqrt (log²(x/(4π)) + π²/4)`. -/
noncomputable def modLog (x : ℝ) : ℝ :=
  Real.sqrt ((Real.log (x / (4 * Real.pi))) ^ 2 + Real.pi ^ 2 / 4)

lemma modLog_nonneg (x : ℝ) : 0 ≤ modLog x := Real.sqrt_nonneg _

/-- **Remark.** The modulus agrees with the absolute value of the complex number
`log (x/(4π)) + i π/2`. -/
lemma modLog_eq_norm (x : ℝ) :
    modLog x = ‖(Real.log (x / (4 * Real.pi)) : ℂ) + Complex.I * (Real.pi / 2)‖ := by
  rw [modLog, Complex.norm_def, Complex.normSq_apply]
  simp
  ring_nf

/-- **Lemma 1 (exact constant arithmetic).** `3.58 + 6.92 = 10.50`. -/
theorem lemma1_constants : (179 : ℚ) / 50 + 173 / 25 = 21 / 2 := by norm_num

/-- **Lemma 2 (denominator direction).** For `x ≥ 200` we have `x - 12 < x - 8.52` and
`x - 12 > 0`, hence dividing a nonnegative numerator by the smaller denominator only
increases the quotient. -/
theorem lemma2_denominator {x : ℝ} (hx : 200 ≤ x) :
    x - 12 < x - 8.52 ∧ 0 < x - 12 ∧ ∀ A : ℝ, 0 ≤ A → A / (x - 8.52) ≤ A / (x - 12) := by
  refine ⟨by norm_num, by linarith, fun A hA => ?_⟩
  exact div_le_div_of_nonneg_left hA (by linarith) (by linarith)

/-- **Lemma 3.** The elementary inequality `1 + u ≤ exp u` for real `u`. -/
theorem one_add_le_exp' (u : ℝ) : 1 + u ≤ Real.exp u :=
  (Real.add_one_le_exp u).trans_eq' (by ring)

/-- **Theorem (conservative weld).**  From Polymath Proposition 6.6(vi) (entering as the
hypothesis `hP66`) one obtains, for `x ≥ 200`, `t ≥ 0`, `N > 0.125`, `e_{C,0} ≥ 0`, the
bound with constant `10.50 = 21/2` and denominator `x - 12`.

The hypotheses `ht : 0 ≤ t` and `he : 0 ≤ eC0` are those requested in the statement of the
problem; the derivation does not in fact need them, since the conclusion follows from the
hypothesis `hP66` by enlarging its right-hand side. -/
theorem conservative_weld
    {x y t N eC0 : ℝ} (hx : 200 ≤ x) (ht : 0 ≤ t) (hN : (1 : ℝ) / 8 < N) (he : 0 ≤ eC0)
    (hP66 : eC0 ≤
      (x / (4 * Real.pi)) ^ (-(1 + y) / 4) *
        Real.exp (-(t / 16) * (Real.log (x / (4 * Real.pi))) ^ 2) *
        Real.exp ((3 * modLog x + 179 / 50) / (x - 8.52)) *
        (1 + (31 / 25) * ((3 : ℝ) ^ y + (3 : ℝ) ^ (-y)) / (N - 1 / 8) + (173 / 25) / (x - 12))) :
    eC0 ≤
      (x / (4 * Real.pi)) ^ (-(1 + y) / 4) *
        Real.exp (-(t / 16) * (Real.log (x / (4 * Real.pi))) ^ 2
          + (31 / 25) * ((3 : ℝ) ^ y + (3 : ℝ) ^ (-y)) / (N - 1 / 8)
          + (3 * modLog x + 21 / 2) / (x - 12)) := by
  have hpi : (0:ℝ) < Real.pi := Real.pi_pos
  have hx12 : (0:ℝ) < x - 12 := by linarith
  have hx852 : (0:ℝ) < x - 8.52 := by linarith
  have hM : 0 ≤ modLog x := modLog_nonneg x
  set L : ℝ := Real.log (x / (4 * Real.pi)) with hL
  set P : ℝ := (x / (4 * Real.pi)) ^ (-(1 + y) / 4) with hP
  have hPpos : 0 < P := Real.rpow_pos_of_pos (by positivity) _
  set A : ℝ := (31 / 25) * ((3 : ℝ) ^ y + (3 : ℝ) ^ (-y)) / (N - 1 / 8) with hA
  have hApos : 0 ≤ A := by
    have h1 : (0:ℝ) < (3:ℝ) ^ y := Real.rpow_pos_of_pos (by norm_num) _
    have h2 : (0:ℝ) < (3:ℝ) ^ (-y) := Real.rpow_pos_of_pos (by norm_num) _
    have h3 : (0:ℝ) < N - 1/8 := by linarith
    positivity
  set B : ℝ := (173 / 25) / (x - 12) with hB
  have hBpos : 0 ≤ B := by positivity
  set C : ℝ := 3 * modLog x + 179 / 50 with hC
  have hCpos : 0 ≤ C := by positivity
  -- Step 1: `1 + u ≤ exp u` applied to the last parenthesized factor.
  have step1 : 1 + A + B ≤ Real.exp (A + B) := by
    have := one_add_le_exp' (A + B); linarith
  -- Step 2: enlarge the denominator `x - 8.52` to `x - 12`.
  have step2 : C / (x - 8.52) ≤ C / (x - 12) :=
    div_le_div_of_nonneg_left hCpos hx12 (by linarith)
  have hexp2 : Real.exp (C / (x - 8.52)) ≤ Real.exp (C / (x - 12)) := Real.exp_le_exp.2 step2
  -- Step 3: collect exponents, using `3.58 + 6.92 = 10.50`.
  have h2 : Real.exp (C / (x - 12)) * Real.exp (A + B)
      = Real.exp (A + (3 * modLog x + 21 / 2) / (x - 12)) := by
    rw [← Real.exp_add]
    congr 1
    simp only [hC, hB]
    field_simp
    ring
  have h1 : Real.exp (C / (x - 8.52)) * (1 + A + B) ≤
      Real.exp (C / (x - 12)) * Real.exp (A + B) :=
    mul_le_mul hexp2 step1 (by linarith) (Real.exp_nonneg _)
  have h3 : (0:ℝ) ≤ P * Real.exp (-(t / 16) * L ^ 2) := by positivity
  calc eC0 ≤ P * Real.exp (-(t / 16) * L ^ 2) * Real.exp (C / (x - 8.52)) * (1 + A + B) := hP66
    _ = (P * Real.exp (-(t / 16) * L ^ 2)) *
          (Real.exp (C / (x - 8.52)) * (1 + A + B)) := by ring
    _ ≤ (P * Real.exp (-(t / 16) * L ^ 2)) *
          (Real.exp (C / (x - 12)) * Real.exp (A + B)) := mul_le_mul_of_nonneg_left h1 h3
    _ = (P * Real.exp (-(t / 16) * L ^ 2)) *
          Real.exp (A + (3 * modLog x + 21 / 2) / (x - 12)) := by rw [h2]
    _ = P * Real.exp (-(t / 16) * L ^ 2 + A + (3 * modLog x + 21 / 2) / (x - 12)) := by
          simp only [Real.exp_add]; ring

end ErrorWeld
