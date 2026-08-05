# Negative result: the P13 margin is not walkable headroom

**STATUS: UNSEALED RESEARCH ONLY; no improved Lambda bound certified.**

Date: 2026-08-04. Recorded so this experiment is not repeated.

## The question

The `0.1782354` lane's binding margin is `4.4457e-4`, about **797 times**
the sealed lane's `5.5787e-7`. Since `Lambda <= t0 + y0^2/2`, every `0.001`
taken off `t0` comes straight off the bound. A margin that large invites the
obvious question: how much further does `t0` go?

## Method

The binding row was probed directly, in the pinned review container
(`dbn-lambda-01787854-review`, `linux/amd64`, base digest
`sha256:52df9b1e…`), using the lane's own producer
`src/lemma_sweep_p23571113.c` compiled with the lane's own flags
(`-O3 -std=c17 -Wall -Wextra -Werror -pedantic -DTRIANGLE_WEIGHT`).

Invocation, varying only `t0` and the precision triple:

```
triangle 690988 690988 <t0> <t0> 100000 350708 10000000 7 <prec> <K> <hw> t
```

## Result

```
t0=0.16070  prec=220 K=14 hw=0.005     L12 = 0.000670513304   certified
t0=0.16000  prec=220 K=14 hw=0.005     UNCERT
t0=0.15900  prec=220 K=14 hw=0.005     UNCERT
t0=0.15800  prec=220 K=14 hw=0.005     UNCERT
t0=0.15600  prec=220 K=14 hw=0.005     UNCERT
t0=0.15400  prec=220 K=14 hw=0.005     UNCERT
t0=0.15000  prec=220 K=14 hw=0.005     UNCERT
t0=0.14500  prec=220 K=14 hw=0.005     UNCERT
t0=0.14000  prec=220 K=14 hw=0.005     UNCERT
```

Precision was then escalated to test whether `UNCERT` was a tuning artifact:

```
t0=0.16000  prec=240 K=16 hw=0.00025   UNCERT
t0=0.16000  prec=320 K=20 hw=0.00025   UNCERT
t0=0.15800  prec=320 K=20 hw=0.00025   UNCERT
t0=0.15000  prec=320 K=20 hw=0.00025   UNCERT
t0=0.14000  prec=400 K=24 hw=0.0001    UNCERT
```

Precision from 220 to 400 bits, Taylor order 14 to 24, half-width narrowed
fiftyfold: no effect.

## Interpretation

**The wall is structural, not numerical.** If the enclosure were merely too
loose, more precision would resolve it; it does not.

The shape reinforces this. `L12` is `6.7e-4` at `t0=0.16070` and undecidable
at `0.16000` — a cliff across `0.0007`, not a margin thinning gradually.
Continuous quantities do not behave that way; a discrete precondition
failing does.

The explanation consistent with both observations is that **the mollifier is
tuned to `t0`**. `mtype 7` is not a generic P13 kernel: its coefficients are
built for `t0 = 1607/10000`, so lowering `t0` while holding it fixed violates
a condition the certification requires, and precision cannot recover a
condition that is not satisfied.

This is exactly the conclusion `research/dynamic_boundary/` reached from a
different direction — that progress needs *"a stronger mollifier lane
**retuned** at lower `t0`"*. Two independent lines now agree, and the
emphasis belongs on "retuned".

### Consequence for the lane

The 797-fold margin at `t0=0.16070` is **specific to that `t0` with that
mollifier**. It is not slack that can be spent by lowering `t0`. Going below
`0.1782354` requires designing a new mollifier, not adjusting a parameter.

That makes `0.1782354` a defensible target to commit to, rather than an
interim value to improve on cheaply — which matters, because changing the
certified bound touches 60 files, the release tag and the repository name,
and is worth paying once.

## What this does not establish

- `UNCERT` means **undecided**, not false. This is not evidence that the
  bound fails at lower `t0`; only that this machinery cannot establish it.
- One row was probed. `N = 690988` is the sealed lane's binding row, but it
  is **not** this lane's: its `L12` here is `6.7e-4` against a lane
  `T_floor` of `4.4e-4`, so the minimum lies elsewhere. A complete picture
  needs a range of `N`.
- One mollifier type was probed. Nothing here bounds what a retuned kernel,
  a different `y0^2`, or a wider window schedule could achieve.

## If this is pursued

The experiment worth running is two-dimensional and belongs in a compute
job, not an ad hoc probe: `t0` against mollifier design, over a range of `N`
rather than a single row, with `y0^2` allowed to move. Screening `t0` alone
at a fixed kernel has now been shown not to work — twice, by two different
routes.
