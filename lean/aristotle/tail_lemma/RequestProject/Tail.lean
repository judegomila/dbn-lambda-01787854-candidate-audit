import RequestProject.Monotone
import RequestProject.Errors

/-!
# The tail theorem

For every `t ∈ I_t`, `y ∈ [y₀, √(1-2t)]` and `x ≥ X_{N_*}(t)` one has
`|f_t(x+iy)| > e_A + e_B + e_{C,0}`, and consequently `H_t(x+iy) ≠ 0`.

The theorem is stated with Hypotheses H1, H2, H3 and the cap/`YM` gates as explicit
hypotheses, exactly as in the source statement; the internal chain uses Lemma 3 (contraction),
Lemma 4 (reduction of all `N ≥ N_*` to the cutoff) and Lemma 5 (the complete `y`-range).

Note on H2: in this packaging Hypothesis H3 already certifies the *numerical* bound on
`e_A+e_B+e_{C,0}` uniformly on the region, so the majorant hypothesis H2 is carried along as a
hypothesis (as requested) but is not needed by the formal derivation; the role it plays in the
informal argument — reducing the errors to the left edge of the window — is exactly the content
of Lemma 6, which is proved separately in `RequestProject/Errors.lean`.
-/

namespace Job2

open Finset

/-- `Δ(N,t) = ((t²/16) L_N(t)² + 0.626)/(X_N(t) - 6.66)`. -/
noncomputable def DeltaW (N t : ℝ) : ℝ :=
  (t^2/16 * Lwin N t ^ 2 + 313/500) / (Xwin N t - 333/50)

/-- The error majorant of Hypothesis H2: `e_A + e_B + e_{C,0}` is bounded by this. -/
noncomputable def errMaj (dh kh : ℝ) (N : ℕ) (t y : ℝ) : ℝ :=
  (Real.exp (DeltaW N t) - 1) *
      ((∑ n ∈ Finset.Icc 1 N, bt t n * (n:ℝ) ^ (-sig1 dh N t y))
        + Gval N t y * ∑ n ∈ Finset.Icc 1 N, bt t n * (n:ℝ) ^ (-sig2 dh kh N t y))
    + Real.exp (-(1+y)/4 * Lwin N t - t/16 * Lwin N t ^ 2
        + (31/25) * ((3:ℝ) ^ y + (3:ℝ) ^ (-y)) / ((N:ℝ) - 1/8)
        + (3 * Real.sqrt (Lwin N t ^ 2 + Real.pi ^ 2 / 4) + 21/2) / (Xwin N t - 12))

/-- `M_max ≥ 1`, because the term `d = 1` contributes `|λ₁| = 1`. -/
lemma one_le_Mmaxq (s : ℝ) : 1 ≤ Mmaxq s := by
  have h1 : (1:ℕ) ∈ S := by decide
  have hterm : |lam 1| * ((1:ℕ):ℝ) ^ (-s) = 1 := by
    simp [lam]
  calc (1:ℝ) = |lam 1| * ((1:ℕ):ℝ) ^ (-s) := hterm.symm
    _ ≤ Mmaxq s := Finset.single_le_sum
        (f := fun d : ℕ => |lam d| * (d:ℝ) ^ (-s))
        (fun d _ => mul_nonneg (abs_nonneg _) (Real.rpow_nonneg (by positivity) _)) h1

lemma y0_pos : 0 < Real.sqrt y0sq := Real.sqrt_pos.2 (by norm_num [y0sq])

lemma yboxL_le_y0 : yboxL ≤ Real.sqrt y0sq := by
  have h := lemma0_y0_bounds.1
  have hL : (0:ℝ) < yboxL := by norm_num [yboxL]
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ y0sq by norm_num [y0sq]),
    Real.sqrt_nonneg y0sq, y0_pos]

lemma y0_le_yboxR : Real.sqrt y0sq ≤ yboxR := by
  have h := lemma0_y0_bounds.2
  have hR : (0:ℝ) < yboxR := by norm_num [yboxR]
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ y0sq by norm_num [y0sq]),
    Real.sqrt_nonneg y0sq]

lemma yboxR_le_yextR : yboxR ≤ yextR := by norm_num [yboxR, yextR]

