# Source for the de Bruijn--Newman bound paper

This directory contains the LaTeX source for:

> Jude Gomila, *A computer-assisted proof of the bound* `Lambda <= 0.1787854` *for the de Bruijn--Newman constant* (20 August 2026).

Build with a standard TeX Live installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error gomila_dbn_lambda_01787854_release.tex
```

The source uses the `article` class and standard TeX Live packages, including
`amsmath`, `amssymb`, `amsthm`, `mathtools`, `booktabs`, `placeins`,
`microtype`, `xurl`, `seqsplit`, and `hyperref`.

The program links in the paper are pinned to Git commit
`6222740efae58d773a70ff929cf12a34932d2af0` of the project repository. The
repository must be publicly accessible for those links to work for readers.

The paper states its review status and use of generative AI in the
Introduction. The source code linked by the paper is not duplicated in this
archive.
