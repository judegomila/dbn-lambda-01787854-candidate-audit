# Summary of changes for run 90cb488c-608c-4f7d-bebb-f7f3e9a3716e
Formalized `job1_ht_continuity.tex` in Lean 4 / Mathlib, in the new file `RequestProject/HTContinuity.lean` (built as part of the project's `RequestProject` library). Everything compiles with no `sorry` and no extra axioms (only `propext`, `Classical.choice`, `Quot.sound`).

Definitions (namespace `HeatFlowKernel`):
- `kernelTerm n u = (2π²n⁴e^{9u} − 3πn²e^{5u})·exp(−πn²e^{4u})`, the n-th term of the Polymath15 heat-flow kernel;
- `Phi u = ∑' n, kernelTerm (n+1) u`, i.e. Φ(u) summed over n ≥ 1;
- `kernelMajorant`, the explicit Weierstrass majorant used for the M-test.

Theorems proved:
- Lemma 1a `summable_kernelTerm`: the series converges for every u ≥ 0.
- Lemma 1b `tendstoUniformlyOn_Phi` (with `tendstoUniformlyOn_Phi_subset`): the partial sums converge to Φ uniformly on all of [0, ∞), hence on every subset — in particular every compact subset — of [0, ∞). This is stronger than the locally uniform statement in the text.
- Lemma 1c `continuousOn_Phi`: Φ is continuous on [0, ∞).
- Lemma 2 `aestronglyMeasurable_Phi`: Φ is a.e. strongly measurable for `volume.restrict (Ioi 0)` — the hypothesis `h_Φ` of the target packaging.
- Lemma 3 `abs_Phi_le` and `abs_Phi_le_of_le_pi_div_two`: there is C > 0 with |Φ(u)| ≤ C·exp(−(π/2)e^{4u}) for all u ≥ 0, and correspondingly a constant C_A for every A ≤ π/2.
- Lemma 4 `integrable_exp_mul_norm_Phi`: for all t₀, y₀ ≥ 0 the function u ↦ exp(t₀u² + y₀u)‖Φ(u)‖ is Lebesgue-integrable on (0, ∞) — the hypothesis `h_dom`.

Supporting estimates are proved along the way: the splitting πn²e^{4u} ≥ (π/2)e^{4u} + (π/4)e^{4u} + (π/4)n² for n ≥ 1, u ≥ 0, boundedness of e^{9u−(π/4)e^{4u}}, summability of the majorant, and the bound t₀u² + y₀u + u − (π/2)e^{4u} ≤ (t₀+y₀+1)² which yields domination of the integrand by a constant multiple of e^{−u}.

One note on faithfulness: in Lemma 3' the hypothesis 0 < A is kept as in the source text even though the proof only needs A ≤ π/2; this is recorded in the docstring.