# Finite window-freeze theorem at the \(0.1787854\) row

## Statement

Fix

\[
t_0=\frac{129}{800},\qquad
y_0^2=\frac{87677}{2500000},\qquad
y_{\max}^2=1-2t_0=\frac{271}{400},
\]

and put

\[
q_N=N^2-\frac{t_0}{16},\qquad
x_N=4\pi q_N,\qquad
W_N=[x_N,x_{N+1}).
\]

For \(y_0\le y\le y_{\max}\), define the paper-side pointwise
majorants/minorant

\[
\begin{aligned}
G(x,y)&=e^{y/50}\left(\frac{x}{4\pi}\right)^{-y/2},\\
K(x,y)&=\frac{t_0y}{2(x-6)},\\
\Sigma(x,y)&=\frac{1+y}{2}
+\frac{t_0}{4}\log\frac{x}{4\pi}
-\frac{t_0}{2x^2}
 \left(1-3y+\frac{4y(1+y)}{x^2}\right)_+ .
\end{aligned}
\]

The producer evaluates the same formulas at \(x=x_N\); write those
values as \(G_N(y),K_N(y),\Sigma_N(y)\).  For every integer
\(690988\le N\le3840000\), every \(x\in W_N\), and every
\(y\in[y_0,y_{\max}]\),

\[
\boxed{
G(x,y)\le G_N(y),\qquad
K(x,y)\le K_N(y),\qquad
\Sigma(x,y)\ge\Sigma_N(y).
}
\]

Thus replacing the true \(x\) by the window's closed left endpoint has
exactly the conservative directions consumed by the finite producer.

## Monotonic signs

The first two signs are immediate on the target domain:

\[
\partial_xG=-\frac{y}{2x}G<0,\qquad
\partial_xK=-\frac{t_0y}{2(x-6)^2}<0.
\]

For the third, let

\[
h(x,y)=1-3y+\frac{A(y)}{x^2},\qquad
A(y)=4y(1+y)\ge0.
\]

Then \(h_x=-2A/x^3\le0\), so \(h_+\) is nonincreasing.  Both
\(x^{-2}\) and \(h_+\) are nonnegative and nonincreasing; hence their
product is nonincreasing.  The logarithmic term in \(\Sigma\) is
strictly increasing.  Therefore \(\Sigma\) is strictly increasing in
\(x\), including across the kink \(h=0\).

Equivalently, away from the kink,

\[
\partial_x\Sigma=
\begin{cases}
\dfrac{t_0}{4x},&h<0,\\[6pt]
\dfrac{t_0}{4x}
+\dfrac{t_0h}{x^3}
+\dfrac{t_0A}{x^5},&h>0,
\end{cases}
\]

and both one-sided derivatives at \(h=0\) are positive.

## Site and endpoint coverage

Let

\[
x_*:=X+\sqrt{1-y_0^2},\qquad X=6000000185827.
\]

Exact rational Machin-series bounds for \(\pi\), exact
integer-square-root brackets, and an independent 400-bit interval
evaluation give the strict inequalities

\[
x_{690988}<x_*<x_{690989}.
\]

The certified lower margins are

\[
x_*-x_{690988}>5377393.9878,\qquad
x_{690989}-x_*>11989041.1746.
\]

Consequently the closed criterion start \(x_*\) lies strictly inside
the first finite window.  Since

\[
q_{N+1}-q_N=2N+1>0
\]

and the right endpoint of \(W_N\) is exactly the left endpoint of
\(W_{N+1}\),

\[
[x_*,x_{690989})\;\cup\!
\bigcup_{N=690989}^{3840000}[x_N,x_{N+1})
=[x_*,x_{3840001}).
\]

There are no gaps or double assignments.  At \(x=x_{N+1}\), the point
belongs to \(W_{N+1}\), not \(W_N\); all three frozen constants reset
in the safer direction there.  The final point \(x_{3840001}\) is not
claimed by the finite lane.  Both independent tail scripts declare the
closed domain \(N\ge3840000\), so the finite and tail domains overlap
on the complete window \(W_{3840000}\); validity of the tail estimate
itself remains a separate theorem.

## Relation to the stored \(t\)-boxes

The first producer leg uses the singleton \(t\)-box
\([16125/100000,16125/100000]\).  Every later leg uses
\([161250000/10^9,161250001/10^9]\).  Both contain \(t_0\), the latter
at its closed left endpoint.  Arb inclusion therefore encloses the
exact frozen \(G_N,K_N,\Sigma_N\) used above.  The theorem here is only
the missing uniform-in-\(x\) step.

## Scope

This is an elementary, unconditional window-freeze lemma.  It does not
by itself prove the paper's effective approximation, the stored finite
floors, the all-\(y\) transfer, the analytic tail, or the final
de Bruijn--Newman criterion.  It closes only the direction and endpoint
logic needed to pass from the paper's pointwise-in-\(x\) bounds to the
producer's per-window constants.

Run:

```bash
python3 verifiers/verify_window_freeze.py
python3 verifiers/verify_window_freeze.py --repo .
```
