# Proof note for the \(0.1787854\) bound

## Status and theorem

This repository presents a **computer-assisted unconditional proof** of

\[
\boxed{\Lambda\le
\frac{893927}{5000000}=0.1787854}.
\tag{0.1}
\]

It has not yet been peer reviewed. “Unconditional” describes
the logical form of the proof: no unproved conjecture is assumed. The
argument depends on two published theorem inputs and on the new mathematical
and computational certificates recorded here; every input's applicability
and every certificate's stated predicate is open for independent
verification, with the referee entry points recorded in
`OPEN_REVIEW_QUESTIONS.md`.

The result does not prove the Riemann hypothesis. Its upper bound
is positive.

## 1. Exact row

Set

\[
X=6000000185827,\qquad
t_0=\frac{129}{800},\qquad
y_0^2=\frac{87677}{2500000}.
\tag{1.1}
\]

Take \(y_0\) to be the positive square root. Then

\[
0<t_0<\frac12,\qquad
0<y_0^2<1-2t_0=\frac{271}{400}<1,
\tag{1.2}
\]

and

\[
t_0+\frac{y_0^2}{2}
=\frac{893927}{5000000}=0.1787854.
\tag{1.3}
\]

Also

\[
y_0^2+2t_0=\frac{893927}{2500000}<1,
\tag{1.4}
\]

which is the canopy inequality used by the barrier form of the criterion.

## 2. The exact criterion being instantiated

The logical weld is Theorem 1.2 of D. H. J. Polymath,
arXiv:1904.12438v2. In the notation of that theorem, it is enough to prove:

1. **Hypothesis (i), verified height.** There are no zeros
   \(\zeta(\sigma+iT)=0\) with
   \[
   \frac{1+y_0}{2}\le\sigma\le1,\qquad
   0\le T\le\frac X2.
   \tag{2.1}
   \]
2. **Hypothesis (ii), final-time right region.** There are no zeros
   \(H_{t_0}(x+iy)=0\) with
   \[
   x\ge X+\sqrt{1-y_0^2},\qquad
   y_0\le y\le\sqrt{1-2t_0}.
   \tag{2.2}
   \]
3. **Hypothesis (iii), intermediate-time barrier.** There are no zeros
   \(H_t(x+iy)=0\) with
   \[
   \begin{aligned}
   &X\le x\le X+\sqrt{1-y_0^2},\\
   &\sqrt{y_0^2+2(t_0-t)}
      \le y\le\sqrt{1-2t},\\
   &0\le t\le t_0.
   \end{aligned}
   \tag{2.3}
   \]

Theorem 1.2 then gives

\[
\Lambda\le t_0+\frac{y_0^2}{2}.
\tag{2.4}
\]

The transcribed criterion audit under
`vendor/dbn21a/certificates/record/criterion_theorem/` records the
\(\xi\)-to-\(H_0\) normalization \(x=2T\) and a proof map to the paper. The
paper remains the authoritative source.

## 3. Theorem 1.2 hypothesis (i): verified height

Platt and Trudgian prove that every nontrivial zeta zero through

\[
T_{\rm PT}=3000175332800
\tag{3.1}
\]

lies on the critical line. The criterion consumes only

\[
\frac X2=\frac{6000000185827}{2}=3000000092913.5.
\tag{3.2}
\]

The exact surplus is

\[
T_{\rm PT}-\frac X2=\frac{350479773}{2}>0.
\tag{3.3}
\]

Because \(y_0>0\), the interval in (2.1) lies strictly to the right of
\(\sigma=1/2\). The finite RH verification therefore excludes every
nontrivial zero with positive ordinate in (2.1). At the endpoint \(T=0\), for
\(0<\sigma<1\), the Dirichlet eta function satisfies
\[
\eta(\sigma)=\sum_{n\ge1}(-1)^{n-1}n^{-\sigma}>0
\]
by grouping consecutive terms, while
\(\eta(\sigma)=(1-2^{1-\sigma})\zeta(\sigma)\) and
\(1-2^{1-\sigma}<0\). Hence \(\zeta(\sigma)<0\) on \(0<\sigma<1\).
At \(s=1\), zeta has a pole, not a zero. This supplies hypothesis (i)
without assuming RH beyond the verified finite height.

