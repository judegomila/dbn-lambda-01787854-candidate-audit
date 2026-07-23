# Unreviewed de Bruijn--Newman candidate at 0.1787854

> **Private external-review snapshot.**  This is an unreviewed conditional
> candidate, not an established theorem or public announcement.  Start with
> `REVIEW_SCOPE.md` and `OPEN_REVIEW_QUESTIONS.md`.

This package records a computer-assisted **candidate upper bound**

\[
\boxed{\Lambda\le\frac{893927}{5000000}=0.1787854}.
\]

The exact row is

\[
t_0=\frac{129}{800}=0.16125,\qquad
y_0^2=\frac{87677}{2500000}=0.0350708,
\]
\[
t_0+\frac{y_0^2}{2}
=\frac{893927}{5000000}.
\]

This is not a proof of the Riemann hypothesis, not an accepted new
theorem, and not a peer-reviewed result.  It is a locally replayable,
internally audited candidate whose final implication remains
conditional on external review of the direct native-functional binding and
the cited winding, site, effective-approximation, and criterion bindings.

The repository intentionally exposes two particularly important unresolved
questions:

- whether the native Triangle functional in the producer is bound to
  \(|f_t|\) in exactly the asserted normalized units; and
- whether the vendored winding-slab artifacts establish a rigorous closed
  real-parameter slab rather than only internally consistent stored output.

These and the known `x-6.66` versus `x-12` error-term transcription are
spelled out in `OPEN_REVIEW_QUESTIONS.md`.  Automated `PASS` output does not
settle them.

## What is certified locally

- Every one of the \(3,149,013\) integers
  \(N=690988,\ldots,3840000\) is stored and parsed exactly.
- There are no missing, duplicate, nonpositive, or `UNCERT` rows.
- The four-prime-set ladder is

  \[
  \begin{array}{c|c|c}
  N\text{-range}&P&\min T_N\\ \hline
  690988\ldots728999&\{2,3,5,7,11\}&0.000000791366\\
  729000\ldots818999&\{2,3,5,7\}&0.000315112459\\
  819000\ldots1027999&\{2,3,5\}&0.000305788807\\
  1028000\ldots3840000&\{2,3\}&0.000309285478
  \end{array}
  \]

- A direct Arb upper-Dini verifier certifies the proposed proof that the exact
  Triangle mass is nonincreasing over the full height interval.  It covers all active
  divisor patterns \(243,81,27,9=3^5,3^4,3^3,3^2\), at both 180 and
  256 bits.  Its worst certified ratio is
  `0.99999860767275095 < 1`.
- A separate interval verifier proves the native Euler normalizer and
  the native \(\kappa\)-correction are nonincreasing.  The worst
  correction log-rate cap is
  `-1.3631121547576400 < 0`.
- Subject to review of the native-functional identification, the producer's
  normalized lower bound itself transfers:

  \[
  L_N(y)\ge L_N(y_0)\ge T_N.
  \]

- The complete upstream \(U1\)--\(U5\) effective-error path gives

  \[
  E_{\max}\le0.000000233494905212335514.
  \]

  The corrected finite binding is in selection units:

  \[
  T_{\min}-E_{\max}
  \ge0.000000557871094787>0.
  \]

- The exact-convolution tail begins at the closed overlapping endpoint
  \(N=3840000\).  Both 160- and 256-bit runs pass 93/93 checks and give

  \[
  D_{\rm ub}\le0.999720909379940,\qquad
  \text{slack}\ge0.000173520942813>0.
  \]

## The repaired analytic bridge

An earlier exploratory argument tried to place the cancellation-sensitive
multi-prime \(A\)-side into the deposited nonnegative
`standard-majorant` class.  That argument is false: composite divisors
retain signed inclusion--exclusion cancellation.  This package does not
use that claim, `seam_ytransfer`, or the exponent-inflation seam.

Instead, `provenance/TRIANGLE_Y_DINI_THEOREM.independent.md` factors the
actual coefficient for every composite divisor and certifies the upper
Dini derivative of the exact native Triangle functional.  The
normalizer/correction note then transfers the native normalized lower
bound directly.  The binding arithmetic is \(T-E\), not the
dimensionally misleading exploratory expression \(M T-E\).

## Verification

Install the locked Python dependencies and run the stored verification:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes -r requirements.txt
./verify.sh
```

It checks the SHA-256 seal, the exact tail-patch lineage, the vendored upstream
subset, all stored interval logs, every finite row, the full error budget,
normalizer/correction gates, and the exact target assembly.  It must end with

```text
RESULT: STORED CANDIDATE PASS
```

For a portable fresh compile/replay:

```sh
docker build -t dbn-lambda-01787854-review .
docker run --rm -v "$PWD:/work" -w /work \
  dbn-lambda-01787854-review
```

It must end with:

```text
RESULT: CONTAINER REVIEW PASS
```

The historical sealed-run image is recorded in `ENVIRONMENT.txt`.  The
original host-side replay command remains
`./scripts/run_interval_verifiers.sh`.

The expensive full finite replay is:

```sh
mkdir replay/full_sweep
IMAGE=dbn-lambda-01787854-review ALLOW_UNPINNED_IMAGE=1 \
  ./scripts/run_full_sweep.sh replay/full_sweep
```

It regenerates every finite row and compares all `N/L12/GT089` tuples
with the sealed evidence.  The runner first proves that its Docker bind
mount is host-visible, preventing silent VM-private `/private/tmp`
output.

## Package map

- `certificates/`: all \(3,149,013\) compressed finite rows.
- `src/`: the stored and compile-switch Triangle producers.
- `verifiers/`: finite/error, direct-Dini, normalizer/correction, tail,
  stored-log, and exact-assembly verifiers.
- `logs/`: stored 120/160/180/256-bit replay outputs.
- `provenance/`: theorem notes, independent implementations, and
  upstream analytic notes.
- `scripts/`: fresh interval and complete finite replay commands.
- `vendor/dbn21a/`: version-locked upstream criterion, error, site, and
  winding review packages.
- `vendor/deposited/`: pristine source used by the target tail patch.
- `references/`: the versioned upstream dbn21a paper.
- `REVIEW_SCOPE.md`: ordered referee workflow and evidence boundaries.
- `OPEN_REVIEW_QUESTIONS.md`: known mathematical pressure points.

Start mathematical review with `REVIEW_SCOPE.md`, then `PROOF_NOTE.md` and
the two Triangle theorem notes under `provenance/`.
