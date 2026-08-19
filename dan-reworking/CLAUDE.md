# Dan's review workspace (`dan-reworking/`)

## What this directory is

This is Dan Romik's workspace for the independent referee review of
this repository's candidate proof of the bound
`Lambda <= 0.1787854` for the de Bruijn–Newman constant. Dan worked
through Jude Gomila's material (the rest of this repository) and the
directory now contains **two publishable-quality LaTeX
manuscripts** presenting the mathematics at journal-level rigor —
a review exposition and a regular research paper — together with
the seven standalone programs that constitute the computer-assisted
proofs, and their run outputs.

## Contents

- `latex/exposition/gomila-proof-exposition.tex` — the review
  manuscript (build with `latexmk -pdf`). It contains: the cited
  literature checked verbatim against arXiv sources; complete proofs
  of every analytic lemma (all verified in the course of the
  review); and the computer-assisted components stated as numbered
  propositions.
- `latex/research-paper/debruijn-newman.tex` — the research paper:
  the same mathematics reframed as a regular research article
  ("We prove..."), author byline "Jude Gomila and [additional
  authors TBD]". No review/verification framing: no "claimed",
  "certified", "verified" language; proofs simply cite the
  supplementary programs. Statement numbering is IDENTICAL to the
  exposition (same sectioning skeleton), so the program headers'
  proposition references apply to both. Final section is "Remarks
  on the computer-assisted components". Keep the two manuscripts'
  mathematical content in sync when editing either.
