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

## Direct finite theorem

The primary verifier in this package is
`verifiers/verify_triangle_y_dini_arb.c`.  Its final source hash is recorded
by the root package seal.

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

The primary target tail is the standalone theorem and FLINT/Arb implementation
in `TAIL_LEMMA.md` and `verifiers/verify_tail_arb.c`.  It reconstructs its
153,814 exact coefficients rather than loading deposited tail values, and its
256- and 512-bit outputs are independently parsed by
`verifiers/verify_tail_arb_logs.py`.

The pristine deposited second-line engine is stored at
`vendor/deposited/assembly1875_1891_secondline.py`.  The target 160- and
256-bit files alter only their precision, maximum exact-convolution head, and
one delimited candidate block.  `verifiers/verify_tail_patch_provenance.py`
reverses those changes and requires byte-for-byte equality with the deposited
source.  See `TAIL_PROVENANCE.md`.

## Closed-barrier lineage

The target closed-barrier implementation is
`barrier/src/TloopSinglemat_closed_cert.c`, a modified LGPL Polymath source.
Its paired stored-sum generator is
`barrier/src/StoredSumSinglemat_interval.c`.  The target repair adds
fail-closed quadrature, interval minima, exact closed time-prism coverage,
Taylor and approximation errors, a complete spatial derivative envelope, and
explicit winding gates.  `BARRIER_CERTIFICATE.md` and
`DERIVATIVE_BOX_LEMMA.md` state the mathematical interface; the fresh replay
regenerates all 7,688 stored-sum components and checks all 883 prisms.  The
historical vendored winding binary and its success marker are not consumed.
The archived matrix input retains its header and all 62 numerical rows but
omits the upstream program's non-mathematical `cpu/wall` profiler footer.

The canonical stored barrier evidence is the complete
Linux/GCC/FLINT 3.0.1 transcript
`barrier/certificates/barrier_target_closed.log` (SHA-256
`2d010f70902dca1627f40ddcd68f3954b37fd9596f7840787415eeafb20805f4`).
The complete independent macOS/Clang/FLINT 3.6.0 replay is retained at
`barrier/certificates/barrier_target_closed_macos_arm64_flint36.log`
(SHA-256
`34f8ed82bcb47a3783099206f67599cf975b7d28cfa398d8a765118311954db7`).
The assembly strict-parses both.  The macOS transcript's anomalous final
`cpu` profiler field is a non-mathematical platform artifact and is ignored;
the certificate parser consumes neither timing field.

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

`scripts/seal.py` defines the stable inventory, rejects symlinks and extra or
missing stable files, and verifies `SHA256SUMS`.  It excludes the manifest
itself; the repository-local transient roots `.git/`, `.venv/`, `replay/`,
and `tmp/`; and Python cache directories named `__pycache__/`.  Everything
else is sealed, and common stray editor, bytecode, object, and output files
are rejected rather than silently excluded.  The final Git commit binds the
manifest.

A green replay establishes artifact integrity and local implementation
consistency; it is not a substitute for independent review of the
mathematical theorem bindings.  The questions a referee should actively
challenge are listed in `OPEN_REVIEW_QUESTIONS.md`.
