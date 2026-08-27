# Summary of changes for run 8316f55a-1cc3-456c-8c52-b400767e8723
I formalized `job8_ec0_certificate.tex` in Lean 4 / Mathlib, in the new file `RequestProject/EC0Certificate.lean`. The project builds cleanly with no `sorry`, and both theorems depend only on the standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

**What is stated.** The exact parameters of the document are defined over the reals: `N0 = 690988`, `t0 = 129/800`, `t1 = 161250001/10^9`, `y0 = √(87677/2500000)`, `ymax = √(271/400)`, `xf t = 4π(N0² − t/16)`, `Lf t = log(N0² − t/16)` (with `EC0.Lf_eq` checking that this equals `log (xf t / (4π))`), and

`EC0.eC0 t y = exp(−((1+y)/4)·L − (t/16)·L² + (31/25)(3^y + 3^(−y))/(N0 − 1/8) + (3√(L² + π²/4) + 21/2)/(xf t − 12))`.

**Results proved (both over the full closed boxes, with the exact rational constants of the document):**
- `EC0.eC0_le_sharp` — the primary target: `eC0 t y ≤ 233492848188649183/10^24` for all `t ∈ [t0,t1]`, `y ∈ [y0,ymax]`.
- `EC0.eC0_le_weak` — the fallback corollary: `eC0 t y ≤ 234/10^9`.
- `EC0.box_nonempty` — `t0 < t1` and `y0 < ymax`, so neither bound is vacuous.

**How it is proved.** Every numeric step is a rigorous rational enclosure; no floating point is used. A general lemma `log_lower_of_pow` turns an exact integer power certificate `ρ·2^b ≤ z^a` into a rational lower bound for `log z` (using `log ρ ≥ 1 − 1/ρ`). It is applied with `a = 59, b = 2289` to certify `log(4774644161439899/10⁴) ≥ 26.89175546` and with `a = 166, b = −3657` to certify `log(233492848188649183/10²⁴) ≥ −15.2701143946`; the underlying big-integer inequalities are checked by exact arithmetic. Mathlib's certified bounds for `log 2`, `exp 1` and `π` supply the remaining constants, `sqrt` bounds are obtained by squaring, and the `y`-dependence is handled by a monotonicity argument (a Lipschitz bound for `y ↦ 3^y` on `[0,1]`) that reduces the two `y`-dependent terms jointly to the endpoint `y = y0`.

**One correction to the informal guidance**, recorded in the file's module docstring: the suggested enclosure `26.98 < L < 26.99` is wrong — the true value is `L = 26.8917554…` on the box, and the certified bound used reflects that. Also, the sharp constant is tight: the maximum of `e_{C,0}` over the box is about `2.3349249936·10⁻⁷`, only a relative `1.5·10⁻⁶` below the target, which is why the two `y`-dependent terms cannot be bounded separately at opposite endpoints.

The original `.tex` file is untouched. All work is committed and pushed.