# External referee report — Λ ≤ 0.1787854 candidate (v3)

**Package:** `dbn-lambda-01787854-candidate-audit`, sealed commit `2e9976c4becbf97e31c56fe75fce07cdff5dd4ea`, tree `7f15ecf8…`, release `review-01787854-v3`.
**Reviewer:** adversarial AI referee panel (four independent agents, one per proof leg + one cross-cutting), directed and synthesized by Claude (Opus 4.8), 2026-07-28.
**Scope reviewed:** the sealed repository source, the handwritten lemma notes, the fail-closed verifiers, the SHA-256 seal, and the bundled primary references (Polymath15 `1904.12438v2`, Platt–Trudgian `2004.09765v1`). The heavy interval computations were **not** independently recompiled (see §7).

> **Status this report supports:** the package **may not yet advance** beyond *unreviewed computer-assisted proof candidate*. No fatal or bound-invalidating defect was found in a deliberately adversarial pass, and every leg is established at the computer-assisted level, but three items require human mathematical sign-off and one requires an independent recompile before acceptance. This is an AI adversarial review, **not** a substitute for human expert peer review.

---

## 1. Summary verdict

The candidate instantiates **Polymath15 Theorem 1.2** (the barrier upper-bound criterion) at the exact row `X = 6000000185827`, `t₀ = 129/800`, `y₀² = 87677/2500000`, yielding `Λ ≤ t₀ + ½y₀² = 893927/5000000 = 0.1787854`. Its logical form is genuinely **unconditional**: it consumes only the published Polymath15 criterion, the published Polymath15 error theory, and the **finite** Platt–Trudgian verification — **no RH beyond finite height, no GUE / pair-correlation, no C_H / collision-meter input.** This places it on the *provable* side of the project's obstruction seam (the verified-height lever), unlike the separately-retracted "Λ ≤ 3.06×10⁻⁵" collision-route claim, which rested on an RH-equivalent modulus.

| Leg | Object | Verdict | Confidence |
|---|---|---|---|
| Assembly / seal / circularity | fail-closed final weld | **coherent, no hidden premise, seal 362/362 OK** | — |
| Hypothesis (i) | verified height + Thm 1.2 transcription | **established** | ~0.97 |
| Hypothesis (iii) | closed-barrier winding certificate | **established (computer-assisted)** | ~0.88 |
| Hypothesis (ii) | finite corpus + all-N tail + Dini transfer | **established modulo cited theorems; one coverage gap** | ~0.85 |

No leg was refuted. No bound-invalidating or fatal finding survived.

---

## 2. Hypothesis (i) — verified height + criterion transcription — ESTABLISHED (~0.97)

- **Polymath15 Theorem 1.2 is transcribed faithfully.** The statement in `PROOF_NOTE.md §2` (2.1–2.4) and `vendor/dbn21a/.../THEOREM_LAMBDA_CRITERION.md §1` matches the bundled primary PDF `references/polymath-1904.12438v2.pdf` (Thm 1.2, p.2) verbatim — same three regions, same open/closed endpoints, same conclusion `Λ ≤ t₀ + ½y₀²`. No hypothesis dropped or weakened. The candidate row satisfies the paper's own preconditions (`X, t₀ > 0`, `0 < y₀ ≤ 1`) and the harmless non-emptiness conditions `0 < t₀ < ½`, `0 < y₀² < 1 − 2t₀`.
- **Normalization is correct.** `H₀(z) = ⅛ ξ(½ + iz/2)` ⇒ a zero `H₀(x+iy)=0 ⇔ ξ((1−y)/2 + ix/2)=0`; the functional equation plus conjugation yields the representative `σ = (1+y)/2, T = x/2`. So `x = 2T` and a barrier at `X` consumes verified height `X/2`. `verifiers/verify_criterion_sign_map.py:33-55` reproduces this affine algebra; `vendor/.../verify_criterion.py:29-50` checks it symbolically + a numeric spot-check.
- **Verified height is genuinely licensed.** Required `X/2 = 3000000092913.5`. **Platt–Trudgian Theorem 1** (bundled PDF `2004.09765v1`, line 54) states RH verified to height **3 000 175 332 800**, which strictly exceeds `X/2` by **175 239 886.5 > 0**. The `T = 0` endpoint is closed classically (`η(σ) > 0` for `σ > 0`; `ζ(σ) < 0` on `(0,1)`; pole at `s=1`), `PROOF_NOTE.md:128-137`.
- **Nothing conditional hides in (i).** Confirmed: only the PT finite verification, classical `ζ < 0` on `(0,1)`, and the ξ functional equation.

