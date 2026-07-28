# Native normalizer and \(\kappa\)-correction monotonicity

Row and domain:

\[
t=129/800,\quad y_0^2=87677/2500000,\quad
y_0\le y\le\sqrt{271/400},\quad
690988\le N\le3840000.
\]

The four finite legs use Euler prime sets P11, P7, P5, and P23 on the
contiguous ranges stated in
`TRIANGLE_Y_DINI_THEOREM.independent.md`.

## 1. Production exponent

Let

\[
q_N=N^2-t/16,\quad x_N=4\pi q_N,
\]
\[
\sigma_N(y)=\frac{1+y}{2}+\frac t4\log q_N
-\frac{t}{2x_N^2}\max(0,h_N(y)),
\]
\[
h_N(y)=1-3y+\frac{4y(1+y)}{x_N^2}.
\]

On the whole domain,

\[
h_N'(y)=-3+\frac{4(1+2y)}{x_N^2}<0.
\]

Therefore \(y\mapsto\max(0,h_N(y))\) is nonincreasing, and for
\(y_2\ge y_1\),

\[
\sigma_N(y_2)-\sigma_N(y_1)\ge\frac12(y_2-y_1).
\tag{1}
\]

This global increment inequality includes the positive-part kink.

## 2. Native mollifier normalizer

For a nonempty Euler prime set \({\cal P}\), put

\[
M_{N,{\cal P}}(y)=
\sum_{d\mid\prod_{p\in{\cal P}}p}
|\lambda_d|d^{-\sigma_N(y)},\qquad
|\lambda_d|=\prod_{p\mid d}b_t(p).
\]

Every coefficient is positive and \(d\ge1\).  By (1), every \(d>1\)
summand is strictly decreasing, while the \(d=1\) summand is the constant
one.  Hence \(M_{N,{\cal P}}\) is strictly decreasing in \(y\) on all four
legs.  Equivalently, wherever differentiated,

\[
M'=-\sigma_N'\sum_{d>1}|\lambda_d|\log(d)d^{-\sigma_N}<0.
\]

## 3. Native correction

Let

\[
g_N=\frac1{50}-\frac12\log q_N,\qquad
k_N=\frac{t}{2(x_N-6)}>0.
\]

The correction subtracted by the native Triangle lower bound is

\[
K_N(y)=\gamma_N(y)\sum_{m=2}^N b_t(m)
\bigl(m^{k_Ny}-1\bigr)m^{y-\sigma_N(y)}.
\]

Every summand is positive.  For \(\ell=\log m\) and
\(u=k_Ny\ell>0\), its upper logarithmic right derivative is

\[
g_N+(1-\sigma_N')\ell+
k_N\ell\frac{e^u}{e^u-1}.
\]

The elementary inequality

\[
\frac{u}{1-e^{-u}}\le1+u\qquad(u>0)
\]

is equivalent to \(1+u\le e^u\).  Since
\(\sigma_N'\ge1/2\), \(m\le N\), and \(y\ge y_0\), the rate is at most

\[
\Xi(N)=g_N+\frac12\log N+k_N\log N+\frac1{y_0}.
\tag{2}
\]

The first two \(N\)-dependent terms decrease because, with \(a=t/16\),

\[
\frac d{dN}\left(g_N+\frac12\log N\right)
=-\frac{N^2+a}{2N(N^2-a)}<0.
\]

Also \(k_N\log N\) has derivative with the sign of

\[
\frac{x_N-6}{N}-8\pi N\log N<0
\]

for \(N\ge690988\) (indeed \(\log N>1/2\)).  Thus (2) is maximized at
\(N=690988,y=y_0\), where outward interval arithmetic gives

\[
\Xi\le-1.3631121547576400<0.
\]

Every correction summand, and hence \(K_N\), is strictly decreasing.

## 4. Composition

The direct Triangle theorem proves
\(\mathrm{Num}_N(y)=1-{\cal F}_N(y)\) is nondecreasing and a positive
fixed-height native certificate makes \(\mathrm{Num}_N(y_0)>0\).
Consequently,

\[
L_N(y)=\frac{\mathrm{Num}_N(y)}{M_{N,{\cal P}}(y)}-K_N(y)
\]

is nondecreasing.  A fixed-height floor \(L_N(y_0)\ge T_{\rm floor}\)
therefore gives \(L_N(y)\ge T_{\rm floor}\) on the full \(y\)-interval.

The effective-approximation error budget of `RECORD_BINDING` R3 is an
additive bound after the lower bound for \(|f_t|\).  Hence, with its own
uniform full-\(y\) cap \(E_{\max}\), the final gate is simply

\[
T_{\rm floor}-E_{\max}>0.
\]

No `RECORD_BINDING` R2 conversion constant is needed here: the native
Triangle functional has already divided by `modmoll` and directly bounds
\(|f_t|\).  The normalizer \(M\) above is that native `modmoll`, not a
second Euler prefactor.  The correction \(K_N\) is part of the native
lower bound, not part of \(e_A+e_B+e_{C,0}\); it must not be counted again
in \(E_{\max}\).

This last paragraph is a load-bearing theorem-level identification, not a
consequence of the interval monotonicity calculation alone.  External review
should derive it directly from the producer and the definitions in
arXiv:1904.12438v2; see `OPEN_REVIEW_QUESTIONS.md`.
