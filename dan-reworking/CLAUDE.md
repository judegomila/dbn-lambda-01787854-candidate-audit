# Dan's review workspace (`dan-reworking/`)

## What this directory is

This is Dan Romik's workspace for the independent referee review of
this repository's candidate proof of the bound
`Lambda <= 0.1787854` for the de Bruijn–Newman constant. Dan is
working through Jude Gomila's material (the rest of this repository)
and compiling a **single publishable-quality LaTeX manuscript** that
presents Jude's work in the format, structure, and level of rigor
suitable for publication in a research mathematics journal.

## Contents

- `latex/gomila-proof-exposition.tex` — the manuscript (build with
  `latexmk -pdf`). It contains: the cited literature checked verbatim
  against arXiv sources; complete proofs of every analytic lemma
  (all verified in the course of the review); and the
  computer-assisted components stated as numbered propositions.
- `papers/` — the arXiv `.tex` sources of the two cited papers
  (Polymath, arXiv:1904.12438v2; Platt–Trudgian, arXiv:2004.09765v1),
  downloaded so citations could be verified against sources rather
  than PDF renderings.
- `code/prop43/` — the verification program for Proposition 4.3
  (`prop43_proof.c`, derived from `src/lemma_sweep_p235711.c` as
  documented in its header) and the complete fresh-run outputs in
  `runs/` (`*_sweep.out`, `*_summary.txt`, `*_progress.txt`),
  referenced by the manuscript as supplementary material.
- `code/prop410/` — the verification program for Proposition 4.10
  (`prop410_proof.py`, derived from
  `verifiers/verify_finite_and_binding.py` as documented in its
  header: the stored-log parsing and the redundant corr-rate gate
  were removed, leaving only the self-contained error-budget
  computation) and its run report `runs/prop410_report.txt`.
  Precedent for pure-calculation Python components: exact rational
  inputs, mpmath.iv interval arithmetic, acceptance by exact
  rational comparison of outward-rounded endpoints, no file reads.

## Working conventions

- **Encapsulation.** Every nontrivial claim sits in a numbered
  lemma/proposition/theorem block with its own proof; each proof
  cites only earlier established statements, so errors localize and
  checking can be distributed. A proposition is tagged
  "computer-assisted" exactly when its *own* proof is a certified
  computation — never merely because it cites one.
- **Gap boxes.** Framed, auto-numbered boxes (labels `gap:*`) mark
  the computer-assisted components not yet independently verified;
  the final section of the manuscript collects them. Verification
  protocol per gap: read the certifying program against the
  corresponding statement in the manuscript, then rerun it on an
  independently built toolchain (FLINT/Arb via Homebrew; the proof
  of Proposition 4.3 in the manuscript is the precedent).
- **Certificates are caches, not evidence.** The stored certificate
  files in this repository cannot be validated by parsing; for this
  review, verification of a computation means re-executing it.

## Status

As of 2026-07-30: literature checks complete; all analytic arguments
carry complete verified proofs; Propositions 4.3 (window sweep) and
4.10 (finite-region error bound) are fully discharged with programs
and proofs in the manuscript; four computer-assisted components
remain to be reproduced (see the manuscript's summary section):
the Dini cell certificates, the tail cutoff inequalities, the
barrier-box uniform error bound, and the barrier prism certificate.

## Session bootstrap (current state as of 2026-07-30)

Read first, in order: this file; the manuscript's final section
("Summary of gaps") and the gap boxes it references; then the header
of `code/prop43/prop43_proof.c` for the verification-run precedent.

**Git / GitHub state.** This directory lives inside the clone of
Jude's repo. The original working branch `dan-reworking-review` was
merged into `main` via PR #2 (squash) and deleted 2026-07-30; new
work happens on `main` locally until a fresh branch is cut for the
next PR. `main` is protected: changes only via PR, with a required CI check
`full-review` (rebuilds Jude's pinned container and replays critical
lanes; up to ~2 h; our directory cannot affect it — the
`.dockerignore` excludes everything but `Dockerfile` and
`requirements.txt`). A PR from `dan-reworking-review` into `main` is
opened via the GitHub web UI (no `gh` installed).

**Toolchain.** FLINT/Arb 3.6.0 installed via Homebrew. Compile
pattern (Jude's own strict flags):
`cc -O2 -std=c17 -Wall -Wextra -Werror -pedantic
-I$(brew --prefix)/include FILE.c -L$(brew --prefix)/lib
-lflint -lgmp -lmpfr -o OUT`.
Cross-toolchain note: fresh runs may differ from Jude's sealed
values in the last digit or two (FLINT 3.6 enclosures are slightly
tighter than his 3.0.1); differences so far were always in the
favorable direction. Prop 4.3 timings: naive mode ~67 s/row;
full sweep ~35 min wall-clock sharded on 8 cores.

**Remaining gaps** (numbering matches the manuscript's gap boxes
after the 2026-07-30 renumbering; all: read program against the
manuscript statement, then rerun on our toolchain; the deliverable
per gap is a standalone pure-calculation program under
`dan-reworking/code/` that reads no stored files, plus a proof
block in the manuscript — see `code/prop43/` and `code/prop410/`
for the C and Python precedents):

| gap | statement | Jude's program (in repo root) | cost |
|---|---|---|---|
| 1 | Prop: Dini cell certificates | `verifiers/verify_triangle_y_dini_arb.c` (180+256 bit) | moderate |
| 2 | Prop: tail cutoff inequalities | `verifiers/verify_tail_arb.c` (256+512 bit; `scripts/run_tail_arb.sh`) | small |
| 3 | Prop: barrier-box uniform error | `barrier/src/verify_uniform_error_01787854.c` | small |
| 4 | Props: prism certificate + tail-exponent gate | `barrier/src/TloopSinglemat_closed_cert.c` (`scripts/run_barrier_replay.sh`) | large |

Gap 2 also discharges the hypotheses of the tail lemmas; gaps 2 and
3 are the natural next targets.

Resolved 2026-07-30: the former gap 2 (finite-region E_max,
Proposition 4.10) — `code/prop410/prop410_proof.py`, with a full
proof block in the manuscript including the monotonicity reduction
of the whole region to the single evaluation at (x_*, N_0); the
program's error evaluation was read line by line against Polymath
eq. (23) and the manuscript's corollary (eq:ec0), and the fresh run
reproduced E_max = 0.000000233494905212337849 exactly. Toolchain
note per Dan: mpmath (independently installed) is acceptable; same
library family as Jude's is not a concern, reliability of the
package is what matters.

**Key findings so far** (details in the manuscript): the displayed
10.44 in Polymath eq. (24) is not derivable from their own stated
reduction — the manuscript uses only the 10.50 corollary; several of
Jude's runtime gates proved mathematically redundant (harmless);
the genuinely tight certified inequalities are N^2 < q(X), the
tail-exponent gate, and the tail contraction 1-D ≈ 2.8e-4; the
thinnest margins overall are the finite-range post-error margin
5.6e-7 and the Dini cell ratio 1.4e-6. Prop 4.3's fresh run
reproduced Jude's T_min = 791366e-12 exactly at N = 690988.

**Dan's editorial principles** (enforced throughout): every
nontrivial claim in a numbered block with its own proof; proofs cite
only earlier established statements; "computer-assisted" tag only
when the statement's own proof is a computation; no repo jargon
(no "lane/leg/gate/floor"; no "handwritten"; no category-A/B talk);
citations verified against arXiv .tex sources, never PDFs; stored
certificates are caches, not evidence. Dan plans to read the full
manuscript himself and run further AI review passes before any
conclusion is drawn.
