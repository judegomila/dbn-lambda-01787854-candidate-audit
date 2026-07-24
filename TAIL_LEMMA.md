# Standalone P1113 tail/contraction lemma for the \(0.1787854\) row

Status: draft for mathematical review. This note states and proves the
generic tail theorem consumed by `verify_tail_arb.c`; it is not merely a
description of the numerical output.

The only non-elementary analytic input is Theorem 1.3, together with the
exact error definitions (71)--(72) and the displayed \(e_{C,0}\) estimate
(24), of D. H. J. Polymath, *Effective approximation of heat flow evolution
of the Riemann \(\xi\) function, and a new upper bound for the
de Bruijn--Newman constant*, arXiv:1904.12438v2.

## 1. Exact target and quantified conclusion

Set

\[
\begin{aligned}
I_t&=\left[\frac{129}{800},\frac{161250001}{10^9}\right],&
N_*&=3840000,\\
M&=153814,&M_{\rm err}&=3000,\\
I_{\rm box}&=\left[\frac{1872719}{10^7},
                         \frac{23409}{125000}\right],&
I_{\rm ext}&=\left[\frac{1872719}{10^7},
                         \frac{8231039}{10^7}\right].
\end{aligned}
\]

The exact design point is

\[
t_0=\frac{129}{800},\qquad
y_0^2=\frac{87677}{2500000},\qquad
t_0+\frac{y_0^2}{2}=\frac{893927}{5000000}=0.1787854.
\]

The verifier checks by exact integer arithmetic that

\[
\left(\frac{1872719}{10^7}\right)^2
<y_0^2<
\left(\frac{23409}{125000}\right)^2
\]

and

\[
\left(\frac{8231039}{10^7}\right)^2\ge1-2t_0.
\]

It also checks that the preceding \(10^{-7}\)-grid point is below
\(\sqrt{1-2t_0}\), and that the top of \(I_{\rm box}\) is below
\(\sqrt{1-2t}\) throughout \(I_t\).

Let

\[
\mathcal S=\{1,2,3,4,5,6,7,10,11,13,14\},
\]

with

\[
\begin{array}{c|rrrrrrrrrrr}
d&1&2&3&4&5&6&7&10&11&13&14\\ \hline
\lambda_d&
1&-\frac{1021}{1000}&-\frac{1054}{1000}&-\frac9{200}&
-\frac{1119}{1000}&\frac{1001}{1000}&-\frac{1043}{1000}&
\frac{128}{125}&-\frac{161}{200}&-\frac{447}{500}&
\frac{456373}{500000}.
\end{array}
\]

The machine checks \(\lambda_1=1\) and
\(\sum|\lambda_d|=9918746/10^6\) exactly.

**Tail theorem.** For every

\[
t\in I_t,\qquad
y\in[y_0,\sqrt{1-2t}],\qquad
x\ge X_{N_*}(t),
\]

where

\[
X_N(t)=4\pi\left(N^2-\frac t{16}\right),
\]

the approximation \(f_t\) in Polymath Theorem 1.3 obeys

\[
|f_t(x+iy)|>e_A+e_B+e_{C,0}.
\]

Consequently \(H_t(x+iy)\ne0\) on this complete region.

The proof is in Sections 2--9.

## 2. Window freezing

For \(x\ge X_{N_*}(t)\), define

\[
N=N(x,t)=
\left\lfloor\sqrt{\frac{x}{4\pi}+\frac t{16}}\right\rfloor.
\]

Then \(N\ge N_*\) and

\[
x\in[X_N(t),X_{N+1}(t)).
\]

Put

\[
b_t(u)=\exp\left(\frac t4\log^2u\right),\qquad
L_N(t)=\log\left(N^2-\frac t{16}\right).
\]

Define

\[
\delta(N,t)=
\frac t4\left[-\log\left(1-\frac{t}{16N^2}\right)\right]
+\frac{t}{2X_N(t)^2}
\]

and

\[
k(N,t)=\frac{t}{2(X_N(t)-6)}.
\]

