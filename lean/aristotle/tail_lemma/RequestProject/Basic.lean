import Mathlib

/-!
# Basic definitions for the all-`N`, all-`y` tail contraction theorem

This file collects the exact rational parameters, the window–freezing definitions
(`bt`, `Xwin`, `Lwin`, `Nidx`, `deltaWin`, `kWin`, `sig1`, `sig2`, `Gval`), the mollifier
`Mlam`, the endpoint cap `Cap`, and the contraction quantities `Pq`, `TRq`, `OVq`, `ABq`,
`Dq` used throughout.  It also contains Lemma 0 (the exact rational facts).

All numerical constants are the exact rationals of the source statement
(`0.02 = 1/50`, `0.626 = 313/500`, `6.66 = 333/50`, `1.24 = 31/25`, `0.125 = 1/8`,
`10.50 = 21/2`).
-/

namespace Job2

open Finset

/-- The support `𝒮 = {1,2,3,4,5,6,7,10,11,13,14}` of the mollifier weights. -/
def S : Finset ℕ := {1, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14}

/-- The mollifier weights `λ_d` (zero outside `𝒮`). -/
noncomputable def lam : ℕ → ℝ
  | 1 => 1
  | 2 => -1021/1000
  | 3 => -1054/1000
  | 4 => -9/200
  | 5 => -1119/1000
  | 6 => 1001/1000
  | 7 => -1043/1000
  | 10 => 128/125
  | 11 => -161/200
  | 13 => -447/500
  | 14 => 456373/500000
  | _ => 0

/-- The cutoff `N_* = 3840000`. -/
def Nstar : ℕ := 3840000

/-- The mollifier length `M = 153814`. -/
def Mcut : ℕ := 153814

/-- The error-side cutoff `M_err = 3000`. -/
def Merr : ℕ := 3000

/-- Left endpoint `t_0 = 129/800` of `I_t`. -/
noncomputable def t0 : ℝ := 129/800

/-- Right endpoint of `I_t`. -/
noncomputable def t1 : ℝ := 161250001/10^9

/-- `y_0^2 = 87677/2500000`. -/
noncomputable def y0sq : ℝ := 87677/2500000

/-- Left endpoint of `I_box` (and of `I_ext`). -/
noncomputable def yboxL : ℝ := 1872719/10^7

/-- Right endpoint of `I_box`. -/
noncomputable def yboxR : ℝ := 23409/125000

/-- Right endpoint of `I_ext`. -/
noncomputable def yextR : ℝ := 8231039/10^7

/-! ## Window freezing -/

/-- `b_t(u) = exp((t/4) log² u)`. -/
noncomputable def bt (t u : ℝ) : ℝ := Real.exp (t/4 * Real.log u ^ 2)

/-- `X_N(t) = 4π (N² - t/16)`. -/
noncomputable def Xwin (N t : ℝ) : ℝ := 4 * Real.pi * (N^2 - t/16)

/-- `L_N(t) = log (N² - t/16)`. -/
noncomputable def Lwin (N t : ℝ) : ℝ := Real.log (N^2 - t/16)

/-- `N(x,t) = ⌊√(x/(4π) + t/16)⌋`. -/
noncomputable def Nidx (x t : ℝ) : ℤ := ⌊Real.sqrt (x/(4*Real.pi) + t/16)⌋

/-- `δ(N,t) = (t/4)(-log(1 - t/(16N²))) + t/(2 X_N(t)²)`. -/
noncomputable def deltaWin (N t : ℝ) : ℝ :=
  t/4 * (-Real.log (1 - t/(16*N^2))) + t/(2 * Xwin N t ^ 2)

/-- `k(N,t) = t/(2 (X_N(t) - 6))`. -/
noncomputable def kWin (N t : ℝ) : ℝ := t / (2 * (Xwin N t - 6))

/-- `σ₁(N,t,y) = (1+y)/2 + (t/2) log N - δ̂`. -/
noncomputable def sig1 (dh N t y : ℝ) : ℝ := (1+y)/2 + t/2 * Real.log N - dh

/-- `σ₂(N,t,y) = (1-y)/2 + (t/2) log N - δ̂ - k̂`. -/
noncomputable def sig2 (dh kh N t y : ℝ) : ℝ := (1-y)/2 + t/2 * Real.log N - dh - kh

/-- `G(N,t,y) = e^{0.02 y} (N² - t/16)^{-y/2}`. -/
noncomputable def Gval (N t y : ℝ) : ℝ := Real.exp (y/50) * (N^2 - t/16) ^ (-y/2)

