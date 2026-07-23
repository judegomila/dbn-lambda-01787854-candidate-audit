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

### LGPL winding source and binary

`vendor/dbn21a/certificates/certified1875/windslab165_v2/TloopthreadedV4.c`
is separately marked copyright 2018 Association des collaborateurs de
D.H.J. Polymath and licensed under LGPL 2.1 or, at the recipient's option,
any later version.  The corresponding `tloop` binary is retained with its
complete source in the same directory.

The official LGPL 2.1 text is included at
`vendor/licenses/LGPL-2.1-or-later.txt`.  Those files should not be described
as solely CC BY 4.0.

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