For clarity about the sign in this normalization, a zero
\(H_0(x+iy)=0\) first gives
\(\xi((1-y+ix)/2)=0\).  The functional equation
\(\xi(s)=\xi(1-s)\), followed by conjugation, gives
\(\xi((1+y+ix)/2)=0\), which is exactly the representative in (2.1).
`verifiers/verify_criterion_sign_map.py` checks this affine algebra over
exact rationals; the functional equation and reality symmetry are the cited
classical analytic inputs.

## 4. Theorem 1.2 hypothesis (ii): finite windows

At \(t=t_0\), define

\[
x_N=4\pi\left(N^2-\frac{t_0}{16}\right),
\qquad
W_N=[x_N,x_{N+1}).
\tag{4.1}
\]

Put

\[
x_*:=X+\sqrt{1-y_0^2}.
\tag{4.2}
\]

`WINDOW_FREEZE_THEOREM.md` proves with exact rational Machin bounds for
\(\pi\), exact square-root brackets, and an independent 400-bit interval
calculation that

\[
x_{690988}<x_*<x_{690989}.
\tag{4.3}
\]

The respective strict margins exceed \(5.37\times10^6\) and
\(1.19\times10^7\). Since

\[
x_{N+1}-x_N=4\pi(2N+1)>0,
\tag{4.4}
\]

the half-open windows associated to the stored rows cover

\[
[x_*,x_{3840001})
\tag{4.5}
\]

without a gap or double assignment.

### 4.1 Conservative \(x\)-freeze

The finite producer freezes three Theorem 1.3 quantities at the closed left
edge of each window. `WINDOW_FREEZE_THEOREM.md` proves, uniformly for the
complete finite \(y\)-range,

\[
G(x,y)\le G_N(y),\qquad
K(x,y)\le K_N(y),\qquad
\Sigma(x,y)\ge\Sigma_N(y)
\quad(x\in W_N).
\tag{4.6}
\]

The signs follow from elementary \(x\)-monotonicity, including the kink of
the positive-part term in \(\Sigma\). At \(x=x_{N+1}\), the point belongs to
\(W_{N+1}\), where all three constants reset in the conservative direction.

### 4.2 Stored fixed-height floors

The 15 compressed finite certificates contain exactly one positive row for
every

\[
690988\le N\le3840000.
\tag{4.7}
\]

There are \(3,149,013\) rows, with no gaps, duplicates, overlaps, `UNCERT`
records, or nonpositive lower bounds. The four auxiliary-prime legs are

\[
\begin{array}{c|c|c}
N\text{-range}&\mathcal P&\min T_N\\ \hline
690988\ldots728999&\{2,3,5,7,11\}&0.000000791366\\
729000\ldots818999&\{2,3,5,7\}&0.000315112459\\
819000\ldots1027999&\{2,3,5\}&0.000305788807\\
1028000\ldots3840000&\{2,3\}&0.000309285478.
\end{array}
\tag{4.8}
\]

### 4.3 Transfer over the complete height interval

The direct all-height note
`provenance/TRIANGLE_Y_DINI_THEOREM.independent.md` bounds the upper-right
Dini derivative of the exact signed-composite-divisor Triangle mass. It
retains the cancellation structure that invalidates the earlier
multi-prime standard-majorant shortcut. The exhaustive divisor-cell counts
are

\[
3^5,\ 3^4,\ 3^3,\ 3^2=243,\ 81,\ 27,\ 9.
\tag{4.9}
\]

The direct Arb runs at 180 and 256 bits prove the required strict
inequalities; the worst stored ratio satisfies

\[
\text{ratio}\le0.99999860767275095<1.
\tag{4.10}
\]

Local Lipschitz continuity and the upper-Dini bound give global
monotonicity. A separate interval proof shows that the Euler normalizer and
the \(\kappa\)-correction are nonincreasing; the worst correction
logarithmic-rate upper bound is

