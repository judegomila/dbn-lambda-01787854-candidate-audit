# Reproducing the three FLINT/Arb verifier packages

Three packages compile their interval tools from bundled C sources and
need gcc with FLINT 3 (Arb merged); everything else in the bundle runs
with Python 3 + `mpmath` + `sympy` alone (`bash check_bundle.sh`).

This file gives a pinned environment that matches the recorded Linux
re-runs of 2026-06-13 (each run from a clean copy of this bundle; all
three exited 0).

## Pinned environment

- **OS:** Ubuntu 24.04 ("noble")
- **Compiler:** gcc (Ubuntu 24.04 default), linking `-lflint -lm`
- **FLINT:** `libflint-dev` **3.0.1** (FLINT 3, with Arb merged — the
  `arb_*`/`acb_*` API lives in libflint)
- **Python:** `/usr/bin/python3` (3.12) with `numpy` **1.26.4**
  (`python3-numpy`), `mpmath` (`python3-mpmath`), `sympy`
  (`python3-sympy`)
- **PARI/GP:** `pari-gp` (used by the `grid_tbox` cross-check layer;
  that layer degrades to SKIP with a notice if `gp` is absent)

The bundled [`Dockerfile`](Dockerfile) builds exactly this environment:

```
docker build -t dbn21a-flint .
docker run --rm -v "$PWD":/bundle -w /bundle dbn21a-flint bash check_bundle.sh
```

Without docker, on any Ubuntu 24.04 box:

```
apt-get install gcc libflint-dev libgmp-dev libmpfr-dev \
                python3 python3-numpy python3-mpmath python3-sympy pari-gp
```

## The three packages: run commands and frozen expected output

Run each from the bundle root (or any clean copy). Each `verify.sh` is
self-contained (digest layer first, then compile + live re-run) and
exits 0 iff every check passes.

### 1. `certificates/record/record_package_197` (~minutes)

```
( cd certificates/record/record_package_197 && bash verify.sh )
```

Frozen key lines (end of output):

```
RECORD PACKAGE VERIFIED:
  ==> Lambda <= 197/1000 = 0.197 EXACTLY, UNCONDITIONAL.
```

(with hypothesis lines naming the slab
`[6000000185827,6000000185828]x[0.1809,1]x[0,0.1809]`, the Euler-2
selection bound `> 0.03 for EVERY integer N >= 690988`, and the two
independent verification lines.)

### 2. `certificates/certified1965/grid_full` (~3 min single core)

```
( cd certificates/certified1965/grid_full && bash verify.sh )
```

Frozen key lines (end of output):

```
N=690988 mtype=2: max-form 0.114594172753 >= conservative 0.023386363903 OK
N=690988 mtype=3: max-form 0.248169881194 >= conservative 0.191442648560 OK
ALL LAYERS PASS (lemma_native_grid adoption gate)
```

### 3. `certificates/certified1965/grid_tbox` (~3 min single core)

```
( cd certificates/certified1965/grid_tbox && bash verify.sh )
```

Frozen key lines (end of output; the two hash-chosen screen points are
derived from the package's own digests and are stable):

```
hash-chosen screen points: t1770 N=1661749 t1775 N=1133018
N=1661749 t=0.1770: screen 0.288665368624 >= logged row 0.285367378777 and >= logged box 0.273723984073 OK
N=1133018 t=0.1775: screen 0.223750396227 >= logged row 0.218946803839 and >= logged box 0.198056782233 OK
ALL LAYERS PASS (ltbox_native_grid adoption gate)
```

## Notes

- On non-FLINT machines, `check_bundle.sh` still validates the digest
  manifests of all three packages (layer [1]) and prints the exact
  re-run command for each as a SKIP notice.
- The verifiers write build artifacts and live logs only under `/tmp`,
  never into the bundle tree, so the bundle-wide `MANIFEST.sha256`
  remains valid after any number of runs (see the idempotency note in
  the README).
