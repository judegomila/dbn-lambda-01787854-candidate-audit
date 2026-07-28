# Native Triangle binding

This note closes the algebraic interface between the stored direct-Triangle
certificates and the normalized function \(f_t\) in Theorem 1.3 of the
[Polymath15 upper-bound paper](https://arxiv.org/abs/1904.12438v2).
It is independent of the barrier/winding certificate.

## Statement

Fix a window \(N\), a real height \(y>0\), and a finite prime set
\(\mathcal P\).  Let

\[
x_N=4\pi\left(N^2-\frac t{16}\right),\qquad
x_N\le x<x_{N+1},
\]

and use the following conservative bounds from Theorem 1.3:

\[
|\gamma|\le g_N,\qquad
\Re s_*\ge \sigma_N,\qquad
|\kappa|\le k_N.
\]

The producer's stored value is

\[
L_N=
\frac{1-g_N-\displaystyle\sum_{n=2}^{DN}
 (|B_{N,n}|+g_N|A_{N,n}|)n^{-\sigma_N}}
{\displaystyle M_N}
-g_N C_N,
\]

where

\[
M_N=\sum_{d\mid D}|\lambda_d|d^{-\sigma_N},
\qquad
C_N=\sum_{m=2}^{N}b_t(m)(m^{k_N}-1)m^{y-\sigma_N}.
\]

**Native Triangle lemma.** If \(L_N>0\), then

\[
|f_t(x+iy)|\ge L_N
\]

throughout the window.  Thus a stored lower endpoint \(T_N\le L_N\) is
already in the same normalized units as the additive error in

\[
\frac{H_t}{B_t}=f_t+O_{\leq}(e_A+e_B+e_{C,0}).
\]

There is no additional Euler-factor conversion.

## Proof

Write the two sums in equation (14) of the paper as

\[
f_t=A+\gamma C_\kappa,
\]

\[
A=\sum_{m=1}^{N}b_t(m)m^{-s_*},\qquad
C_\kappa=\sum_{m=1}^{N}m^yb_t(m)m^{-\overline{s_*}-\kappa}.
\]

For the real-coefficient Euler mollifier

\[
E(s_*)=\prod_{p\in\mathcal P}(1-b_t(p)p^{-s_*})
      =\sum_{d\mid D}\lambda_d d^{-s_*},
\]

define

\[
B_{N,n}=\sum_{\substack{d\mid D,\ d\mid n\\n/d\le N}}
\lambda_d b_t(n/d),
\]

\[
A_{N,n}=\sum_{\substack{d\mid D,\ d\mid n\\n/d\le N}}
\lambda_d b_t(n/d)(n/d)^y.
\]

Exact Dirichlet convolution gives

\[
EA=\sum_{n=1}^{DN}B_{N,n}n^{-s_*},
\qquad
\overline E C_0=\sum_{n=1}^{DN}A_{N,n}n^{-\overline{s_*}},
\]

with \(B_{N,1}=A_{N,1}=1\).  The conjugate in the second identity is
essential; it is valid here because the coefficients \(\lambda_d\) are real
and \(|\overline E|=|E|\).

The triangle inequality and \(\Re s_*\ge\sigma_N\) imply

\[
|EA|\ge1-\sum_{n=2}^{DN}|B_{N,n}|n^{-\sigma_N},
\]

\[
|\overline E C_0|
\le1+\sum_{n=2}^{DN}|A_{N,n}|n^{-\sigma_N}.
\]

For complex \(\kappa\),

\[
|m^{-\kappa}-1|
=|e^{-\kappa\log m}-1|
\le e^{|\kappa|\log m}-1
\le m^{k_N}-1.
\]

Consequently,

\[
|\overline E(C_\kappa-C_0)|\le |E|C_N.
\]

Combining these inequalities gives

\[
|E|\,|f_t|\ge Q_N-g_N|E|C_N,
\]

where

\[
Q_N=1-g_N-\sum_{n=2}^{DN}
(|B_{N,n}|+g_N|A_{N,n}|)n^{-\sigma_N}.
\]

The mollifier triangle bound is

\[
|E|\le M_N.
\]

Every positive producer row has \(Q_N>0\), because
\(L_N=Q_N/M_N-g_NC_N>0\), \(M_N>0\), and \(g_NC_N\ge0\).
The preceding inequality also forces \(E\ne0\): if \(E=0\), its left
side and correction term vanish while \(Q_N>0\).  Division is therefore
legitimate, and the sign of \(Q_N\) gives

\[
|f_t|
\ge\frac{Q_N}{|E|}-g_NC_N
\ge\frac{Q_N}{M_N}-g_NC_N
=L_N.
\]

This proves the lemma.

## Correspondence with the producer

In `src/lemma_sweep_p235711.c`:

- `bt_eval` constructs \(b_t\);
- the `mtype` branches construct the real \(\lambda_d\);
- `bA0` constructs \(B_{N,n}\) and \(A_{N,n}\);
- `TRIANGLE_WEIGHT` constructs \(|B_{N,n}|+g_N|A_{N,n}|\);
- `modmoll` constructs \(M_N\);
- the naive and amortized correction paths enclose \(g_NC_N\); and
- the final four operations form \(Q_N/M_N-g_NC_N\).

`verifiers/verify_native_binding.py` checks this structural contract and
independently stress-tests both exact convolution identities and the final
inequality with complex phases and complex \(\kappa\).

## Error units

The candidate's direct verifier evaluates conservative effective-error
denominators directly:

- \(x-6.66\) in equation (23), for \(e_A+e_B\);
- \(x-12\) in the \(10.50\) corollary of Proposition 6.6(vi), for
  \(e_{C,0}\).

The inherited helper that substituted \(x-6.66\) into an \(e_{C,0}\) term is
not in the target verification path.  Neither is the displayed \(10.44\)
constant in equation (24); see `ERROR_CONSTANT_WELD.md`.

The sealed finite values give

\[
T_{\min}=0.000000791366,
\qquad
E_{\max}\le0.000000233494905213,
\]

and hence

\[
T_{\min}-E_{\max}
\ge0.000000557871094787>0.
\]
