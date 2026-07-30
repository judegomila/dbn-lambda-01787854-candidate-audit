# Closed barrier certificate

## Statement

Let

\[
X=6000000185827,\qquad t_0=\frac{129}{800},\qquad
R=[X,X+1]+i\left[\frac{1809}{10000},1\right].
\]

The certificate proves that

\[
H_t(z)\ne0\qquad
(z\in R,\;0\le t\le t_0).
\]

This is the rectangular superset needed for the curved barrier in
Polymath Theorem 1.2.  If

\[
y_0^2=\frac{87677}{2500000},
\]

then

\[
y_0^2-\left(\frac{1809}{10000}\right)^2
=\frac{234599}{100000000}>0,
\]

the required horizontal width is
\(\sqrt{1-y_0^2}<1\), and

\[
0<y_0^2+2(t_0-t)\le y_0^2+2t_0<1.
\]

Thus every point on the theorem's curved intermediate-time barrier lies
inside the certified closed rectangle.

## Effective approximation, including \(t=0\)

Write

\[
g_t(z)=\frac{H_t(z)}{B_t(z)}.
\]

Polymath Theorem 1.3 gives, for \(0<t\le1/2\),

\[
|g_t(z)-f_t(z)|\le e_A+e_B+e_{C,0}.
\]

`barrier/src/verify_uniform_error_01787854.c` independently evaluates
bounds (20)--(23) and the conservative \(10.50\) corollary of Proposition
6.6(vi) proved in `ERROR_CONSTANT_WELD.md`, with Arb on the complete box

\[
x\in[X,X+1],\quad y\in[0.1809,1],\quad t\in[0,t_0].
\]

It first proves that

\[
N=\left\lfloor\sqrt{\frac{x}{4\pi}+\frac t{16}}\right\rfloor=690988
\]

throughout the box and that \(N^2<x/(4\pi)\).  The latter inequality both
fixes the sign of the heat exponent and justifies

\[
|\gamma|n^y
\le e^{0.02y}\left(\frac{n^2}{x/(4\pi)}\right)^{y/2}
\le e^{0.02}
\qquad(1\le n\le N).
\]

The primary 256-bit Arb result is

\[
\begin{aligned}
e_A+e_B&<
3.639278679550541\times10^{-10},\\
e_{C,0}&<
0.000356522647672172,\\
e_A+e_B+e_{C,0}&<
0.000356523011600040<0.00125.
\end{aligned}
\]

The Python barrier verifier contains a separate, deliberately coarser
interval transcription; it obtains a total below \(0.000356942\).  Both
paths use \(x-6.66\) for \(e_A+e_B\) and \(x-12,\ 10.50\) for \(e_{C,0}\).
Neither consumes the displayed \(10.44\) in equation (24).

The paper states Theorem 1.3 for positive \(t\).  Its use at the closed
endpoint \(t=0\) follows as a limit, as follows.

1. On the fixed compact set \(R\),
   \[
   |e^{tu^2}\Phi(u)\cos(zu)|
   \le e^{t_0u^2+u}|\Phi(u)|.
   \]
   The super-exponential decay of \(\Phi\) makes the right side integrable.
   Dominated convergence therefore makes \(H_t(z)\) jointly continuous down
   to \(t=0\).
2. The paper defines
   \[
   M_t(s)=\exp\!\left(\frac t4\alpha(s)^2\right)M_0(s),
   \qquad
   B_t(x+iy)=M_t\!\left(\frac{1+y-ix}{2}\right).
   \]
   On this compact set the argument stays away from the branch cut,
   \(M_0\) is nonzero, and the exponential is never zero.  Hence \(B_t\)
   and \(1/B_t\) are continuous and \(B_t\ne0\).
3. Because the window index is constant, \(f_t\) is a fixed finite sum of
   continuous explicit functions on the closed box.
4. The conservative error majorant is continuous there: all denominators are
   strictly positive and the positive-part map is continuous.

For fixed \(z\in R\), apply Theorem 1.3 to any sequence \(t_j\downarrow0\)
and pass to the limit.  This gives the same inequality at \(t=0\), uniformly
with the certified \(0.00125\) allowance.  No large-\(x\), \(t\to0\)
interchange is used.

## Uniform derivative majorants

`DERIVATIVE_BOX_LEMMA.md` supplies the theorem behind the \(D_z\) and
\(D_t\) values used below. It separates increasing and decreasing
\(x,y\)-factors from the pointwise bounds in Polymath Lemma 8.4, proves
the required core monotonicities with fail-closed Arb gates, and therefore
turns them into bounds on the complete spatial box.

It also closes two numerical-analysis interfaces. Each discrete
Lemma 8.4 sum is evaluated as an exact 16-term Arb head plus the integral
of a rigorously decreasing tail. The quadrature callbacks preserve the
complete complex integration variable and use FLINT's analytic logarithm
and power operations; no projection to the real part enters a holomorphic
quadrature bound.

## One closed-prism gate

At an exact time seam \(t_i\), the C verifier encloses \(f_{t_i}\) at every
point of a cyclic boundary mesh.  Let \(M_i\) be the minimum lower modulus
of those enclosures.  If each edge has `num` points, its step is at most
\(1/(\texttt{num}-1)\).  Let \(D_{z,i}\) enclose the spatial derivative on
the boundary and let \(D_{t,i}\) enclose the time derivative on the complete
closed prism \(R\times[t_i,t_{i+1}]\).

The accepted-prism predicate is the strict interval inequality

\[
M_i>
\frac{D_{z,i}}{2(\texttt{num}-1)}
+D_{t,i}(t_{i+1}-t_i)+0.00125.
\tag{1}
\]