/-- The mollifier `M_λ(z) = ∑_{d ∈ 𝒮} λ_d d^{-z}`. -/
noncomputable def Mlam (z : ℂ) : ℂ := ∑ d ∈ S, (lam d : ℂ) * (d:ℂ) ^ (-z)

/-- `M_max = ∑_{d ∈ 𝒮} |λ_d| d^{-σ₁}`. -/
noncomputable def Mmaxq (s : ℝ) : ℝ := ∑ d ∈ S, |lam d| * (d:ℝ) ^ (-s)

/-! ## Endpoint caps -/

/-- `E_{t,σ}(u) = exp((1-σ) log u + (t/4) log² u)`. -/
noncomputable def Ecap (t s u : ℝ) : ℝ := Real.exp ((1-s) * Real.log u + t/4 * Real.log u ^ 2)

/-- `Cap_t(a,c;σ) = max(E_{t,σ}(a), E_{t,σ}(c)) log(c/a)`. -/
noncomputable def Cap (t a c s : ℝ) : ℝ := max (Ecap t s a) (Ecap t s c) * Real.log (c/a)

/-! ## Contraction quantities -/

/-- `c_m(t) = ∑_{d ∈ 𝒮, d ∣ m} λ_d b_t(m/d)`. -/
noncomputable def cconv (t : ℝ) (m : ℕ) : ℝ :=
  ∑ d ∈ S.filter (· ∣ m), lam d * bt t ((m/d : ℕ) : ℝ)

/-- `P = ∑_{m=2}^{M} |c_m(t)| m^{-σ₁}`. -/
noncomputable def Pq (t s : ℝ) : ℝ := ∑ m ∈ Finset.Icc 2 Mcut, |cconv t m| * (m:ℝ) ^ (-s)

/-- `TR = ∑_{d ∈ 𝒮} |λ_d| d^{-σ₁} Cap_t(⌊M/d⌋, N; σ₁)`. -/
noncomputable def TRq (t N s : ℝ) : ℝ :=
  ∑ d ∈ S, |lam d| * (d:ℝ) ^ (-s) * Cap t ((Mcut / d : ℕ) : ℝ) N s

/-- `OV = ∑_{d ∈ 𝒮, d > 1} |λ_d| d^{-σ₁} Cap_t(N/(d+1), N; σ₁)`. -/
noncomputable def OVq (t N s : ℝ) : ℝ :=
  ∑ d ∈ S.filter (fun d => 1 < d), |lam d| * (d:ℝ) ^ (-s) * Cap t (N/((d:ℝ)+1)) N s

/-- `AB = G (∑_{k=1}^{M} b_t(k) k^{-σ₂} + Cap_t(M,N;σ₂))`. -/
noncomputable def ABq (t N s g : ℝ) : ℝ :=
  g * ((∑ k ∈ Finset.Icc 1 Mcut, bt t k * (k:ℝ) ^ (-s)) + Cap t (Mcut : ℝ) N s)

/-- `D = P + TR + OV + M_max · AB`. -/
noncomputable def Dq (dh kh N t y : ℝ) : ℝ :=
  Pq t (sig1 dh N t y) + TRq t N (sig1 dh N t y) + OVq t N (sig1 dh N t y)
    + Mmaxq (sig1 dh N t y) * ABq t N (sig2 dh kh N t y) (Gval N t y)

/-! ## Lemma 0 : exact rational facts -/

/-- Lemma 0(i): `λ₁ = 1`. -/
theorem lemma0_lam_one : lam 1 = 1 := rfl

/-- Lemma 0(ii): `∑_{d ∈ 𝒮} |λ_d| = 9918746/10⁶`. -/
theorem lemma0_abs_sum : ∑ d ∈ S, |lam d| = 9918746/10^6 := by
  simp [S, lam]
  norm_num [abs_of_nonneg, abs_of_nonpos]

/-- Lemma 0(iii): `(1872719/10⁷)² < y₀² < (23409/125000)²`. -/
theorem lemma0_y0_bounds : yboxL ^ 2 < y0sq ∧ y0sq < yboxR ^ 2 := by
  constructor <;> norm_num [yboxL, yboxR, y0sq]

/-- Lemma 0(iv): `(8231039/10⁷)² ≥ 1 - 2 t₀`. -/
theorem lemma0_ext_right : 1 - 2 * t0 ≤ yextR ^ 2 := by
  norm_num [yextR, t0]

end Job2
