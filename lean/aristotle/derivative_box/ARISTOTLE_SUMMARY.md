# Summary of changes for run 317233c4-93e6-46dc-b084-dbce980828f4
I formalized `job6_derivative_box.tex` in Lean 4 (Mathlib), in the new file `RequestProject/DerivativeBox.lean`. The file builds cleanly and contains no `sorry`; the target theorems depend only on the standard axioms `propext`, `Classical.choice`, `Quot.sound`.

Definitions introduced (matching the source): `qbox x = x/(4π)`, `hbox x y = 1 − 3y + 4y(1+y)/x²`, `cbox x y = ¼ log q(x) − (hbox x y)₊/(2x²)`, the slope majorant `eta`, the tail exponent slope `pslope`, the tail power `Pfun`, and the time-derivative bracket `Bfun`.

Proved theorems, by lemma of the source document:

(a) Lemma 1 — sign facts `hbox_hasDerivAt_y` / `hbox_deriv_y_neg` (h_y = −3 + 4(1+2y)/x² < 0) and `hbox_hasDerivAt_x` / `hbox_deriv_x_nonpos` (h_x = −8y(1+y)/x³ ≤ 0); monotonicity `hbox_anti`, `hbox_pos_div_anti`, `cbox_mono` (c increases in both variables), `cbox_strictMono_x`; the uniform envelope `cbox_envelope`, which takes the pointwise Polymath Lemma 8.4 bound as an explicit hypothesis and yields the bound at the corner (X, y_min); and the quantitative statements `hbox_le_one`, `hbox_div_hasDerivAt_x`, `hbox_div_deriv_abs_le` (|∂ₓ(h/2x²)| ≤ 2/x³ where h > 0) together with `cbox_deriv_x_pos`, which, under X² > 8 and 1/(4(X+1)) − 2/X³ > 0, gives differentiability of c in x off the positive-part kink, the bound |c_x − 1/(4x)| ≤ 2/x³, and c_x ≥ 1/(4(X+1)) − 2/X³ > 0.

(b) Lemma 2 — `eta_le_corner`: η(x,t,n) ≤ 0.02 − ½ log q(X) + t₀ log N/(2(X−6)) + ½ log N for 1 ≤ n ≤ N, x ≥ X > 6, 0 ≤ t ≤ t₀.

(c) Lemma 3 — the generic head-plus-integral bound `sum_le_head_add_integral` for a nonincreasing F on [K,N]; the gate implications `pslope_le`, `logderiv_le`, `logderiv_neg` (all displayed logarithmic r-derivatives are ≤ (y_min−1)/2 + 1/log K, hence negative under the second gate), `Bfun_pos`, `Bfun_hasDerivAt`, `Bfun_logDeriv_le` (B'/B ≤ 1/r); the resulting monotonicity of the summands `Pfun_mul_log_antitoneOn`, `Pfun_mul_rpow_antitoneOn`, `Pfun_mul_B_antitoneOn`; and the packaged end-to-end bound `spatial_sum_le_head_add_integral` for a nonnegative linear combination of the three spatial summands.

(d) Lemma 4 — `mem_slitPlane_of_mem_ball`, `clog_differentiableOn_ball`, `cpow_differentiableOn_ball`, `clog_analyticOnNhd_ball`: holomorphy of u ↦ log(Nu) and u ↦ (Nu)^α on complex balls B(u₀, ρ) with u₀ > 0 real and ρ ≤ u₀, which avoid the branch cut; plus `integral_change_of_variables` showing that integrating from K/N to 1 and multiplying by N equals ∫_K^N F.

(e) Lemma 5 — `chord_disk_left` and `chord_disk_right` (two-disk containment of the true curve and its chord from the Lipschitz bound D_z), `homotopy_mem_disk` (convexity gives the straight-line homotopy), `enlarged_disk` (radius enlarged by D_t(t_{i+1} − t_i) + 1/800, with 1/800 exact), `zero_not_mem_closedBall`, and the packaged `prism_zero_free`, giving zero-avoidance under the strict prism predicate.

Two small faithfulness notes recorded in the file: `hbox_hasDerivAt_y` needs no x ≠ 0 hypothesis, and in the Lemma 4 statements the hypothesis 0 < u₀ is kept as in the source although only ρ ≤ u₀ is used. The original `.tex` file is untouched, and all work is committed and pushed.