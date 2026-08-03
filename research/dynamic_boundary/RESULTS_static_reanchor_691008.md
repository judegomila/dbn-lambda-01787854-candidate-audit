# Run record: static re-anchor transcript smoke pass (N = 691008)

STATUS: UNSEALED RESEARCH ONLY; no improved Lambda bound certified.

Date: 2026-07-31.  Repository branch `research/dynamic-boundary`.

## Certified-smoke run

| field | value |
|---|---|
| anchor `X` | 6000345678901 |
| window `N` (both slab corners) | 691008 |
| slab | `[X, X+1] + i[0.1809, 1]`, `t in [0, 0.16125]` |
| stored-sum matrix | `StoredSumSinglemat_interval X 20` (62 x 62 terms, 20 digits) |
| barrier program | `TloopSinglemat_closed_cert 0 0.16125 0.1809 0 <mat>` |
| terminal marker | `RESULT: CLOSED SLAB CERTIFIED` |
| consecutive passing prisms | 3709 |
| closed coverage endpoint | `[0.161250000000000000000000000000 +/- 2e-35]` |
| validator | `validate_barrier_transcript.py --expected-n 691008` → SMOKE PASS |
| wall time (barrier) | 1583.25 s |
| transcript sha256 | `b208bc5a182d39f33ec411dff0e5c5f989096b52de30636466b66b66bb7436c6` |
| matrix sha256 | `6fdb3f5927b75d7fd18eb40e732938de20d9bc01344103030d3774ae81333d9f` |
| toolchain | FLINT/Arb 3.6.0 (Homebrew), Apple clang 21.0.0, macOS arm64 |

Transcript and matrix are regenerable caches (~3 min matrix + ~26 min
barrier) and are not committed; the commands above reproduce them.

## Anchor-quality probe

| anchor | outcome |
|---|---|
| 6000342141913 (naive height-budget endpoint `X*`) | FAIL: no positive certified time-motion budget (first prism) |
| 6000343000000 | FAIL: no positive certified time-motion budget (first prism) |
| 6000345678901 | CLOSED SLAB CERTIFIED (3709 prisms) |
| 6000348141913 | 790+ prisms passing, margins ≈ 0.60; stopped as redundant |

Conclusion: barrier viability at a new site is a property of the specific
anchor, not of the window; an anchor-quality search must precede any
re-anchor pilot.  The height-budget analysis (landing/rank) bounds *where*
to search — the 8,523,687-integer slack below the Platt–Trudgian ceiling —
but does not itself select the anchor.

## Outstanding obligations (unchanged)

```text
new_site_taylor_tail=NOT_CERTIFIED
new_site_uniform_error=NOT_CERTIFIED
new_site_proof_to_code=NOT_AUDITED
new_site_theorem_assembly=NOT_WRITTEN
```

Nothing in this record is evidence for, or modifies, the sealed
`0.1787854` candidate.
