# Conservative effective-error constant weld

## Purpose

The target proof does **not** use the \(10.44\) constant in displayed
equation (24) of Polymath Theorem 1.3.  Instead it takes the preceding
Proposition 6.6(vi) as the input and derives the slightly larger constant
\(10.50\) directly.  This closes the paper-internal reduction issue recorded
in `provenance/ERROR_TERMS_AUDIT.upstream.md`.

The historical upstream files under `vendor/` and all files whose names end
in `.upstream.md` are retained verbatim for provenance.  Their
transcriptions of \(10.44\) are not target-proof premises.

## Exact derivation

Proposition 6.6(vi) bounds the \(e_{C,0}\) factor by an expression containing

\[
\exp\!\left(
 \frac{3|\log(x/(4\pi))+i\pi/2|+3.58}{x-8.52}
\right)
\left(
 1+
 \frac{1.24(3^y+3^{-y})}{N-0.125}
+\frac{6.92}{x-12}
\right).
\]

The theorem domain has \(x\ge200\), so

\[
x-8.52>x-12>0.
\]

All numerators are nonnegative.  Applying \(1+u\le e^u\), then enlarging
the first denominator from \(x-8.52\) to \(x-12\), gives

\[
\begin{aligned}
e_{C,0}\le
\left(\frac{x}{4\pi}\right)^{-(1+y)/4}
\exp\bigg(
&-\frac{t}{16}\log^2\!\frac{x}{4\pi}
+\frac{1.24(3^y+3^{-y})}{N-0.125}\\
&+\frac{3|\log(x/(4\pi))+i\pi/2|+3.58+6.92}{x-12}
\bigg).
\end{aligned}
\]

The constant arithmetic is exact:

\[
3.58+6.92=\frac{179}{50}+\frac{173}{25}
=\frac{21}{2}=10.50.
\]

Thus every target lane uses the conservative bound

\[
\boxed{
e_{C,0}\le
\left(\frac{x}{4\pi}\right)^{-(1+y)/4}
\exp\!\left(
-\frac{t}{16}\log^2\!\frac{x}{4\pi}
+\frac{1.24(3^y+3^{-y})}{N-0.125}
+\frac{3|\log(x/(4\pi))+i\pi/2|+10.50}{x-12}
\right).
}
\]

This derivation is valid uniformly on the full \(x\ge200\) theorem domain;
it does not rely on the displayed \(10.44\) formula or on numerical
smallness at the campaign height.

## Fail-closed implementation map

`verifiers/verify_error_constant_weld.py` checks the exact rational
arithmetic, the denominator direction, and the source-level presence of
\(10.50\) in every consuming target verifier.  The assembly executes that
checker before either the final-time or barrier hypothesis may pass.

The consuming numerical lanes are:

- `verifiers/verify_finite_and_binding.py`;
- `verifiers/verify_tail_1787854_160.py`;
- `verifiers/verify_tail_1787854_256.py`;
- `verifiers/verify_tail_arb.c`;
- `verifiers/verify_barrier_binding.py`; and
- `barrier/src/verify_uniform_error_01787854.c`.

Each lane independently recomputes its interval enclosure with \(10.50\).
The resulting margins remain strict; no stored finite Triangle tuple or
barrier coefficient depends on this change.
