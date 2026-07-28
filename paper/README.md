# Paper artifacts

## Deterministic repository referee manuscript

Create or activate the repository virtual environment, install the
hash-locked paper dependencies, and generate the deterministic release-grade
manuscript with:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes -r paper/requirements.txt
python3 paper/generate_paper.py
```

The stable output path is:

```text
output/pdf/dbn_lambda_01787854_candidate_audit.pdf
```

The generator uses ReportLab invariant mode, PDF standard fonts, and no
operating-system font dependency. The version used for the committed PDF is
pinned in `paper/requirements.txt`.

Render and inspect every page before sealing:

```sh
mkdir -p tmp/pdfs/rendered
pdftoppm -png -r 150 \
  output/pdf/dbn_lambda_01787854_candidate_audit.pdf \
  tmp/pdfs/rendered/page
pdfinfo output/pdf/dbn_lambda_01787854_candidate_audit.pdf
```

`pdftoppm` and `pdfinfo` are supplied by Poppler and are therefore external
system tools rather than Python dependencies.

ReportLab invariant mode fixes the PDF metadata creation and modification
timestamps to a synthetic value for byte stability. The visible date and the
repository commit identify the actual review snapshot.

The PDF is a referee guide and proof summary. The repository proof notes,
source code, directed transcripts, and cited published papers remain
authoritative.

## Supplied theorem-style exposition

`external/gomila-proof-exposition.pdf` is a separately supplied
theorem-style exposition. Its LaTeX source and claimed finite-scan
supplement were not supplied, so the original PDF is preserved byte-for-byte
rather than regenerated here.

Read `external/README.md` before the PDF. That cross-check records the exact
artifact hash, binds the audited baseline tag and commit, lists required
corrections, and distinguishes the useful exposition from independent
acceptance. The supplied PDF is not authoritative when it conflicts with
the sealed repository evidence.
