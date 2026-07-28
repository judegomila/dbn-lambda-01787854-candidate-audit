# Spatial-box repair for the barrier derivative majorants

## Defect being repaired

Polymath Lemma 8.4 is pointwise in \(x,y,t\). The original barrier
program called `generate_ddzbound` and `generate_ddtbound` with the points
\((x,y)=(X,y_{\min})\) and then used the returned values as bounds on

\[
[X,X+1]\times[y_{\min},1].
\]

That substitution is not termwise conservative. For example, when
\(t=0\), the \(B\)-part of the time-derivative majorant contains a
positive factor involving \(\log(x/(4\pi n))\), which increases with
\(x\); there is then no heat-exponent decay that could make evaluation at
\(X\) an automatic upper bound. Rounding the resulting value to an
integer does not prove that the omitted increase fits below the next
integer.

## Endpoint-separated upper bound

Put

\[
q(x)=\frac{x}{4\pi},\qquad
h(x,y)=1-3y+\frac{4y(1+y)}{x^2},
\]

\[
c(x,y)=\frac14\log q(x)-\frac{h(x,y)_+}{2x^2}.
\]

On the target box,

\[
h_y=-3+\frac{4(1+2y)}{x^2}<0,\qquad
h_x=-\frac{8y(1+y)}{x^3}\le0.
\]

Thus \(h_+\) decreases in both variables. Since \(x^{-2}\) also
decreases, \(c\) increases in both variables. Consequently

\[
\Re s_*\ge \frac{1+y}{2}+t\,c(X,y_{\min})
\]

uniformly on the complete spatial box. This is the `const1` used by the
program.

The source also checks a numerical lower bound for the \(x\)-monotonicity
rather than relying only on the preceding sign argument. When \(h>0\),

\[
\frac{\partial}{\partial x}\frac{h}{2x^2}
=-\frac{4y(1+y)}{x^5}-\frac{h}{x^3}.
\]

On \(0\le y\le1\), the separately checked condition \(X^2>8\) gives
\(h_+\le1\), so this derivative has absolute value at most
\(1/x^3+8/x^5\le2/x^3\). The same correction is zero where \(h<0\),
and continuity handles the positive-part kink. The program fails closed
unless Arb proves

\[
\frac1{4(X+1)}-\frac2{X^3}>0.
\]

It follows directly that \(c_x>0\) throughout the complete spatial box.

The common \(A\)-side core in Lemma 8.4 is bounded by

\[
\mathcal A(x,y,t;n)=
e^{0.02y}q(x)^{-y/2}
N^{ty/(2(x-6))}
n^y n^{-\Re s_*}.
\]

Its logarithmic upper-right \(y\)-derivative is at most

\[
\eta(x,t,n)=
0.02-\frac12\log q(x)
+\frac{t\log N}{2(x-6)}
+\frac12\log n.
\]

For \(n\le N\), \(x\ge X\), and \(0\le t\le t_0\),

\[
\eta(x,t,n)\le
0.02-\frac12\log q(X)
+\frac{t_0\log N}{2(X-6)}
+\frac12\log N<0.
\tag{1}
\]

The repaired C source verifies the final strict inequality with Arb.
It follows that every \(A\)-core is maximized at \(y=y_{\min}\).
The core also decreases with \(x\): the displayed gamma/kappa factor
decreases with \(x\), while \(c(x,y)\) increases.

All remaining factors in the Lemma 8.4 right sides are nonnegative and
are bounded independently in their conservative directions:

- \(1/(x-6)\), \(3/x\), and \(8/(x-6)\) are evaluated at \(X\);
- \(\log(x/(4\pi))\) is evaluated at \(X+1\);
- \(\log(|1+y+ix|/(4\pi))\) is evaluated at \((X+1,1)\);
- the \(B\)-side power is evaluated with \(y=y_{\min}\) and the uniform
  lower bound \(c(X,y_{\min})\);
- the \(A\)-side power is covered by (1), again at \(y=y_{\min}\).

The program also verifies

\[
2\log N<\log\frac{X}{4\pi},
\]

which makes every bracket accumulated as a nonnegative majorant,
including the `const2-log(n)/4` factor in the time derivative.

Therefore the values returned by the patched derivative routines
enclose

\[
\sup_{\substack{x\in[X,X+1]\\y\in[y_{\min},1]}}
\left|\partial_z f_t(x+iy)\right|
\]

at a fixed seam and

\[
\sup_{\substack{x\in[X,X+1]\\y\in[y_{\min},1]\\
                  t\in[t_i,t_{i+1}]}}
\left|\partial_t f_t(x+iy)\right|
\]

on a closed time prism.

The statement of Polymath Lemma 8.4 is written for \(t>0\).  This creates
no open-endpoint assumption here.  For the fixed integer \(N\), the defining
finite sums and their displayed \(z\)- and \(t\)-derivatives are \(C^1\) on
the whole compact box \(0\le t\le t_0\): the same interval checks used below
keep every denominator nonzero and every logarithm away from its branch cut.
Apply Lemma 8.4 first on \(\varepsilon\le t\le t_0\).  The majorants above
are independent of \(\varepsilon\), so continuity of the finite-sum formulas
lets \(\varepsilon\downarrow0\) and gives the same derivative bounds at
\(t=0\).  Equivalently, the uniform \(t>0\) bound may be integrated down to
the zero-time seam and the limit taken there.

## Certified discrete-sum majorant

