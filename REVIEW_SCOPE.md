# External review scope

## Review status

This repository is a private referee package for the unreviewed,
computer-assisted candidate

\[
\Lambda\le\frac{893927}{5000000}=0.1787854.
\]

It is not an announcement of an established theorem.  The stored numerical
evidence and fresh interval replay pass, but several theorem-level interfaces
remain deliberately open for external review.  In particular, a green script
does not settle the questions in `OPEN_REVIEW_QUESTIONS.md`.

## Ten-minute orientation

Read, in order:

1. `README.md` for the claim and evidence map.
2. `PROOF_NOTE.md` for the conditional implication.
3. `OPEN_REVIEW_QUESTIONS.md` for the known pressure points.
4. `CANDIDATE_PARAMETERS.md` for the exact row and all closed boxes.

Then run:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes -r requirements.txt
./verify.sh
```

The final line must be:

```text
RESULT: STORED CANDIDATE PASS
```

That command checks the repository seal, the exact provenance of the patched
tail engine, the vendored upstream subset, every stored finite row, decisive
interval logs, and the exact target assembly.

## Container replay

The repository includes a buildable Ubuntu 24.04/FLINT 3 environment:

```sh
docker build -t dbn-lambda-01787854-review .
docker run --rm \
  -v "$PWD:/work" -w /work \
  dbn-lambda-01787854-review
```

The container recompiles the direct Arb verifier at 180 and 256 bits,
compares its output byte-for-byte with the sealed logs, compiles the finite
producer, and freshly reruns the normalizer and tail verifiers.  It must end:

```text
RESULT: CONTAINER REVIEW PASS
```

The historical image used for the sealed runs is separately recorded in
`ENVIRONMENT.txt`.  Its image ID is platform-specific; the repository
Dockerfile is the portable review route.

## Mathematical review layers

### 1. Criterion, height, winding, and site

- `vendor/dbn21a/certificates/record/criterion_theorem/`
- `vendor/dbn21a/certificates/certified1875/windslab165_v2/`
- `vendor/dbn21a/certificates/certified1875/windslab165_corner_secondline/`
- `vendor/dbn21a/certificates/certified1965/site_glue/`
- `vendor/dbn21a/certificates/certified1965/site_glue_secondline/`
- `PROOF_NOTE.md` sections 1, 2, and 8

The winding material is included so that the inherited claim can be reviewed
locally.  Its inclusion is not an endorsement of its rigor; the open coverage
and interval-output questions are listed explicitly in
`OPEN_REVIEW_QUESTIONS.md`.

### 2. Fixed-height finite evidence

- `src/lemma_sweep_p235711.c`
- `certificates/`
- `verifiers/verify_finite_and_binding.py`
- `scripts/run_full_sweep.sh`

The stored path parses all 3,149,013 rows.  The full producer replay is the
expensive optional step:

```sh
mkdir replay/full_sweep
IMAGE=dbn-lambda-01787854-review ALLOW_UNPINNED_IMAGE=1 \
  ./scripts/run_full_sweep.sh replay/full_sweep
```

It is CPU-intensive and machine-dependent; allow hours rather than minutes
and at least 1 GB of free working space.  It was not rerun as part of this
repository-preparation pass.

### 3. Direct all-height Triangle theorem

- `provenance/TRIANGLE_Y_DINI_THEOREM.independent.md`
- `verifiers/verify_triangle_y_dini_arb.c`
- `provenance/verify_triangle_y_monotonicity_independent.py`
- `provenance/p11_triangle_tail_cells_iv.py`

The key issue is whether the branch-free Dini bound and finite cell reduction
really imply global monotonicity on the stated closed domain.

### 4. Native normalization and effective error

- `provenance/TRIANGLE_NORMALIZER_CORR_MONOTONICITY.md`
- `verifiers/verify_triangle_normalizer_corr_iv.py`
- `provenance/ERROR_TERMS_AUDIT.upstream.md`
- `vendor/dbn21a/certificates/record/error_terms_audit/`

The target implication depends on the native Triangle functional being the
correct lower bound for \(|f_t|\) after its built-in normalization and
correction.  This is a theorem-level review item, not something established
merely by the numerical gates.

### 5. Infinite tail

- `TAIL_PROVENANCE.md`
- `vendor/deposited/assembly1875_1891_secondline.py`
- `verifiers/verify_tail_patch_provenance.py`
- `verifiers/verify_tail_1787854_160.py`
- `verifiers/verify_tail_1787854_256.py`

The provenance checker proves that each target is the deposited engine plus
the declared precision/head changes and one delimited candidate block.

### 6. Closed weld and conclusion

- `verifiers/verify_assembly_1787854.py`
- `logs/assembly_1787854.log`
- `PROOF_NOTE.md` section 8

The assembly checks exact arithmetic and source-level parameter agreement.
Documentary theorem interfaces are printed as documentary assertions, not as
numerical `PASS` gates.

## What the automated checks do not establish

- correctness of the cited analytic theorems;
- rigor of midpoint-printed or fail-open upstream winding output;
- independence of two runs of the same `mpmath.iv` implementation;
- the native Triangle-to-\(|f_t|\) theorem-level binding;
- peer review, priority, novelty, or suitability for public announcement.

Use `REVIEWER_REPORT_TEMPLATE.md` for a concise referee response.
