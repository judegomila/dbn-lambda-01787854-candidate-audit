# Moving real-rung barrier program

Status: exploratory conditional lemma and research program. This document is
not used by the `0.1782354` assembly and proves no improvement by itself.

## Purpose

The finite P13 construction strengthens the final-time zero-free strip but
does not change de Bruijn's contraction law

\[
\Lambda\leq T+\frac{y_0^2}{2}.
\]

A genuinely Twin-Ladder-like improvement would retain certified real zeros
as moving rungs during the heat flow and use their repulsion against a
topmost nonreal zero. The rungs cannot be frozen at their original locations:
their trajectories must either be followed or enclosed in certified tubes.

## Heat-compatible coordinates

With Newman time denoted by \(\tau\),

\[
H_\tau(z)=\int_0^\infty e^{\tau u^2}\Phi(u)\cos(zu)\,du,
\qquad
(\partial_\tau+\partial_z^2)H_\tau=0.
\]

Equivalently, for \(X_\tau(w)=8H_\tau(-2iw)\),

\[
\partial_\tau X_\tau=\frac14\partial_w^2X_\tau,
\qquad
\Psi_\tau(v)=e^{\tau v^2/4}\Psi(v).
\]

This is the compatible way to transport a Twin Ladder carrier through
Newman time.

## Conditional real-rung velocity lemma

Assume that on \(T\leq\tau\leq T+S\):

1. every zero of \(H_\tau\) lies in the symmetric strip
   \(|\operatorname{Im}z|\leq Y(\tau)\);
2. the boundary zero under consideration is simple, or the corresponding
   collision-limiting argument has been supplied;
3. the zero-dynamics expansion is justified with its complete tail; and
4. a certified collection of real zeros \(r\), counted with multiplicity,
   satisfies the uniform Poisson lower bound

   \[
   P_\tau(x,Y):=
   \sum_{r\in\mathbb R:H_\tau(r)=0}
   m_r\frac{Y}{(x-r)^2+Y^2}\geq p(\tau,Y)
   \]

   for every real \(x\) relevant to a first boundary contact.

For a boundary zero \(z=x+iY\), its conjugate contributes \(-1/Y\) to the
imaginary velocity. Each real zero contributes

\[
-\frac{2Y}{(x-r)^2+Y^2},
\]

and zeros already below the top boundary contribute nonpositively. Hence

\[
Y'\leq-\frac1Y-2P_\tau(x,Y)
\leq-\frac1Y-2p(\tau,Y).
\]

Writing \(u=Y^2\) gives

\[
u'\leq-2-4Yp(\tau,Y),
\qquad
\frac{d}{d\tau}\left(\tau+\frac{u}{2}\right)
\leq-2Yp(\tau,Y).
\]

Thus any strictly positive uniform rung contribution makes the standard
de Bruijn conserved quantity strictly decrease.

## Maximum-gap corollary

Suppose, more concretely, that at every relevant \((\tau,x)\) there is a
real zero within distance \(R\). Then

\[
P_\tau(x,Y)\geq\frac{Y}{R^2+Y^2},
\]

so comparison with

\[
u'=-2-\frac{4u}{R^2+u}
\]

gives the collapse time

\[
S_R=
\frac{u_0}{6}
+\frac{R^2}{9}\log\left(1+\frac{3u_0}{R^2}\right),
\qquad u_0=y_0^2.
\]

Conditionally,

\[
\Lambda\leq T+S_R<T+\frac{y_0^2}{2}.
\]

For the present \(T=1607/10000\) and
\(u_0=87677/2500000\), values such as \(R=1\) are useful only as scale
illustrations; they are not certified maximum-gap inputs.

## Why literal freezing is invalid

If \(H_\tau=A_\tau+B_\tau\) and one substitutes
\(A_{\tau_*}+B_\tau\), then

\[
(\partial_\tau+\partial_z^2)(A_{\tau_*}+B_\tau)
=\partial_z^2A_{\tau_*}.
\]

Except for an affine component, the frozen comparator no longer follows the
Newman equation. A fixed zero factor similarly ceases to divide the evolved
function when its zeros move. Literal freezing is therefore valid only as a
Rouche/Duhamel comparator with an explicit residual bound.

## Missing certificate

A proof-grade moving-rung improvement requires all of the following:

- a real-zero mesh or direct Poisson lower bound uniform in every real \(x\);
- uniformity throughout the complete collapse-time interval;
- proof that the selected zeros remain real;
- certified trajectory tubes, rather than fixed \(H_0\) anchors;
- a treatment of the central gap and all zero collisions; and
- an infinite-height tail bound for the zero-dynamics sum.

Average Riemann--von Mangoldt density is insufficient: the barrier needs a
uniform maximum-gap or Poisson-floor certificate. Until those items exist,
the moving-rung program must remain logically separate from the verified
P13/Polymath lane.
