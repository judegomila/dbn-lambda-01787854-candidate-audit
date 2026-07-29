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

As of 2026-07-29: literature checks complete; all analytic arguments
carry complete verified proofs; five computer-assisted components
remain to be reproduced (see the manuscript's summary section):
the Dini cell certificates, the finite-region error bound, the tail
cutoff inequalities, the barrier-box uniform error bound, and the
barrier prism certificate.
