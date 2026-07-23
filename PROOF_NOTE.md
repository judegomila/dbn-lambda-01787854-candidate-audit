# Conditional proof note for the 0.1787854 candidate

## Status

This package proposes the computer-assisted candidate

\[
\boxed{\Lambda\le\frac{893927}{5000000}=0.1787854}.
\]

It does not prove the Riemann hypothesis.  The numerical and new
direct-Triangle legs are locally replayable and were freshly replayed while
this referee package was prepared.  The final conclusion is still conditional
on external mathematical review of the native Triangle-to-\(|f_t|\) binding
and the inherited winding, site, effective-approximation, and criterion
bindings.  `OPEN_REVIEW_QUESTIONS.md` is part of this proof note's scope.

## 1. Exact row and criterion quantity

\[
X=6000000185827,\qquad
t_0=\frac{129}{800},\qquad
y_0^2=\frac{87677}{2500000}.
\]

Then

\[
t_0+\frac{y_0^2}{2}
=\frac{893927}{5000000}=0.1787854
\]

and

\[
0<y_0^2<1-2t_0=\frac{271}{400}<1.
\]

The assembly consumes the criterion encoded from Theorem 1.2 of
arXiv:1904.12438: verified height, full right-half-line nonvanishing,
and the winding/barrier interface imply
\(\Lambda\le t_0+y_0^2/2\).

## 2. Verified-height and site interfaces

The Platt--Trudgian height used by the deposited campaign is

\[
T_{\rm PT}=3000175332800.
\]

Exactly,

\[
\frac X2\le T_{\rm PT},\qquad
T_{\rm PT}-\frac X2=\frac{350479773}{2}.
\]

The deposited winding/site slab has lower height \(33/200\) and
\(t\)-ceiling \(1809/10000\).  The exact containments are

\[
\left(\frac{33}{200}\right)^2\le y_0^2,\qquad
t_0<\frac{1809}{10000},\qquad
y_0^2+2t_0=2\cdot\frac{893927}{5000000}<1.
\]

The assembly verifier also reproduces the deposited site-window endpoint
strings.  The underlying winding and site packages are vendored under
`vendor/dbn21a/` for local review; their successful replay is not assumed to
settle the rigor of the closed real-parameter slab.

## 3. Fixed-height finite evidence

The stored Arb/Taylor evidence covers every integer

\[
690988\le N\le3840000
\]

on a closed \(t\)-box containing \(t_0\), at the exact height
\(y_0\).  Its four consecutive auxiliary Euler legs are:

\[
\begin{array}{c|c|c}
N\text{-range}&{\cal P}&\min T_N\\ \hline
690988\ldots728999&\{2,3,5,7,11\}&0.000000791366\\
729000\ldots818999&\{2,3,5,7\}&0.000315112459\\
819000\ldots1027999&\{2,3,5\}&0.000305788807\\
1028000\ldots3840000&\{2,3\}&0.000309285478 .
\end{array}
\]

There are exactly \(3,149,013\) rows, with no gaps, overlaps,
duplicates, nonpositive values, or uncertainty rows.

The temporary sawtooth mass used during a shard dominates the exact
current-\(N\) Triangle mass because \(\gamma_N\) decreases in \(N\).
Thus a positive stored floor is a valid lower floor for the exact native
Triangle functional.

## 4. Direct all-height theorem

For each fixed \(N\) and prime set, let

\[
{\cal F}_N(y)=\gamma_N(y)+
\sum_{n\ge2}\bigl(|B_{N,n}|+
\gamma_N(y)|A_{N,n}(y)|\bigr)n^{-\sigma_N(y)}
\]

be the exact finite Triangle mass and put \(Q_N=1-{\cal F}_N\).
The direct theorem in
`provenance/TRIANGLE_Y_DINI_THEOREM.independent.md` uses the exact
composite-divisor factor

\[
\exp\!\left[\frac{t}{4}
\left(\sum_{p\mid d}\log^2p+\log^2d-2\log n\log d\right)\right]
\]

and certifies a nonpositive upper right Dini derivative for every
summand.  Its exhaustive pattern counts are

\[
3^5,3^4,3^3,3^2=243,81,27,9.
\]

The 180- and 256-bit Arb runs agree on coverage counts and have worst
strict ratio

\[
0.99999860767275095<1.
\]

