# Independent recomputation programs

Self-contained programs that recompute quantities the candidate also
derives by its own route. Each one reads no stored certificates: it
calculates from exact rational inputs and prints a certified bound.
Their value is cross-implementation agreement — if two independently
written implementations produce the same digits, neither route's
implementation error is silently load-bearing.

These are sealed. `SHA256SUMS` covers them and
`verifiers/verify_independent_crosscheck.py` executes them.

## Origin

Written by Dan Romik (write access) as part of the referee rework, and
promoted here from the unsealed workspace `dan-reworking/code/` at
commit `f4d2d03ebc6342b3bce4e0c0b695b82f2e213f1a`.

The author's working copies remain under `dan-reworking/`, which is
outside the seal (see `REVIEW_SCOPE.md`). Those copies may move ahead of
these as the manuscript develops. **The copies in this directory are the
ones the audit attests**; a same-named file under `dan-reworking/` is
the author's draft, not the sealed artifact. Promotion of a revised
program is a deliberate step, not an automatic sync.

## Contents

| Program | Proposition | Derived from | Cost |
|---|---|---|---|
| `prop43/prop43_proof.c` | 4.3 | `src/lemma_sweep_p235711.c` | ~3 h over nine shards |
| `prop410/prop410_proof.py` | 4.10 | `verifiers/verify_finite_and_binding.py` | < 1 s |
| `prop62/prop62_proof.c` | 6.2 | `barrier/src/verify_uniform_error_01787854.c` | < 1 s |

Each program's own header records its derivation and what was removed
from its ancestor. Read those before the code.

## What the cross-check establishes

Two sharp constants were published in prose but never machine-checked at
their displayed digits:

- `E_max = 0.000000233494905212337849` — `verify_finite_and_binding.py`
  gates only on `error_max < 234/10**9`;
- `0.000356523011600040` — `barrier/src/verify_uniform_error_01787854.c`
  gates only on the loose `0.00125` allowance.

`verify_independent_crosscheck.py` now recomputes both and compares them,
as exact decimal strings, against the digits `README.md`,
`PROOF_NOTE.md`, `MAXIMUM_CHECKS.md`, `CANDIDATE_PARAMETERS.md` and
`BARRIER_CERTIFICATE.md` publish. A document drifting from a program is
a seal failure.

This is corroboration, not proof. A pass means two implementations agree
and the published digits are reproducible. It does not establish either
proposition, and it does not upgrade the candidate's review status.

## Modifications made during promotion

Only one, to `prop410/prop410_proof.py`:

- the report directory is now overridable via `PROP410_OUTPUT_DIR`,
  defaulting to the original `runs/`. The review container mounts the
  repository read-only, so the hardcoded path was unwritable there. The
  certified arithmetic and the exit status are untouched.

`prop43_proof.c` and `prop62_proof.c` are byte-identical to their
`dan-reworking/` originals at the promotion commit.

## Running them

`prop410` and `prop62` run automatically as part of `./verify.sh`.

### `prop43` — invocations recovered

`prop43_proof.c` is sealed and now has a documented, complete invocation
set: see [`prop43/INVOCATIONS.md`](prop43/INVOCATIONS.md).

The seven arguments previously described here as unrecorded were never lost.
They are in `scripts/run_full_sweep.sh`, which is sealed and has always been
on `main`; only the mapping from the stored sweeps to that schedule was
missing. Eight of the nine stored runs correspond to canonical bands exactly.
The one residue is which `prec K hw` triple the author used inside each
re-sharded `p23_s*` run, and it does not affect reproducibility: the
canonical schedule is authoritative, and the stored runs are corroboration
produced under a different sharding.

Nothing runs it yet. At roughly three hours single-threaded it belongs in a
dedicated workflow job sharding the bands across parallel runners, on
dispatch and a schedule, never on the merge path.

### Promotion candidates not yet promoted

`dan-reworking/code/` now also holds `prop49`, `prop510`, `prop612` and
`prop65`, which discharge the manuscript's remaining gaps. They are not
promoted here yet and nothing in `verify.sh` runs them.

Their reproducibility is markedly better than `prop43`'s: `prop49` and
`prop65` take no arguments at all, and `prop510` takes an optional
precision defaulting to 320 bits and refusing anything below 256. Only
`prop612` carries a residual gap — it requires four arguments
(`ts te y0 Prt`) and its report records three of them
(`X = 6000000185827…828`, `N = 690988`, `y0 = 0.1809`, `t = 0…0.16125`)
but not `Prt`. From the source `Prt` controls output rather than the
arithmetic, so it likely does not change the certified values, but the
report cannot be reproduced byte-for-byte without it.

