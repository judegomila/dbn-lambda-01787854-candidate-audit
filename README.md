# Unreviewed computer-assisted unconditional proof candidate at \(0.1787854\)

> **Status.** This private repository is an **unreviewed
> computer-assisted unconditional proof candidate**. It is not an established
> theorem, has not been peer reviewed, and is not a public announcement.

The candidate conclusion is

\[
\boxed{\Lambda\le
\frac{893927}{5000000}=0.1787854}.
\]

The exact parameters are

\[
X=6000000185827,\qquad
t_0=\frac{129}{800}=0.16125,\qquad
y_0^2=\frac{87677}{2500000}=0.0350708,
\]

where \(y_0\) is the positive square root. Thus

\[
t_0+\frac{y_0^2}{2}
=\frac{893927}{5000000}.
\]

Here “unconditional” means that the assembled argument does not assume the
Riemann hypothesis or another unproved conjecture. It uses the published
Platt--Trudgian finite verification of RH, the published Polymath Theorems
1.2 and 1.3, and the interval certificates and elementary lemmas in this
repository. The word does **not** mean that the new argument has already
been independently checked. If any cited theorem has been misapplied, any
new lemma is wrong, or any implementation fails to certify its stated
mathematical predicate, the candidate conclusion does not follow.

This positive upper bound is not a proof of RH.

## Proof architecture

The package supplies the three hypotheses of Polymath Theorem 1.2 in its
canonical order.

1. **Verified-height hypothesis (i).** Platt--Trudgian verify RH through
   \(T_{\rm PT}=3000175332800\). The criterion needs only
   \(X/2=3000000092913.5\), leaving the exact margin
   \(350479773/2\).
2. **Final-time right-half-line hypothesis (ii).** At \(t=t_0\), the finite
   Triangle certificates cover all windows
   \(N=690988,\ldots,3840000\), and the standalone tail lemma covers every
   \(N\ge3840000\). The two lanes overlap on the complete
   \(N=3840000\) window. Together they prove nonvanishing for
   \[
   x\ge X+\sqrt{1-y_0^2},\qquad
   y_0\le y\le\sqrt{1-2t_0}.
   \]
3. **Intermediate-time barrier hypothesis (iii).** A fail-closed Arb
   certificate proves
   \[
   H_t(z)\ne0
   \quad\text{on}\quad
   [X,X+1]+i[0.1809,1],\quad 0\le t\le t_0.
   \]
   This closed rectangle contains the complete curved barrier required by
   Theorem 1.2.

The theorem then gives
\(\Lambda\le t_0+y_0^2/2=0.1787854\).

## Decisive certified margins

- The \(3,149,013\)-row finite scan has
  \[
  T_{\min}=0.000000791366,\qquad
  E_{\max}\le0.000000233494905212335514,
  \]
  hence
  \[
  T_{\min}-E_{\max}
  \ge0.000000557871094787>0.
  \]
- The independent 256- and 512-bit Arb tail certificates prove
  \(D<0.999721\) and a normalized post-error margin greater than
  \(0.00017352\).
- The barrier uses an approximation allowance \(0.00125\). A separate
  256-bit Arb calculation bounds the complete displayed Theorem 1.3 error
  by
  \[
  0.000356523011600037<0.00125.
  \]
- All 883 consecutive closed time prisms pass. The independently parsed
  minimum prism margin is greater than
  \(0.519849894613872543374989997\), and the final coverage endpoint contains
  \(129/800\). Complete Linux/GCC/FLINT 3.0.1 and
  macOS/Clang/FLINT 3.6.0 replays both pass the strict 54-check parser.

These margins are rigorous interval inequalities in the recorded
certificates; the rounded decimals above are for orientation.

## New theorem-level bridges in this package

- `NATIVE_BINDING.md` proves by exact Dirichlet convolution that each positive
  stored Triangle floor is already a lower bound for the paper's normalized
  \(|f_t|\). No extra Euler-factor conversion is needed.
- `WINDOW_FREEZE_THEOREM.md` proves the conservative directions of the
  per-window \(x\)-freeze and the exact half-open endpoint coverage.