\[
-1.3631121547576400<0.
\tag{4.11}
\]

Thus each stored positive fixed-height floor transfers to every

\[
y_0\le y\le\sqrt{1-2t_0}.
\tag{4.12}
\]

### 4.4 Native binding and effective error

`NATIVE_BINDING.md` closes the algebraic interface to the function \(f_t\)
in Polymath Theorem 1.3. With the real Euler mollifier \(E\), exact
Dirichlet convolution gives

\[
EA=\sum B_{N,n}n^{-s_*},\qquad
\overline E\,C_0=\sum A_{N,n}n^{-\overline{s_*}}.
\tag{4.13}
\]

The second conjugate is essential. The triangle inequalities, the
\(\kappa\)-correction, and \(|E|\le M_N\) yield

\[
|f_t|\ge
\frac{1-g_N-\sum_{n\ge2}
(|B_{N,n}|+g_N|A_{N,n}|)n^{-\sigma_N}}
{M_N}
-g_NC_N=L_N.
\tag{4.14}
\]

Positivity of the stored row supplies the sign needed when replacing
\(|E|\) by \(M_N\), and also rules out \(E=0\). Therefore the stored
\(T_N\) is already in the same normalized units as the additive
Theorem 1.3 error. There is no second Euler-factor conversion.

The target error verifier uses \(x-6.66\) for \(e_A+e_B\) and the
conservative \(x-12,\ 10.50\) corollary of Proposition 6.6(vi) for
\(e_{C,0}\), as derived in `ERROR_CONSTANT_WELD.md`.  It does not rely on
the displayed \(10.44\) in equation (24).  It obtains

\[
\begin{aligned}
e_A+e_B&\le0.000000000002057023688667,\\
e_{C,0}&\le0.000000233492848188649183,\\
E_{\max}&\le0.000000233494905212337849.
\end{aligned}
\tag{4.15}
\]

Consequently

\[
|f_{t_0}|-E_{\max}
\ge0.000000791366-E_{\max}
\ge0.000000557871094787>0.
\tag{4.16}
\]

Theorem 1.3 and nonvanishing of its factor \(B_{t_0}\) then give
\(H_{t_0}\ne0\) on the finite region (4.5) and (4.12).

### 4.5 Authoritative Arb backend for the error budget

The bounds (4.15) and the margin (4.16) are certified authoritatively by
the standalone FLINT/Arb program `verifiers/verify_prop410_arb.c`.  It
recomputes the complete U1--U5 budget and every associated domain/sign
gate from the exact rational inputs
\(t\in[129/800,\,161250001/10^9]\), \(y_0^2=87677/2500000\),
\(y_{\max}^2=271/400\), \(N_0=690988\), \(m_0=2000\) using rigorous Arb
enclosures for every square root, logarithm, exponential, power, and
\(\pi\); decimal constants enter as exact rationals
(\(0.02=1/50\), \(0.626=313/500\), \(1.24=31/25\), \(6.66=333/50\),
\(10.50=21/2\), \(0.125=1/8\)).  Each decisive inequality subtracts the
exact rational bound and requires the entire resulting ball to be on the
strict side, so an indeterminate comparison fails closed.  The program
reads no stored certificate, requires its precision as an explicit
argument, and refuses precision below 256 bits.  The sealed transcripts
`logs/prop410_arb_256.log` and `logs/prop410_arb_512.log` were produced
in the pinned review container and are strictly parsed by
`verifiers/verify_prop410_arb_logs.py` (prerequisite P17 of the final
assembly); `scripts/run_prop410_arb.sh` replays the calculation from
source.

The earlier `mpmath.iv` computation of the same budget (inside
`verifiers/verify_finite_and_binding.py`, and its derived copy
`independent/prop410/prop410_proof.py`) remains in place as
non-authoritative corroboration.  The two Python programs share one
backend and a line-for-line identical `effective_error_budget()`, so the
second is a same-backend replay rather than an independent numerical
implementation; cross-backend independence for Proposition 4.10 is
supplied by the Arb program above.