For fixed \(t\ge0\), both functions decrease with \(N\). Let
\(\widehat\delta\) and \(\widehat k\) be rigorous upper bounds for
\(\delta(N_*,t)\) and \(k(N_*,t)\) over the whole interval \(I_t\).

For \(N\ge N_*\), define

\[
\begin{aligned}
\sigma_1(N,t,y)
 &=\frac{1+y}{2}+\frac t2\log N-\widehat\delta,\\
\sigma_2(N,t,y)
 &=\frac{1-y}{2}+\frac t2\log N-\widehat\delta-\widehat k,\\
G(N,t,y)
 &=e^{0.02y}\left(N^2-\frac t{16}\right)^{-y/2}.
\end{aligned}
\]

Polymath (20)--(22) imply

\[
|\gamma|\le G,\qquad
\Re s_*\ge\sigma_1,\qquad
|\kappa|\le\widehat k.
\tag{2.1}
\]

Indeed, \(x/(4\pi)\ge N^2-t/16\). The positive-part expression in
(21) is at most \(1\) for \(0\le y\le1\) on the present domain, and

\[
\frac t4\log\left(N^2-\frac t{16}\right)
=\frac t2\log N
-\frac t4\left[-\log\left(1-\frac t{16N^2}\right)\right].
\]

The factors \(x^{-2}\), \((x-6)^{-1}\), and
\((x/(4\pi))^{-y/2}\) are all worst at the window's left edge.
The verifier checks \(0<t\le1/2\), \(0<y\le1\), \(X_N>200\), and all
positive denominators.

## 3. Endpoint-cap lemma

For \(1\le a<c\), define

\[
E_{t,\sigma}(u)
=u\,b_t(u)u^{-\sigma}
=\exp\left((1-\sigma)\log u+\frac t4\log^2u\right)
\]

and

\[
\operatorname{Cap}_t(a,c;\sigma)
=\max(E_{t,\sigma}(a),E_{t,\sigma}(c))\log(c/a).
\tag{3.1}
\]

**Lemma 3.1.** If

\[
\sigma>\frac t2\log c
\tag{3.2}
\]

and \(a\le J<K\le c\) are integers, then

\[
\sum_{J<n\le K}b_t(n)n^{-\sigma}
\le\operatorname{Cap}_t(a,c;\sigma).
\tag{3.3}
\]

**Proof.** The logarithmic derivative of
\(b_t(u)u^{-\sigma}\), with respect to \(\log u\), is
\((t/2)\log u-\sigma<0\). Thus the summand is decreasing, and

\[
\sum_{J<n\le K}b_t(n)n^{-\sigma}
\le\int_J^K b_t(u)u^{-\sigma}\,du
\le\int_a^c b_t(u)u^{-\sigma}\,du.
\]

With \(v=\log u\), the last integrand becomes

\[
\exp\left((1-\sigma)v+\frac t4v^2\right).
\]

Its logarithm is convex, so its maximum on
\([\log a,\log c]\) occurs at an endpoint. Multiplication by the
interval length \(\log(c/a)\) gives (3.3). \(\square\)

The Arb checker constructs (3.1) from independently rounded exponentials
and a directed upper maximum. Its `SC1` and `SC2` checks prove (3.2) for
every cap used below.

## 4. Exact convolution and the complete B-side remainder

Write the two sums in Polymath (14) as

\[
F_B=\sum_{k\le N}b_t(k)k^{-s_*},
\qquad
F_A=\sum_{k\le N}k^yb_t(k)k^{-\overline{s_*}-\kappa},
\]

so \(f_t=F_B+\gamma F_A\). Define

\[
M_\lambda(z)=\sum_{d\in\mathcal S}\lambda_d d^{-z}.
\]

Since \(M<N_*\le N\),

\[
M_\lambda(s_*)F_B
=\sum_{d\in\mathcal S}\sum_{k\le N}
\lambda_d b_t(k)(dk)^{-s_*}.
\tag{4.1}
\]

For \(m\le M\), let

\[
c_m(t)=\sum_{\substack{d\in\mathcal S\\d\mid m}}
\lambda_d b_t(m/d).
\tag{4.2}
\]

