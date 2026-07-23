# Artifact bundle — certified de Bruijn–Newman bound Λ ≤ 3/16 = 0.1875 (with the intermediate Λ ≤ 0.1891, Λ ≤ 0.1965, and Λ ≤ 0.197 record chains)

**Start here: [`THEOREM_MAP.md`](THEOREM_MAP.md)** (machine-readable
[`THEOREM_MAP.json`](THEOREM_MAP.json)) — the front-page manifest of the
bundle: one row per certificate leg of both chains, giving the exact
statement each certificate proves, its bundle path, its sha256 manifest
digests (writeup + verifier), its toolchain pins, its frozen expected
output lines, and its run command.

**STATUS: RELEASE.** The `certified1875/` directory carries the record
ladder below 0.1965: the two window-tiling assemblies (`assembly_1875/`,
Λ ≤ 3/16 = 0.1875 exactly, 58 checks; `assembly_1891/`, Λ ≤ 0.1891
exactly, 58 checks), their independent dual second-line sign-off
(`assembly_secondline/`, 76 gates, zero shared code), and every cited leg
certificate. The `certified1965/` directory carries every certified leg
of the Λ ≤ 0.1965 chain **including** the combined assembly certificate
(`assembly_1965/`, 52 checks) and its independent second-line sign-off
(`assembly_secondline/`, 42 gates).

This is the self-contained artifact bundle for the paper *"A certified
unconditional upper bound Λ ≤ 0.1875 for the de Bruijn–Newman constant"*
(Mosaic Intelligence, 2026). It contains the exact certificates, the
independent checkers, the producer writeups, and the run logs behind the
paper's claims.

Framed against the public record: Λ ≤ 0.197 is a certified improvement
below the recorded Λ ≤ 0.20 consequence of Platt–Trudgian (2020;
arXiv:2004.09765, exact height 3,000,175,332,800, with Corollary 2 there
stating Λ ≤ 0.2); Λ ≤ 0.1965 improves further and lies below the earlier
uncertified 0.1972624050 sighting (Rudolph, 1 May 2020 blog comment) at
the same barrier site; the window-tiling assembly ladder of
`certificates/certified1875/` extends the certified record to Λ ≤ 0.1891
and then Λ ≤ 3/16 = 0.1875 exactly, values with, to our knowledge, no
prior published or informally reported counterpart at any site.

This is a fully AI-derived body of results: the campaign design,
parameter optimization, interval implementations, certificates,
verification tooling, and the paper text were produced by Mosaic
Intelligence's AI research system; human involvement was strategic
direction. **Every claim can be re-verified from this bundle alone,
without trusting any part of the producing system** — and that is now
literally true end-to-end: the published theorems the chains instantiate
(the Polymath15 criterion = Thm 1.2, the Thm 1.3 error bounds, and the
y-quantifier reduction theorem) ship here as the self-contained,
re-runnable `criterion_theorem/`, `error_terms_audit/`, and `y_reduction/`
packages rather than as external citations. Pure-Python verifiers
(Python 3 + mpmath + sympy) re-derive every non-FLINT claim in-place; the
three FLINT/Arb packages are re-runnable on any FLINT-capable machine.

## Layout

