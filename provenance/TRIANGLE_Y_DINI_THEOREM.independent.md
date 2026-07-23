# Direct-Triangle \(y\)-monotonicity theorem at the \(0.1787854\) row

This note records the theorem checked by
`verifiers/verify_triangle_y_dini_arb.c`.  It replaces the invalid
claim that the mollified \(A\)-side has the `Y_REDUCTION` standard-majorant
form.

## 1. Native finite functional

Fix \(t=129/800\), an integer cutoff \(N\), and one of the Euler prime
sets

\[
 {\cal P}\in\{\{2,3,5,7,11\},\{2,3,5,7\},\{2,3,5\},\{2,3\}\}.
\]

Put \(D=\prod_{p\in{\cal P}}p\),
\(b_t(m)=\exp((t/4)\log^2m)\), and

\[
 \lambda_d=(-1)^{\omega(d)}\prod_{p\mid d}b_t(p)
 \qquad(d\mid D).
\]

For \(2\le n\le DN\), let

\[
 {\cal D}_{N,n}=\{d\mid D:d\mid n,\ n\le dN\},
\]
\[
 B_{N,n}=\sum_{d\in{\cal D}_{N,n}}\lambda_d b_t(n/d),
 \quad
 A_{N,n}(y)=\sum_{d\in{\cal D}_{N,n}}
     \lambda_d b_t(n/d)(n/d)^y .
\]

The active set \({\cal D}_{N,n}\) is independent of \(y\).

Write

\[
 q_N=N^2-t/16,\quad x_N=4\pi q_N,\quad
 \gamma_N(y)=\exp(y/50)q_N^{-y/2},
\]
\[
 \sigma_N(y)=\frac{1+y}{2}+\frac t4\log q_N
 -\frac{t}{2x_N^2}
 \max\!\left(0,1-3y+\frac{4y(1+y)}{x_N^2}\right).
\]

The direct Triangle mass is

\[
 {\cal F}_{N,{\cal P}}(y)=\gamma_N(y)+
 \sum_{n=2}^{DN}\bigl(|B_{N,n}|+
 \gamma_N(y)|A_{N,n}(y)|\bigr)n^{-\sigma_N(y)}.
\]

## 2. Branch-free upper Dini derivative

Let

