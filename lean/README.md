# Lean 4 formalization — barrier analytic skeletons

`BarrierAnalyticSkeleton.lean` machine-checks (Lean 4 + mathlib v4.22.0, `sorry`-free,
axioms `[propext, Classical.choice, Quot.sound]`) the **reduction logic** of the two
prose-only analytic steps flagged in `EXTERNAL_REFEREE_REPORT_2026-07-28.md` §3:

1. **t=0 endpoint extension** — a lower bound on `(0, t0]` passes to the closed endpoint
   `t=0` by continuity (`lowerbound_extends_to_endpoint`), plus the compact-interval
   minimizer device the certificate uses (`strict_lowerbound_on_Icc_of_min`).
2. **B_t ≠ 0 on the rectangle** — `M0 · exp ≠ 0` (`Btmul_ne_zero`), positivity→uniform-δ
   on a compact set (`M0_ne_zero_of_continuous_pos_on_compact`), and the exact reduction
   `H z = 0 ↔ (H/B) z = 0` where `B ≠ 0` (`zeros_Ht_eq_zeros_g_of_B_ne_zero`).

**Scope (honest):** this formalizes only the reduction *logic*. Two candidate-specific
hypotheses remain to be discharged and are NOT proved here (they need the real Ξ / H_t):
(a) joint continuity of the true `H_t` up to `t=0` (dominated convergence, dominator
`e^{t0 u^2 + u} |Φ(u)|`); (b) `M0 ≠ 0` on the actual rectangle `R` (from the numerical
certificate bounding `‖M0‖` below). So it SHRINKS but does not eliminate the human-review
surface.

**Build:** requires Lean toolchain `leanprover/lean4:v4.22.0` + mathlib v4.22.0. Canonical
build environment is the mathexplorer project (`formalization/lean-mathlib-probe/`); this
copy is included as a review artifact. Verify:
`echo 'import BarrierAnalyticSkeleton
#print axioms Polynomial…'  -- see the file's #print axioms block`
