# Improved-bound research lane

Scaffold for a reduction intended to improve on the certified bound.
**Nothing is implemented yet.** `core.improved_bound()` raises.

## Status of the repository's claim

The certified claim is and remains

```
Lambda <= 893927/5000000 = 0.1787854
```

It stays frozen while this lane develops. A referee is mid-review against
that number; the bound must not move under him as a side effect of
exploratory work. This lane is unsealed precisely so it can be wrong,
incomplete, and rewritten without touching the audited artifact.

`REVIEW_SCOPE.md` states the invariant: nothing under `research/` is
evidence for the candidate, and nothing in the sealed tree may cite it.

## Why the bound is expensive to change

If the reduction succeeds, the change is not a pull request:

| Surface | Extent |
|---|---|
| Files naming `1787854` | 60 |
| Files naming `893927` | 24 |
| Release tag | `review-01787854-v3` |
| Repository name | `dbn-lambda-01787854-candidate-audit` |

Plus every certificate in the chain and the assembly that consumes them.
Decide *before* landing anything whether that is a `v4` in place with a
repository rename, or a fresh repository with this one frozen as the v3
record. Doing it accidentally, halfway, is the expensive path.

## The staged pipeline

Each stage has an exit condition. Do not start the next one early — the
whole value of the sequence is that a reduction cannot become
load-bearing before it has earned it.

- [ ] **0. Land here, unsealed.** Iterate freely: no reseal, ~3 min CI.
      *Exit:* the reduction runs and produces a candidate bound.
- [ ] **1. Write the proposition first.** A numbered statement with its
      own proof block, citing only earlier-established results, in the
      manuscript's style. Mark it with a gap box until independently
      verified. *Exit:* a referee could read the claim without the code.
- [ ] **2. Make the program self-contained.** No stored certificates,
      exact or outward-rounded arithmetic, fail-closed, deterministic.
      *Exit:* it certifies its bound from literals alone.
- [ ] **3. Cross-check against the existing route** where they overlap.
      Agreement is corroboration. *Disagreement is the most valuable
      output available and must be chased, not smoothed.*
      *Exit:* the two routes agree, or the discrepancy is explained.
- [ ] **4. Promote into `independent/`.** Sealed, run by `verify.sh`,
      constants bound to the digits the documents publish.
      *Exit:* `verify.sh` fails if a document drifts from the program.
- [ ] **5. Version the bound.** Only now. Reseal, regenerate the affected
      certificates, update the assembly, retag, rename.

Record the outcome against the seven-part structure in
`ADVERSARIAL_REVIEW_PROTOCOL.md` § Independent sign-off. That document
warns explicitly against treating one green check as acceptance.

## Conventions the scaffold enforces

Two failures already paid for in this repository, made structural here so
promotion needs no modification:

**Invocations are recorded.** `report.write_report` puts the exact quoted
command line on the first line of every report.
`independent/prop43/prop43_proof.c` is sealed but unrunnable: it takes
twelve positional arguments, seven of which appear nowhere in its nine
stored sweep outputs, so roughly three hours of certified compute cannot
be regenerated from the tree.

**Output is redirectable.** `IMPROVED_BOUND_OUTPUT_DIR` overrides the
report directory. The review container mounts the repository read-only,
so a hardcoded `runs/` path makes a program unrunnable under the seal —
`prop410_proof.py` had to be patched during promotion for exactly this.

Both are covered by tests, so they cannot regress silently.

## Usage

```sh
cd research
python3 -B -m unittest improved_bound.test_improved_bound
python3 -B -m improved_bound status
python3 -B -m improved_bound compare 893000/5000000
```

## Layout

| File | Purpose |
|---|---|
| `core.py` | The reduction. Carries the promotion criteria; **start here.** |
| `report.py` | Invocation recording, output redirection, status line |
| `cli.py` | Subcommands |
| `test_improved_bound.py` | Convention tests (12), not mathematics |

Rename the lane by moving the directory and updating the `-m`
invocations; all internal imports are relative.
