# Review-subset note

This directory is a byte-preserving subset of the Mosaic Intelligence
dbn21a certificate archive from Zenodo record 21175533.

`UPSTREAM_MANIFEST.sha256` is the complete 760-entry archive manifest.
`SELECTED_MANIFEST.sha256` contains only entries present in this subset and is
the file used by the local verifier.

Consumed target-review packages:

- `record/criterion_theorem`;
- `record/error_terms_audit`;
- `certified1965/site_glue` and `site_glue_secondline`;
- `certified1875/windslab165_v2` and
  `windslab165_corner_secondline`.

Historical context only:

- `record/binding`;
- `record/binding_secondline`.

The historical binding packages use a route that is not consumed by the
candidate's direct multi-prime Triangle argument.  Their presence is for
traceability, not a target `PASS` gate.

See the repository-root `UPSTREAM.md`, `THIRD_PARTY.md`, and
`OPEN_REVIEW_QUESTIONS.md`.