## 5. Theorem 1.2 hypothesis (ii): infinite tail

The tail begins at the closed cutoff

\[
N_*=3840000.
\tag{5.1}
\]

`TAIL_LEMMA.md` is a quantified theorem, not merely a numerical log. It uses
an exact finite Dirichlet convolution, endpoint-cap bounds, and analytic
monotonicity to reduce every \(N\ge N_*\) to one interval computation at
the cutoff. It treats the complete \(t\)-box

\[
\left[\frac{129}{800},\frac{161250001}{10^9}\right],
\tag{5.2}
\]

a closed box strictly containing \(y_0\), and an extended \(y\)-box whose
top covers \(\sqrt{1-2t_0}\). No sampling in \(N\) and no assumed
monotonicity in \(t\) is used.

One standalone FLINT/Arb implementation, run at 256 and 512 bits, certifies

\[
D<0.999721,\qquad
\frac{1-D}{M_{\max}}-(e_A+e_B+e_{C,0})
>0.00017352.
\tag{5.3}
\]

The error calculation uses the exact definitions (71)--(72) for
\(e_A+e_B\) and the conservative \(x-12,\ 10.50\) corollary of Proposition
6.6(vi) for \(e_{C,0}\). Hence

\[
H_{t_0}(x+iy)\ne0
\quad\text{for every}\quad
x\ge x_{3840000},\quad
y_0\le y\le\sqrt{1-2t_0}.
\tag{5.4}
\]

The finite lane includes the complete window
\(W_{3840000}=[x_{3840000},x_{3840001})\), while the tail starts at
\(x_{3840000}\). Thus (4.5) and (5.4) overlap and jointly cover every
\(x\ge x_*\). This proves hypothesis (ii).

## 6. Theorem 1.2 hypothesis (iii): closed barrier

Set

\[
R=[X,X+1]+i\left[\frac{1809}{10000},1\right].
\tag{6.1}
\]

`BARRIER_CERTIFICATE.md` proves

\[
H_t(z)\ne0
\quad(z\in R,\ 0\le t\le t_0).
\tag{6.2}
\]

### 6.1 Containment of the required curved barrier

The exact lower-edge margin is

\[
y_0^2-\left(\frac{1809}{10000}\right)^2
=\frac{234599}{100000000}>0.
\tag{6.3}
\]

Moreover,

\[
\sqrt{1-y_0^2}<1,\qquad
y_0^2+2(t_0-t)\le y_0^2+2t_0<1.
\tag{6.4}
\]

Therefore the entire region (2.3) lies in the closed box (6.1).

### 6.2 Effective approximation on the complete box

Write \(g_t=H_t/B_t\). A separate 256-bit Arb calculation evaluates
the bounds (20)--(23) and the conservative Proposition 6.6(vi) corollary
over the complete
\((x,y,t)\)-box and proves

\[
e_A+e_B+e_{C,0}
<0.000356523011600040<0.00125.
\tag{6.5}
\]

It also proves that the Riemann--Siegel index is exactly \(N=690988\)
throughout the box. The endpoint \(t=0\), outside the literal positive-\(t\)
statement of Theorem 1.3, follows by a compact dominated-convergence limit:
\(H_t\), \(B_t^{\pm1}\), the fixed finite sum \(f_t\), and this conservative
majorant are continuous down to \(t=0\), while \(B_t\ne0\).

### 6.3 Fail-closed prism certificate

For each closed prism \([t_i,t_{i+1}]\), the verifier encloses \(f_{t_i}\)
on a cyclic boundary mesh. If \(M_i\) is the minimum mesh modulus,
\(D_{z,i}\) bounds the spatial derivative, and \(D_{t,i}\) bounds the time
derivative on the complete prism, the sole acceptance gate is

\[
M_i>
\frac{D_{z,i}}{2(\mathrm{num}-1)}
+D_{t,i}(t_{i+1}-t_i)+0.00125.
\tag{6.6}
\]

