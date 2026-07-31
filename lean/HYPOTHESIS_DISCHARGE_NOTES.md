# Discharging the two open hypotheses of `BarrierAnalyticSkeleton.lean`

Scoping + progress notes, 2026-07-31.  Companion Lean file: `lean/HypothesisDischarge.lean`
(compiled, **sorry-free**; see §4 for the verified compiler output).

## 1. Build status

**The existing skeleton compiles as-is.**  Verified today in the canonical build
environment `~/Documents/GitHub/mathexplorer/formalization/lean-mathlib-probe/`:

- Toolchain: `leanprover/lean4:v4.22.0` (present in elan; `lean-toolchain` pins it).
- mathlib: tag `v4.22.0`, commit `79e94a093aff4a60fb1b1f92d9681e407124c2ca`
  (from `lake-manifest.json`), oleans already cached (`.lake` ≈ 5.5 GB).
- `lake build BarrierAnalyticSkeleton` → `Build completed successfully.`
- The copy in this repo is byte-identical to the probe copy (`diff` → identical),
  and `lake env lean <this repo>/lean/BarrierAnalyticSkeleton.lean` exits 0 with no output.

## 2. Hypothesis (a): joint continuity of the true `H_t` up to `t = 0`

### Target statement

With `Φ(u) := Σ_{n≥1} (2π²n⁴e^{9u} − 3πn²e^{5u})·exp(−πn²e^{4u})` (Polymath15 eq. (3))
and `H_t(z) = (1/8)·∫_{u>0} e^{tu²}·Φ(u)·cos(zu) du` (constant irrelevant to continuity):

```lean
theorem continuousOn_Ht :
    ContinuousOn
      (fun p : ℝ × ℂ =>
        ∫ u in Set.Ioi (0 : ℝ),
          Complex.exp ((p.1 : ℂ) * (u : ℂ) ^ 2) * Φ u * Complex.cos (p.2 * (u : ℂ)))
      (Set.Icc 0 t0 ×ˢ {z : ℂ | |z.im| ≤ y0})
```

### What is DONE (compiled, sorry-free, in `HypothesisDischarge.lean`)

`continuousOn_Ht_integral` proves exactly the statement above for an **abstract** `Φ`,
assuming only:

- `hΦ : AEStronglyMeasurable Φ (volume.restrict (Set.Ioi 0))`, and
- `hdom : Integrable (fun u => Real.exp (t0*u^2 + y0*u) * ‖Φ u‖) (volume.restrict (Set.Ioi 0))`
  — the README's dominator `e^{t0·u² + u}·|Φ(u)|`, with `e^u` generalized to `e^{y0·u}`
  (the README's form is the case `y0 = 1`; the rectangle has `0 ≤ y ≤ 1`).

Specializations `continuousOn_Ht_in_t` / `continuousOn_norm_Ht_in_t` (fixed `z`,
`t ∈ [0,t0]`) produce the exact `ContinuousOn F (Set.Icc 0 t0)` shape consumed by
`BarrierAnalyticSkeleton.strict_lowerbound_on_Icc_of_min` and
`lowerbound_extends_to_endpoint`.  A helper `norm_cos_le_exp_abs_im : ‖cos w‖ ≤ e^{|Im w|}`
was needed (no such bound found in mathlib v4.22.0).

### mathlib tools (names verified in the v4.22.0 checkout, not recalled)

- `MeasureTheory.continuousOn_of_dominated` — `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean:439`
  (also `continuousAt_of_dominated` :428, `continuous_of_dominated` :450; all under
  `[FirstCountableTopology X]`, satisfied by `ℝ × ℂ`).
- `Complex.norm_exp : ‖exp z‖ = Real.exp z.re` — `Mathlib/Data/Complex/Trigonometric.lean:937`.
- `Complex.mul_I_re` — `Mathlib/Data/Complex/Basic.lean:253` (for `‖e^{±iw}‖`).
- `MeasureTheory.ae_restrict_mem` — `Mathlib/MeasureTheory/Measure/Restrict.lean:590`.
- `Continuous.prodMk` — `Mathlib/Topology/Constructions/SumProd.lean:139`.
- `Continuous.aestronglyMeasurable`, `AEStronglyMeasurable.mul`, `Real.exp_le_exp`,
  `fun_prop` (dispatches all pointwise continuity goals).

### Genuinely new content still required

Instantiating `Φ`.  Two obligations, both **Φ-specific analysis, not assembly**:

1. **Measurability** (easy route: continuity of the series on `(0,∞)`, e.g. locally
   uniform convergence via `continuous_tsum` / Weierstrass M-test with the bound below).
2. **Integrability of the dominator**: needs a decay estimate of the shape
   `‖Φ u‖ ≤ C · e^{9u} · exp(−π e^{4u})` for `u ≥ 0` (sum the series against its `n = 1`
   term: `Σ n⁴ exp(−πn²e^{4u}) ≤ (Σ n⁴ e^{−π(n²−1)}) · exp(−πe^{4u})`), then
   `exp(t0·u² + y0·u + 9u − π·e^{4u})` integrable on `(0,∞)` by comparison with e.g.
   `exp(−u)` (the exponent is eventually `≤ −u`; split `[0,A]` compact + tail).
   Mathlib pieces: `summable_of_ratio_norm_eventually_le` or geometric comparison,
   `MeasureTheory.Integrable.mono`, `integrableOn_Ioi_deriv_of_nonneg`-style or
   `exp_neg` integrability (`Real.GammaIntegral`-adjacent lemmas / `integrable_exp_neg_mul_sq`
   are nearby models, none directly applicable).

Note also: full discharge of the skeleton's STEP-1 hypothesis for the **candidate's
actual barrier functional `F`** additionally needs continuity in `t` of the other
constituents (`B_t^{±1}`, the fixed finite Riemann–Siegel sum `f_t`, and the error
majorant — items 2–4 of the limit argument in `BARRIER_CERTIFICATE.md`).  Those are
finite sums / explicit elementary functions (no interchange-of-limits content); the
integral term addressed here is the only analytically nontrivial constituent.

### Difficulty verdict

**Bounded work, not a research project.**  The DCT/parametric-integral half is done
(compiled).  The remaining Φ-instantiation is a self-contained estimate; realistic
effort ≈ 300–800 lines of Lean, order of days to ~2 weeks for someone fluent in
mathlib's `MeasureTheory`/`tsum` API.  Main friction points: choosing a workable
form of the M-test bound, and the compact+tail integrability argument.

## 3. Hypothesis (b): `M0 ≠ 0` on the rectangle `R`

### Key finding: (b) is STRUCTURAL, not numerical — and is now discharged

The candidate's exposition (`dan-reworking/latex/gomila-proof-exposition.tex`,
§"The effective approximation") defines `M_0` by citing Polymath15 (arXiv:1904.12438v2)
eq. (6):

