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
  dynamic_boundary.test_dynamic_boundary_research
python3 -B -m dynamic_boundary geometry
python3 -B -m dynamic_boundary landing 691008
python3 -B -m dynamic_boundary rank \
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
  research/dynamic_boundary/run_static_reanchor_pilot.sh \
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

## Anchor-quality finding (2026-07-31)

The conservative height-budget endpoint \(X_*=6\,000\,342\,141\,913\) is
**not** a viable barrier site: the closed-slab program fails at the first
prism with no positive certified time-motion budget.  This is expected in
hindsight — the sealed anchor \(6\,000\,000\,185\,827\) was *selected* for
barrier quality, not chosen arbitrarily.  Height budget alone does not
select a wall location; an anchor-quality search inside the
\(8\,523\,687\)-integer slack must precede the pilot.

A three-point probe across the slack range found:

| anchor | first-prism budget | outcome |
|---|---|---|
| \(6\,000\,342\,141\,913\) (\(X_*\)) | none | FAIL |
| \(6\,000\,343\,000\,000\) | none | FAIL |
| \(6\,000\,345\,678\,901\) | positive | **CLOSED SLAB CERTIFIED** |
| \(6\,000\,348\,141\,913\) | positive | 790+ prisms passing (stopped; redundant) |

At \(X=6\,000\,345\,678\,901\) (window \(N=691008\) at both corners) the
full closed slab certified over \(t\in[0,0.16125]\) with 3,709 consecutive
passing prisms in about 26 minutes of wall time, and the strict transcript
validator accepts the run
(`validate_barrier_transcript.py --expected-n 691008`).  See
`RESULTS_static_reanchor_691008.md` for the run record.  This smoke pass
shows the stronger window is numerically viable; the new-site Taylor-tail,
uniform-error, proof-to-code, and theorem-assembly obligations remain
outstanding, so no improved Lambda bound is certified.

## Parameterized site checkers (2026-07-31)

`src/uniform_error_site.c` and `src/storedsum_taylor_tail_site.c` are
research-lane derivatives of the two pinned checkers
(`barrier/src/verify_uniform_error_01787854.c`,
`barrier/src/StoredSumTaylorTail_cert.c`); the only change is that \(X\)
and \(N\) are command-line arguments, plus an unmistakable SITE/RESEARCH
banner.  Regression at the sealed site reproduces the sealed outputs
ball-for-ball.  At the new site \(X=6\,000\,345\,678\,901\), \(N=691008\):
the uniform conservative error total is \(0.000356517 < 0.00125\) and the
Taylor truncation is \(1.9546\times10^{-22} < 10^{-20}\) — both certified.
Outstanding before any promotion: independent proof-to-code audit of the
two derivatives and a separate theorem assembly.

## t0 sensitivity (2026-07-31)

Measured with the sealed sweep parameters at \(N=691008\): the certified
finite row is linear in \(t\) with slope \(19.05\), so the entire
stronger-window reserve \(8.24\times10^{-6}\) converts to
\(\Delta t_0\approx4.3\times10^{-7}\), i.e.
\(\Delta\Lambda\approx4\times10^{-7}\) at fixed \(y_0^2\) and fixed
mollifier.  The proof's \(t_0=129/800\) sits within \(\sim5\times10^{-7}\)
of the smallest certifiable \(t_0\).  See
`RESULTS_t0_sensitivity.md`.  Material reductions require restructuring
(mollifier retuning at lower \(t_0\), larger windows, or a different
barrier/window trade), for which the stronger window is a prerequisite
rather than the payoff; step 3 below is accordingly demoted from
"directly lowers the objective" to "bounded by \(\sim4\times10^{-7}\)
without restructuring".

## Route toward a smaller bound

1. Establish the fixed \(N=691008\) barrier pilot at the current row —
   **done 2026-07-31** at anchor \(6\,000\,345\,678\,901\) (smoke only; see
   above), after an anchor-quality search sub-step that the original list
   omitted.
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