Because \(\lambda_1=b_t(1)=1\), \(c_1=1\). Partitioning the pairs
\((d,k)\) in (4.1) by \(dk\le M\) and \(dk>M\) gives the exact identity

\[
\begin{aligned}
M_\lambda(s_*)F_B-1
={}&\sum_{m=2}^{M}c_m(t)m^{-s_*}\\
&+\sum_{d\in\mathcal S}\lambda_d d^{-s_*}
  \sum_{\lfloor M/d\rfloor<k\le N}b_t(k)k^{-s_*}.
\end{aligned}
\tag{4.3}
\]

This is a disjoint exhaustive pair partition: \(dk>M\) is equivalent to
\(k>\lfloor M/d\rfloor\), and every pair has one unique \(d\).

Using (2.1) and Lemma 3.1,

\[
|M_\lambda(s_*)F_B-1|\le P+\mathrm{TR},
\tag{4.4}
\]

where

\[
P=\sum_{m=2}^{M}|c_m(t)|m^{-\sigma_1}
\tag{4.5}
\]

and

\[
\mathrm{TR}=
\sum_{d\in\mathcal S}|\lambda_d|d^{-\sigma_1}
\operatorname{Cap}_t(\lfloor M/d\rfloor,N;\sigma_1).
\tag{4.6}
\]

The implementation also reproduces

\[
\mathrm{OV}=
\sum_{\substack{d\in\mathcal S\\d>1}}
|\lambda_d|d^{-\sigma_1}
\operatorname{Cap}_t(N/(d+1),N;\sigma_1).
\tag{4.7}
\]

This is nonnegative padding, not a missing piece of (4.3). The complete
remainder is already covered by \(\mathrm{TR}\). The checked inequality
\(N\ge d(d+1)\) implies
\(\lfloor N/d\rfloor\ge N/(d+1)\) if one wants to interpret (4.7) as an
overshoot bound, but no disjointness claim about `OV` is needed.

## 5. The A branch and contraction quantity

From (2.1),

\[
\left|k^yb_t(k)k^{-\overline{s_*}-\kappa}\right|
\le b_t(k)k^{-\sigma_2}.
\tag{5.1}
\]

Also

\[
|M_\lambda(s_*)|
\le M_{\max}:=
\sum_{d\in\mathcal S}|\lambda_d|d^{-\sigma_1}.
\tag{5.2}
\]

Lemma 3.1 gives

\[
|\gamma F_A|\le\mathrm{AB},
\]

where

\[
\mathrm{AB}=G\left(
\sum_{k=1}^{M}b_t(k)k^{-\sigma_2}
+\operatorname{Cap}_t(M,N;\sigma_2)\right).
\tag{5.3}
\]

Therefore

\[
|M_\lambda(s_*)f_t-1|
\le D:=P+\mathrm{TR}+\mathrm{OV}+M_{\max}\mathrm{AB}.
\tag{5.4}
\]

The extra `OV` makes (5.4) weaker but remains valid.

## 6. Reduction from all \(N\ge N_*\) to one cutoff

Fix \(t,y\) and put \(q=\log N\). For
\(\sigma=\sigma_1\) or \(\sigma_2\),

\[
\frac{d\sigma}{dq}=\frac t2.
\tag{6.1}
\]

For a cap with fixed left endpoint \(a\), the two candidates in (3.1),
after multiplication by \(q-\log a\), have logarithmic derivatives

\[
-\frac t2\log a+\frac1{q-\log a}
\tag{6.2}
\]

and

\[
1-\sigma+\frac1{q-\log a}.
\tag{6.3}
\]

Both are negative if

\[
\frac t2\log a\,(q-\log a)>1
\tag{6.4}
\]

and

\[
(\sigma-1)(q-\log a)>1.
\tag{6.5}
\]

Once true at \(N_*\), (6.4) remains true as \(N\) grows. Under
\(t>0\) and \(\sigma>1\), both factors in (6.5) increase. Thus every
fixed-left cap used by \(\mathrm{TR}\), \(\mathrm{AB}\), and the error
calculation decreases for all \(N\ge N_*\).

The checker verifies (6.4)--(6.5):

