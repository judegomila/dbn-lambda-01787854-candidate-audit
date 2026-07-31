# Dynamic-boundary and stronger-window research lane

## Status

This directory is deliberately under `dan-reworking/`, which the repository
seal excludes.  Nothing here is consumed by `verify.sh`, and no output from
these programs is evidence for the sealed `0.1787854` candidate.

The research calculations and certificate-path manifest were audited against
repository commit `16148718742023ebf16598a3e598d7d97b08914d`.

The principal finding is that **dynamic steering is not the first experiment
to run**.  The published Platt--Trudgian verified height permits

\[
X'\le 2T_{\rm PT}=6\,000\,350\,665\,600.
\]

The current anchor is only

\[
X=6\,000\,000\,185\,827.
\]

At \(t_0=129/800\), the unused verified-height budget reaches
Riemann--Siegel window \(N=691008\), while \(N=691009\) lies beyond it.
A conservative integer endpoint for the height-dependent terminal splice is

\[
X_*=6\,000\,342\,141\,913.
\]

The complete stored finite suffix starting at \(N=691008\) has floor

\[
T_{\min}=0.000008478389,
\]

so the current effective error gives

\[
T_{\min}-E_{\max}
=0.000008244894094787662151.
\]

This is about \(14.78\) times the present finite binding margin.  At the
unchanged \((t_0,y_0)\), the stored later finite rows and Arb tail can be
reused; the new obligations are:

1. an exact suffix/start-window verifier;
2. a new static barrier at \(X_*\);
3. a new-site stored-sum Taylor-tail/truncation certificate;
4. a generalized uniform-error check at that site; and
5. a separate theorem assembly.

For any genuinely smaller \(t_0+y_0^2/2\), all parameter-dependent finite,
Dini, freeze, tail, and barrier evidence must be regenerated.

## Why long-range steering is secondary

The moving collar has the exact parameterization

\[
\Phi(t,r,s)=a(t)+Wrs
+i\sqrt{y_0^2+2(t_0-t)+W^2r^2},
\qquad
W^2=1-y_0^2-2t_0.
\]

Its time derivative contains

\[
\Phi_t=a'(t)-\frac{i}{y}.
\]

Therefore a moving-prism gate must pay a term comparable to

\[
D_z\left(|a'|+\frac1{y_{\min}}\right)\Delta t.
\]

Skipping only the first weak window from the current \(X\) requires about
\(1.2\times10^7\) horizontal units and average speed above
\(7.4\times10^7\).  Moreover, downward velocity at the bottom boundary does
not protect an expanding lateral wall: a boundary zero would also need

\[
\Re(H_t''/H_t')>a'(t).
\]

Using that lateral velocity inequality as a valve requires new enclosures of
\(H_t'\) and \(H_t''\); the current derivative majorants do not supply them.
A direct nonvanishing certificate for the entire moving collar can instead
continue to use value enclosures and \(D_z,D_t\), but it must pay the
\(D_z|a'|\) motion term above.

The stored current-row data also identify the farthest useful finite target.
For the suffix starting at \(N=691439\),

\[
L_{\mathrm{suffix}}=0.000173764764,\qquad
L_{\mathrm{suffix}}-E_{\max}
=0.000173531269094787\ldots,
\]

which just exceeds the stored tail margin
\(0.0001735209373337\).  Beyond this point the tail, rather than the finite
lane, becomes the bottleneck.  Reaching it would require a terminal site near
\(6.007830\times10^{12}\) (the integer anchor is
\(6\,007\,829\,621\,038\)), roughly \(7.8\times10^9\) units right of the
current anchor, so it is a theoretical steering frontier rather than the
recommended first computation.

## Run the exact research checks

From the repository root:

```sh
cd dan-reworking/code
python3 -B -m unittest -v \
  dynamic_boundary_research.test_dynamic_boundary_research
python3 -B -m dynamic_boundary_research geometry
python3 -B -m dynamic_boundary_research landing 691008
python3 -B -m dynamic_boundary_research rank \
  --first 690988 --last 691020
```

The `rank` command parses all 3,149,013 stored rows, computes genuine suffix
minima, applies the existing effective-error upper bound, and compares the
finite result with the stored tail margin.

Every command prints:

```text
STATUS: UNSEALED RESEARCH ONLY; no improved Lambda bound certified.
```

## Run the static re-anchor pilot

The pilot compiles the existing FLINT/Arb stored-sum and barrier producers,
regenerates the matrix at \(X_*\), and runs the existing closed-slab program:

```sh
ACKNOWLEDGE_UNPROVED_NEW_SITE_TAIL=1 \
  dan-reworking/code/dynamic_boundary_research/run_static_reanchor_pilot.sh \
  replay/static-reanchor-691008
```

The output directory must not already exist.  The transcript smoke parser requires
the requested Riemann--Siegel index at both slab corners, consecutive passing
prisms, and the C program's terminal success marker.

This is only a **transcript smoke pilot**.  The barrier program internally
allows a \(10^{-20}\) stored-sum Taylor truncation error, but the repository's
`StoredSumTaylorTail_cert.c` is pinned to the old \(X,N\).  The pilot therefore
refuses to run unless the explicit acknowledgement variable above is set, and
does not run the old Taylor-tail checker.

It also intentionally does **not** call the sealed
`verify_uniform_error_01787854.c` or `verify_barrier_binding.py`: both pin the
old \(X\), \(N\), filenames, and transcript shape.  Reusing any of these
checkers would create a false proof signal.  A smoke pass is useful for
measuring whether the new site is numerically viable, but the next
implementation step is to parameterize and independently audit the
Taylor-tail, uniform-error, and barrier-binding checks before anything is
moved into the sealed proof surface.

## Route toward a smaller bound

1. Establish the fixed \(N=691008\) barrier pilot at the current row.
2. Generalize the uniform-error and suffix/window welds.
3. Hold \(y_0^2\) fixed and screen rational \(t_0<129/800\).  This directly
   lowers the objective while keeping the final bottom height fixed.
4. For promising rows, regenerate selected singleton finite rows, Dini and
   freeze gates, and the 256/512-bit tail before spending on a full sweep.
5. Run the complete finite sweep only for the best surviving rational row.
6. Explore \(N>691008\) with a moving wall only if the fixed-anchor reserve
   remains the limiting factor.

The stronger window supplies numerical reserve; it does not itself lower
\(\Lambda\).
