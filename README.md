# Unreviewed computer-assisted proof candidate for \(\Lambda\le0.1787854\)

> **Status.** This private repository presents an **unreviewed
> computer-assisted candidate for an unconditional proof**. It is designed to
> use no unproved conjecture, but its cited-theorem applications, new lemmas,
> proof-to-code correspondence, and interval computations have not yet been
> independently validated. Therefore the bound below is not an established
> theorem, has not been peer reviewed, and is not a public announcement.

The proposed conclusion is

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

The intended logical form is unconditional: the proposed argument does not
assume the Riemann hypothesis or another unproved conjecture. It uses the
published Platt--Trudgian finite verification of RH, the published Polymath
Theorems 1.2 and 1.3, and the interval certificates and elementary lemmas in
this repository. If independent review confirms the cited-theorem
applications, the new lemmas, the proof-to-code correspondence, and the
computations, the resulting proof would be unconditional. Until then, this
repository must be described as a **candidate for an unconditional proof**,
not as an unconditional result.

This positive upper bound is not a proof of RH.

## Proof architecture

The package proposes suppliers for the three hypotheses of Polymath Theorem
1.2 in its canonical order.

1. **Verified-height hypothesis (i).** Platt--Trudgian verify RH through
   \(T_{\rm PT}=3000175332800\). The criterion needs only
   \(X/2=3000000092913.5\), leaving the exact margin
   \(350479773/2\).
2. **Final-time right-half-line hypothesis (ii).** The candidate argues that,
   at \(t=t_0\), the finite Triangle certificates cover all windows
   \(N=690988,\ldots,3840000\), and the standalone tail lemma covers every
   \(N\ge3840000\). The two lanes overlap on the complete
   \(N=3840000\) window. Together they are intended to prove nonvanishing for
   \[
   x\ge X+\sqrt{1-y_0^2},\qquad
   y_0\le y\le\sqrt{1-2t_0}.
   \]
3. **Intermediate-time barrier hypothesis (iii).** The candidate uses a
   fail-closed Arb certificate intended to prove
   \[
   H_t(z)\ne0
   \quad\text{on}\quad
   [X,X+1]+i[0.1809,1],\quad 0\le t\le t_0.
   \]
   This closed rectangle contains the complete curved barrier required by
   Theorem 1.2.

If these three suppliers and their theorem weld are validated, Theorem 1.2
would give \(\Lambda\le t_0+y_0^2/2=0.1787854\).

Some historical notes under `vendor/` state older conditional implications
that did not themselves certify hypotheses (ii) and (iii). They are retained
as provenance; the new finite, tail, and barrier arguments are the proposed
suppliers that require independent review.

## Decisive certified margins

- The \(3,149,013\)-row finite scan has
  \[
  T_{\min}=0.000000791366,\qquad
  E_{\max}\le0.000000233494905212337849,
  \]
  hence
  \[
  T_{\min}-E_{\max}
  \ge0.000000557871094787>0.
  \]
- One standalone FLINT/Arb implementation, run at both 256 and 512 bits,
  proves
  \(D<0.999721\) and a normalized post-error margin greater than
  \(0.00017352\). A separate Python interval implementation supplies
  cross-implementation corroboration.
- The barrier uses an approximation allowance \(0.00125\). A separate
  256-bit Arb calculation bounds the complete Theorem 1.3 error, using the
  conservative Proposition 6.6(vi) corollary,
  by
  \[
  0.000356523011600040<0.00125.
  \]
- All 883 consecutive closed time prisms pass. The independently parsed
  minimum prism margin has certified lower bound
  \(0.519849894613872543374989997\), and the final coverage endpoint contains
  \(129/800\). Complete Linux/GCC/FLINT 3.0.1 and
  macOS/Clang/FLINT 3.6.0 replays both pass the strict 54-check parser.

These margins are rigorous interval inequalities in the recorded
certificates; the rounded decimals above are for orientation.

## New theorem-level bridges in this package

- `NATIVE_BINDING.md` proves by exact Dirichlet convolution that each positive
  stored Triangle floor is already a lower bound for the paper's normalized
  \(|f_t|\). No extra Euler-factor conversion is needed.
- `ERROR_CONSTANT_WELD.md` derives the conservative \(10.50\) effective-error
  constant directly from Proposition 6.6(vi), avoiding reliance on the
  displayed \(10.44\) in equation (24).
- `WINDOW_FREEZE_THEOREM.md` proves the conservative directions of the
  per-window \(x\)-freeze and the exact half-open endpoint coverage.
- `TAIL_LEMMA.md` states and proves the all-\(N\), all-\(y\) tail contraction
  theorem consumed by a standalone FLINT/Arb implementation.
