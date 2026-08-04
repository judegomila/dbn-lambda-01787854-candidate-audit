# Standalone P1113 tail lemma for the `0.1782354` row

Status: computer-assisted lemma candidate. The analytic template is the
endpoint-cap/exact-convolution argument documented in `TAIL_LEMMA.md`; this
file records its separate lower-time instantiation and its independent Arb
certificate.

## Exact statement

Let

\[
t_0=\frac{1607}{10000},\qquad
y_0^2=\frac{87677}{2500000},\qquad
y_{\max}^2=1-2t_0=\frac{3393}{5000},
\]

and let \(N\geq N_*=4{,}050{,}000\). Use the fixed real P1113 stencil

\[
d\in\{1,2,3,4,5,6,7,10,11,13,14\}
\]

with the exact rational coefficients embedded in
`verifiers/verify_tail_01782354_arb.c`. Then the normalized tail contraction
and effective-approximation error satisfy, uniformly for the complete
height interval \(y_0\leq y\leq y_{\max}\),

\[
D<1,
\qquad
\frac{1-D}{M_{\max}}-E>0.
\]

Consequently the P1113 tail lane supplies the final-time nonvanishing
hypothesis on every window with \(N\geq4{,}050{,}000\). Its closed-left
start overlaps the finite lane's final window at \(N=4{,}050{,}000\).

## Exact domains

The Arb verifier encloses the slightly stronger time box

\[
\frac{160700000}{10^9}
\leq t\leq
\frac{160700001}{10^9},
\]

whose left endpoint is exactly \(t_0\). It checks

\[
\left(\frac{1872719}{10^7}\right)^2
<y_0^2<
\left(\frac{23409}{125000}\right)^2
\]

and the minimal upper bracket

\[
\left(\frac{8237718}{10^7}\right)^2
<\frac{3393}{5000}
\leq
\left(\frac{8237719}{10^7}\right)^2.
\]

The convolution head remains \(M=153814\); only the finite/tail cutoff and
the exact time/height domains differ from the `0.1787854` instantiation.

## Directed certificate values

At 512-bit precision the verifier returns

\[
D_{\rm ub}
=0.996263624349153199188926591862\ldots,
\]

\[
E_{\rm ub}
=1.09373050959164082758046405643\times10^{-8},
\]

and

\[
\left(\frac{1-D}{M_{\max}}-E\right)_{\rm lb}
=0.00232329680607003070087534456632\ldots>0.
\]

All comparisons use directed endpoints and fail closed. The source performs
37 domain, monotonicity, convolution, cap, error and strict-margin gates.

## Replay

Run

```text
RUN_SANITIZERS=1 ./scripts/run_tail_01782354_arb.sh FRESH_OUTPUT_DIRECTORY
```

The runner requires a fresh evidence directory, compiles with strict C17
warnings, runs 256- and 512-bit certificates, rejects precision below 256
bits, and optionally runs ASan/UBSan. Archived successful logs are under
`certificates/lower_time_01782354/`.

This lemma is independent of the speculative moving-real-rung barrier in
`MOVING_REAL_RUNG_BARRIER.md`; it belongs to the ordinary Polymath
final-time/tail lane.