**Documentary finding (robustness, not bound-invalidating):** the licensing depends on PT's **precise** reached height `3 000 175 332 800`, **not** the round "3×10¹²" of the abstract — with the round figure, `X/2` would *exceed* it by 92,913.5 and hypothesis (i) would fail. Any writeup must cite the precise Theorem-1 number. This is the thinnest external hook in the chain.

---

## 3. Hypothesis (iii) — closed-barrier winding certificate — ESTABLISHED, computer-assisted (~0.88)

- **The argument-principle mechanism is correctly implemented** (`barrier/src/TloopSinglemat_closed_cert.c`): a closed boundary polygon of `4·num−4` effective-sum values; each consecutive argument increment gated strictly inside `(−π, π)` (1259-1292); every endpoint ball gated zero-free; summed winding gated strictly inside `(−¼, ¼)` → integer 0 (1296-1306). The zero-avoiding homotopy (polygon → true `f_{t_i}` boundary → `f_τ` → `g_τ = H_t/B_t`) is rigorous: spatial ≤ `D_z·h/2` (`h ≤ 1/(num−1)`, the length-1 x-edge dominates; the `num−1` fix at 1345 is correct), time motion bounded on the **whole** prism via re-evaluation on the t-box (1390-1428, not a left-endpoint assumption), approximation ≤ 0.00125. Decisive predicate `min|f_{t_i}| > spatial + D_t·Δt + 0.00125` (1435-1444) is a strict fail-closed interval inequality.
- **The t=0 endpoint — the sharpest a-priori risk — is defused.** The first prism's left seam is **exactly** `t=0` (`arb_is_zero(ts)` required, 988), so `min|f₀|` on `∂R` is a **direct** interval evaluation (=4.278, margin 1.888), *not* a limit. The derivative majorants provably **do not blow up as `t→0`**: the relevant exponents contain no `1/t` or `log t`; `afac` carries `N^{t·y/(2(x−6))} → 1`. This eliminates the fatal "majorant diverges at the endpoint" scenario.
- **Margins clear with headroom.** Uniform error `e_A + e_B + e_{C,0} = 3.565230×10⁻⁴ < 0.00125` (3.5×); floor-square `y₀² − 0.1809² = 234599/10⁸ > 0`; per-prism margins reproduce from the printed enclosures; both toolchains (Linux/FLINT 3.0.1, macOS/FLINT 3.6.0) independently emit all 883 prisms + `RESULT: CLOSED SLAB CERTIFIED`.
- **Coefficient provenance + Taylor remainder clear.** 7688/7688 components regenerated inside restored balls `1e-20·max(1,|c|)`; the omitted Taylor tail `< 1.954234593244762×10⁻²²` is carried **separately** as a flat `1e-20` error added to every value — two distinct handlings, no double-count, no drop.

**Residual (documentary/local, standard & correct-as-written, not machine-verified):**
1. **`B_t ≠ 0` on the closed rectangle `R`** (needed for the argument principle to count `H_t` zeros) — asserted in `BARRIER_CERTIFICATE.md:110-118`, a standard Polymath fact, indirectly reinforced by `|g_t − f_t| ≤ 0.00125` with `|f_t|` bounded (a `B_t` zero would make `g_t` unbounded).
2. **The `t>0 → t=0` extension** of Lemma 8.4 / Theorem 1.3 by a dominated-convergence limit — `DERIVATIVE_BOX_LEMMA.md:141-150`, self-disclaimed at `verify_uniform_error_01787854.c:249` ("analytic justification at t=0 remains external").

---