All quantities are interval-directed. Overlap or indeterminacy is failure.
The \(D_t\) bound is recomputed on the whole proposed prism, not sampled at
its left endpoint. Each boundary polygon must also have zero-free endpoint
balls, argument increments strictly inside \((-\pi,\pi)\), and a complete
winding enclosure strictly inside \((-1/4,1/4)\).

`DERIVATIVE_BOX_LEMMA.md` supplies the uniform \(D_z,D_t\) theorem used
here. It evaluates increasing and decreasing \(x,y\)-factors at their
separately conservative endpoints and proves the remaining coupled
monotonicities. The discrete Lemma 8.4 sums are bounded by an exact
16-term Arb head plus an integral of a rigorously decreasing tail. The
quadrature callbacks retain the complete complex variable and use analytic
logarithms and powers when FLINT requests a holomorphic enclosure.

The factor \(1/2\) in (6.6) also controls the winding homotopy. On each
half of a mesh subedge, both the true boundary image and its endpoint chord
remain inside the convex disk of radius \(D_zh/2\) about the nearer mesh
value. Time motion and the approximation error enlarge that radius by the
other two terms in (6.6). The strict gate makes every such disk zero-free.

The stored 20-digit coefficient components are restored as balls and
independently regenerated: all \(7,688\) regenerated components are
contained. A separate factorial estimate bounds the omitted Taylor tail by

\[
1.954234593244762\times10^{-22}<10^{-20},
\tag{6.7}
\]

and that radius is propagated through every barrier value.

The sealed result consists of 883 consecutive closed prisms beginning
exactly at \(0\), with byte-identical adjacent seams, whose final stored
endpoint encloses \(129/800\).  The last prism is restricted to its
intersection with \(t\le129/800\); this can only decrease its displacement
allowance, and the uniform approximation estimate is used only through the
exact endpoint. Every prism has winding zero, and the independently
recomputed minimum margin has certified lower bound

\[
\ge0.519849894613872543374989997.
\tag{6.8}
\]

The interpolation and time-motion bounds give a zero-avoiding homotopy from
the certified polygon to \(g_t(\partial R)\). Since \(B_t\ne0\), the
argument principle proves (6.2). This proves hypothesis (iii).

The historical vendored winding and site-glue outputs are not consumed by
this argument.

## 7. Conclusion

Sections 3, 4--5, and 6 respectively supply hypotheses (i), (ii), and (iii)
of Polymath Theorem 1.2. Substitution of (1.1) into its conclusion yields

\[
\boxed{\Lambda\le
t_0+\frac{y_0^2}{2}
=\frac{893927}{5000000}
=0.1787854}.
\tag{7.1}
\]

This is an unconditional implication in the sense that no
conjectural hypothesis remains. It is a **computer-assisted unconditional
proof, not yet peer reviewed**: formal peer review of the cited-theorem
applications, the new lemmas, the proof-to-code maps, and
the interval computations is the remaining step.

## 8. Review boundary

The automated checks establish, relative to their source code and interval
libraries:

- exact rational parameter identities and theorem-domain containments;
- integrity and complete parsing of the stored evidence;
- strict directed inequalities for all encoded finite, tail, and barrier
  gates;
- absence of finite-window gaps and a closed finite/tail overlap;
- provenance of the barrier coefficient matrix and Taylor remainder; and
- fail-closed completion of the exact target assembly.

They do not, merely by printing `PASS`, establish:

- the correctness or applicability of the published Polymath and
  Platt--Trudgian theorems;
- the correctness of each handwritten analytic reduction in
  `NATIVE_BINDING.md`, `WINDOW_FREEZE_THEOREM.md`, `TAIL_LEMMA.md`,
  `DERIVATIVE_BOX_LEMMA.md`, and `BARRIER_CERTIFICATE.md`;
- faithful implementation of every mathematical bound in C and Python;
- the absence of compiler, library, or hardware faults common to all
  replays; or
- peer review, novelty, priority, or readiness for public announcement.

Those are the intended tasks of the external review.
