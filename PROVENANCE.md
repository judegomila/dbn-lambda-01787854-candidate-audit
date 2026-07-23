# Provenance and replay boundary

## Pinned runtime

The FLINT/Arb computations use:

```text
dbn21a-flint
sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538
```

The Python interval verifiers use `mpmath==1.4.1`.
The root `Dockerfile` supplies a portable review environment; exact package
details and the historical sealed-run image are recorded in
`ENVIRONMENT.txt`.

## Finite producer

`src/lemma_sweep_p235711.c` is the compile-switch source used by the
complete replay script.  `-DTRIANGLE_WEIGHT` selects the direct Triangle
kernel.

The earliest P11 evidence was generated from the equivalent hard-wired
source `src/lemma_sweep_p235711_triangle_stored.c`.  The only material
difference is that the compile-switch source retains the older sharp
kernel behind the opposite preprocessor branch and prints a kernel tag.
The sealed P11 rows are compared by exact `N/L12/GT089` tuples.

The later P7/P5/P23 evidence was regenerated into a host-visible
workspace directory after discovering that Docker Desktop/Colima maps a
VM-private `/private/tmp` silently.  Both replay scripts now perform a
write/read bind-mount preflight before starting expensive work.

## New direct theorem

The primary verifier in this package is
`verifiers/verify_triangle_y_dini_arb.c`.  Before sealing, its SHA-256
was independently reported as:

```text
7163fc8a6c13cca63e60e7d5cada22ba2a3b786fd5fc42be379db3e09c487a42
```

It was independently compiled at 180 and 256 bits in the pinned image.
The two runs have identical pattern, rectangle, and split counts.

Cross-checks are retained under `provenance/`:

- `verify_triangle_y_monotonicity_independent.py`, one implementation run
  with separate head and tail decompositions;
- `p11_triangle_tail_cells_iv.py`, using the more conservative
  \(|u'|\) bound on a stronger all-P11 tail domain;
- the formal theorem note and the normalizer/correction note.

The stale prototype that omitted the composite-divisor
\(\sum_{p\mid d}\log^2p\) factor is not included and is not evidence.

## Tail source lineage

The pristine deposited second-line engine is stored at
`vendor/deposited/assembly1875_1891_secondline.py`.  The target 160- and
256-bit files alter only their precision, maximum exact-convolution head, and
one delimited candidate block.  `verifiers/verify_tail_patch_provenance.py`
reverses those changes and requires byte-for-byte equality with the deposited
source.  See `TAIL_PROVENANCE.md`.

## Inherited analytic sources

The copied review notes originate in the Mosaic Intelligence dbn21a
deposit:

```text
Zenodo record: https://zenodo.org/records/21175533
dbn21a-certificates.zip SHA-256:
d6f76c7351a8b1be0ae09de27f2a1720eeafa105eba3035a05823bf1a9563957
extracted MANIFEST.sha256 SHA-256:
dee28651ec9f5295d8c28d9d045e2d2049753cc9f8e84ab0286dc6491fb8de91
```

The relevant copied notes are:

- `ERROR_TERMS_AUDIT.upstream.md`;
- `RECORD_BINDING.upstream.md`;
- `STRETCH_BINDING.upstream.md`;
- `SEAM_KAPPA.upstream.md`;
- `THEOREM_LAMBDA_CRITERION.upstream.md`;
- `SITE_GLUE.upstream.md`.

They are supplied for review context.  The new direct theorem deliberately
does not consume the invalid multi-prime standard-shape step from
`STRETCH_BINDING` P1.

A byte-preserving subset of the upstream executable review packages is
vendored under `vendor/dbn21a/`.  It includes the criterion theorem,
effective-error audit, site glue, and winding slab, together with their
recorded checks.  `UPSTREAM.md` gives the exact archive and manifest locks.
The record-binding directories are retained only as historical interface
context and are not target `PASS` gates.

## Scope

The SHA-256 manifest seals every stable file except the manifest itself
and disposable `replay/` output.  A green replay establishes artifact
integrity and local implementation consistency; it is not a substitute
for independent review of the mathematical theorem bindings.  Known open
questions are listed in `OPEN_REVIEW_QUESTIONS.md`.
