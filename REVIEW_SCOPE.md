# External review scope

## Review status

This is a private referee package for the **unreviewed computer-assisted
unconditional proof candidate**

\[
\Lambda\le\frac{893927}{5000000}=0.1787854.
\]

It is not an established theorem, has not been peer reviewed, and should not
be described as a public result. The package is called “unconditional”
because its candidate proof assumes no unproved conjecture; that description
does not prejudge whether the new proof is correct.

The requested review has two separate parts:

1. verify the mathematics and the proof-to-code correspondence; and
2. reproduce the decisive computations in an independent environment.

A green replay answers the second question only relative to the encoded
predicates. It does not substitute for the first.

## Ten-minute orientation

Read:

1. `README.md` for the claim and package map;
2. `PROOF_NOTE.md` for the complete theorem chain;
3. `OPEN_REVIEW_QUESTIONS.md` for the requested referee decisions;
4. `CANDIDATE_PARAMETERS.md` for exact domains and margins; and
5. `BIBLIOGRAPHY.md` for the two published theorem inputs.

Then run:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes -r requirements.txt
./verify.sh
```

The assembly portion must report:

```text
RESULT: UNCONDITIONAL CANDIDATE ASSEMBLY PASS
CONCLUSION: Lambda <= 893927/5000000 = 0.1787854.
STATUS: unreviewed computer-assisted unconditional proof candidate; not an established theorem.
```

The status line is as important as the numerical conclusion.

## Recommended mathematical audit order

### 1. Canonical criterion and verified height

Read:

- Polymath Theorem 1.2 in arXiv:1904.12438v2;
- `PROOF_NOTE.md` sections 1--3 and 7;
- `vendor/dbn21a/certificates/record/criterion_theorem/`; and
- Platt--Trudgian's finite RH-verification theorem.

Confirm the \(x=2T\) normalization and the exact matching of the three
Theorem 1.2 hypotheses:

- (i) verified zeta height;
- (ii) final-time right-half-line nonvanishing; and
- (iii) intermediate-time curved barrier.

The exact height margin is \(350479773/2\).

### 2. Closed intermediate-time barrier

Read:

- `DERIVATIVE_BOX_LEMMA.md`;
- `BARRIER_CERTIFICATE.md`;
- `barrier/src/TloopSinglemat_closed_cert.c`;
- `barrier/src/StoredSumSinglemat_interval.c`;
- `barrier/src/StoredSumTaylorTail_cert.c`;
- `barrier/src/verify_uniform_error_01787854.c`; and
- `verifiers/verify_barrier_binding.py`.

Audit the complete-box derivative envelopes, exact-head/decreasing-tail
sum bound, holomorphic quadrature callbacks, midpoint-disk interpolation
lemma, complete-prism \(t\)-derivative bound, winding/argument-principle
step, \(B_t\ne0\) normalization, Theorem 1.3 limit at \(t=0\), and
coefficient/Taylor provenance.

This target proof consumes the new 883-prism fail-closed certificate. It does
not consume the historical midpoint-printed winding or site-glue artifacts
under `vendor/`.

### 3. Finite final-time lane

Read:

- `NATIVE_BINDING.md`;
- `WINDOW_FREEZE_THEOREM.md`;
- `provenance/TRIANGLE_Y_DINI_THEOREM.independent.md`;
- `provenance/TRIANGLE_NORMALIZER_CORR_MONOTONICITY.md`;
- `src/lemma_sweep_p235711.c`; and
- the corresponding verifiers under `verifiers/`.

The core obligations are:

- the exact real-coefficient Euler convolutions, including
  \(\overline E C_0\);
- the sign used to replace \(|E|\) by \(M_N\);
- the upper-Dini argument at coefficient zeros and the passage to global
  monotonicity;
- monotonicity of the native normalizer and correction;
- the conservative directions of the \(x\)-window freeze; and
- the half-open window convention at every endpoint.

The target effective-error path uses the paper's \(x-12\) denominator in
equation (24). A historical \(x-6.66\) substitution is not consumed.

### 4. Infinite final-time lane

Read:

- `TAIL_LEMMA.md`;
- `verifiers/verify_tail_arb.c`;
- `verifiers/verify_tail_arb_logs.py`;
- `TAIL_PROVENANCE.md`; and
- the older Python interval tail scripts as corroboration.

Audit the endpoint-cap lemma, exact convolution partition, harmless
nonnegative `OV` padding, all-\(N\) monotonicity gates, full-height transfer,
complete \(t\)-box evaluation, and exact error formulas.

The primary target certificates are independent FLINT/Arb runs at 256 and
512 bits. The result is not dependent only on two precisions of the same
`mpmath.iv` program.

### 5. Site coverage and final weld

Return to:

- `WINDOW_FREEZE_THEOREM.md`;
- `verifiers/verify_window_freeze.py`;
- `verifiers/verify_assembly_1787854.py`; and
- `PROOF_NOTE.md` sections 4--7.

Confirm:

- \(X+\sqrt{1-y_0^2}\) is strictly inside \(W_{690988}\);
- the finite windows cover through \(x_{3840001}\) with the stated
  half-open convention;
- the tail starts at \(x_{3840000}\), producing a complete overlap;
- the closed rectangle contains the full curved barrier; and
- no theorem hypothesis has been renamed, swapped, or silently weakened.

## Computational replay levels

### Level A: stored fail-closed verification

Run:

```sh
./verify.sh
```

This checks the repository seal, exact source provenance, all stored finite
rows, decisive interval logs, new theorem-source contracts, and the final
assembly.

### Level B: portable clean container

Run:

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

The container recompiles and reruns the bounded-cost verifiers. It should
finish with:

```text
RESULT: CONTAINER REVIEW PASS
```

### Level C: fresh closed barrier

Run:

```sh
./scripts/run_barrier_replay.sh replay/barrier
```

This independently regenerates all \(7,688\) stored coefficient components,
checks their containment, recomputes the factorial Taylor tail and uniform
Theorem 1.3 error, and certifies all 883 closed time prisms.

### Level D: fresh standalone Arb tail

Run:

```sh
./scripts/run_tail_arb.sh replay/tail_arb
```

This compiles and runs the standalone fixed-domain tail checker at 256 and
512 bits and subjects both transcripts to the strict parser.

### Level E: complete finite regeneration

Run:

```sh
docker build -t dbn-lambda-01787854-review .
review_image_id=$(docker image inspect --format '{{.Id}}' \
  dbn-lambda-01787854-review)