```
certificates/record/        the Λ ≤ 0.197 record chain
  record_package_197/       combined record manifest (winding, stored sums,
                            sweep, tail, y-bridge legs + exact assembly
                            arithmetic; verify.sh re-runs everything)
  binding/                  record-binding theorem package (line 1)
  binding_secondline/       independent record-binding line (line 2)
  fullmarch/                100% stored-sums re-march (both artifacts)
  winding_rects_secondline/ hash-chosen winding rectangles, zero shared code
  sweep_secondline/         sweep second line
  tail_secondline/          tail second line (N0 row)
  tail_row19_secondline/    tail second line (row-19 regime)
  nconst_glue/              N-constancy / window-gluing lemmas (x2)
  criterion_theorem/        the Polymath15 criterion (Thm 1.2) instantiated
                            (spine; shared by both chains)
  error_terms_audit/        effective-approximation error bounds (Thm 1.3,
                            displays (20)-(24)), two independent transcriptions
certificates/certified1965/ the certified Λ ≤ 0.1965 chain
  y_reduction/              the y-quantifier reduction theorem (spine; closes
                            the right-region hypothesis over the full y-range
                            from a single-height sweep)
  assembly_1965/            combined assembly manifest (citation-arithmetic
                            package; exact assembly Λ ≤ 393/2000 = 0.1965,
                            every joint gated; 52 checks, exit 0)
  assembly_secondline/      independent second-line sign-off on the
                            assembled statement (zero shared code; 42 gates)
  stretch_binding(+_secondline)/   row-parameterized binding theorem, 2 lines
  grid_full/                Euler-3 full-grid sweeps, t = 0.1770 / 0.1775
                            (4,309,013 contiguous N per row, ball-certified)
  grid_tbox/                t-box-uniform sweep over [0.1770, 0.1775]
  tbox_blockuniform/        block-uniform t-box certificate (zero shared code)
  seam_exponent(+_secondline)/     conversion stage 1 (exponent alignment)
  seam_kappa(+_secondline)/        conversion stage 2 (normalization/leak)
  seam_ytransfer(+_secondline)/    conversion stage 3 (y-transfer routing),
                            2 lines
  tail_bound_box/ tail_box_anchor/ tail_bound_e3box(+_secondline)/
                            box-uniform unbounded tails (Euler-2 and Euler-3)
  site_glue(+_secondline)/  site gluing + row instantiation
certificates/certified1875/ the certified record ladder below 0.1965
                            (window-tiling assembly route)
  assembly_1875/            THE RECORD assembly: Λ ≤ 3/16 = 0.1875 exactly
                            at t0 = 1680/10^4, y0 = sqrt(39/1000); one split
                            at Nmid = 2745000; the N ≥ Nmid tail leg is
                            re-derived LIVE in-script (58 checks, exit 0)
  assembly_1891/            the intermediate rung: Λ ≤ 0.1891 exactly at
                            t0 = 1696/10^4 (citation-arithmetic; 58 checks)
  assembly_secondline/      independent dual second-line sign-off on BOTH
                            assembled statements (zero shared code, AST-
                            audited no-file-IO; 76 gates; the live tail leg
                            re-proved, not merely checked)
  lwin2_compose/            finite-window certificate, N ∈ [690988, 2745000],
                            closed tile t ∈ [1680, 1685]/10^4 (58 checks)
  lresid_compose/           finite-window certificate, hull [1695, 1760]/10^4
                            (the 0.1891 finite leg; 58 checks)
  windowleft/               middle-window WYBOX certificate + extension
                            (35 gates)
  finwin_ybind/             y-extension to the hypothesis ceiling (102 checks)
  optcoeff_ytail_nmid1680/  the N-cutoff descent tail device at
                            N1' = 2745000 (29 checks)
  optcoeff_ytail_down1690/  tail certificate, band [1690, 1700]/10^4
                            (64 checks)
  windslab165_v2/           boundary-winding-0 slab certificate,
                            [X, X+1] × [33/200, 1], all t ∈ [0, 0.1809]
                            (34 checks)
  windslab165_corner_secondline/  independent corner audit of the slab
certificates/upstream/      documented upstream artifact findings
  storedsums_rounding_defect/  published 0.19/0.18-row stored-sums entries
                            proven nearest-rounded (floor+1) from exact
                            endpoints; self-contained run_checks.sh
lean/                       machine-checked Lean 4 implication skeleton for
                            the Λ ≤ 0.197 chain (implication only — NOT a
                            formal verification of the record; 0.197 chain
                            only, see lean/README.md). Re-verify on a Linux
                            box / build pod: needs the Lean toolchain.
paper/                      main.pdf — the camera-ready record paper
                            (headline Λ ≤ 3/16 = 0.1875)
```

The Λ ≤ 0.1965 proof is carried in full by `certificates/certified1965/`
(the load-bearing Euler-3 mollifier sweeps `grid_full`, `grid_tbox`,
`tbox_blockuniform`, and the box-uniform tails are all there). Three
supplementary studies named in earlier drafts — the Euler-family
**saturation** map (E2–E7), the **negative/feasibility** map (Euler-2
death, 0.19-wall costing), and the **GPU** verification-economics study —
are summarized in the paper but are **not** shipped as standalone
certificate directories in this release; they are not part of the certified
bound chain.

## Reproduction

`check_bundle.sh` verifies the bundle-wide `MANIFEST.sha256` and re-runs
every checker that needs only Python 3 with `mpmath` and `sympy`
(42 verifiers — including the three binding-spine packages
`criterion_theorem`, `error_terms_audit`, `y_reduction` and the eleven
`certified1875/` record-ladder packages; each must exit 0):

```
bash check_bundle.sh
```

Three packages additionally compile their interval tools from bundled C
sources and need gcc with FLINT/Arb (Linux); they are skipped with a
notice when the toolchain is absent and can be run on any FLINT-capable
machine:

```
( cd certificates/record/record_package_197 && bash verify.sh )
( cd certificates/certified1965/grid_full   && bash verify.sh )
( cd certificates/certified1965/grid_tbox   && bash verify.sh )
```

Their digest manifests (layer 0 of each verify.sh) are also checked by
`check_bundle.sh` on every platform.

**Idempotency note.** Verifiers never write inside their own
(manifest-pinned) directories: live re-run output goes to `/tmp`
(caller-overridable where offered, e.g. `E3BOX_LIVE_LOG` for
`tail_e3box_secondline`), while the as-received logs/artifacts ship pinned
(`run_log*.txt`; `live_run_asreceived.log` and the `live_15e6.log` /
`live_3e7.log` as-received copies; and `winding_rects_secondline/runs/*_combined.json`),
against which the live output is byte-diffed where deterministic. Every
verifier path was audited for writes/redirects/compiles into its own
directory (not relying on the manifest staying green): the only producers
that write into a package directory are the explicitly-named
*regeneration utilities* (`run_corner.sh`, `gen_key_values.sh`, the
`fullmarch_storedsums.py march` subcommand), which are NOT on any
verification path. `check_bundle.sh` can therefore be re-run in place any
number of times; the bundle-wide `MANIFEST.sha256` self-check passes
before and after every run, and the tree is byte-identical after.