lemma sqrt_one_sub_two_t_le_yextR {t : ℝ} (ht : t0 ≤ t) : Real.sqrt (1 - 2*t) ≤ yextR := by
  have h1 : 1 - 2*t ≤ yextR ^ 2 := le_trans (by linarith) lemma0_ext_right
  have h2 : (0:ℝ) ≤ yextR := by norm_num [yextR]
  calc Real.sqrt (1 - 2*t) ≤ Real.sqrt (yextR ^ 2) := Real.sqrt_le_sqrt h1
    _ = yextR := Real.sqrt_sq h2

/-- **Tail theorem.** For every `t ∈ I_t`, `y ∈ [y₀, √(1-2t)]` and `x ≥ X_{N_*}(t)`,
`|f_t(x+iy)| > e_A + e_B + e_{C,0}`, and consequently `H_t(x+iy) ≠ 0`.

All the hypotheses of the source statement are carried: H1, H2, the cap gates, the `YM` gate,
and the five numerical items of H3.  Three of them (H2, the `M_max < 1.608290` item of H3 and
the final margin item of H3) turn out not to be needed by the formal derivation — the chain
Lemma 3 → Lemma 4 → Lemma 5 together with `D < 0.999721`, `(1-D)/M_max > 0.0001735` and
`e_A+e_B+e_{C,0} < 1.1672·10⁻⁸` already gives the conclusion — but they are kept because the
source statement lists them. -/
theorem tail_theorem
    {dh kh : ℝ} (hdh : 0 ≤ dh) (hkh : 0 ≤ kh) (hsmall : dh + kh + yextR/2 < 1/2)
    {f Hfun Bfun : ℝ → ℂ → ℂ} {err : ℝ → ℝ → ℝ → ℝ} {sstar gam kap : ℝ → ℝ → ℝ → ℂ}
    -- Hypothesis H1 (Polymath Theorem 1.3)
    (hH1 : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc (Real.sqrt y0sq) (Real.sqrt (1 - 2*t)),
      ∀ x, Xwin Nstar t ≤ x → ∃ N : ℕ, Nstar ≤ N ∧
        f t ((x:ℂ) + (y:ℂ)*Complex.I) =
          (∑ k ∈ Finset.Icc 1 N, (bt t k : ℂ) * (k:ℂ) ^ (-sstar t y x))
          + gam t y x * ∑ k ∈ Finset.Icc 1 N, (((k:ℝ) ^ y : ℝ) : ℂ) * (bt t k : ℂ) *
              (k:ℂ) ^ (-(starRingEnd ℂ) (sstar t y x) - kap t y x) ∧
        ‖gam t y x‖ ≤ Gval N t y ∧
        sig1 dh N t y ≤ (sstar t y x).re ∧
        ‖kap t y x‖ ≤ kh ∧
        ‖Hfun t ((x:ℂ) + (y:ℂ)*Complex.I) / Bfun t ((x:ℂ) + (y:ℂ)*Complex.I)
            - f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ ≤ err t y x ∧
        Bfun t ((x:ℂ) + (y:ℂ)*Complex.I) ≠ 0)
    -- Hypothesis H2 (error majorants, at the window index supplied by H1)
    (hH2 : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yextR, ∀ x, Xwin Nstar t ≤ x →
      ∃ N : ℕ, Nstar ≤ N ∧ err t y x ≤ errMaj dh kh N t y)
    -- the cap gates of Lemma 4 at the cutoff
    (hTRgate : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yextR, ∀ d ∈ S,
        1 ≤ t/2 * Real.log ((Mcut/d : ℕ):ℝ)
              * (Real.log (Nstar:ℝ) - Real.log ((Mcut/d : ℕ):ℝ)) ∧
        1 ≤ (sig1 dh (Nstar:ℝ) t y - 1)
              * (Real.log (Nstar:ℝ) - Real.log ((Mcut/d : ℕ):ℝ)))
    (hABgate : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yextR,
        1 ≤ t/2 * Real.log (Mcut:ℝ) * (Real.log (Nstar:ℝ) - Real.log (Mcut:ℝ)) ∧
        1 ≤ (sig2 dh kh (Nstar:ℝ) t y - 1) * (Real.log (Nstar:ℝ) - Real.log (Mcut:ℝ)))
    (hsig1gate : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yextR, 1 ≤ sig1 dh (Nstar:ℝ) t y)
    -- the `YM` gate
    (hYM : ∀ t ∈ Set.Icc t0 t1, 1/50 - Lwin (Nstar:ℝ) t / 2 + Real.log (Nstar:ℝ) / 2 ≤ 0)
    -- Hypothesis H3 (Arb-certified numerics at the cutoff)
    (hD3 : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yboxR,
        Dq dh kh (Nstar:ℝ) t y < 999721/10^6)
    (hM3 : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yboxR,
        Mmaxq (sig1 dh (Nstar:ℝ) t y) < 1608290/10^6)
    (hR3 : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yboxR,
        1735/10^7 < (1 - Dq dh kh (Nstar:ℝ) t y) / Mmaxq (sig1 dh (Nstar:ℝ) t y))
    (herr3 : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yextR, ∀ x, Xwin Nstar t ≤ x →
        0 < err t y x ∧ err t y x < 11672/10^12)
    (hmargin : ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc yboxL yextR, ∀ x, Xwin Nstar t ≤ x →
        17352/10^8 < (1 - Dq dh kh (Nstar:ℝ) t (Real.sqrt y0sq))
            / Mmaxq (sig1 dh (Nstar:ℝ) t (Real.sqrt y0sq)) - err t y x) :
    ∀ t ∈ Set.Icc t0 t1, ∀ y ∈ Set.Icc (Real.sqrt y0sq) (Real.sqrt (1 - 2*t)),
      ∀ x, Xwin Nstar t ≤ x →
        err t y x < ‖f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ ∧ Hfun t ((x:ℂ) + (y:ℂ)*Complex.I) ≠ 0 := by
  intro t ht y hy x hx
  obtain ⟨N, hNstar, hfeq, hgam, hRe, hkapb, herrH, hB⟩ := hH1 t ht y hy x hx
  -- elementary facts about the parameters
  have ht0 : 0 ≤ t := le_trans (by norm_num [t0]) ht.1
  have ht1 : t ≤ 1 := le_trans ht.2 (by norm_num [t1])
  have hy0 : 0 < Real.sqrt y0sq := y0_pos
  have hyge : Real.sqrt y0sq ≤ y := hy.1
  have hypos : 0 ≤ y := le_trans hy0.le hyge
  have hyle : y ≤ yextR := le_trans hy.2 (sqrt_one_sub_two_t_le_yextR ht.1)
  have hyext : y ∈ Set.Icc yboxL yextR := ⟨le_trans yboxL_le_y0 hyge, hyle⟩
  have hy0box : Real.sqrt y0sq ∈ Set.Icc yboxL yboxR := ⟨yboxL_le_y0, y0_le_yboxR⟩
  have hy0ext : Real.sqrt y0sq ∈ Set.Icc yboxL yextR :=
    ⟨yboxL_le_y0, le_trans y0_le_yboxR yboxR_le_yextR⟩
  have hyextpos : (0:ℝ) < yextR := by norm_num [yextR]
  have hdhalf : dh < 1/2 := by linarith
  -- `N` versus the cutoff
  have hNstarR : ((Nstar:ℕ):ℝ) ≤ (N:ℝ) := by exact_mod_cast hNstar
  have hMN : Mcut < N := lt_of_lt_of_le (by norm_num [Mcut, Nstar]) hNstar
  have hMNstar : (Mcut:ℝ) < ((Nstar:ℕ):ℝ) := by norm_num [Mcut, Nstar]
  have hNstarpos : (0:ℝ) < ((Nstar:ℕ):ℝ) := by norm_num [Nstar]
  have hNstar15 : (15:ℝ) ≤ ((Nstar:ℕ):ℝ) := by norm_num [Nstar]
  have hNtstar : 0 < ((Nstar:ℕ):ℝ)^2 - t/16 := by
    have : ((Nstar:ℕ):ℝ) = 3840000 := by norm_num [Nstar]
    rw [this]
    nlinarith
  have hNt : 0 < (N:ℝ)^2 - t/16 := by nlinarith
  -- the cap-validity gates for Lemma 3
  have hcap1 : t/2 * Real.log (N:ℝ) < sig1 dh (N:ℝ) t y := by
    rw [sig1]; linarith
  have hcap2 : t/2 * Real.log (N:ℝ) < sig2 dh kh (N:ℝ) t y := by
    rw [sig2]; linarith
  -- Lemma 3 : the contraction bound at the window index `N`
  have h3 := lemma3_contraction (t := t) (y := y) (dh := dh) (kh := kh) (N := N)
      (sstar := sstar t y x) (gam := gam t y x) (kap := kap t y x)
      (f := f t ((x:ℂ) + (y:ℂ)*Complex.I)) ht0 hMN rfl rfl hfeq hRe hkapb hgam
      (Gval_pos hNt).le hcap1 hcap2
  -- Lemma 4 : reduce to the cutoff
  have h4 : Dq dh kh (N:ℝ) t y ≤ Dq dh kh ((Nstar:ℕ):ℝ) t y := by
    refine lemma4_reduction ht0 hypos hNstarpos hNstarR hNtstar (hsig1gate t ht y hyext)
      (fun d hd => ?_) hMNstar (hABgate t ht y hyext).1 (hABgate t ht y hyext).2
    have hd0 : 0 < d := one_le_of_mem_S hd
    have hdM : 1 ≤ Mcut / d := by
      refine (Nat.one_le_div_iff hd0).2 ?_
      have hd14 : d ≤ 14 := by fin_cases hd <;> norm_num
      simp only [Mcut]
      omega
    refine ⟨by exact_mod_cast hdM, ?_, (hTRgate t ht y hyext d hd).1, (hTRgate t ht y hyext d hd).2⟩
    calc ((Mcut/d : ℕ):ℝ) ≤ (Mcut:ℝ) := by exact_mod_cast Nat.div_le_self Mcut d
      _ < ((Nstar:ℕ):ℝ) := hMNstar
  -- Lemma 5 : reduce to `y = y₀`
  have h5 : Dq dh kh ((Nstar:ℕ):ℝ) t y ≤ Dq dh kh ((Nstar:ℕ):ℝ) t (Real.sqrt y0sq) :=
    lemma5_y_monotone hNstar15 hNtstar hMNstar hyge (hYM t ht)
  -- the mollifier bound
  have hMlam : ‖Mlam (sstar t y x)‖ ≤ Mmaxq (sig1 dh ((Nstar:ℕ):ℝ) t (Real.sqrt y0sq)) := by
    refine le_trans (norm_Mlam_le hRe) (Mmaxq_antitone ?_)
    refine le_trans (sig1_mono_y hyge) (sig1_mono_N ht0 hNstarpos hNstarR)
  -- numerics
  set Dstar := Dq dh kh ((Nstar:ℕ):ℝ) t (Real.sqrt y0sq) with hDstar
  set Mstar := Mmaxq (sig1 dh ((Nstar:ℕ):ℝ) t (Real.sqrt y0sq)) with hMstar
  have hMpos : (0:ℝ) < Mstar := lt_of_lt_of_le one_pos (one_le_Mmaxq _)
  have hDlt : Dstar < 999721/10^6 := hD3 t ht _ hy0box
  have hratio : 1735/10^7 < (1 - Dstar) / Mstar := hR3 t ht _ hy0box
  have herrlt : err t y x < 11672/10^12 := (herr3 t ht y hyext x hx).2
  -- `‖M_λ f‖ ≥ 1 - D`
  have hnorm1 : 1 - Dstar ≤ ‖Mlam (sstar t y x) * f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ := by
    have h := norm_sub_norm_le (1 : ℂ) (Mlam (sstar t y x) * f t ((x:ℂ) + (y:ℂ)*Complex.I))
    rw [norm_one, norm_sub_rev] at h
    have := le_trans h3 (le_trans h4 h5)
    linarith
  have hfnorm : (1 - Dstar) / Mstar ≤ ‖f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ := by
    rw [div_le_iff₀ hMpos]
    calc 1 - Dstar ≤ ‖Mlam (sstar t y x) * f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ := hnorm1
      _ = ‖Mlam (sstar t y x)‖ * ‖f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ := norm_mul _ _
      _ ≤ Mstar * ‖f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ :=
          mul_le_mul_of_nonneg_right hMlam (norm_nonneg _)
      _ = ‖f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ * Mstar := mul_comm _ _
  have hlt : err t y x < ‖f t ((x:ℂ) + (y:ℂ)*Complex.I)‖ := by
    have : (11672:ℝ)/10^12 ≤ 1735/10^7 := by norm_num
    linarith
  refine ⟨hlt, ?_⟩
  intro hH0
  rw [hH0, zero_div, zero_sub, norm_neg] at herrH
  linarith

end Job2
