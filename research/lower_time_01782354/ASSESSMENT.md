# Assessment of the 0.1782354 lower-time extension

**Status: unsealed research. This repository certifies
`Lambda <= 893927/5000000 = 0.1787854` and nothing here changes that.**

Imported from the orphan branch `codex/extension-work-01782354`
(head `3962701`, rooted at `8ba1779`, 24 July 2026). That branch has **no
common ancestor** with `main`: it predates the referee review, the
`independent/` promotions, the Lean formalisation and the depth-split CI,
and lacks 129 files that `main` has. It could not be merged; this is an
extraction of the 33 files it adds.

## What the extension proposes

Keep `X = 6000000185827` and `y0^2 = 87677/2500000`; lower the time.

| | sealed | proposed |
|---|---|---|
| `t0` | `129/800 = 0.16125` | `1607/10000 = 0.1607` |
| bound | `893927/5000000 = 0.1787854` | `891177/5000000 = 0.1782354` |

The improvement is exactly `11/20000 = 0.00055`.

The approach is economical, and its central reuse argument is sound in
form: because `1607/10000 < 129/800`, the new curved barrier is a **subset**
of the already-certified one, so the existing 883-prism transcript can be
cited as a *stronger* premise rather than regenerated. Independently, this
is the direction `research/dynamic_boundary/` had already identified as the
one worth trying — retuning at lower `t0` rather than steering the boundary.

## What has been checked here

`verify_lower_time_claims.py` re-derives every displayed rational in exact
arithmetic and re-verifies the archive. 20 checks, all passing:

- all five parameter identities are exact, including the `11/20000` gain;
- the Polymath Theorem 1.2 domain conditions hold at the new parameters
  (`0 < t0 < 1/2`, `0 < y0^2 < 1-2t0`, `y0^2 + 2t0 < 1`);
- the lowered time lies strictly inside the certified `t`-range, which is
  what the barrier-reuse argument needs;
- all 27 archived certificate files match the manifest they shipped with;
- the archived assembly transcript reaches
  `RESULT: LOWER-TIME UNCONDITIONAL CANDIDATE ASSEMBLY PASS`, concludes at
  `Lambda <= 891177/5000000`, contains no `[FAIL]`, and keeps its
  unreviewed-status line.

**This is the arithmetic and the archive, not the mathematics.** Nothing
here validates the finite, tail or barrier computations themselves.

## Three findings that need resolving before promotion

### 1. The complete finite replay came from a dirty working tree

`certificates/REPLAY_METADATA.txt`:

```
repository_commit=8ba17791a42e57fe502050121275b09f21ebf5c5
repository_dirty=true
```

The exact source state that produced 3,359,013 finite rows is therefore not
recoverable from any commit. This is the same defect class as
`independent/prop43`'s unrecorded invocations, and more consequential,
because it applies to the headline evidence rather than one lane.

### 2. It was produced in a different container from the sealed one

| | image | pinned |
|---|---|---|
| this repository | `dbn-lambda-01787854-review`, base digest `sha256:52df9b1e…` | yes, asserted in CI |
| the replay | `dbn21a-flint`, id `sha256:bedf7303…` | no |

The review container is built from this repository's `Dockerfile` with its
base digest, Ubuntu snapshot, platform and source labels all asserted before
anything runs. The replay used neither that image nor those assertions, and
the image name suggests it derives from the upstream `dbn21a` bundle rather
than from this package.

### 3. The wall-clock time invites a question

```
started_utc=2026-08-02T02:37:22Z
finished_utc=2026-08-02T02:42:43Z      -> 5 min 21 s
finite_N=690988..4050000               -> 3,359,013 rows
```

`main`'s `complete-finite-replay` takes **about 54 minutes** for 3,149,013
rows in the pinned container. The replay claims 7% more rows in roughly a
tenth of the time. Sharding across cores on faster hardware plausibly
explains a large factor, and the wider range is expected at lower `t0` —
but combined with findings 1 and 2 the throughput should be explained
rather than assumed.

### Also: the filename contradicts its contents

`LOWER_TIME_01782354_PROOF_GAP.md` reads as an open gap. Its own header
says *"completion record … the completed evidence is archived under
`certificates/lower_time_01782354/`"*. One of the two is wrong, and a
reader will believe the filename.

## What promotion would require

Per `research/improved_bound/README.md`, this sits at **stage 0**. Before
it could move toward the sealed tree:

1. regenerate the finite replay from a clean, committed tree in the pinned
   review container, with the invocation recorded — resolving findings 1–3
   together;
2. state the extension as numbered propositions with proofs, in the
   manuscripts' style, rather than as a parameter table plus logs;
3. cross-check against the sealed route where they overlap;
4. only then promote — and note that changing the certified bound touches
   60 files, the `review-01787854-v3` tag, and the repository name itself.

`COMPARISON_BASELINE.md` is also imported here. It documents the
relationship to the separate `dbn-lambda-01858207-candidate-audit` package
and had no counterpart on `main`, which is why references to it did not
resolve.

## The constraint that matters most

A referee is mid-review against `0.1787854`. That number stays frozen until
this work has been through the stages above. Landing an improvement into the
certified claim while its review is in progress would invalidate the target
being reviewed — a much larger cost than waiting.
