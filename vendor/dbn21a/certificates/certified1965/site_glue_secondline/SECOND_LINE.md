# Second line: the auxiliary line's site-uniform window-gluing lemma (site_glue_v1)

Prepared 2026-06-12.

## What is being second-lined

The verified the auxiliary line fact "SITE-UNIFORM WINDOW-GLUING LEMMA AT THE
CAMPAIGN SITE + Lambda<=0.1965-ROW PRECONDITION INSTANTIATION" (bundle
`claims/site_glue_v1/` in the auxiliary line's workspace), which retires
record-chain preconditions P10 (N-constancy) / P11 (window gluing) for
EVERY row at the campaign site with t0 <= 0.1809, and instantiates the
Lambda <= 0.1965 stretch row (t0 = 1770/10000, y0^2 = 39/1000). It is
the precondition certificate that the imminent 0.1965 assembly will
cite as a hypothesis — citation-weight makes it second-line-worthy
under the tiered verification policy, post-record stream.

Also re-anchored in passing: the point-row margins and N-constancy
robustness strings of the verified the auxiliary line bundle
`claims/nconst_gap_v2/` (the t0 = 1775/10000 = 0.197-record row).

## Verification tier (verification policy, item 2c — this line's tier assessment)

**Tier (b)-strength line delivered at below tier-(a) cost.** The
producing machinery here is elementary (window-start algebra
ws(N,t) = 4*pi*N^2 - pi*t/4 plus one floor-of-sqrt), so a FULL
zero-shared-code independent line costs less than a minute of compute;
no reason to settle for anchor validation. The line nevertheless ALSO
contains the rung-(a) content: gates A1/A2/S2/S3 machine-reproduce
pinned the auxiliary line strings from a different (0.197-era) row — two
regimes (0.1965 stretch row + 0.197 record row), exactly the
known-anchor discipline.

## Zero-shared-code statement

Producer's line: mpmath.iv prec 250, endpoint extraction via the
`_mpi_` binary-tuple path (their verified extraction machinery).
THIS line: **stdlib only — `fractions.Fraction` + `math.isqrt`. No
mpmath, no ARB, no pari, no interval library at all.** Pi is enclosed
from scratch by TWO independent Machin-type alternating-series brackets
(classic Machin and the Gauss 8/57/239 formula) which are gated to
intersect (PI1) before their intersection is consumed; sqrt brackets
come from integer `isqrt` scaling with a straddle self-test (SQ0).
Their verifier was never opened; the window formula is derived from
arXiv:1904.12438's stored-sums construction (same source as my pinned
s2/s4 toolchain facts) and the pinned fact texts.

## Quantifier audit (restated; machine teeth named)

The certified ∀-statement: FOR ALL t in the CLOSED interval
[0, 1809/10000] the N0=690988 window starts >= 5377392.8789 below
X = 6000000185827 (exact integer) and the N0+1 window starts
>= 11989041.1415 past X+1; and FOR ALL (x,t) in the CLOSED box
[X, X+1] x [0, 1809/10000], N(x,t) = floor(sqrt(x/(4pi) + t/16))
= 690988. Directions: ws(N,t) is linear in t with slope -pi/4 < 0
(gate Q1), so sup_t ws is at t=0 and inf_t ws at t=0.1809 — the
t-for-all reduces EXACTLY to the two endpoints, no sampling; the
radicand is linear in (x,t) with positive coefficients (gates Q2/Q3),
so the box-for-all reduces EXACTLY to the two extreme corners (X,0)
and (X+1, 0.1809). Open/closed: all intervals CLOSED; the strict
inequalities U3/S1 hold at the closed endpoints, hence everywhere.
The window-membership identity x >= ws(N,t) iff x/(4pi)+t/16 >= N^2
is gated as exact rational algebra with pi a free positive symbol
(ALG1).

## Gate map (30 gates, every quoted decimal machine-derived)

- PI1–PI3, SQ0, ALG1: toolchain self-tests (pi cross-enclosure width
  < 1e-60; isqrt straddle; window identity).
- Q1–Q3: monotonicity legs of the quantifier audit.
- U1a/b, U2a/b, U3: site-uniform margins. My exact rational enclosures
  floor-truncate (4 decimals) to strings IDENTICAL to the producer's
  pinned literals on BOTH endpoints: 5377392.8789 and 11989041.1415.
- R1–R7: the 0.1965 row. Exact identities t0 + y0^2/2 = 1965/10000,
  y0^2 + 2t0 = 393/1000 <= 1, slab containment, PT2021 admissibility
  X/2 = 3000000092913.5 <= T = 3000175332800 (exact rationals); row
  point margins floor4-match their literals 5377393.0179 /
  11989041.1446 on both endpoints; R7 gates point-dominates-uniform
  consistency (the same inclusion-isotonicity exercise as my an earlier run
  dominance gates).
- A1/A2: anchor regime 2 — the 0.197-record row t0 = 1775/10000;
  my floor2 strings equal the auxiliary line's pinned >= 5377393.01 /
  >= 11989041.14 literals (my sharper floor4: 5377393.0183 /
  11989041.1442).
- S1–S3: full-slab N-constancy via the corner reduction; my certified
  S-range [690988.3096430277.., 690988.3096430935..]; the pinned
  robustness literals 0.3096430277 and 0.6903569064 are reproduced as
  floor10 strings of my exact endpoints.
- G1–G3: rung-menu candidates t0 = 0.162/0.161/0.160 contained in the
  uniform t-range.

## Discrepancies

NONE found. Every pinned literal reproduced exactly at its stated
rounding mode (all the producer's strings are floor truncations, and
my independent exact-rational endpoints floor-truncate to the same
strings).

## RH-height dependency

NONE in any inequality certified here (finite exact arithmetic at
fixed X). Gate R4 is itself the exact PT2021 height comparison; the
Lambda chains these preconditions serve are unconditional via PT2021
T = 3000175332800.

## Reproduce

    bash verify.sh        # from this directory; expected exit 0, ~1 s

verify.sh md5-pins siteglue_pureint.py, re-runs it live with
/usr/bin/python3, requires 30 PASS / 0 FAIL / RESULT: ALL PASS, and
diffs the live PASS lines against the pinned run_log.txt.