- separately for all eleven \(\lfloor M/d\rfloor\) routed caps;
- for the A cap with \(a=M\); and
- explicitly for both error caps with \(a=M_{\rm err}=3000\).

The last checks are not inferred from a different cutoff.

For the moving cap in `OV`, both endpoints have the form \(N/r\) and
the width is constant. Direct differentiation gives

\[
\frac d{dq}\log E_{t,\sigma}(N/r)=1-\sigma<0.
\tag{6.6}
\]

Every other factor also decreases:

- \(P\), because \(c_m(t)\) is fixed when \(t\) is fixed and
  \(\sigma_1\) increases;
- \(d^{-\sigma_1}\), hence \(M_{\max}\);
- \(G\), because
  \[
  \frac d{dq}\log G
  =-\frac{yN^2}{N^2-t/16}<0;
  \]
- the finite A head, because \(\sigma_2\) increases.

Products and sums of nonnegative decreasing functions decrease. Hence

\[
D(N,t,y)\le D(N_*,t,y)
\qquad(N\ge N_*).
\tag{6.7}
\]

No sampling in \(N\) is involved.

## 7. The complete \(y\)-range and the \(t\)-interval

At fixed \(N,t\),

\[
\frac{\partial\sigma_1}{\partial y}=\frac12,\qquad
\frac{\partial\sigma_2}{\partial y}=-\frac12.
\]

All B-side terms decrease with \(y\). For every A-side head or cap
endpoint \(u\le N\),

\[
\frac{\partial}{\partial y}\log\bigl(GE_{t,\sigma_2}(u)\bigr)
=0.02-\frac12L_N(t)+\frac12\log u
\le0.02-\frac12L_N(t)+\frac12\log N.
\tag{7.1}
\]

The two algebraically equivalent `YM` gates certify that the last
quantity is strictly negative at \(N_*\), uniformly in \(I_t\); it
only becomes more negative as \(N\) grows. Therefore `AB` decreases
with \(y\). Since \(M_{\max}\) also decreases, so does
\(M_{\max}\mathrm{AB}\), and hence \(D\) decreases above
\(I_{\rm box}\).

The Arb calculation evaluates the whole closed \(I_{\rm box}\), which
contains \(y_0\), and (7.1) covers all larger \(y\). The error calculation
uses the whole closed interval \(I_{\rm ext}\), whose top is at least
\(\sqrt{1-2t}\) for every \(t\in I_t\).

No monotonicity in \(t\) is assumed. Arb evaluates the entire closed
\(t\)-interval at \(N_*\). The all-\(N\) and all-\(y\) arguments above
are pointwise for each fixed \(t\), so inclusion of \(I_t\) at the cutoff
proves the uniform result.

## 8. Error terms

Define

\[
\Delta(N,t)=
\frac{(t^2/16)L_N(t)^2+0.626}{X_N(t)-6.66}.
\tag{8.1}
\]

For \(n\le N\) and \(x\) in the \(N\)-window,

\[
\left|\log\frac{x}{4\pi n^2}\right|
\le\log\frac{x}{4\pi}.
\]

The only potentially negative logarithm occurs near \(n=N\); the checked
gate \(N(1-t/(16N^2))>1\) makes the displayed domination immediate at
the left edge.

For \(L=\log(x/(4\pi))>2\), \(A=t^2/16\), \(c=0.626\), and \(b=6.66\),

\[
\frac{d}{dx}\frac{AL^2+c}{x-b}<0,
\]

because its numerator is less than

\[
2AL-(AL^2+c)=-AL(L-2)-c<0.
\]

Thus (8.1) bounds the error exponent throughout the window and decreases
as \(N\) grows.

Using the exact definitions (71)--(72), not merely the coarser displayed
formula (23),

\[
\begin{aligned}
e_A+e_B
\le (e^\Delta-1)\bigg[
&\sum_{n\le N}b_t(n)n^{-\sigma_1}\\
&+G\sum_{n\le N}b_t(n)n^{-\sigma_2}
\bigg].
\end{aligned}
\tag{8.2}
\]

The A estimate uses, term by term,

