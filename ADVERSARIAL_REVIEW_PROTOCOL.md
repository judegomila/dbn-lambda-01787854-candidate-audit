# Adversarial review protocol

## Purpose

This protocol is for an external mathematician or independent computational
team attempting to falsify the candidate proof. A successful repository replay
is necessary evidence, but it is not by itself a mathematical review.

The protocol follows a Polymath-style division of the argument into explicit
obligations that can be attacked and signed off independently. It does not
claim endorsement by any particular mathematician.

## Dependency blueprint

| ID | Obligation | Primary evidence | Failure consequence |
|---|---|---|---|
| P1 | The cited verified-height theorem has the stated normalization and range. | `BIBLIOGRAPHY.md`; `PROOF_NOTE.md` sections 1--3 | Criterion hypothesis (i) is unavailable. |
| P2 | Polymath Theorems 1.2 and 1.3 and Lemma 8.4 are transcribed with the correct domains, endpoints, and nonzero hypotheses. | `references/`; `PROOF_NOTE.md`; `BARRIER_CERTIFICATE.md` | The criterion or barrier implication is unavailable. |
| P3 | Proposition 6.6(vi) implies the conservative \(x-12,\ 10.50\) error bound without using displayed equation (24)'s \(10.44\). | `ERROR_CONSTANT_WELD.md`; `verifiers/verify_error_constant_weld.py` | Every target effective-error lane is unavailable. |
| G1 | Exact parameters, sign conventions, coordinate maps, and the final substitution are correct. | `CANDIDATE_PARAMETERS.md`; `NATIVE_BINDING.md`; `verifiers/verify_assembly_1787854.py` | The numerical certificates do not imply the claimed bound. |
| F1 | The finite native convolution and effective-error bridge are valid. | `NATIVE_BINDING.md`; `WINDOW_FREEZE_THEOREM.md` | The finite final-time lane is unavailable. |
| F2 | The upper-Dini and normalizer monotonicity arguments cover every coefficient zero and kink. | `provenance/TRIANGLE_Y_DINI_THEOREM.independent.md`; `provenance/TRIANGLE_NORMALIZER_CORR_MONOTONICITY.md` | Finite rows do not transfer to the complete height interval. |
| F3 | All finite rows and every half-open window seam are certified. | `logs/`; `scripts/run_full_sweep.sh`; `scripts/run_direct_singletons.sh` | A gap may remain in the finite half-line. |
| T1 | The endpoint-cap lemma, exact convolution partition, and all-\(N\) monotonicity are valid. | `TAIL_LEMMA.md`; `TAIL_PROVENANCE.md` | The infinite final-time lane is unavailable. |
| T2 | The independent tail implementations enclose the same load-bearing quantities. | `verifiers/verify_tail_arb.c`; Python interval verifiers; sealed transcripts | The tail computation lacks adequate corroboration. |
| B1 | Complete-box derivative bounds, quadrature, Taylor remainder, and coefficient provenance are valid. | `DERIVATIVE_BOX_LEMMA.md`; `BARRIER_CERTIFICATE.md`; `barrier/` | The curved barrier is unavailable. |
| B2 | Every prism is covered, adjacent seams agree, and the winding homotopy avoids zero. | `barrier/certificates/`; `scripts/run_barrier_replay.sh` | Criterion hypothesis (iii) is unavailable. |
| C1 | The finite and tail domains overlap and all three criterion hypotheses are welded without renaming or weakening. | `PROOF_NOTE.md` sections 4--7; `verifiers/verify_assembly_1787854.py` | The final conclusion does not follow. |

The reviewer should record one of `accepted`, `rejected`, or `unresolved` for
each row, together with exact file, line, theorem, and transcript references.

## Clean-room theorem-source audit

Two reviewers should independently transcribe the cited theorem statements
directly from the versioned papers without consulting this repository's
summary prose. They should then compare:

- variable and coordinate normalizations;
- open, closed, and half-open endpoints;
- every positivity or nonzero assumption;
- the \(t=0\) limiting step;
- the direction of every reciprocal inequality; and
- the exact expression substituted into the final criterion.

Disagreement must be resolved from the cited source rather than by choosing the
version implemented in code.

## Boundary and quantifier attack matrix

The external audit should explicitly exercise:

- \(t=0\) and \(t=t_0\);
- \(y=y_0\) and \(y=\sqrt{1-2t}\);
- the left and right endpoint of every finite window;
- every prime-family, shard, and precision transition;
- \(N=3840000\) and the first tail window;
- coefficient zeros and the positive-part kink;
- every moving floor or ceiling in the tail cap;
- logarithm branch-cut separation;
- coefficient-ball endpoints; and
- the first and last face of every barrier prism.

Passing interior sample points is not evidence for an untested boundary.

## Independent recomputation

An implementation counts as independent only if it does not reuse the
repository's source, parser, interval partition, or intermediate decimal
tables. Priority targets are:

1. the weakest finite row and every transition row;
2. the worst Dini cell and its complete cell coverage;
3. the tail bound from a separately derived partition; and
4. the barrier winding or root exclusion using a different interval library
   or a different certified algorithm.

Two precisions of the same program test numerical stability. They do not
constitute independent implementations.

## Required mutation tests

Each mutation below should cause a nonzero exit or a rejected proof
obligation:

1. remove the conjugation on the native \(\overline E C_0\) term;
2. reverse the inequality used for \(1/|E|\);
3. substitute \(x-6.66\) for the required \(x-12\) denominator;
4. remove one finite row, tail cell, or barrier prism;
5. close a half-open finite window at both ends;
6. evaluate a time-dependent bound only at its left endpoint;
7. remove the exact head from the decreasing-tail estimate;
8. project a complex quadrature ball onto its real part;
9. corrupt one coefficient radius or adjacent-prism seam; and
10. swap or weaken two criterion hypotheses.

The final report should state the mutation kill rate by obligation. A
surviving mutation is a release-blocking finding until it is shown to be
mathematically irrelevant.

## Parameter perturbation and calibration

Recompute nearby choices of \(t_0\), \(y_0\), finite cutoff, tail head size,
working precision, cell mesh, and prism mesh. Recorded margins should move in
the analytically predicted direction. The pipeline should also reproduce a
known wider published configuration and should reject deliberately failing
configurations. This distinguishes a genuine implementation of the theorem
from code hard-wired to one target output.

## Formal-methods path

Lean 4 is not a release prerequisite. A useful formalization should begin with
the exact theorem contract, parameter and sign glue, window seams, native
convolution identities, Dini transfer, tail endpoint cap, and generic prism
homotopy. Merely declaring all analytic inputs as axioms and restating the
final decimal would add little assurance.

For numerical kernel checking, the interval programs would need to emit exact
dyadic or rational proof certificates consumed by a proved Lean checker.
Checking only the printed decimal margins in Lean would continue to trust the
same C and interval-arithmetic implementation.

## Independent sign-off

The final referee record should separate:

1. theorem-source acceptance;
2. handwritten reduction acceptance;
3. proof-to-code acceptance;
4. clean-environment replay;
5. independent recomputation;
6. mutation-test results; and
7. unresolved assumptions or corrections.

No single green badge should be used as a substitute for these distinct
decisions.