Local Lipschitz continuity turns the pointwise upper-Dini inequalities
into global monotonicity:

\[
{\cal F}_N(y)\le{\cal F}_N(y_0),\qquad
Q_N(y)\ge Q_N(y_0).
\]

One corrected Python implementation reproduces the sign result on separate
head and tail decompositions; the Arb verifier is the primary interval
implementation.

## 5. Native normalization and correction

The producer's native lower bound is

\[
L_N(y)=\frac{Q_N(y)}{M_N(y)}-\operatorname{corr}_N(y),
\]

where

\[
M_N(y)=\sum_{d\mid D}|\lambda_d|d^{-\sigma_N(y)}.
\]

The production exponent satisfies the global increment inequality

\[
\sigma_N(y_2)-\sigma_N(y_1)\ge\frac12(y_2-y_1).
\]

Consequently \(M_N\) is nonincreasing.  The separate correction verifier
bounds every positive correction summand's logarithmic rate by

\[
\Xi(N,y)\le
\frac1{50}-\frac12\log(N^2-t/16)
+\frac1y+\left(\frac12+
\frac{t}{2(4\pi(N^2-t/16)-6)}\right)\log N.
\]

This is maximized at \((N,y)=(690988,y_0)\), where

\[
\Xi\le-1.3631121547576400<0.
\]

Thus the correction is nonincreasing.  Since the stored floor is
positive, \(Q_N(y_0)>0\), and therefore

\[
L_N(y)\ge L_N(y_0)\ge T_N
\]

throughout the full height interval.

This is the key repair.  It does not use the false multi-prime
standard-shape assertion, sharp-to-crude \(Y2/Y3\), or an
exponent-inflation seam.

The further identification of this native normalized functional with the
paper's lower bound for \(|f_t|\), in the units used by the error budget, is a
load-bearing theorem-level review item.  The numerical monotonicity checks do
not prove that identification by themselves.

## 6. Effective-approximation error

The paper's displayed bounds (20)--(24) control
\(H_t/B_t-f_t\) before Euler multiplication and are therefore independent
of the auxiliary prime set.  The complete inherited \(U1\)--\(U5\)
monotonicity path is re-evaluated at this row and gives

\[
\begin{aligned}
e_A+e_B&\le0.000000000002057023688667,\\
e_{C,0}&\le0.000000233492848188646848,\\
E_{\max}&\le0.000000233494905212335514.
\end{aligned}
\]

The finite interface is in normalized selection units:

\[
T_{\min}-E_{\max}
\ge0.000000557871094787>0.
\]

The earlier exploratory number \(M T-E\) is not used.

The inherited audit records an `x-6.66` implementation denominator where the
paper displays `x-12`.  The audit argues that this is absorbed by later slack,
but the direction and absorption remain an explicit referee question.

## 7. Infinite tail

The exact-convolution tail starts at the closed integer

\[
N_{\rm mid}=3840000
\]

with \(M_{\rm head}=153814\).  Both 160- and 256-bit replays pass 93/93
checks and certify

\[
\begin{aligned}
D_{\rm ub}&\le0.999720909379940<1,\\
\operatorname{flow}_{\rm lo}&\ge0.000173532614415,\\
\operatorname{error}_{\rm ub}&\le0.00000001167160258919,\\
\operatorname{slack}_{\rm lo}&\ge0.000173520942813>0.
\end{aligned}
\]

Its \(t\)-box contains \(t_0\); its small \(y\)-box straddles \(y_0\);
and its minimally selected extended top covers
\(\sqrt{1-2t_0}\).  Both the finite and tail legs include
\(N=3840000\).

## 8. Conditional conclusion and review boundary

The local package discharges the finite numerical, new all-height,
normalizer/correction, effective-error, tail, exact-height, and exact
interface arithmetic at the implementation level.  Accepting the direct
native-functional identification and the cited inherited winding, site,
effective-approximation theorem, and de Bruijn--Newman criterion bindings,
the assembled implication is

\[
\boxed{\Lambda\le\frac{893927}{5000000}=0.1787854}.
\]

Even if independently accepted, this remains positive and therefore
does not prove RH.  Together with the established lower bound
\(\Lambda\ge0\), RH would require an accepted upper bound
\(\Lambda\le0\).

The known unresolved questions are not merely editorial.  In particular,
failure of the winding slab or native-functional binding would block the
headline implication even if every stored numerical check remains green.
