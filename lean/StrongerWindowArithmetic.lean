/-
  StrongerWindowArithmetic — machine-checked EXACT ARITHMETIC of the
  stronger-window (static re-anchor) research lane for the de Bruijn–Newman
  candidate bound Λ ≤ 0.1787854.

  The research lane (research/dynamic_boundary/) claims:

    CLAIM 1.  The candidate's objective is the exact rational identity
              t₀ + y₀²/2 = 0.1787854 with t₀ = 16125/100000 = 129/800 and
              y₀² = 350708/10⁷, and the collar width satisfies
              W² = 1 − y₀² − 2t₀ = 1606073/2500000.

    CLAIM 2.  The re-anchor site X = 6000345678901 fits inside the
              Platt–Trudgian verified-height budget X + 1 ≤ 2·T_PT with
              T_PT = 3000175332800, and the Riemann–Siegel window index
              N(x,t) = ⌊√(x/(4π) + t/16)⌋ equals 691008 on the WHOLE slab
              x ∈ [X, X+1], t ∈ [0, 129/800] (not merely at two corners).

    CLAIM 3.  Window 691009 is out of reach: for EVERY x within the budget
              (x ≤ 2·T_PT) and t ∈ [0, 129/800], √(x/(4π) + t/16) < 691009.

    CLAIM 4.  The finite reserve at the new site is exactly
              T_min − E_max = 8478389/10¹² − 233494905212337849/10²⁴
                            = 8244894094787662151/10²⁴,
              and it exceeds 14 times the current binding margin
              791366/10¹² − 233494905212337849/10²⁴.

    CLAIM 5.  (Conditional conversion.)  If the certified finite row erodes
              at slope ≥ 19 per unit t (the measured value is ≈ 19.05), then
              any t₀ decrease Δ ≥ 0 whose margin cost Δ·slope fits inside
              the reserve satisfies Δ < 44/10⁸ = 4.4·10⁻⁷.  Hence the
              reserve alone cannot lower Λ = t₀ + y₀²/2 by more than
              4.4·10⁻⁷ at fixed y₀².

  This file proves all five, sorry-free.  Real-number content enters ONLY
  through mathlib's proved bounds 3.141592 < π < 3.141593; everything else
  is exact integer/rational arithmetic discharged by `norm_num`/`nlinarith`.

  ## HONEST SCOPE STATEMENT

  What IS machine-checked here: the exact arithmetic and window-index
  geometry of the re-anchor claims, including both floor computations.

  What is NOT proved here: everything numerical-analytic — that the barrier
  program's certified transcript at X is valid (3,709 Arb prisms), the
  stored-row values T_min and E_max themselves (they are certified by the
  repository's interval-arithmetic programs and enter here as exact rational
  INPUTS), and the measured slope 19.05 (an empirical regression, entering
  CLAIM 5 only as an explicit hypothesis).  This file checks that the
  bookkeeping AROUND those certificates is exact, not the certificates.

  Axiom footprint of every result below is the mathlib-standard
  [propext, Classical.choice, Quot.sound] (verify via #print axioms).
-/
import Mathlib

open Real

namespace StrongerWindowArithmetic

/-! ## CLAIM 1 — the exact objective and collar-width identities -/

/-- **Λ objective identity**: t₀ + y₀²/2 = 0.1787854 exactly. -/
theorem lambda_row_identity :
    (16125 : ℚ) / 100000 + (350708 / 10 ^ 7) / 2 = 1787854 / 10 ^ 7 := by
  norm_num

/-- t₀ = 16125/100000 is the reduced rational 129/800. -/
theorem t0_reduced : (16125 : ℚ) / 100000 = 129 / 800 := by norm_num

/-- **Collar width identity**: W² = 1 − y₀² − 2t₀ = 1606073/2500000. -/
theorem curved_width_sq :
    (1 : ℚ) - 350708 / 10 ^ 7 - 2 * (129 / 800) = 1606073 / 2500000 := by
  norm_num

/-! ## CLAIMS 2 and 3 — window-index geometry of the re-anchor site

The Riemann–Siegel window index is N(x,t) = ⌊√(x/(4π) + t/16)⌋.  π enters
only through mathlib's `Real.pi_gt_3141592` / `Real.pi_lt_3141593`; the
decisive inequalities reduce to integer arithmetic under `norm_num`. -/

/-- The re-anchor site fits the Platt–Trudgian budget: X + 1 ≤ 2·T_PT. -/
theorem anchor_within_pt_budget :
    (6000345678901 : ℤ) + 1 ≤ 2 * 3000175332800 := by norm_num

/-- **Lower corner**: 691008 ≤ √(x/(4π) + t/16) whenever x ≥ X and t ≥ 0. -/
theorem sqrt_ge_691008 {x t : ℝ}
    (hx : (6000345678901 : ℝ) ≤ x) (ht : 0 ≤ t) :
    (691008 : ℝ) ≤ Real.sqrt (x / (4 * π) + t / 16) := by
  have hπu : π < 3.141593 := pi_lt_d6
  have hπ0 : (0 : ℝ) < π := pi_pos
  have h4π : (0 : ℝ) < 4 * π := by positivity
  -- 691008² · (4π) < 691008² · 12.566372 ≤ 6000345678901 ≤ x
  have hmul : (691008 : ℝ) ^ 2 * (4 * π) ≤ x := by nlinarith
  have hdiv : (691008 : ℝ) ^ 2 ≤ x / (4 * π) := by
    rw [le_div_iff₀ h4π]; exact hmul
  have ht16 : (0 : ℝ) ≤ t / 16 := by positivity
  have hq : (691008 : ℝ) ^ 2 ≤ x / (4 * π) + t / 16 := by linarith
  calc (691008 : ℝ) = Real.sqrt ((691008 : ℝ) ^ 2) := by
        rw [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 691008)]
    _ ≤ Real.sqrt (x / (4 * π) + t / 16) := Real.sqrt_le_sqrt hq