- `DERIVATIVE_BOX_LEMMA.md` proves the uniform spatial-envelope,
  discrete-sum, and holomorphic-quadrature contracts behind the barrier
  derivative bounds.
- `BARRIER_CERTIFICATE.md` gives the closed-prism, interpolation, winding,
  coefficient-provenance, Taylor-remainder, effective-error, and
  \(t=0\)-continuity arguments for the barrier.

Historical standard-majorant, site-glue, and winding artifacts under
`vendor/` are retained for provenance only. They are not proof inputs for
the new native binding, exact site coverage, or closed barrier certificate.
The target error paths use \(x-6.66\) for \(e_A+e_B\) and the conservative
Proposition 6.6(vi) corollary with \(x-12\) and \(10.50\) for \(e_{C,0}\).

## Start here

For mathematical review, read in this order:

1. [Referee manuscript (PDF)](output/pdf/dbn_lambda_01787854_candidate_audit.pdf)
2. [`PROOF_NOTE.md`](PROOF_NOTE.md)
3. [`OPEN_REVIEW_QUESTIONS.md`](OPEN_REVIEW_QUESTIONS.md)
4. [`CANDIDATE_PARAMETERS.md`](CANDIDATE_PARAMETERS.md)
5. [`NATIVE_BINDING.md`](NATIVE_BINDING.md)
6. [`ERROR_CONSTANT_WELD.md`](ERROR_CONSTANT_WELD.md)
7. [`WINDOW_FREEZE_THEOREM.md`](WINDOW_FREEZE_THEOREM.md)
8. [`TAIL_LEMMA.md`](TAIL_LEMMA.md)
9. [`DERIVATIVE_BOX_LEMMA.md`](DERIVATIVE_BOX_LEMMA.md)
10. [`BARRIER_CERTIFICATE.md`](BARRIER_CERTIFICATE.md)
11. the Polymath and Platt--Trudgian papers listed in
    [`BIBLIOGRAPHY.md`](BIBLIOGRAPHY.md)

[`REVIEW_SCOPE.md`](REVIEW_SCOPE.md) gives a referee workflow and separates
theorem review from software replay. [`MAXIMUM_CHECKS.md`](MAXIMUM_CHECKS.md)
records the strongest checks performed before handoff and the final-seal
checks that must remain green. Reviewers should also read
[`ADVERSARIAL_REVIEW_PROTOCOL.md`](ADVERSARIAL_REVIEW_PROTOCOL.md) for the
dependency blueprint, boundary matrix, mutation catalogue, and independent
recomputation standard. They should also read
[`CITATION.md`](CITATION.md), [`REVIEW_TERMS.md`](REVIEW_TERMS.md), and
[`THIRD_PARTY.md`](THIRD_PARTY.md). [`SECURITY.md`](SECURITY.md) states the
private reporting, execution, integrity, and secret-handling boundaries.
[`CONTAINER_IMAGE.md`](CONTAINER_IMAGE.md) specifies the pinned local build
and release-attested OCI digest verification.

The release-grade referee manuscript is generated deterministically from
`paper/generate_paper.py`. See `paper/README.md` for generation and visual-QA
commands.

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
of peer review or proof that the proposed argument is unconditional. The
phrase `UNCONDITIONAL CANDIDATE` in the machine transcript names the intended
logical form of the candidate only.

## Fresh replays

Portable container replay:

```sh
docker build --platform linux/amd64 -t dbn-lambda-01787854-review .
mkdir -p replay/container-review
docker run --rm --platform linux/amd64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
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

Fresh 256- and 512-bit runs of the standalone Arb tail checker:

```sh
./scripts/run_tail_arb.sh replay/tail_arb
```

Expensive regeneration of every finite row:

```sh
docker build --platform linux/amd64 -t dbn-lambda-01787854-review .
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
- `scripts/fetch_release_image_oci.py` and
  `scripts/verify_release_image_archive.py`: complete offline-image
  reconstruction and fail-closed verification.
- `references/`: the versioned upstream proof record.
- `ADVERSARIAL_REVIEW_PROTOCOL.md`: falsification and independent-sign-off
  protocol.
- `SECURITY.md`: private reporting and execution policy.
- `CONTAINER_IMAGE.md`: canonical container and exact verified image binding.
- `paper/`: deterministic source for the referee manuscript.
- `output/pdf/`: release-grade referee manuscript.

The proper description of this repository remains: **an unreviewed
computer-assisted candidate for an unconditional proof**, awaiting
independent mathematical and computational review. The proposed bound is not
an established theorem.