`M₀(s) := (1/8)·(s(s−1)/2)·π^{−s/2}·√(2π)·exp((s/2 − 1/2)·Log(s/2) − s/2)`

Every factor is nonzero away from `s ∈ {0,1}`: a `cpow` with nonzero base never
vanishes (`Complex.cpow_ne_zero_iff`, `Mathlib/Analysis/SpecialFunctions/Pow/Complex.lean:45`)
and `exp` never vanishes (`Complex.exp_ne_zero`).  On the rectangle the argument
`s = (1+y−ix)/2` has `Im s = −x/2 ≠ 0` (barrier region has `x ≥ 200`), so `s ∉ {0,1}`.
**No numerical certificate is needed for nonvanishing.**  (The certificate's lower
bound on `‖M₀‖` matters elsewhere — conditioning of the `g_t` evaluations — but not
for hypothesis (b) itself.  The certificate-shaped route
`M0_ne_zero_of_lt_norm_on` in the skeleton remains valid but is unnecessary.)

### What is DONE (compiled, sorry-free, in `HypothesisDischarge.lean`)

Verbatim transcriptions of Polymath15 eqs. (6), (9), (10), (11) as `M0`, `alpha`,
`Mt`, `Bt` (mathlib's `Complex.log` **is** the standard branch, `Im ∈ (−π, π]`,
matching the paper's `Log`), plus:

- `M0_ne_zero : s ≠ 0 → s ≠ 1 → M0 s ≠ 0`
- `M0_ne_zero_of_im_ne_zero`, `M0_ne_zero_on` (set-level shape consumed by the skeleton)
- `Mt_ne_zero : ∀ t, s ∉ {0,1} → Mt t s ≠ 0`
- `Bt_ne_zero : ∀ t y, x ≠ 0 → Bt t x y ≠ 0`  ← **hypothesis (b), and in fact the
  stronger `B_t ≠ 0` statement of the skeleton's STEP 2, discharged.**

### Remaining audit surface for (b)

One review item, not a proof item: confirm the candidate's Arb implementation of
`M₀/M_t/B_t` computes the same closed form as Polymath15 eqs. (6)/(9)/(10)/(11)
transcribed here.  (The exposition asserts this by citation; this repo contains no
independent formula definition to diff against.)

### Difficulty verdict

**Done** (modulo the definition-identification review item above).  ~70 lines of Lean.

## 4. Compiler evidence

`cd mathexplorer/formalization/lean-mathlib-probe && lake env lean <repo>/lean/HypothesisDischarge.lean`
(exit 0, no errors, no warnings, no `sorry`) prints exactly:

```
'HypothesisDischarge.M0_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'HypothesisDischarge.Bt_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'HypothesisDischarge.M0_ne_zero_on' depends on axioms: [propext, Classical.choice, Quot.sound]
'HypothesisDischarge.norm_cos_le_exp_abs_im' depends on axioms: [propext, Classical.choice, Quot.sound]
'HypothesisDischarge.continuousOn_Ht_integral' depends on axioms: [propext, Classical.choice, Quot.sound]
'HypothesisDischarge.continuousOn_Ht_in_t' depends on axioms: [propext, Classical.choice, Quot.sound]
'HypothesisDischarge.continuousOn_norm_Ht_in_t' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## 5. Recommendation

**Attempt (b) first — it is now effectively closed** at essentially zero marginal
cost (structural nonvanishing; this session).  Direct all remaining formalization
effort at (a)'s Φ-instantiation in this order:

1. define `Φ` as a `tsum`; prove the termwise bound and summability (M-test);
2. prove `‖Φ u‖ ≤ C·e^{9u}·exp(−π·e^{4u})` on `(0,∞)`;
3. prove integrability of `exp(t0·u² + y0·u)·‖Φ u‖` by comparison (compact `[0,A]`
   piece + dominated tail);
4. feed the two facts into the already-compiled `continuousOn_Ht_integral`.

Rationale: (b) had the better ratio of certainty to effort and is finished; (a)'s
remaining piece is the only step with real estimate content, and its interface
(`hΦ`, `hdom`) is now frozen by a compiled theorem, so the work is parallelizable
and cannot drift.