Lemma 8.4 gives discrete sums over \(1\le n\le N\). Numerical
quadrature by itself does not turn such a sum into an upper bound. In
particular, the time-derivative summand is not decreasing near \(n=1\),
so the previously used expression

\[
F(1)+\int_1^N F(u)\,du
\]

had no stated justification.

The repaired program sets \(K=16\), evaluates every term
\(F(1),\ldots,F(K)\) directly with Arb, and uses quadrature only for the
tail. To justify the tail, put \(r=\log u\) and

\[
P(u)=u^{-(1+y_{\min})/2+t(\log u/4-c_0)},
\qquad c_0=c(X,y_{\min}).
\]

The logarithmic derivative of \(P\) is

\[
p(r)=-\frac{1+y_{\min}}2+t\left(\frac r2-c_0\right).
\]

The source fails closed unless

\[
c_0>\frac12\log N
\tag{2}
\]

and

\[
\frac{y_{\min}-1}{2}+\frac1{\log K}<0.
\tag{3}
\]

Since \(0\le t\) and \(r\le\log N\), (2) gives
\(p(r)\le-(1+y_{\min})/2\).

The spatial-derivative summand is a nonnegative linear combination of

\[
P(u)r,\qquad P(u)u^{y_{\min}}r,\qquad
P(u)u^{y_{\min}}.
\]

Their logarithmic derivatives with respect to \(r\) are respectively

\[
p+\frac1r,\qquad p+y_{\min}+\frac1r,\qquad
p+y_{\min}.
\]

For the time derivative put

\[
B(r)=r(C-r/4).
\]

The program separately fails closed unless \(C-\log(N)/4>0\).
Consequently \(B\ge0\) on the complete tail, and

\[
\frac{B'(r)}{B(r)}
=\frac1r-\frac1{4(C-r/4)}
\le\frac1r.
\]

The time-derivative summand is a nonnegative linear combination of
\(PB\), \(Pu^{y_{\min}}B\), and \(Pu^{y_{\min}}\). Every logarithmic
derivative in both sums is therefore at most

\[
-\frac{1+y_{\min}}2+y_{\min}+\frac1{\log K},
\]

which is strictly negative by (3). Thus both continuous summands
decrease for \(u\ge K\), and

\[
\sum_{n=1}^N F(n)
\le
\sum_{n=1}^K F(n)+\int_K^N F(u)\,du.
\tag{4}
\]

The C code evaluates the finite head in the same Arb callback used by
the quadrature. Its change of variables integrates from \(K/N\) to
\(1\) and multiplies by \(N\), which is exactly the integral in (4).

## Holomorphic quadrature contract

FLINT's `acb_calc_integrate` may call its callback with `order=1` to
obtain a holomorphic enclosure on a complex ball around the real
integration path. Projecting that ball to its real part does not define
the required holomorphic function and therefore cannot justify the
Gauss--Legendre error bound.

Both repaired callbacks now retain the complete complex integration
variable. Every occurrence of \(\log(Nu)\) uses
`acb_log_analytic`, and every nonintegral power of \(Nu\) uses
`acb_pow_analytic`, with the analytic flag set exactly when
`order != 0`. They refuse unsupported orders above one. If a complex
ball touches the logarithm branch cut, the analytic operations produce
a nonfinite enclosure and the checked quadrature call fails closed.

The 16 finite-head evaluations explicitly call the same callback with
`order=0` at positive real points. Runtime counters additionally
require that each numerical integral actually invoked the callback at
least once with `order=1`; checked integrator success is the decisive
finite-enclosure condition.

## Use in the boundary homotopy

Let a mesh subedge have length at most \(h\), with true image \(F(s)\)
and endpoint chord \(P(s)\). On \(0\le s\le1/2\), both \(F(s)\) and
\(P(s)\) lie in the closed disk of radius \(D_zh/2\) about \(F(0)\);
on \(1/2\le s\le1\), the symmetric statement holds about \(F(1)\).
Each disk is convex, so it contains the straight-line homotopy between
the true curve and its chord.

Adding the certified time motion and \(H_t/B_t\)-approximation error
enlarges the radius to

\[
\frac{D_zh}{2}+D_t(t_{i+1}-t_i)+0.00125.
\]

The strict prism predicate makes this smaller than the modulus of every
possible disk center. Thus every disk excludes zero and the complete
spatial, time, and approximation homotopy is zero-avoiding.

## Source changes

`TloopSinglemat_closed_cert.c` now:

1. constructs exact Arb points `x_upper=X+1` and `y_upper=1`;
2. uses them only in the increasing
   \(\log|1+y+ix|\) factor of \(D_z\);
3. constructs `logxdiv4pi_upper=log((X+1)/(4*pi))`;
4. uses it in the increasing logarithmic factors of \(D_t\), while
   retaining `1/(X-6)` for decreasing reciprocal factors;
5. fails closed unless the strict \(A\)-core \(y\)-slope gate and the
   derivative-bracket positivity gate both pass, together with an
   explicit lower bound for \(c_x\);
6. evaluates the first 16 terms of each Lemma 8.4 sum directly;
7. integrates only from \(16\) to \(N\);
8. fails closed unless the tail-exponent, tail-monotonicity, and
   time-bracket gates above all pass;
9. uses genuinely complex analytic quadrature callbacks, with no
   projection to the real part; and
10. fails unless the integrator exercises its analytic callback path.

This avoids a wide direct interval \(y\)-box, which would destroy the
important correlation between the decay of \(|\gamma|\) and the factor
\(n^y\).
