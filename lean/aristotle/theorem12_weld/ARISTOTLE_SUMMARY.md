# Summary of changes for run 8cf76e04-449a-4f1e-9d98-b5260090dfc5
I formalized `job7_theorem12_weld.tex` in `RequestProject/Weld.lean` (namespace `Weld`). The file builds cleanly with Mathlib and contains no `sorry`; all results depend only on the standard axioms `propext`, `Classical.choice`, `Quot.sound`.

Objects and row constants
- `Phi`, `H t z = ∫_0^∞ e^{tu²}Φ(u)cos(zu)du` (Polymath15 normalization), `xi`, and `IsDeBruijnNewmanConstant` (the characterization of Λ).
- `X = 6000000185827`, `t0 = 129/800`, `y0sq = 87677/2500000`, `y0 = √y0sq`, `TPT = 3000175332800`.

Hypotheses, stated as Lean predicates exactly as in the document: `CondI`/`CondII`/`CondIII` (conditions (i)–(iii)), `T12Hyp`, `PTHyp` (Platt–Trudgian), `BRHyp` (barrier rectangle), `SignMapHyp` (ξ functional-equation sign map), and `EtaZetaHyp` (the classical continuation identity η(σ) = (1−2^{1−σ})ζ(σ)). Hypothesis FT is literally `CondII`.

Proved results
- (a) `lemma1_rational_identities`: the five exact rational identities/inequalities of the row, plus real-valued versions of every Lemma‑1 fact used later (e.g. `t0_add_half_y0sq`, `y0sq_add_two_t0_lt_one`, `y0sq_sub_barrier_sq`, `TPT_sub_half_X`).
- η-theory: `exists_hasEtaSum` (convergence of the alternating series for σ > 0) and `hasEtaSum_pos` (the grouping argument, η(σ) > 0), both proved; from these and `EtaZetaHyp`, `zeta_lt_zero_of_mem_Ioo` shows ζ(σ) is a negative real for 0 < σ < 1, hence `zeta_ne_zero_of_mem_Ioo`.
- (b) `lemma2`: condition (i) from PT. The three cases are handled: σ = 1 by non-vanishing of ζ on Re s ≥ 1, the endpoint T = 0 by the η-argument above, and 0 < T ≤ X/2 < T_PT by PT together with (1+y₀)/2 > 1/2. As formalized, condition (i) is a statement about ζ alone, so the sign map is not needed in the proof; its role is recorded separately as `xi_zero_of_H0_zero`.
- (c) `lemma3_subset : regionIII ⊆ barrierPrism`, a pure set-containment theorem over the reals (√(1−y₀²) ≤ 1, √(y₀²+2(t₀−t)) ≥ y₀ > 1809/10000, √(1−2t) ≤ 1), and `lemma3 : BRHyp → CondIII`.
- (d) `weld`: for any real `Lam`, from `T12Hyp Lam`, `PTHyp`, FT (`CondII`) and `BRHyp` one gets `Lam ≤ 893927/5000000`.

One caveat on (d): besides the four hypotheses listed in the document, `weld` also carries `EtaZetaHyp`. It is needed for the T = 0 endpoint of condition (i), which cannot be obtained from PT alone; the document explicitly permits this endpoint input (ζ(σ) < 0 on (0,1) / the η-manipulation) to enter as a hypothesis, and the preferred part — the grouping argument η(σ) > 0 — is proved rather than assumed.

The work is committed and pushed.