## 4. Hypothesis (ii) — finite corpus + all-N tail + Dini transfer — ESTABLISHED modulo cited theorems (~0.85), with one coverage gap

**Sound on adversarial inspection:**
- **The all-N tail is a genuine uniform theorem, not sampling** (`TAIL_LEMMA.md §6`, `verify_tail_arb.c:504-620`): frozen `δ̂, κ̂` at `N_*` give a conservative lower-σ surrogate valid for all `N ≥ N_*`; every fixed-left cap decreases via gated bounds; no monotonicity in `t` assumed (the whole t-interval is Arb-evaluated).
- **The tail is robust, not fragile.** The reported `D = 0.99972…` includes deliberately-redundant OV padding (0.0392); §4 shows OV is redundant (`dk > M ⇔ k > ⌊M/d⌋`), so dropping it gives a genuine contraction ≈ **0.9605**, margin ~0.04 — four orders above the interval widths. Directed rounding is conservative throughout (`D` via upper, `flow = (1−D)/M_max` via lower, etc.).
- **Window-freeze kink handled correctly** (`WINDOW_FREEZE_THEOREM.md:60-85`): `Σ` strictly increasing in `x` through the `h=0` kink, both one-sided derivatives positive; tiling `[x_*, x_{3840001}) ∪ [x_{3840000}, ∞)` with no gap/overlap.
- **Finite margin robust to storage.** Producer stores `ARF_RND_FLOOR` of the lower ball endpoint (safe direction); binding `T_min = 7.91366×10⁻⁷` sits ~5 orders above the `1e-12` granularity; min-floor and `E_max` evaluated at the joint worst window `N₀ = 690988`. `E_max = 2.334949×10⁻⁷` ⇒ margin `5.5787×10⁻⁷ > 0`.
- **Error-constant weld enlarges the right way** (`ERROR_CONSTANT_WELD.md:30-49`): `1+u ≤ e^u`, `x−8.52 → x−12`, `10.44 → 10.50` all increase the error (conservative).
- **Native binding algebra sound** (`NATIVE_BINDING.md`): conjugate-convolution identity valid; `|m^{−κ}−1| ≤ m^{k_N}−1` for complex `κ` correct; `E ≠ 0` forced by `Q_N > 0`.

**Finding (LOCAL / GATING — the one real gap):** the **thinnest** load-bearing inequality — the Dini y-transfer proving numerator monotonicity `Num_N(y) ≥ Num_N(y₀)`, worst ratio **0.99999860767275095** (slack ≈ 1.39×10⁻⁶, `logs/triangle_y_dini_{180,256}.log:2`) — is **not executed or log-audited by the sealed assembly.** `verify_assembly_1787854.py`'s W2 gate consumes `verify_triangle_normalizer_corr_iv` (which gates only `M_N↓`, `K_N↓` — these do **not** imply the numerator mass transfer, since the A-side `|A_{N,n}(y)|` grows in `y`; that is precisely why `verify_triangle_y_dini_arb.c` exists). The tail C verifier **is** gated (via `verify_tail_arb_logs.py`); the Dini C verifier has **no** audited consumer in W2. Consequence: `verify.sh` passing does **not** check the most fragile load-bearing inequality in (ii) — it lives only as an out-of-band C program + sealed log + provenance note. **Not proof-invalidating** (the Dini theorem `provenance/TRIANGLE_Y_DINI_THEOREM.independent.md §1-4` is a rigorous branch-free upper-Dini-derivative argument, the C verifier is fail-closed, and 180/256-bit agree to 17 digits), but the "run the seal and everything load-bearing is verified" claim is **false for exactly the riskiest step**. See §6 for the remediation applied.

**Finding (documentary, non-binding):** the Dini verifier runs at the `t₀` singleton (`t = 16125/100000`) only, while some finite legs stored floors on the t-box `[t₀, t₀+1e-9]`. Non-binding: the global binding floor is in the leg that itself uses the `t₀` singleton; other legs exceed `E_max` by ~400×.

---

## 5. Cross-cutting — assembly, circularity, seal — COHERENT