/-- **Budget ceiling (CLAIM 3)**: √(x/(4π) + t/16) < 691009 for every x
within the Platt–Trudgian budget (x ≤ 2·T_PT = 6000350665600) and every
t ≤ 129/800.  In particular window 691009 is unreachable, and (with
`anchor_within_pt_budget`) the upper slab corner of the re-anchor site
stays inside window 691008. -/
theorem sqrt_lt_691009 {x t : ℝ}
    (hx : x ≤ (6000350665600 : ℝ)) (ht : t ≤ 129 / 800) :
    Real.sqrt (x / (4 * π) + t / 16) < 691009 := by
  have hπl : (3.141592 : ℝ) < π := pi_gt_d6
  have hπ0 : (0 : ℝ) < π := pi_pos
  have h4π : (0 : ℝ) < 4 * π := by positivity
  -- x < 691009² · (4π) − (4π)·(129/12800): follows from
  -- 6000350665600 + 12.566372·(129/12800) < 691009² · 12.566368
  have hmul : x + (4 * π) * (t / 16) < (691009 : ℝ) ^ 2 * (4 * π) := by
    nlinarith
  have hq : x / (4 * π) + t / 16 < (691009 : ℝ) ^ 2 := by
    rw [div_add' _ _ _ (ne_of_gt h4π), div_lt_iff₀ h4π]
    nlinarith
  exact (Real.sqrt_lt' (by norm_num : (0 : ℝ) < 691009)).mpr hq

/-- **CLAIM 2 (main)**: the window index is 691008 on the whole re-anchor
slab x ∈ [X, X+1], t ∈ [0, 129/800]. -/
theorem window_index_691008 {x t : ℝ}
    (hx : (6000345678901 : ℝ) ≤ x) (hx' : x ≤ (6000345678902 : ℝ))
    (ht : 0 ≤ t) (ht' : t ≤ 129 / 800) :
    ⌊Real.sqrt (x / (4 * π) + t / 16)⌋ = 691008 := by
  have hlo := sqrt_ge_691008 hx ht
  have hhi := sqrt_lt_691009 (by linarith : x ≤ (6000350665600 : ℝ)) ht'
  rw [Int.floor_eq_iff]
  constructor
  · exact_mod_cast hlo
  · push_cast
    linarith

/-! ## CLAIM 4 — the exact reserve arithmetic

T_min = 8478389/10¹² is the sealed stored suffix floor at N = 691008;
E_max = 233494905212337849/10²⁴ is the certified Proposition 4.10 error
bound; 791366/10¹² is the sealed binding row at the current anchor
(N = 690988).  All three enter as exact rational inputs — their own
certification is interval-arithmetic work outside this file. -/

/-- **Reserve identity**: T_min − E_max = 8244894094787662151/10²⁴
(= 0.000008244894094787662151, the value displayed by the research lane). -/
theorem reserve_value :
    (8478389 : ℚ) / 10 ^ 12 - 233494905212337849 / 10 ^ 24
      = 8244894094787662151 / 10 ^ 24 := by
  norm_num

/-- **The new-site reserve exceeds 14× the current binding margin.**
(The exact ratio is ≈ 14.78.) -/
theorem reserve_exceeds_14x_current :
    14 * ((791366 : ℚ) / 10 ^ 12 - 233494905212337849 / 10 ^ 24)
      < 8478389 / 10 ^ 12 - 233494905212337849 / 10 ^ 24 := by
  norm_num

/-! ## CLAIM 5 — conditional conversion of reserve into a Λ reduction -/

/-- **Reserve-to-Δt₀ conversion.**  If the finite row erodes at slope ≥ 19
per unit t (measured: 19.05) and a t₀ decrease Δ ≥ 0 keeps the eroded
margin inside the reserve (Δ·slope ≤ reserve), then Δ < 4.4·10⁻⁷.  Since
Λ = t₀ + y₀²/2 falls one-for-one with t₀ at fixed y₀², the stronger-window
reserve alone cannot lower Λ by more than 4.4·10⁻⁷. -/
theorem reserve_conversion {slope Δ : ℚ}
    (hslope : 19 ≤ slope) (hΔ : 0 ≤ Δ)
    (hfits : Δ * slope ≤ 8244894094787662151 / 10 ^ 24) :
    Δ < 44 / 10 ^ 8 := by
  nlinarith [mul_le_mul_of_nonneg_left hslope hΔ]

/-- **The corresponding Λ floor of the pure-reserve route**: even spending
the whole conversion allowance, Λ cannot drop below 0.17878496. -/
theorem lambda_floor_of_reserve_route {Δ : ℚ}
    (hΔ : Δ < 44 / 10 ^ 8) :
    (17878496 : ℚ) / 10 ^ 8 < 1787854 / 10 ^ 7 - Δ := by
  have h : (1787854 : ℚ) / 10 ^ 7 - 44 / 10 ^ 8 = 17878496 / 10 ^ 8 := by
    norm_num
  linarith

#print axioms lambda_row_identity
#print axioms window_index_691008
#print axioms sqrt_lt_691009
#print axioms reserve_value
#print axioms reserve_exceeds_14x_current
#print axioms reserve_conversion

end StrongerWindowArithmetic
