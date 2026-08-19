# Certified Twistor–Phase Freeze Lane

**Status: certified research infrastructure and a certified negative pilot. No improved bound for the de Bruijn–Newman constant is claimed.**

The exact target is

\[
y_0=0.1809,
\qquad t_0=0.123637595,
\qquad t_0+y_0^2/2=0.14.
\]

The existing verified-height and closed-barrier evidence reduce this target to
a new final-time zero-free theorem. This package replaces the original
floating-point disk screen with a fail-closed FLINT/Arb audit.

## What is now certified

1. The target arithmetic is exact and its intermediate barrier is contained
   in the existing certified barrier interval.
2. The correct two-ladder center is
   \(1+\gamma M/\overline M\), not merely 1.
3. At `N=4050000`, with the current tail mollifier and endpoint-cap theorem,
   the directed lower endpoint of the residual majorant is strictly larger
   than the directed upper endpoint of the available center margin.
4. The failure is independent of floating-point sampling and cannot be
   repaired by increasing Arb precision.

## What is not certified

The program does not show that the phase-aware strategy fails. It shows that
the existing absolute endpoint caps still discard too much phase even after
the reflected constant term is moved into the center. The missing theorem is
an explicit, uniform bound for the residual logarithmic exponential sums that
retains mollifier cancellation.

## Run in the repository's pinned FLINT environment

```sh
research/twistor_phase_freeze/certified/scripts/run_certified_pilot.sh \
  replay/twistor-phase-certified
```

The runner compiles at strict C17 warnings, executes independently at 256 and
512 bits, verifies exact markers and directed-ball output, and rejects any run
below 256 bits.
