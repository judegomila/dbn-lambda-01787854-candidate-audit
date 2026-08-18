# Twistor / phase-freeze research lane

**Status: unsealed research only. Nothing in this directory certifies a new de Bruijn--Newman bound, and nothing here is consumed by the repository's sealed verification.**

## Objective

The current finite certificates replace a complex, highly correlated Riemann--Siegel sum by absolute-value majorants. This lane tests whether retaining some of the phase geometry can cross the lower-time wall of the triangle certificate.

The first rows deliberately keep

\[
y_0^2=\frac{87677}{2500000}=0.0350708.
\]

That choice keeps the already-certified closed rectangular barrier available at every smaller time. The target objective values are therefore

| final time \(t_0\) | \(t_0+y_0^2/2\) |
|---:|---:|
| 0.130 | 0.1475354 |
| 0.125 | 0.1425354 |
| 0.120 | 0.1375354 |

Closing any row still requires a complete final-time finite lane, the infinite tail, all approximation-error transfers, and theorem assembly. The barrier alone is not enough.

## Phase interpretation

For the Polymath finite approximant, every Dirichlet phase has the form

\[
e^{iq\log n}=\prod_p\left(e^{iq\log p}\right)^{v_p(n)}.
\]

Thus the apparent collection of independent oscillators is the restriction of a Laurent system in prime-phase coordinates. The quaternionic/twistor language packages the projective phase and its first two jets, but the actual certificate must remain an ordinary rigorous inequality. This lane tests two increasingly strong relaxations:

1. the source's existing sharp two-channel L-type functional, compiled without `TRIANGLE_WEIGHT`; and
2. a future physical-orbit interval certificate for the mollified complex sum and the radial jet of \(|Ef_t|^2\).

The full prime torus is a conservative closure of the physical orbit; it must not be confused with an automatic one-dimensional global minimization.

## Direct diagnostic

`screen_direct_ft.py` evaluates the exact finite approximant from the Polymath formula, its Euler mollifier, and optionally the first two spatial jets. It uses NumPy/IEEE double precision and finite sampling, so its output is diagnostic only.

```sh
python3 research/twistor_phase_freeze/screen_direct_ft.py \
  --t 0.13,0.125,0.12 \
  --n 690988,850000,1075000,2000000,4050000 \
  --fractions 0,0.25,0.5,0.75,0.999 \
  --output replay/twistor-direct-screen
```

Add `--jets` for the slower first- and second-derivative calculation.

## Arb sharp-functional probe

The workflow `twistor-phase-freeze-pilot.yml` builds the repository's pinned review container and compiles the lower-time producer **without** `-DTRIANGLE_WEIGHT`. It then evaluates exact singleton rows for the three target times. The run is deliberately fail-open with respect to `UNCERT`: an undecided row is a research result, not a CI failure. Arithmetic or tool failures still fail the job.

The sharp functional is not yet a promoted proof interface. In particular, its transfer to the full final-height interval and its relationship to the standard-window theorem obligations require a separate proof-to-code audit.

## Known correction to the earlier assessment

`research/lower_time_01782354/RESULTS_p13_t0_ceiling.md` attributed the failure below `t0=0.1607` to a P13 kernel held fixed at that time. The producer does not do that: `bt_eval` recomputes every Euler coefficient from the supplied `t` ball. The observed `UNCERT` wall is therefore a failure of the selected absolute-value certificate, not evidence that a fixed kernel was used.