- **Final assembly is fail-closed and free of hidden premises** (`verifiers/verify_assembly_1787854.py`): `(i) ∧ (ii) ∧ (iii) ⇒ Λ ≤ t₀ + ½y₀²` with an exact-rational parameter identity `T0 + Y0²/2 == 893927/5000000` (A1/W4). The three genuine external premises are printed as `[CITED THEOREM INPUT]` and correctly **not** code-gated (code cannot prove them).
- **No circularity.** `t₀, y₀², X` are inputs; the bound is their output; no certificate imports a value derived from `0.1787854`; the three hypotheses are logically independent.
- **Independence caveats (disclosed):** barrier `P12` vs `P13` (Linux/macOS) are genuinely different Arb runs (radii differ); tail `P9` vs `P10` are the **same file at two precisions** (a precision cross-check, not implementation independence) — the repo discloses this. The fast verifiers **parse the printed enclosures**; they do not recompile the heavy C, so a green PASS certifies "the printed balls satisfy the gates," not that `min_mesh` / `D_z` / `D_t` / producer floors `L_N` are *true* bounds on `|f_t|`.
- **Seal:** `shasum -a 256 -c SHA256SUMS` = **362/362 OK** on this checkout.
- **Honesty:** README headline is "unreviewed computer-assisted proof candidate"; `PROOF_NOTE §8` and `OPEN_REVIEW_QUESTIONS` disclose the weak points; overclaim grep ("proven / QED / established theorem") = **zero matches**. Calibration is excellent.

---

## 6. Remediation applied by this review (the gating gap)

To close the §4 coverage gap, this review adds a fail-closed, stdlib-only log-auditor `verifiers/verify_triangle_y_dini_logs.py` (mirroring `verify_tail_arb_logs.py`) that audits the sealed `logs/triangle_y_dini_{180,256}.log`, and wires it into the W2 (hypothesis-ii) gate of `verify_assembly_1787854.py`. After this change the sealed assembly **does** require the Dini worst-ratio check to pass. This is a *gating/coverage* fix at the **parse-the-sealed-log** level (the same trust level as the already-gated tail); it does **not** replace the still-needed independent recompile (§7). The SHA-256 manifest is regenerated to cover the new file (the pre-existing 362 entries are unchanged; the seal is re-issued as part of this review, not the original v3 seal).

---

## 7. What must still happen before acceptance (the residual, prioritized)

1. **Independent recompile of the heavy interval bounds** — rebuild the 883-prism barrier and the Arb tail in a fresh toolchain and confirm `min_mesh`, `D_z`, `D_t`, and the producer floors `L_N` are *true* bounds (the sealed fast path trusts the printed balls). This is the manuscript's own Priority 7.
2. **Human sign-off on the two prose-only analytic imports of §3** — `B_t ≠ 0` on `R`, and the `t>0 → t=0` limit of Lemma 8.4 / Thm 1.3.
3. **Human sign-off on the Dini y-transfer derivation** (§4) — the `abs(L·C + C′) + (g − L/2)·abs(C)` upper-Dini bound and the exhaustiveness of the `(L, y)` rectangle cover over all active-set sectors; it is the thinnest margin and the least self-checking step.
4. **Cite Platt–Trudgian's precise height** `3 000 175 332 800` (not the round `3×10¹²`) wherever hypothesis (i) is stated (§2).

---

## 8. Disposition

**Unreviewed computer-assisted proof candidate — confirmed as such, and materially strengthened by this pass.** No fatal or bound-invalidating defect was found; the criterion transcription and verified-height licensing are verified against primary sources; the barrier and tail computations are robust with real (non-knife-edge) margins; the one coverage gap has been closed at the log-audit level. It is **not** an established theorem: acceptance requires the §7 items — chiefly an independent recompile and human sign-off on three standard-but-un-machine-verified analytic steps. If those close, the result would be a genuine **unconditional** improvement on the Platt–Trudgian bound (0.2 → 0.1787854), obtained by the legitimate verified-height lever, not by any RH-hard or conjectural input.

*This review was performed by AI agents under human direction. It is an adversarial technical audit, not human expert peer review, and its confidence figures are calibrated estimates, not guarantees.*