Every overlap or indeterminate comparison is failure.  The factor \(1/2\)
is rigorous in the required zero-avoiding homotopy, not merely as a
pointwise interpolation estimate. Let a mesh subedge have length at most
\(h\), let \(F(s)\) be its true \(f_{t_i}\)-image, and let \(P(s)\) be
the chord between its endpoint values. For \(0\le s\le1/2\), both
\(F(s)\) and \(P(s)\) lie in the closed disk of radius \(D_zh/2\) about
\(F(0)\); for \(1/2\le s\le1\), both lie in the corresponding disk about
\(F(1)\). Indeed,

\[
|F(s)-F(0)|,\ |P(s)-F(0)|\le sD_zh
\quad(0\le s\le1/2),
\]

with the symmetric estimate from \(F(1)\) on the second half. Each disk
is convex, so the straight-line homotopy from the true subedge to its
chord stays in that same disk.

At time \(\tau\in[t_i,t_{i+1}]\), time motion adds at most
\(D_t(\tau-t_i)\), and passage from \(f_\tau\) to \(H_\tau/B_\tau\)
adds at most \(0.00125\). Predicate (1) says that every resulting disk,
centered at the nearer stored mesh value, excludes zero strictly.
Consequently the complete spatial, time, and approximation homotopy is
zero-avoiding.

The code first proposes a dyadic next seam, then interval-evaluates \(D_t\)
again on the whole proposed prism, rounds its directed upper endpoint to an
exact integer, and rechecks (1).  It does not assume monotonicity of a
left-endpoint derivative estimate.

For each boundary polygon it also requires that:

- every endpoint enclosure excludes zero;
- every complete argument increment lies strictly inside \((-\pi,\pi)\);
- the complete winding enclosure lies strictly inside \((-1/4,1/4)\).

The C source accumulates
\(\arg(f(z_j)/f(z_{j+1}))\), the reverse of the forward orientation
\(\arg(f(z_{j+1})/f(z_j))\) used in some expositions. This negates the
winding orientation but leaves both the strict increment gate and the
load-bearing conclusion, winding number zero, unchanged.

The polygon winding is an integer and is therefore exactly zero.  The
spatial interpolation, time-motion, and approximation bounds give a
zero-avoiding homotopy from that polygon to \(g_t(\partial R)\).  Since
\(B_t\) is nonzero, \(g_t\) and \(H_t\) have the same zeros.  The argument
principle therefore gives zero \(H_t\)-zeros in the rectangle throughout
the prism.

## Stored coefficients and omitted Taylor terms

The archived \(62\times62\) complex coefficient matrix was printed to 20
decimal digits.  The verifier does not treat those decimals as exact:
it adds to each real and imaginary component the radius

\[
10^{-20}\max(1,|\text{component}|).
\]

The archived data file contains exactly its header and 62 matrix rows. A
non-mathematical FLINT profiler footer from the preparation host was
omitted; neither the barrier reader nor the provenance comparison consumes
timing output.

`StoredSumSinglemat_interval.c` independently regenerates all 7,688 real
components as Arb balls.  All 7,688 regenerated balls fit inside those
restored radii; there are zero containment failures.  The largest
regenerated-radius/use-of-allowance ratio is below \(0.018\).

`StoredSumTaylorTail_cert.c` separately bounds the omitted rectangular
Taylor tail at

\[
1.954234593244762\times10^{-22}<10^{-20}.
\]

That \(10^{-20}\) truncation radius is added to every complex value used by
the barrier program.

## Recorded result

The sealed run has:

- 883 consecutive closed time prisms;
- byte-identical adjacent seam serializations;
- first time exactly \(0\);
- final endpoint enclosing \(129/800\);
- aggregate winding interval \([ -8.95,8.95]\times10^{-13}\);
- independently recomputed lower bound for the minimum prism margin
  \[
  0.519849894613872543374989997>0;
  \]
- terminal `RESULT: CLOSED SLAB CERTIFIED`.

The dyadic stepping code deliberately permits the right endpoint of the last
stored prism to enclose a value at least as large as the exact
\(t_0=129/800\).  The theorem uses only that prism intersected with
\([0,t_0]\).  Restricting a certified closed prism cannot increase its
spatial or time displacement allowances, and the uniform approximation
bound is invoked only through the exact \(t_0\).  Thus the recorded cover
certifies the closed interval \([0,t_0]\) without assuming an approximation
estimate beyond \(t_0\).

`verifiers/verify_barrier_binding.py` parses every prism, independently
recomputes (1) from the printed directed endpoints, checks the mesh formula
and derivative products, rejects malformed or extra records, and checks the
coefficient, Taylor, and uniform-error artifacts.  All sources and evidence
are bound by the repository's `SHA256SUMS`.

Two complete 883-prism transcripts from the same sealed source are retained
and parsed by the top-level assembly:

- the canonical portable Linux/GCC/FLINT 3.0.1 transcript,
  `barrier_target_closed.log`, SHA-256
  `2d010f70902dca1627f40ddcd68f3954b37fd9596f7840787415eeafb20805f4`;
- an independent macOS/Clang/FLINT 3.6.0 corroborating transcript,
  `barrier_target_closed_macos_arm64_flint36.log`, SHA-256
  `34f8ed82bcb47a3783099206f67599cf975b7d28cfa398d8a765118311954db7`.

Both pass all 54 strict parser checks, cover all 883 prisms, and certify the
same zero winding.  The displayed lower bound above is the smaller common
cross-toolchain margin.  The macOS transcript's final `cpu` profiler field is
a known non-mathematical platform artifact; the parser ignores both timing
fields, while its sane wall time is retained for transparency.

For a complete fresh replay, including coefficient regeneration and all
883 prisms, run inside the review container:

```sh
./scripts/run_barrier_replay.sh replay/barrier
```

The historical vendored winding logs are retained only for provenance.
They are not consumed by this proof.
