# Third-party provenance and licensing

## Mosaic Intelligence dbn21a bundle

Portions of this repository reproduce or derive from:

- *A certified unconditional upper bound \(\Lambda\le0.1875\) for the
  de Bruijn--Newman constant*;
- creator: Mosaic Intelligence;
- version DOI: <https://doi.org/10.5281/zenodo.21175533>;
- publication date recorded by Zenodo: 2026-07-03;
- license recorded by Zenodo: Creative Commons Attribution 4.0
  International, <https://creativecommons.org/licenses/by/4.0/>.

The copied material includes:

- the selected review packages under `vendor/dbn21a/`;
- `vendor/deposited/assembly1875_1891_secondline.py`;
- the upstream notes under `provenance/*.upstream.md`;
- the adapted finite/tail/assembly verifier lines whose headers identify
  their upstream bases;
- `references/dbn21a-main.pdf`; and
- the package set adapted in the root `Dockerfile`.

Exact archive, manifest, file hashes, and acquisition information are in
`UPSTREAM.md`.

### LGPL Polymath numerical sources and historical binary

`vendor/dbn21a/certificates/certified1875/windslab165_v2/TloopthreadedV4.c`
is separately marked copyright 2018 Association des collaborateurs de
D.H.J. Polymath and licensed under LGPL 2.1 or, at the recipient's option,
any later version.  The corresponding historical `tloop` binary is retained
with its complete source in the same directory.

The repaired target sources
`barrier/src/TloopSinglemat_closed_cert.c` and
`barrier/src/StoredSumSinglemat_interval.c` retain the same notice.  They are
modified descendants, with the changes exposed as ordinary source in this
repository.  The target proof does not execute the historical binary.

The official LGPL 2.1 text is included at
`vendor/licenses/LGPL-2.1-or-later.txt`.  Those files should not be described
as solely CC BY 4.0.

## Reference PDFs

`references/` includes only the redistributable Zenodo PDF
(`dbn21a-main.pdf`, CC BY 4.0).  The Polymath, Platt--Trudgian, and Romik
arXiv PDFs used for the review are distributed by arXiv under its
non-exclusive-distribution 1.0 license, which does not grant this
repository redistribution rights, so they were removed from the tree
before public release.  `references/README.md` records the exact arXiv
URLs and the SHA-256 hashes of the reviewed files so byte-identical
copies can be fetched and verified.  Copyright remains with their
respective authors or publishers.

## mpmath

The Python dependency `mpmath==1.4.1` is distributed under BSD-3-Clause.
Its package hashes are locked in `requirements.txt`.

## SymPy

The Python dependency `sympy==1.12` is distributed under the New BSD
license.  Its package hashes are locked in `requirements.txt`.

## Referee-manuscript dependencies

The deterministic PDF generator uses:

- `reportlab==4.4.9`, distributed under the ReportLab BSD license;
- `pillow==12.3.0`, distributed under the MIT-CMU license; and
- `charset-normalizer==3.4.9`, distributed under the MIT license.

Their release hashes are locked in `paper/requirements.txt`. These packages
are installation dependencies; their distributions are not copied into the
repository.

## Referee workspace (`dan-reworking/`)

The unsealed referee workspace described in `REVIEW_SCOPE.md` carries its own
copies of third-party material. Because that root is excluded from the seal,
these copies are **not** covered by `SHA256SUMS` and their integrity is not
attested by `verify.sh`.

It reproduces the same two preprints already noted under “Reference PDFs”,
in fuller form — arXiv source archives rather than only the rendered PDFs:

- `dan-reworking/papers/polymath-1904.12438v2.tar.gz` and its extracted
  sources, including the figure images under
  `dan-reworking/papers/polymath-1904.12438v2/`; and
- `dan-reworking/papers/platt-trudgian-2004.09765v1.tar.gz` and
  `dan-reworking/papers/platt-trudgian-2004.09765v1.tex`.

Copyright remains with their respective authors or publishers. Their
inclusion here is not a claim that this repository can relicense or
redistribute them, and arXiv source archives are a broader reproduction than
the review PDFs under `references/`. The caution recorded under “Reference
PDFs” applies to these copies with at least equal force: reassess or remove
them before any public redistribution if the applicable arXiv license or
permission does not permit the intended release.

`dan-reworking/latex/gomila-proof-exposition.pdf` and its `.tex` source are
a reviewer's reworking of repository-original material, not third-party
content. They are not the sealed exposition; see `REVIEW_SCOPE.md`.

## Repository-original material

This notice records third-party rights only.  Material original to this
repository is licensed as recorded in `LICENSE` (MIT, source code) and
`LICENSE-DOCS` (CC BY 4.0, documentation and data), with the exceptions
listed there.  See `REVIEW_TERMS.md`.