\[
 g_N=\frac{\gamma_N'}{\gamma_N}
 =\frac1{50}-\frac12\log q_N<0.
\]

The inner function in the positive part defining \(\sigma_N\) is
strictly decreasing on the target region.  Consequently, for
\(y_2\ge y_1\),

\[
 \sigma_N(y_2)-\sigma_N(y_1)\ge \frac12(y_2-y_1).
\]

In particular, the lower right slope of \(\sigma_N\) is at least \(1/2\),
including at its single positive-part kink.

Since \(A=A_{N,n}\) is differentiable,

\[
 D^+\{\gamma|A|\}=
 \begin{cases}
 \gamma(g|A|+\operatorname{sgn}(A)A'),&A\ne0,\\
 \gamma|A'|,&A=0,
 \end{cases}
\]
and therefore, at every point including a zero of \(A\),

\[
 D^+\{\gamma|A|\}\le \gamma(g|A|+|A'|).
\]

It follows that

\[
\begin{split}
D^+\!\left[
 (|B|+\gamma|A|)n^{-\sigma}\right]
\le n^{-\sigma}\bigl[
 \gamma|A'|+\gamma g|A|
 -\tfrac12\log n\,(|B|+\gamma|A|)
\bigr].
\end{split}
\tag{1}
\]

The negative term \(\gamma g|A|\) is exact and may be retained even
though \(g<0\).  This is why the verifier's
`abs(L*C+Cprime) + (g-L/2)*abs(C)` expression is valid.

## 3. Finite divisor-pattern reduction

Let \(L=\log n\), \(\ell_d=\log d\), and

\[
 r_d(L)=\exp\!\left\{\frac t4\left(
 \sum_{p\mid d}\log^2p+\ell_d^2-2L\ell_d\right)\right\}.
\]

The term \(\sum_{p\mid d}\log^2p\) is essential: the Euler coefficient is
\(\prod_{p\mid d}b_t(p)\), not \(b_t(d)\).

For the active set \(S={\cal D}_{N,n}\), define

\[
 C_0=\sum_{d\in S}(-1)^{\omega(d)}r_d,\quad
 C=\sum_{d\in S}(-1)^{\omega(d)}r_d d^{-y},\quad
 C'=-\sum_{d\in S}(-1)^{\omega(d)}r_d d^{-y}\ell_d.
\]

Then

\[
 B=b_t(n)C_0,\quad A=b_t(n)e^{yL}C,\quad
 A'=b_t(n)e^{yL}(LC+C').
\]

With \(G=\gamma e^{yL}\), the bracket on the right of (1), after
removing the positive factor \(b_t(n)\), is at most

\[
 G\,h-\frac L2|C_0|,\qquad
 h=|LC+C'|+(g-L/2)|C|.
\tag{2}
\]

Thus a sufficient branch-free gate is

\[
 G\max(h,0)<\frac L2|C_0|.
\tag{3}
\]

If \(h\le0\), the \(A\)-side and the \(B\)-side are separately
nonincreasing.  If \(C=0\), (2) uses \(|LC+C'|=|C'|\), exactly the upper
Dini derivative required at the absolute-value kink.

For a given gcd mask \(G_0=\gcd(n,D)\), let its allowed divisors be
\(1=d_0<d_1<\cdots<d_s\), and set \(d_{-1}=0\).  On the ratio sector

\[
 d_{j-1}<n/N\le d_j\qquad(0\le j\le s)
\]

the active set is exactly \(\{d_j,\ldots,d_s\}\).  Hence all active sets
are exhausted by

\[
 \sum_{G_0\mid D}\tau(G_0)=3^{|{\cal P}|}
\]

cells: \(243,81,27,9\) for the four prime sets.

The verifier covers each cell by outward-rounded \((L,y)\) rectangles.
For \(L\le\log(N_{\min}d_j)\), it uses
\(q_N\ge N_{\min}^2-t/16\).  Above that transition,
\(n/N\le d_j\) gives
\(q_N\ge e^{2L}/d_j^2-t/16\).  Both are one-sided in the conservative
direction.  Explicitly, with \(c=|C|\ge0\) and
\(K=|LC+C'|-(L/2)c\), the positive contribution depending on \(g\) is

\[
 U(g)=e^{y(L+g)}[K+gc]_+.
\]

On the positive branch,
\(U'(g)=e^{y(L+g)}(y[K+gc]+c)\ge0\), while on the zero branch
\(U=0\).  Thus \(U\) is nondecreasing in \(g\); since \(g_N\) decreases
with \(q_N\), replacing \(N\) by its smallest feasible value is safe.
Padded binary64 endpoints are checked to contain the exact logarithmic
and square-root endpoints.

## 4. Certified domain and output

The closed \(y\)-domain is

\[
 \sqrt{87677/2500000}\le y\le\sqrt{271/400}.
\]

The four contiguous finite ranges are

| prime set | integer \(N\)-range |
|---|---:|
| \(\{2,3,5,7,11\}\) | \(690988\ldots728999\) |
| \(\{2,3,5,7\}\) | \(729000\ldots818999\) |
| \(\{2,3,5\}\) | \(819000\ldots1027999\) |
| \(\{2,3\}\) | \(1028000\ldots3840000\) |

At both 180-bit and 256-bit Arb precision, (3) passes on every
rectangle.  The coverage counts are:

| prime set | patterns | leaf rectangles | splits | \(h\le0\) leaves |
|---|---:|---:|---:|---:|
| P11 | 243 | 297490 | 297004 | 93662 |
| P7 | 81 | 52239 | 52077 | 15287 |
| P5 | 27 | 9290 | 9236 | 4367 |
| P23 | 9 | 237 | 219 | 81 |

The largest certified ratio \(G h_+/((L/2)|C_0|)\) is
`0.99999860767275095`, strictly below one.  Therefore every summand of
\({\cal F}_{N,{\cal P}}\) has nonpositive upper right Dini derivative.
Each summand is locally Lipschitz (an absolute value of an analytic
function times the exponential of the clipped, hence Lipschitz,
\(\sigma_N\)).  It is therefore absolutely continuous; its ordinary
derivative is nonpositive almost everywhere and integration makes it
nonincreasing.  Since \(\gamma_N\) is strictly decreasing, hence

\[
 {\cal F}_{N,{\cal P}}(y)\le
 {\cal F}_{N,{\cal P}}(y_0)
\quad(y\ge y_0)
\]

on every certified finite window.

## 5. Numerator transfer and two composition options

Let

\[
 \mathrm{Num}_N(y)=1-{\cal F}_{N,{\cal P}}(y).
\]

The certified theorem immediately gives

\[
 \mathrm{Num}_N(y)\ge \mathrm{Num}_N(y_0).
\]

If the fixed-height producer certifies

\[
 \mathrm{lbound}_N(y_0)
 =\frac{\mathrm{Num}_N(y_0)}{M_N(y_0)}-K_N(y_0)\ge T_N,
\]

then \(M_N>0\) and \(K_N\ge0\) imply

\[
 \mathrm{Num}_N(y_0)\ge M_N(y_0)T_N\ge M_{\rm lo}T_N.
\]

This numerator floor can be composed directly with independent uniform
caps:

\[
 |f_t|\ge
 \frac{M_{\rm lo}T_N}{M_{\rm max}}-K_{\rm max}.
\]

Thus monotonicity of \(M_N\) and \(K_N\) is not logically needed if the
composition certifies the explicit final gate

\[
 \frac{M_{\rm lo}T_N}{M_{\rm max}}
 -K_{\rm max}-E_{\rm max}>0.
\]

This is the shortest production route.

For completeness, one may instead transfer the native lower bound itself
using the following monotonicities.

The native normalizer

\[
 M_{N,{\cal P}}(y)=\sum_{d\mid D}|\lambda_d|d^{-\sigma_N(y)}
\]

is nonincreasing because \(\sigma_N\) is increasing.

The native \(\kappa\)-correction is

\[
 K_N(y)=\gamma_N(y)\sum_{m=2}^N b_t(m)
 (m^{\rho_N y}-1)m^{y-\sigma_N(y)},\qquad
 \rho_N=\frac{t}{2(x_N-6)}.
\]

For \(z=\rho_Ny\log m>0\),

\[
 \frac{e^z}{e^z-1}\le1+\frac1z
\]

gives the per-term upper log-rate

\[
 g_N+(1-\sigma_N')\log m+
 \rho_N\log m\frac{e^z}{e^z-1}
\le
 g_N+\frac12\log N+\rho_N\log N+\frac1{y_0}.
\]

The right side is decreasing in \(N\), and at
\((N,y)=(690988,y_0)\) it is at most

\[
 -1.3631121547576400<0.
\]

Thus \(K_N(y)\) is nonincreasing.

Set \(L_N(y)=\mathrm{Num}_N(y)/M_{N,{\cal P}}(y)-K_N(y)\).

If a fixed-height certificate gives \(L_N(y_0)>0\), then
\(\mathrm{Num}_N(y_0)>0\).  The numerator is increasing, the positive
normalizer is decreasing, and the correction is decreasing.  Therefore

\[
 L_N(y)\ge L_N(y_0)\qquad(y\ge y_0).
\]

This is a direct theorem for the production exponent and the native
Triangle functional.  It uses neither the invalid standard-majorant
claim, nor `seam_exponent`, nor `seam_ytransfer` Y2/Y3, nor a separate
\(C_{\cal P}\) conversion.  The remaining inputs are the fixed-\(y_0\)
finite sweep, a uniform effective-approximation error budget, and the
separate \(N>3840000\) tail/criterion/slab legs.