IMAGE=dbn-lambda-01787854-review \
EXPECTED_IMAGE_ID="$review_image_id" \
  ./scripts/run_full_sweep.sh replay/full_sweep
```

The runner requires a fresh, nonexistent output path and the locked
image ID unless an unpinned image is explicitly authorized. It regenerates
every one of the \(3,149,013\) finite rows and compares the canonical tuples
with all 15 sealed shards. See `MAXIMUM_CHECKS.md` for the completed
pre-handoff replay and direct-boundary stress checks.

## Evidence hierarchy

For each component, distinguish:

1. the mathematical statement;
2. its proof or reduction;
3. the implementation of the reduction;
4. the directed interval output;
5. the parser and final assembly; and
6. the integrity seal binding those files.

Agreement at levels 4--6 cannot repair an error at levels 1--3. Conversely,
a mathematically correct reduction still needs a faithful, fail-closed
implementation.

## What is not claimed

The repository does not claim:

- that the result has passed independent review;
- that the Polymath or Platt--Trudgian papers have been re-proved here;
- that a finite set of software replays excludes every toolchain fault;
- that the result establishes RH;
- priority, novelty, or suitability for public announcement.

The desired referee report should identify any fatal gap, required repair,
or independently accepted component. `REVIEWER_REPORT_TEMPLATE.md` may be
used for a concise response.
