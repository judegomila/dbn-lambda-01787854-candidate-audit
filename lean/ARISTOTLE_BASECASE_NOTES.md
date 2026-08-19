# DeBruijnNewman_BaseCase.aristotle.lean — Aristotle autoformalization

Independent Lean formalization (by **Harmonic Aristotle**, arXiv:2510.01346, 2026-08)
of the SAME two prose-only analytic steps that `BarrierAnalyticSkeleton.lean` reduces by
hand:

* **Step 1** endpoint extension by continuity → `DeBruijnNewman.zero_free_endpoint`;
* **Step 2** nonvanishing factor `B=M₀·exp(φ)` ⇒ zeros/winding of `g=H/B` equal those of
  `H` → `zeros_div_eq_zeros`, `analyticOrderAt_div_eq`, `windingRect_div_eq`.

15 lemmas, Lean-4 kernel-verified, recompiled sorry-free against mathlib v4.28.0
(key results axiom-clean `[propext, Classical.choice, Quot.sound]`).

**Scope (honest).** Abstract: `H : ℝ→ℂ→ℂ` is an abstract entire-function family, not the
built Riemann ξ/H_t. The argument principle is taken as an explicit hypothesis
(`windingRect_div_eq_zeroCount`) because mathlib lacks it — Aristotle flagged this itself.
So the *reduction logic* is machine-checked, at the same scope as `BarrierAnalyticSkeleton`.
Autoformalization caveat: proofs are verified; faithfulness of the statements/definitions
to the intended mathematics still warrants referee review.

This is a supplementary addition; the sealed certificate release (`SHA256SUMS`) is unchanged.