- `papers/` — removed before public release: it held the arXiv
  `.tex` sources of the two cited papers (Polymath,
  arXiv:1904.12438v2; Platt–Trudgian, arXiv:2004.09765v1),
  downloaded so citations could be verified against sources rather
  than PDF renderings. arXiv's non-exclusive-distribution license
  does not permit redistribution here; re-download from the exact
  arXiv versions if needed.
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
- `code/prop65/` — the verification program for Proposition 6.5
  (`prop65_proof.c`, written fresh for the review as a standalone
  extraction of the barrier program's tail-exponent gate) and its
  run report `runs/prop65_report.txt`.
- `code/prop612/` — the verification program for Proposition 6.12
  (`prop612_proof.c`, merged from three of Jude's barrier sources
  as documented in its header; fully self-contained, no file
  reads) and its run report `runs/prop612_report.txt`.
- `code/prop49/` — the verification program for Proposition 4.9
  (`prop49_proof.c`, derived from
  `verifiers/verify_triangle_y_dini_arb.c` as documented in its
  header; adds an aggregated certified ratio threshold) and its run
  reports `runs/prop49_report_{180,256}.txt`.
- `code/prop510/` — the verification program for Proposition 5.10
  (`prop510_proof.c`, derived from `verifiers/verify_tail_arb.c` as
  documented in its header; adds a strict check of the manuscript's
  margin constant) and its run reports
  `runs/prop510_report_{256,512}.txt`.
- `code/prop62/` — the verification program for Proposition 6.2
  (`prop62_proof.c`, derived from
  `barrier/src/verify_uniform_error_01787854.c` as documented in
  its header; adds a strict check of the manuscript's sharp
  constant) and its run report `runs/prop62_report.txt`.

## Working conventions

- **Encapsulation.** Every nontrivial claim sits in a numbered
  lemma/proposition/theorem block with its own proof; each proof
  cites only earlier established statements, so errors localize and
  checking can be distributed. A *proof* opens with "The proof is
  computer-assisted" exactly when it is carried out by one of the
  supplementary programs — statements themselves carry no
  "computer-assisted" tag (per Dan: claims aren't computer-assisted,
  proofs are).
- **One proposition, one program.** Each computer-assisted
  proposition is proved by a standalone program in `code/propNN/`
  (naming: `propNN_proof.{c,py}` for Proposition N.N). Protocol,
  applied to all seven: read the program line by line against the
  manuscript statement; rerun on our toolchain; the program reads
  NO stored files (all inputs exact integers/rationals in source);
  every displayed constant in the statement is checked by an
  explicit strict comparison against an exact rational; all
  decisions fail closed. Each program's header documents its
  provenance and every deviation from Jude's source.
- **Certificates are caches, not evidence.** The stored certificate
  files in Jude's repository cannot be validated by parsing; they
  are consumed nowhere in the manuscripts or programs.
- **Gap boxes (historical).** Earlier drafts marked unverified
  computer-assisted components with framed `gap:*` boxes. All gaps
  were resolved by 2026-07-31 and the boxes removed; the `gap`
  environment survives unused in the exposition preamble only.

## Status

As of 2026-08-01: ALL GAPS RESOLVED. Literature checks complete; all
analytic arguments carry complete verified proofs; all seven
computer-assisted propositions — 4.3 (window sweep), 4.9 (Dini
cells), 4.10 (finite-region error bound), 5.10 (tail cutoff
inequalities), 6.2 (barrier-box error bound), 6.5 (tail-exponent
inequality) and 6.12 (prism decomposition) — are fully discharged
with standalone no-stored-data programs in `code/` and proof blocks
in both manuscripts. Cosmetic passes done: eq:gsk split into three
numbered bounds (eq:gammabound / eq:resbound / eq:kappabound) with
all references retargeted; "computer-assisted" bracket tags removed
from statement titles (Dan); a sign typo in Remark rem:1044 fixed
in both manuscripts ("does not rely on (24)"). Remaining per Dan's
stated plan: his own full read of the manuscripts and further AI
review passes before any overall conclusion is drawn; author list
of the research paper TBD.

## Session bootstrap (current state as of 2026-08-01)

Read first, in order: this file; the exposition's final section
("Summary of the verification"); then the header of
`code/prop43/prop43_proof.c` for the program-header precedent.

**Git / GitHub state.** This directory lives inside the clone of
Jude's repo. History: branch `dan-reworking-review` merged via
PR #2 (2026-07-30); the first two gap commits (Props 4.10 and 6.2)
were merged by Jude around PR #7 — which also promoted copies of
our prop43/prop410/prop62 programs into a top-level `independent/`
directory with a cross-check verifier — and the old PR branch was
deleted. Current branch: `dan-prop410-gap2`, rebased onto that
main, carrying one commit with everything since (Props 5.10, 4.9,
6.5, 6.12; the latex/ split into exposition/ and research-paper/;
the research paper; cosmetic passes). `main` is protected: changes
only via PR, with a required CI check `full-review` (PRs now run
at quick replay depth per Jude's PR #7; full replay on main; our
directory cannot affect it — the `.dockerignore` excludes
everything but `Dockerfile` and `requirements.txt`). PRs are
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

**Remaining gaps**: none.

**Gap-resolution log** (each following the protocol of the Working
conventions; Prop 4.3 was resolved before this log began, 6.2 and
4.10 on 2026-07-30, the rest on 2026-07-31):
- Finite-region E_max (Proposition 4.10) —
  `code/prop410/prop410_proof.py`; monotonicity reduction of the
  whole region to the single evaluation at (x_*, N_0); read against
  Polymath eq. (23) and corollary (eq:ec0); fresh run reproduced
  E_max = 0.000000233494905212337849 exactly. Toolchain note per
  Dan: mpmath (independently installed) is acceptable; package
  reliability is what matters, not differing from Jude's library.
- Tail-exponent inequality (Proposition 6.5, resolved 2026-07-31) —
  `code/prop65/prop65_proof.c`, a small fresh standalone extraction
  of the barrier program's "derivative-tail exponent gate": strict
  ball comparison of (1/4)log(q(X)/N^2) ~ 2.24e-7 against
  h(X,ymin)_+/(2X^2) ~ 6.35e-27 at 256 bits. Runs in milliseconds.
- Prism decomposition (Proposition 6.12, resolved 2026-07-31) —
  `code/prop612/prop612_proof.c`, merged from
  TloopSinglemat_closed_cert.c + StoredSumSinglemat_interval.c
  (in-memory 62x62 coefficient generation from the defining series;
  NO stored file read — resolves the matrix-provenance question) +
  StoredSumTaylorTail_cert.c (in-program hypothesis and truncation
  certificates). Compiled WITHOUT -Werror (benign unused-variable
  warnings pre-exist in Jude's Polymath-derived sources); needs
  -I$(brew --prefix)/include/flint in addition to the usual include
  path (quoted includes). Fresh run: 883 prisms (same count as
  Jude's sealed transcripts), worst margin 0.51984989461387254365
  certified against the exact rational 5198498946e-10, aggregate
  winding [±1.18e-14], Taylor truncation 1.9543e-22 < 1e-20;
  ~7.5 min wall. The Taylor-reconstruction identity (poly eval x
  n0-prefactor = sum of b_t(n) n^{-...}) was verified symbolically
  during the review; the F_z/F_t integrands and runtime gates match
  the manuscript's Section 6 definitions line for line.
- Dini cell inequalities (Proposition 4.9, resolved 2026-07-31) —
  `code/prop49/prop49_proof.c` (Arb; compile twice, default PREC=180
  and -DPREC=256; each run ~7 s, far below the "moderate" estimate).
  Cell enumeration per Lemma 4.8, q_N freezing, padded-binary64
  rectangle covers with in-program containment certification
  (log_padding_covers), adaptive bisection failing closed. Fresh
  runs reproduce Jude's leaf counts (297490/52239/9290/237) and
  worst ratio 0.99999860767275095 exactly, at both precisions; an
  aggregated certified threshold check (worst < 0.9999988) was
  added in this review.
- Tail cutoff inequalities (Proposition 5.10, resolved 2026-07-31) —
  `code/prop510/prop510_proof.c` (Arb, run at 256 and 512 bits;
  derived from `verifiers/verify_tail_arb.c`, Gomila's own
  from-scratch C reimplementation of his Python tail verifier).
  Certifies cap-validity, all cutoff gates, the A-side slope
  condition, the lemma hypotheses, and the four displayed constants
  D < 0.999721, M_max < 1.608290, errors < 1.1672e-8, margin >
  0.00017352 — the margin check was added in this review (original
  certified only positivity; corridors alone give ~0.00017349).
  Suprema over I_t x I_box / I_ext are captured by hull arithmetic
  with directed endpoint extraction. Repo codename "P1113" for the
  mollifier removed from output labels.
- Barrier-box uniform error (Proposition 6.2) —
  `code/prop62/prop62_proof.c` (256-bit Arb); two-corner argument
  for window-index constancy (monotonicity of x/4pi + t/16 under
  floor-sqrt), N^2 < x/4pi, and the uniform majorization of eq.
  (23) + (eq:ec0) with every t- and y-dependent factor at its worst
  endpoint; the sharp displayed constant 0.000356523011600040 is
  now itself certified (added strict ball check, documented in the
  header); fresh run passes all checks in under a second.

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
