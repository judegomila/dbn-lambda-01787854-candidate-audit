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

For exact private-review provenance, `references/` includes the three PDFs
named in `BIBLIOGRAPHY.md`.  The Polymath and Platt--Trudgian preprints were
downloaded from the exact arXiv versions recorded in
`references/README.md`; copyright remains with their respective authors or
publishers.  Their inclusion here is not a claim that this repository can
relicense them.  Reassess or remove those two files before any public
redistribution if the applicable arXiv license or permission does not permit
the intended release.

## mpmath

The Python dependency `mpmath==1.4.1` is distributed under BSD-3-Clause.
Its package hashes are locked in `requirements.txt`.

## SymPy

The Python dependency `sympy==1.12` is distributed under the New BSD
license.  Its package hashes are locked in `requirements.txt`.

## Repository-original material

This notice records third-party rights only.  No public license has been
selected for material original to this private review repository.  See
`REVIEW_TERMS.md`.
