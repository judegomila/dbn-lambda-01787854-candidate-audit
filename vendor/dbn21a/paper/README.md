# `paper/`

`main.pdf` — the camera-ready record paper *"A certified unconditional
upper bound Λ ≤ 0.1965 for the de Bruijn–Newman constant"* (Mosaic
Intelligence, 2026).

**Manifest note.** `main.pdf` is intentionally **excluded from
`MANIFEST.sha256`**. The paper's "Artifacts" section quotes the digest of
`MANIFEST.sha256` itself as the bundle's root-of-trust; if the PDF were
listed in that manifest, its hash would depend on a number printed inside
it — a self-reference. The PDF is therefore also deposited as a separate
file alongside the bundle archive; verify its integrity against the
deposit's published file checksum. Every certificate, verifier, manifest,
and front-page document in the bundle *is* pinned by `MANIFEST.sha256`.