\[
n^{-\Re\kappa}\le n^{|\kappa|}\le n^{\widehat k}.
\]

This point matters: equation (23) places \(N^{|\kappa|}\) outside the
sum. The implementation's sharper \(n^{\widehat k}\) estimate is justified
from (71), not from (23) alone.

Both sums in (8.2) are bounded by their first \(M_{\rm err}=3000\)
terms plus Lemma 3.1. The checker verifies their cap validity and
all-\(N\) gates directly.

The \(e_{C,0}\) bound is the displayed Polymath formula (24), with the
paper's denominator \(x-12\):

\[
\begin{aligned}
e_{C,0}\le\exp\bigg(
&-\frac{1+y}{4}L_N(t)-\frac t{16}L_N(t)^2\\
&+\frac{1.24(3^y+3^{-y})}{N-0.125}\\
&+\frac{3\sqrt{L_N(t)^2+\pi^2/4}+10.44}{X_N(t)-12}
\bigg).
\end{aligned}
\tag{8.3}
\]

At fixed \(N\), the exponent is maximal at the window's left edge. It
also decreases with \(N\). For the last quotient, put

\[
Q(L)=3\sqrt{L^2+\pi^2/4}+10.44.
\]

Since \(dQ/dx<3/x\),

\[
Q'(x)(x-12)-Q(x)<3-10.44<0.
\]

All other \(N\)-directions in (8.3) are immediate. Therefore the Arb
error enclosure at \(N_*\), on the complete \(I_t\times I_{\rm ext}\),
is uniform for every \(N\ge N_*\).

## 9. Numerical contraction and nonvanishing

At both 256 and 512 bits, the independent Arb implementation proves

\[
D<0.999721<1,
\]

\[
M_{\max}<1.608290,
\]

\[
\frac{1-D}{M_{\max}}>0.0001735,
\]

and

\[
0<e_A+e_B+e_{C,0}<0.000000011672.
\]

The strict final margin satisfies

\[
\frac{1-D}{M_{\max}}-(e_A+e_B+e_{C,0})
>0.00017352.
\]

From (5.4),

\[
|M_\lambda(s_*)f_t|\ge1-D.
\]

Together with (5.2), this gives

\[
|f_t|\ge\frac{1-D}{M_{\max}}
>e_A+e_B+e_{C,0}.
\]

Theorem 1.3 then yields

\[
\left|\frac{H_t}{B_t}\right|
\ge |f_t|-(e_A+e_B+e_{C,0})>0.
\]

The same theorem's normalizing factor \(B_t\) is nonzero on this domain,
so \(H_t(x+iy)\ne0\). This proves the tail theorem. \(\square\)

## 10. Proof-to-code map and scope

| Obligation | `verify_tail_arb.c` check or block |
|---|---|
| Exact target, boxes, and P1113 vector | initial exact-integer checks |
| Frozen \(\widehat\delta,\widehat k,\sigma_1,\sigma_2\) | `delta`, `kappa`, `s1*`, `s2*` |
| Cap validity | `SC1`, `SC2` |
| Exact convolution | `coefficient` construction |
| \(P,\mathrm{TR},\mathrm{OV}\) | named accumulation blocks |
| A branch and \(M_{\max}\) | `Mmax`, `Gbox`, `PA`, `AB` |
| All-\(N\) fixed caps | `GN-TR`, `GN-AB`, `GN-error` |
| Moving `OV` and floors | `OVW` |
| Complete \(y\)-range | `YM` and exact hull checks |
| Error monotonicity | `Delta N-monotonicity`, `eC0 quotient` |
| \(D<1\), flow \(>\) error | final strict Arb comparisons |

The C program reads no data files and uses no stored decimal as a
load-bearing bound. Broad two-sided corridors are regression tests only;
the proof uses the directed Arb inequalities.

This closes the internal cap/convolution/overshoot/all-\(N\)/full-\(y\)
tail implication, subject to the cited published approximation theorem.
The checker does not re-prove Polymath Theorem 1.3 itself. It also says
nothing about the separate finite sweep, winding slab, RH-height input, or
final criterion assembly.
