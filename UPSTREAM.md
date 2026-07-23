# Upstream artifact lock

## Versioned record

- Record: <https://zenodo.org/records/21175533>
- DOI: <https://doi.org/10.5281/zenodo.21175533>
- Publication date: 2026-07-03
- License recorded by Zenodo: CC BY 4.0

The independently recorded downloads are:

| file | bytes | Zenodo MD5 | SHA-256 |
|---|---:|---|---|
| `main.pdf` | 239740 | `582c7644a252d6d77fdd8c1d9857cbe3` | `10648df3b7222397d88ec5c32681138898c198122cf002e4fb08eac60c9a2477` |
| `dbn21a-certificates.zip` | 196150822 | `70afd79715d3c3e82c68d62395d468a3` | `d6f76c7351a8b1be0ae09de27f2a1720eeafa105eba3035a05823bf1a9563957` |

The extracted archive-root `MANIFEST.sha256` has 760 entries and SHA-256:

```text
dee28651ec9f5295d8c28d9d045e2d2049753cc9f8e84ab0286dc6491fb8de91
```

An exact copy is stored as
`vendor/dbn21a/UPSTREAM_MANIFEST.sha256`.  The filtered
`vendor/dbn21a/SELECTED_MANIFEST.sha256` verifies every vendored file that
appears in that original manifest.

## Vendored review subset

The repository carries the packages needed to inspect the inherited
interfaces locally:

- `certificates/record/criterion_theorem/`;
- `certificates/record/error_terms_audit/`;
- `certificates/certified1965/site_glue/`;
- `certificates/certified1965/site_glue_secondline/`;
- `certificates/certified1875/windslab165_v2/`;
- `certificates/certified1875/windslab165_corner_secondline/`.

The `record/binding/` and `record/binding_secondline/` directories are
included only as historical theorem-interface context.  Their original
standard-majorant route is not consumed by the target multi-prime direct
Triangle argument and must not be treated as a green target gate.

Run:

```sh
./scripts/verify_upstream_subset.sh
```

This checks provenance and reruns the consumed upstream arithmetic packages.
The corner second line is provenance-checked but deliberately not promoted to
a target-green gate: it samples only five corners, and its original wrapper
rewrites deterministic combined JSON outputs.  Passing output establishes
artifact identity and internal replay only.  It does not settle the
winding-rigor questions in `OPEN_REVIEW_QUESTIONS.md`.

## Full archive

The 196 MB archive is intentionally not committed.  A reviewer who wants the
entire upstream campaign should download it from the versioned record, verify
the archive SHA-256 above, extract it, and then verify its root manifest:

```sh
sha256sum -c MANIFEST.sha256
```

On macOS:

```sh
shasum -a 256 -c MANIFEST.sha256
```
