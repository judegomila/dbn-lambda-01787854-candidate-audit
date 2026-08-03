# Run record: t0 sensitivity of the finite lane at N = 691008

STATUS: UNSEALED RESEARCH ONLY; no improved Lambda bound certified.

Date: 2026-07-31.  Toolchain: FLINT/Arb 3.6.0 (Homebrew), Apple clang 21.
Producer: `src/lemma_sweep_p235711.c` compiled with `-DTRIANGLE_WEIGHT`,
invoked with the sealed full-sweep parameters
(`N N t_num t_num t_den 350708 10000000 6 220 14 0.005 t`).

## Measured rows at N = 691008 (fresh, this toolchain)

| t | certified L12 lower bound |
|---|---|
| 0.161300 | 0.000961204939 |
| 0.161270 | 0.000390138541 |
| 0.161260 | 0.000199657054 |
| 0.161255 | 0.000104392668 |
| 0.161252 | 0.000047226469 |
| 0.161250 (= 129/800) | 0.000009112516 |
| 0.161249 and every value tried below | UNCERT |

(The sealed-toolchain stored row at 129/800 is 0.000008478389; the fresh
FLINT 3.6 value is slightly higher, the usual favorable cross-toolchain
difference.  The sealed value is used for all margin arithmetic below.)

## Finding: the finite-lane slope in t0 is ~19

The certified lower bound is linear in t over this whole range with

    dT/dt0 = 19.05 +/- 0.02   (per unit t)

and extrapolates to zero 4.8e-7 below 129/800, exactly matching the
observed certification collapse between t = 0.161249 and 0.161250.
The proof's t0 = 129/800 sits within ~5e-7 of the smallest t0 this
machinery can certify at all — the construction is razor-tuned in t.

E_max moves much more slowly: rerunning the Proposition 4.10 error
budget at N0 = 691008 with T0 varied gives dE_max/dt0 ≈ -1.1e-5
(E_max grows as t0 falls) — negligible against 19.05.

## Consequence: what the N=691008 reserve buys

Using sealed stored values, the new-site finite reserve is

    T_min - E_max = 0.000008478389 - 0.000000233484 = 8.2449e-6.

Dividing by the measured slope:

    max Delta-t0 ≈ 8.2449e-6 / 19.05 ≈ 4.3e-7.

Since Lambda_bound = t0 + y0^2/2 with y0^2 fixed, the entire stronger-
window reserve converts to a Lambda reduction of about

    Delta-Lambda ≈ 4e-7,   i.e.  0.1787854 -> ~0.1787850,

versus ~2.9e-8 available at the current anchor (5.578e-7 / 19.05).
The re-anchor multiplies the achievable step by ~15, but the absolute
step is small because the slope is steep.  Even the theoretical
steering frontier at N = 691439 (reserve ~1.735e-4, tail-limited)
would cap out near Delta-t0 ≈ 9e-6.

Conclusion: marginal t0 screening at fixed y0^2 and fixed mollifier
cannot lower the bound materially.  A material reduction requires
restructuring — a stronger mollifier lane retuned at lower t0, larger
windows, or a different barrier/window trade — for which the stronger
window's reserve is a prerequisite, not the payoff.

## Reproduce

```sh
bash -c 'source scripts/flint_flags.sh && flint_resolve_flags && \
  "${FLINT_CC[@]}" -O3 -std=c17 -Wall -Wextra -Werror -pedantic \
  "${FLINT_CPPFLAGS[@]}" -DTRIANGLE_WEIGHT src/lemma_sweep_p235711.c \
  "${FLINT_LDFLAGS[@]}" -o /tmp/triangle_producer "${FLINT_LIBS[@]}"'
/tmp/triangle_producer 691008 691008 161252 161252 1000000 \
  350708 10000000 6 220 14 0.005 t
```

Nothing in this record is evidence for, or modifies, the sealed
`0.1787854` candidate.