A pinned environment recipe for the three FLINT/Arb packages is in
[`REPRODUCE_FLINT.md`](REPRODUCE_FLINT.md) (with a `Dockerfile`
matching the toolchain of the recorded Linux re-runs).

**What the gates mean (exit codes are load-bearing).** Each verifier
asserts its gates and `sys.exit(1)` (or shell `exit 1` / `set -e`) on the
first failed gate, so a printed "PASS"/"OK" line is never the contract —
the *process exit code* is. `check_bundle.sh` runs each verifier and
counts a pass only on exit 0, prints a final `N pass / M fail / K skipped`
summary, and itself exits non-zero if any `M > 0`. A green run therefore
means every gate of every re-run verifier actually passed, not merely that
reassuring text was printed.

**What the FLINT skips do NOT cover.** When gcc + FLINT/Arb is absent, the
three FLINT/Arb packages (`record_package_197`, `grid_full`, `grid_tbox`)
are reported as `SKIP` (with the exact command to run them elsewhere; they
were re-run on Linux 2026-06-13, all exit 0). **No load-bearing inequality
of either bound rests solely on a skipped package:** the finite-range
Dirichlet lower bound that the binding theorem consumes is also certified
by the *pure-Python* crude-class T-box / block-uniform certificates
(`tbox_blockuniform`, `tail_bound_box`, `tail_bound_e3box`, and the
`record/sweep_secondline` / `tail_secondline` second lines), which run in
the default pure-Python set on every platform. The FLINT packages provide
the high-resolution grid/box re-runs and the digit-matched 0.197 record
manifest; their digest manifests (layer 0) are checked on every platform
even when the live leg is skipped.

## Conventions

- **Two-line verification.** Every load-bearing claim carries two
  mechanically independent verification lines with zero shared code
  wherever the paper's verification tables say "2"; single-line rows are
  explicitly marked in the paper and in the writeups here.
- **Floor truncation.** Quoted decimal digit strings are floor-truncated
  from certified interval endpoints at the stated precision unless a
  rounding mode is named; verify scripts re-derive every quoted string
  machine-side.
- **"Hypothesis (S)".** Throughout the writeups, *hypothesis (S)* denotes
  the frozen-exponent selection-bound form consumed by the binding
  theorem (the selection certificate ≥ θ hypothesis of the conditional
  binding theorem); the three `seam_*` packages certify the conversion
  from the production evaluator's normalization into this form.
- **Hypothesis numbering (ii)/(iii).** The Polymath15 criterion
  (`criterion_theorem`) and the 0.1965 assembly (`assembly_1965`) number
  the two finite-region hypotheses as **(ii)** = the zero-free RIGHT region
  `x ≥ X+√(1−y₀²)` (sweep + tail) and **(iii)** = the BARRIER slab
  `X ≤ x ≤ X+√(1−y₀²)` (winding + N-constancy). The 0.197 record-package
  writeup (`record_package_197/MANIFEST.md`) uses the OPPOSITE numbering
  for these two — barrier slab "(ii)", sweep/tail "(iii)". **The conditions,
  regions, and certificates are identical; only the (ii)↔(iii) labels are
  transposed.** Hypothesis (i) (the RH height) is "(i)" in both. The full
  mapping table is in `THEOREM_MAP.md` ("Hypothesis-label convention") and
  in `THEOREM_MAP.json` (`hypothesis_label_convention`).

## Solver and toolchain provenance

- Interval certificates were produced with ARB/FLINT (C, compiled from
  the bundled sources where re-run live), PARI/GP (the bundled
  `ltest_bundled.gp` reference), and `mpmath.iv`; independent second
  lines use disjoint toolchains (pure `fractions.Fraction` integer
  arithmetic in several legs, with π enclosed from scratch by
  Machin-type brackets where noted).
- The winding artifact digit-matches the 2018 published artifact of the
  Polymath-15 repository on 444/444 rectangles (same code lineage,
  different hardware/OS/FLINT minor version).
- All checkers in `check_bundle.sh`'s runnable set were re-run from a
  clean copy of this bundle on an independent machine (macOS, Python
  3.9, mpmath 1.3) before staging.

## Redaction note

Provenance text in writeups, script comments/docstrings, and run-log
banners was redacted for release (removal of internal infrastructure
details: machine names, internal queue/role labels); **mathematical and
numerical content is byte-identical to the producing runs**. Certified
payload artifacts (stored-sums matrices, winding logs, compressed sweep
shards, C/GP sources used by live re-runs) ship byte-identical to the
producing machines. Where a package-internal digest manifest pinned a
redacted text file, the post-redaction digest is the manifest of record
(the `PRODUCER_MANIFEST*.sha256` files in `grid_tbox/` are retained
verbatim as as-received import records; see the note in
`PRODUCER_README.md` there). The bundle-wide `MANIFEST.sha256` is the
release manifest of record.

License: see the deposit metadata (recommended: MIT for code and
certificates in this bundle; CC-BY 4.0 for the paper PDF).