- `TAIL_LEMMA.md` states and proves the all-\(N\), all-\(y\) tail contraction
  theorem consumed by an independent FLINT/Arb implementation.
- `DERIVATIVE_BOX_LEMMA.md` proves the uniform spatial-envelope,
  discrete-sum, and holomorphic-quadrature contracts behind the barrier
  derivative bounds.
- `BARRIER_CERTIFICATE.md` gives the closed-prism, interpolation, winding,
  coefficient-provenance, Taylor-remainder, effective-error, and
  \(t=0\)-continuity arguments for the barrier.

Historical standard-majorant, site-glue, and winding artifacts under
`vendor/` are retained for provenance only. They are not proof inputs for
the new native binding, exact site coverage, or closed barrier certificate.
The target error paths use \(x-6.66\) in equation (23) and the paper's
\(x-12\) in equation (24).

## Start here

For mathematical review, read in this order:

1. `PROOF_NOTE.md`
2. `OPEN_REVIEW_QUESTIONS.md`
3. `CANDIDATE_PARAMETERS.md`
4. `NATIVE_BINDING.md`
5. `WINDOW_FREEZE_THEOREM.md`
6. `TAIL_LEMMA.md`
7. `DERIVATIVE_BOX_LEMMA.md`
8. `BARRIER_CERTIFICATE.md`
9. the Polymath and Platt--Trudgian papers in `BIBLIOGRAPHY.md`

`REVIEW_SCOPE.md` gives a referee workflow and separates theorem review from
software replay. `MAXIMUM_CHECKS.md` records the strongest checks performed
before handoff and the final-seal checks that must remain green.

## Quick stored verification

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes -r requirements.txt
./verify.sh
```

The assembly transcript must include

```text
RESULT: UNCONDITIONAL CANDIDATE ASSEMBLY PASS
STATUS: unreviewed computer-assisted unconditional proof candidate; not an established theorem.
```

“PASS” means that the encoded predicates were certified; it is not a claim
of peer review.

## Fresh replays

Portable container replay:

```sh
docker build -t dbn-lambda-01787854-review .
mkdir -p replay/container-review
docker run --rm --network none --read-only \
  --user "$(id -u):$(id -g)" \
  --tmpfs /tmp:rw,exec,nosuid,size=4g \
  -e REVIEW_OUTPUT=/review-output/evidence \
  -v "$PWD:/work:ro" \
  -v "$PWD/replay/container-review:/review-output" \
  -w /work dbn-lambda-01787854-review
```

Fresh coefficient regeneration and all 883 barrier prisms:

```sh
./scripts/run_barrier_replay.sh replay/barrier
```

Fresh independent 256- and 512-bit Arb tail checks:

```sh
./scripts/run_tail_arb.sh replay/tail_arb
```

Expensive regeneration of every finite row:

```sh
docker build -t dbn-lambda-01787854-review .
review_image_id=$(docker image inspect --format '{{.Id}}' \
  dbn-lambda-01787854-review)
IMAGE=dbn-lambda-01787854-review \
EXPECTED_IMAGE_ID="$review_image_id" \
  ./scripts/run_full_sweep.sh replay/full_sweep
```

The output path must not already exist. The full sweep regenerates all
\(3,149,013\) tuples and compares them with the 15 sealed certificate
shards.

## Package map

- `certificates/`: the complete compressed finite certificate.
- `barrier/`: closed-prism sources, coefficient data, provenance evidence,
  and the sealed 883-prism run.
- `logs/`: finite, Dini, normalizer, Python-tail, Arb-tail, and assembly
  transcripts.
- `src/`: finite Triangle producers.
- `verifiers/`: fail-closed parsers and independent interval checkers.
- `provenance/`: direct all-height proofs and historical audit notes.
- `vendor/`: version-locked upstream material and historical provenance.
- `scripts/`: stored, container, barrier, tail, and full-sweep replay paths.
- `references/`: the versioned upstream proof record.

The proper description of this repository remains: **an unreviewed
computer-assisted unconditional proof candidate**, awaiting independent
mathematical and computational review.
