# THEOREM MAP — certified de Bruijn–Newman bounds Λ ≤ 0.197, Λ ≤ 0.1965, Λ ≤ 0.1891, and Λ ≤ 3/16 = 0.1875

This is the front page of the artifact bundle: **one row per certificate leg of all chains**.
Machine-readable version: [`THEOREM_MAP.json`](THEOREM_MAP.json). The manifest of record is
`MANIFEST.sha256` (bundle root); every sha256 below is copied from it, and every digit string in the
statements was byte-checked against the certificate directory contents when this map was generated.

A *check* (synonymously, *gate*) is one machine-evaluated pass/fail assertion inside the standalone
verifier — it recomputes (never re-reads) an interval enclosure, a closed-tile coverage or containment,
an exact rational parameter identity, or a machine-derived floor truncation compared against the frozen
manifest string — and any mismatch fails the entire verifier. Each verifier exits 0 iff all checks pass.

All chains consume the Riemann hypothesis ONLY through hypothesis (i) of the Polymath15 criterion
(arXiv:1904.12438, Thm 1.2), supplied unconditionally by Platt–Trudgian (arXiv:2004.09765, Thm 1, exact
height T = 3,000,175,332,800): X/2 = 3,000,000,092,913.5 ≤ T with exact slack 350479773/2.

> ### Hypothesis-label convention (read before comparing the two chains' writeups)
>
> The Polymath15 criterion (Thm 1.2; `certificates/record/criterion_theorem/THEOREM_LAMBDA_CRITERION.md`,
> Theorem 0) numbers its three hypotheses as: **(i)** the RH height; **(ii)** the zero-free **RIGHT
> region** `x ≥ X + √(1−y₀²)` (discharged by the Dirichlet **sweep + tail**); **(iii)** the **BARRIER
> slab** `X ≤ x ≤ X + √(1−y₀²)` (discharged by the **winding-number** certificate + N-constancy). The
> Λ ≤ 0.1965 assembly (`certificates/certified1965/assembly_1965/ASSEMBLY_1965.md`) follows this
> convention exactly. The Λ ≤ 0.197 record-package writeup
> (`certificates/record/record_package_197/MANIFEST.md`) uses the **opposite numbering for the two
> finite-region hypotheses**: it labels the barrier-winding slab "(ii)" and the sweep/tail right region
> "(iii)". **The two numberings denote IDENTICAL mathematical conditions on identical regions, verified
> by identical certificates — only the (ii)↔(iii) labels are transposed.** Explicit mapping:
>
> | condition | region | discharged by | criterion / assembly_1965 label | record_package_197 label |
> |---|---|---|---|---|
> | barrier non-vanishing | `X ≤ x ≤ X+√(1−y₀²)` | winding cert + N-constancy | **(iii)** | **(ii)** |
> | right-region non-vanishing | `x ≥ X+√(1−y₀²)` | sweep + tail | **(ii)** | **(iii)** |
>
> Hypothesis (i) (the RH height) is labelled "(i)" in both and is unaffected. No certificate math
> depends on the labelling; this note reconciles the writeups only.

## Binding-spine theorem packages (shared by both chains)

### `criterion_theorem` — the Polymath15 criterion (arXiv:1904.12438 Thm 1.2) instantiated; the spine theorem both chains use

**Statement proved (exact).** Lemma 0.1 normalization x = 2T, y = 1 - 2 sigma (sympy-symbolic + numeric H0(2 gamma1) ~ 0 spot check); Theorem 2.1 instantiation arithmetic; Corollaries 3.1/3.2 at X' = 6000000185827: Lambda = t0 + y0^2/2 exact (0.197262405 and 0.197), X'/2 <= T_PT with exact margin, barrier-region containments, N = floor(sqrt(x/4pi + t/16)) constant on the slab (interval), and the X' <= 2 T_PT admissibility ceiling.

| field | value |
|---|---|
| bundle path | `certificates/record/criterion_theorem/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/criterion_theorem/THEOREM_LAMBDA_CRITERION.md`<br>`9a187fc6e27b92d8735808848ca58b1961c5cddb0bc90c0d85b2e62365770371` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/criterion_theorem/verify_criterion.py`<br>`95cac65f7ecab2dac1b6b4f5c49c828464e0a5912237872bea91040d4f393b06` |
| toolchain pins | /usr/bin/python3; sympy exact + mpmath/mpmath.iv; no disk reads, no network |
| expected stdout (frozen key lines) | `ALL CHECKS PASSED (criterion_theorem package)` |
| verification lines | 1 |
| run | `( cd certificates/record/criterion_theorem && /usr/bin/python3 verify_criterion.py )` |

### `error_terms_audit` — effective-approximation error bounds (arXiv:1904.12438 Thm 1.3, displays (20)-(24)), two independent transcriptions

**Statement proved (exact).** Two mechanically independent transcriptions (T1 paper-direct head-first; T2 log-space tail-first) of the bounds (20)-(24) for |gamma|, Re s_*, |kappa|, e_A+e_B, e_C0. At 5 campaign points the enclosures intersect and endpoints agree to <= 1e-6 (the (23) sum) / <= 1e-12 (closed forms); certified total e_A+e_B+e_C0 < 1e-3, orders below the 0.03 threshold. Flags (not a failure) the repo 6.92/(xN-6.66) vs paper 6.92/(x-12) discrepancy (sign + < 2e-12 magnitude certified).

| field | value |
|---|---|
| bundle path | `certificates/record/error_terms_audit/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/error_terms_audit/ERROR_TERMS_AUDIT.md`<br>`da91b3dada1d8f60d7da190361b6c75afb0e7889d030c8eddeb189e10e85d20d` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/error_terms_audit/verify_error_audit.py`<br>`73248b6b9581ea522f479c102be87436072ec70e1b29748600ad5d5091dabacc` |
| toolchain pins | /usr/bin/python3; mpmath.iv interval arithmetic dps 40; no disk reads, no network |
| expected stdout (frozen key lines) | `ALL CHECKS PASSED (error_terms_audit package)` |
| verification lines | 2 |
| run | `( cd certificates/record/error_terms_audit && /usr/bin/python3 verify_error_audit.py )` |

### `y_reduction` — the y-quantifier reduction theorem: closes the right-region hypothesis over the full y-range from a single-height (y=y0) sweep

**Statement proved (exact).** Y_REDUCTION Theorem 1: at t0 = 71/400, for every N >= N0 = 690988 and every x in the window of N, the Euler-2 mollified majorant D(N,y) and prefactor E2max(y) >= |lambda| are nonincreasing in y on [y0,1] (y0 = sqrt(0.039)), and the error majorants dominate at the stated worst corners over [y0, sqrt(0.645)]. Hence a per-window certificate 1 - D(N,y0) >= m > 0 at the single height y = y0 excludes zeros for all y in [y0, ymax] when m exceeds the window error budget. 14 interval gates (G0-G4 + structural); honest record that D(N0,y0) > 1 (the finite sweep remains necessary).

| field | value |
|---|---|
| bundle path | `certificates/certified1965/y_reduction/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/y_reduction/Y_REDUCTION.md`<br>`93a6e0c465d5aaaef5f1412899bcaee7f405060c84c021b6230da2b243d13f08` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/y_reduction/verify_y_reduction.py`<br>`9368a8caeed87007cbe469c512618653203ca158cfaf7c746c0c820b8f5acdd2` |
| toolchain pins | /usr/bin/python3; mpmath.iv interval arithmetic prec 220; no disk reads, no network |
| expected stdout (frozen key lines) | `14/14 checks passed`<br>`ALL CHECKS PASSED` |
| verification lines | 1 |
| run | `( cd certificates/certified1965/y_reduction && /usr/bin/python3 verify_y_reduction.py )` |

## The Λ ≤ 0.197 chain (hypotheses of the criterion + record binding)

### `record_package_197` — combined record manifest: hypotheses (i)+(ii) + stored sums + sweep + y-bridge legs + exact assembly arithmetic (line 1 + bundled line-2 winding legs)

**Statement proved (exact).** Lambda <= 0.197 (= 197/1000 exactly), UNCONDITIONALLY, via arXiv:1904.12438 Thm 1.2 instantiated at X = 6000000185827, t0 = 0.1775 (= 71/400 exactly), y0 = sqrt(0.039) (0.1974841765 floor-truncated), N0 = 690988, with Lambda <= t0 + y0^2/2 = 71/400 + 39/2000 = 197/1000 by exact rational arithmetic; hypothesis (i): T_PT = 3000175332800 >= X/2 = 3000000092913.5, exact slack 350479773/2 (PT2021, the only height input); hypothesis (ii): certified winding number 0 over the FULL closed slab x in [X, X+1], y in [0.1809, 1], t in [0, 0.1809].

| field | value |
|---|---|
| bundle path | `certificates/record/record_package_197/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/record_package_197/MANIFEST.md`<br>`10ba702011249c7d796640d4b10d7d5c89cf96ac1037a9fc329b416b4f47daa3` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/record_package_197/verify.sh`<br>`d602757b42d41dc8000ced4c5755484ee94e15a21eeff6ba20dd931e1cb3a5a2` |
| toolchain pins | bash; gcc + FLINT/Arb for the full live leg (re-run 2026-06-13 from a clean copy on Ubuntu, gcc, libflint-dev 3.0.1 = FLINT 3 w/ Arb merged, /usr/bin/python3 + numpy 1.26.4 + mpmath); MD5SUMS.txt digest layer checked on every platform |
| expected stdout (frozen key lines) | `RECORD PACKAGE VERIFIED:`<br>`==> Lambda <= 197/1000 = 0.197 EXACTLY, UNCONDITIONAL.` |
| verification lines | 2 |
| run | `( cd certificates/record/record_package_197 && bash verify.sh )` |

### `record_binding` — binding lemma R1-R4: certified sweep => hypothesis (iii) => Lambda <= 0.197 (line 1)

**Statement proved (exact).** (R1) the swept trib2 functional is of standard-window-majorant form (s*-phase cancellation verified sympy-exact, identically in s*); (R2) mollifier conversion: |f_t0| >= 0.03/C >= 0.0231663603 (FLOOR) uniformly for N >= N0 = 690988, y in [y0, y_max]; (R3) ONE global uniform error budget e_A+e_B+e_C0 <= 0.000000104590 (CEILING) over all windows N >= N0, x in window N, y in [y0, y_max]; (R4) the binding inequality m_min - E_max >= 0.0231662557 > 0 (FLOOR) -- hypothesis (iii) of Thm 1.2 with certified margin, at t0 = 71/400, y0 = sqrt(0.039), y_max = sqrt(0.645), X = 6000000185827 (closed domains).

| field | value |
|---|---|
| bundle path | `certificates/record/binding/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/binding/RECORD_BINDING.md`<br>`9c708b42641f399f7632c59f5e15961b9fa3a33fa0ea2388edef12cd7d6773bb` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/binding/verify_record_binding.py`<br>`e1ea194c27fbc555191fb86e75e5bdec1242a2113c7d1106cfb201e00677c9bf` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 220 + sympy exact + exact rationals; no disk reads |
| expected stdout (frozen key lines) | `50/50 checks passed`<br>`ALL CHECKS PASSED -- exit 0` |
| verification lines | 2 |
| run | `( cd certificates/record/binding && /usr/bin/python3 verify_record_binding.py )` |

### `record_binding_secondline` — record-binding second line (zero shared code; one of the two record-binding second lines)

**Statement proved (exact).** Independent zero-shared-code re-derivation of R1-R4 with deliberately different majorant chains (p-series integral tail vs endpoint-cap lemma): Lambda <= t0 + y0^2/2 = 197/1000 exactly; X/2 = 6000000185827/2 <= T_PT = 3000175332800 with margin exactly 350479773/2; R4 on this line's own constants: m_min - E_my >= 0.0231662557 (FLOOR) -- the same 10-digit floor the producer printed (two-line value match).

| field | value |
|---|---|
| bundle path | `certificates/record/binding_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/binding_secondline/RECBIND_SECONDLINE.md`<br>`5e3b788ac2f61631c5655930dedb3fe0c4154c2213b500811cf730264a3b8abd` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/binding_secondline/verify.sh`<br>`140cc13ab78a7b7f480948d3e2aaa760d41208ed4915219a14d4e80e9a4a3f49` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 200 + sympy exact + exact Fraction rationals; no disk reads |
| expected stdout (frozen key lines) | `TOTAL GATES RUN: 35`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/record/binding_secondline && bash verify.sh )` |

### `record_sweep_secondline` — hypothesis-(iii) finite-sweep second line (block-uniform, zero shared code)

**Statement proved (exact).** ROW 197 (t0 = 0.1775 exact, y0 = sqrt(0.039), outward-rounded intervals): for ALL x with N(x) in [690988, 9999999] (closed; N(x) = floor(sqrt(x/4pi + t0/16))), at y = y0: |f_t0(x+iy0)| - (eA+eB+eC0) >= 2.119901028e-2 and |1-beta_2|.|f_t0(x+iy0)| >= 2.745245414e-2 (both FLOOR-truncated), hence |H_t0/B_t0| > 0 on the whole range; 12 certified blocks; jointly gap-free with this line's tail certificate (all N >= 10^7).

| field | value |
|---|---|
| bundle path | `certificates/record/sweep_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/sweep_secondline/WRITEUP.md`<br>`1abd51fdcb934b7b33a8439299375fb9195de286297274a0e8cd5d631ef78579` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/sweep_secondline/verify.sh`<br>`dfa8ec30ade7fd9ecf2ba51e2ee27f213ebd2638a43a7c2f1e225a7c9bd763e7` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 64; zero shared code with the ARB/FLINT and pari lines |
| expected stdout (frozen key lines) | `min over blocks of  \|f_t0\| - (eA+eB+eC0)  >= 2.119901028e-2`<br>`min over blocks of  \|1-beta_2\|\|f_t0\|      >= 2.745245414e-2`<br>`SWEEP COMPLETE: 12 certified blocks` |
| verification lines | 2 |
| run | `( cd certificates/record/sweep_secondline && bash verify.sh )` |

### `record_tail_secondline` — hypothesis-(iii) N0-window + unbounded-tail second line (zero shared code)

**Statement proved (exact).** At the record row (t0 = 0.1775, y0 = sqrt(0.039), N0 = 690988): for every x with N(x) = N0 (the full N0 window), |1-beta_2||f_t| >= 3.028482891e-2 and |f_t| >= 2.338630869e-2 (FLOOR-truncated); tail certificate at N1 = 10^7: |f_t - 1| <= 9.15175207149e-1 < 1 for all x with N(x) >= N1; the N1 = 5e6 variant is gated to FAIL (bound > 1), demonstrating the gates have teeth.

| field | value |
|---|---|
| bundle path | `certificates/record/tail_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/tail_secondline/WRITEUP.md`<br>`02d56c16adafeb0e1a155e4ce4a8db1289dc7486bfd38cc9a281aa3afe3b947f` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/tail_secondline/verify.sh`<br>`9150318eb12a01b606a6fd8109c79adc36091bfd9061388431c8bd1e21c91c40` |
| toolchain pins | /usr/bin/python3; mpmath.iv (100-bit / 64-bit); exact rational comparisons of binary interval endpoints; zero shared code |
| expected stdout (frozen key lines) | `LB_SELECT = \|1-beta_2\|\|f_t\| >= 3.028482891e-2`<br>`BOUND = \|f_t - 1\| upper bound   <= 9.15175207149e-1` |
| verification lines | 2 |
| run | `( cd certificates/record/tail_secondline && bash verify.sh )` |

### `record_tail_row19_secondline` — supporting tail second line, row-19 regime (policy-2 parameter substitution; not consumed by either assembly -- regime anchor for the box-tail machinery)

**Statement proved (exact).** At t0 = 17/100 exact, y0 = 1/5 exact, N1 = 15000000: |f_t0(x+iy0) - 1| + e_A+e_B+e_C0 <= 19/20, hence |H_t0/B_t0| >= 1/20, for all x with N(x) >= N1 (closed); pinned bound |f_t - 1| <= 9.44730018300e-1; every side condition (C1-C3 monotonicity gates, 1-3y > 0) re-checked by runtime assertion at the new parameters.

| field | value |
|---|---|
| bundle path | `certificates/record/tail_row19_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/tail_row19_secondline/WRITEUP.md`<br>`5f6125d145e51c3a9253f1ed1f6786aed60399ddba2004672acdbfd433725e55` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/tail_row19_secondline/verify.sh`<br>`be0abf35b35bbcfd5ac30a8b24d3cbd4b6ff70142f54255dce9e01ab27ccbff6` |
| toolchain pins | /usr/bin/python3; mpmath.iv; zero shared code with the ARB/FLINT line |
| expected stdout (frozen key lines) | `BOUND = \|f_t - 1\| upper bound   <= 9.44730018300e-1`<br>`\|H_t0/B_t0\| >= 1/20` |
| verification lines | 2 |
| run | `( cd certificates/record/tail_row19_secondline && bash verify.sh )` |

### `record_winding_rects_secondline` — hypothesis-(ii) second line: hash-chosen rectangles + corner audit (zero shared code)

**Statement proved (exact).** Zero-shared-code interval recomputation on the certified 444-rectangle slab x in [X, X+1], y in [0.1809, 1], t in [0, 0.1809], X = 6000000185827, N = 690988 constant: hash-chosen rectangles (selection seeded by the sha256 of the audited line-1 t-march log, md5 2a395fe6219af7959b3dd2febc8b981b) and the corner rectangles including the t-march boundary rectangle 444 -- enclosure excludes 0 at every mesh point, certified mesh winding 0, containment and machine-derived width gates (CEIL) per corner.

| field | value |
|---|---|
| bundle path | `certificates/record/winding_rects_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/winding_rects_secondline/CLAIM.md`<br>`be34da9d78ec73d400239108db887a9276c3bf942efc5b3667d891f7f3891f6b` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/winding_rects_secondline/verify.sh`<br>`d9faa4e23b9f19d4d0f17008efc0b2c12fe9df4a0ee5f05177d1e2c534c1cea4` |
| toolchain pins | /usr/bin/python3; mpmath.iv; zero shared code with the ARB/FLINT line; live chunk re-run gated against pinned endpoints |
| expected stdout (frozen key lines) | `ALL GATES PASS`<br>`EXIT=0` |
| verification lines | 2 |
| run | `( cd certificates/record/winding_rects_secondline && bash verify.sh )` |

### `record_fullmarch` — stored-sums input matrix: 100% independent re-march, campaign + baseline artifacts (second line on the (ii)-leg input)

**Statement proved (exact).** FULL independent re-march of the campaign-site stored-sums artifact storedsum_nolemma_6000000185827_dig_20.txt (sha256 548592cde8b0793a6413e1d7b6b6fdfe12a62db641e35a7413280c78b4978f27) and the baseline artifact SingleStoredSums_x60000083951.5_dig_20.txt: chunk enclosures summed in EXACT rational arithmetic and ALL 62x62x2 = 7688 re/im components floor-truncation-compared against the published strings at 20 significant digits; exit 0 iff 7688/7688 pass.

| field | value |
|---|---|
| bundle path | `certificates/record/fullmarch/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/fullmarch/verify_fullmarch_campaign.sh`<br>`3d38b680cdf43933e05688b0ec291dffb5d7cee536339241a99dd90b9a03b0cf` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/fullmarch/verify_fullmarch_campaign.sh`<br>`3d38b680cdf43933e05688b0ec291dffb5d7cee536339241a99dd90b9a03b0cf` |
| toolchain pins | bash + /usr/bin/python3 (tools/fullmarch_storedsums.py, exact binary-endpoint rationals); sha256sum |
| expected stdout (frozen key lines) | `548592cde8b0793a6413e1d7b6b6fdfe12a62db641e35a7413280c78b4978f27` |
| verification lines | 2 |
| run | `( cd certificates/record/fullmarch && bash verify_fullmarch_campaign.sh && bash verify_fullmarch_baseline.sh )` |

### `record_nconst_gap` — slab N-constancy + window-gluing lemma at the record row (line 1; one digit string superseded by v2)

**Statement proved (exact).** N(x,t) = 690988 everywhere on the closed slab [X, X+1] x [0, 1775/10000] at X = 6000000185827, plus the sweep-window gluing inequalities (window-(N0+1) start > X+1 with margin >= 11989041.14). Original line; its printed robustness digit string for 1 - frac(S_hi) was nearest-rounded and is corrected in nconst_gap_v2 (see that row); retained as the original certificate.

| field | value |
|---|---|
| bundle path | `certificates/record/nconst_glue/nconst_gap/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/nconst_glue/nconst_gap/NCONST_GAP.md`<br>`aea09e624b9fad6c5e756ba134f343300b92b1d70f360ba99f7ec00ac30556c3` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/nconst_glue/nconst_gap/verify_nconst.py`<br>`bfa651e0a38ae9f0edb0085de0c82046f7ccc21fe3d053f93c78ecf694699639` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic; exact rationals |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 7`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/record/nconst_glue/nconst_gap && /usr/bin/python3 verify_nconst.py )` |

### `record_nconst_gap_v2` — slab N-constancy + window-gluing lemma, v2 (exact-binary-endpoint extraction; the cited line)

**Statement proved (exact).** N(x,t) = 690988 everywhere on the closed slab [X, X+1] x [0, 1775/10000] at X = 6000000185827, with robustness margins frac(S_lo) >= 0.3096430277 and 1 - frac(S_hi) >= 0.6903569064 (TRUE floor truncations: endpoints extracted from exact binary interval tuples with pure integer arithmetic, self-tested by check C0; check C2c gates that certified threshold strings EQUAL the machine-printed floor truncations); window gluing margin >= 11989041.14.

| field | value |
|---|---|
| bundle path | `certificates/record/nconst_glue/nconst_gap_v2/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/record/nconst_glue/nconst_gap_v2/NCONST_GAP.md`<br>`59a6c061632a8a1646c84b8507f638269ace67109c754fbfb4acef2f957242da` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/record/nconst_glue/nconst_gap_v2/verify_nconst.py`<br>`56dbd0d76d5950c99b9d1cbb4c69c98e4c4747b2a72e5fee2848d2a79294c381` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic; exact integer endpoint extraction (no precision context) |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 10`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/record/nconst_glue/nconst_gap_v2 && /usr/bin/python3 verify_nconst.py )` |

## The Λ ≤ 0.1965 chain (reduction / sweeps / conversion stages / tails / assembly)

### `stretch_binding` — row-parameterized binding theorem (reduction) at the stretch row, multi-prime form (line 1)

**Statement proved (exact).** At the stretch row t0 = 177/1000, y0 = sqrt(39/1000), X = 6000000185827, N0 = 690988, y_max = sqrt(646/1000), Lambda functional t0 + y0^2/2 = 393/2000 = 0.1965 exactly, for Euler mollifiers P inside {2,3,5,7}: conversion constants sigma-floor >= 1.7887022679 (FLOOR), C_{2} <= 1.2956514986, C_{2,3} <= 1.4871894818, C_{2,3,5,7} <= 1.6384739261 (CEILING); global uniform error budget e_A+e_B+e_C0 <= 0.000000106981 (CEILING) over all windows N >= N0 and all y in [y0, y_max]; the conditional binding theorem reduces the assembly to ONE sweep hypothesis -- a selection certificate >= theta at y = y0 for every integer N in [N0, 5e6) suffices whenever theta exceeds the analytic floor C_P * E_max <= 0.000000159101 (Euler-3); binding margin >= 0.0201721712 (FLOOR) at theta = 0.03.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/stretch_binding/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/stretch_binding/STRETCH_BINDING.md`<br>`561668d17787296d5a6c4e5143e85878ef5481613f1033ece17d6ed5d2d2323e` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/stretch_binding/verify_stretch_binding.py`<br>`824e38f8f64d28c27fe3943fd2bc72e97314b481654c5d4abd62d856be73a15c` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 220 + sympy exact + exact rationals; no disk reads |
| expected stdout (frozen key lines) | `84/84 checks passed`<br>`ALL CHECKS PASSED -- exit 0` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/stretch_binding && /usr/bin/python3 verify_stretch_binding.py )` |

### `stretch_binding_secondline` — binding-theorem second line (zero shared code, different freeze family + tail majorant)

**Statement proved (exact).** Independent zero-shared-code re-derivation of the row-parameterized binding theorem: independently computed constants agree digit-exactly on the sigma-floor, all three conversion constants C_P, the error budget, and the binding margin; the deliberate crudeness of this line's own tail majorant is isolated and bounded; pointwise falsification probe passes; NO DISCREPANCY.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/stretch_binding_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/stretch_binding_secondline/STRETCHBIND_SECONDLINE.md`<br>`4df8aa69a266c0491c04f80e9bae7865901dc8e15253d161adebcd8a9e41733c` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/stretch_binding_secondline/verify.sh`<br>`a24c933fda9af210705511e0c5fe51142668fc75ab56314910a8650ba245c370` |
| toolchain pins | /usr/bin/python3; mpmath.iv + sympy exact + exact Fraction rationals; zero shared code |
| expected stdout (frozen key lines) | `TOTAL GATES RUN: 58`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/stretch_binding_secondline && bash verify.sh )` |

### `grid_full` — Euler-3 T-type full-grid finite sweeps, both endpoint rows (hypothesis-(iii) finite leg, certificate family 1)

**Statement proved (exact).** The pari-T-type Euler-3 mollified lemma bound at y0 = sqrt(39/1000) exact is ball-certified (arb_gt) > 0.03 at EVERY integer N in the closed range [690988, 5000000] (4,309,013 contiguous points, no sampled-grid gap), at t = 0.1770 (min 0.184889586327 at N0, max 0.487572439544) and at t = 0.1775 (min 0.191442648559, max 0.490581145542); per-N floor-truncated lower ball endpoints logged; live hash-selected naive ARB recomputes and an adversarial zero-shared-code mpmath.iv screen are part of the verifier.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/grid_full/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/grid_full/CLAIM.md`<br>`c35c964537c359c9b137a630d7afd0b14b600c888847dab1e5eb52fa3fa3ceb9` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/grid_full/verify.sh`<br>`1f616487a0f9402142cf708c4a097b6d6a9be65e393b8a6d99e50068299cc458` |
| toolchain pins | gcc + FLINT/Arb (re-run 2026-06-13 from a clean copy: Ubuntu, gcc, libflint-dev 3.0.1, /usr/bin/python3 + numpy + mpmath; pari/gp present); MD5SUMS digest layer checked on every platform |
| expected stdout (frozen key lines) | `ALL LAYERS PASS (lemma_native_grid adoption gate)` |
| verification lines | 1 |
| run | `( cd certificates/certified1965/grid_full && bash verify.sh )` |

### `grid_tbox` — L-type Euler-2 full-grid certificates, t-box-uniform + both endpoint rows (selection-leg evidence under its own quantifiers)

**Statement proved (exact).** For every integer N in the CLOSED range [690988, 5000000] and SIMULTANEOUSLY for every real t in the CLOSED interval [1770/10000, 1775/10000] (t as one outward-rounded arb ball), the published improved-triangle-inequality (L-type) Euler-2 lemma bound at y^2 = 39/1000 EXACT is certified > 3/100 (arb_gt); box-min 0.085215888792 at N = 690988, box-max 0.430367711874 at N = 5000000; plus per-row certificates at t = 1770/10000 (min 0.102903409873) and t = 1775/10000 (min 0.110518831042). NOTE: these L-type values are certified NON-convertible termwise into the binding form at face value (see seam_ytransfer); they enter the chain as selection-leg evidence only.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/grid_tbox/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/grid_tbox/CLAIM.md`<br>`ea1e2b93e8b81506dea424a34c17a3a21f97a073e1e63b3e9bf12bab2bec583b` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/grid_tbox/verify.sh`<br>`09e491314d99c6deaa16b813d7c2d54caf46e142e9b4497651bc5ca7a2bc3439` |
| toolchain pins | gcc + FLINT/Arb (re-run 2026-06-13 from a clean copy on Ubuntu, FLINT 3.0.1); /usr/bin/python3 + numpy + mpmath; MD5SUMS digest layer checked on every platform |
| expected stdout (frozen key lines) | `ALL LAYERS PASS (ltbox_native_grid adoption gate)` |
| verification lines | 1 |
| run | `( cd certificates/certified1965/grid_tbox && bash verify.sh )` |

### `tbox_blockuniform` — block-uniform T-type t-box certificate (zero shared code; certificate family 2 of the finite range -- the certificate stage 3 routes through)

**Statement proved (exact).** FOR ALL real t in the CLOSED interval [1770/10000, 1775/10000] and FOR ALL real x such that N_t(x) = floor(sqrt(x/4pi + t/16)) lies in the CLOSED integer range [690988, 5000000], at y = y0: the crude-class T-type selection bound is certified positive with margin (the certificate consumed by conversion stage 3); anchor regimes re-run live, anchor197: min over blocks |f_t0| - (eA+eB+eC0) >= 2.119901028e-2 and |1-beta_2||f_t0| >= 2.745245414e-2 (FLOOR-truncated).

| field | value |
|---|---|
| bundle path | `certificates/certified1965/tbox_blockuniform/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/tbox_blockuniform/WRITEUP.md`<br>`d1f307fc5e7126c19e0252c6a4ea355a09d037c39a6d59a90fd756115de9fe99` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/tbox_blockuniform/verify.sh`<br>`954fdd902a15769c061e2c18170f45187d90e29f027bfef2424ec26b4210bf53` |
| toolchain pins | /usr/bin/python3; mpmath.iv + fractions ONLY (AST-audited import allowlist); md5 pin of ltbox_sweep_iv.py inside verify.sh |
| expected stdout (frozen key lines) | `VERIFY OK` |
| verification lines | 1 |
| run | `( cd certificates/certified1965/tbox_blockuniform && bash verify.sh )` |

### `seam_exponent` — conversion stage 1: exponent alignment (production per-N exponent -> frozen-exponent selection form)

**Statement proved (exact).** (L3) the frozen exponent sits strictly below the pari (production) exponent for every N >= N0, one-sided gap < 1.04e-15 uniformly in N, proved cancellation-free; (L4) mass-inflation lemma: any production-normalization numerator certificate at threshold c converts to the frozen-form bound at threshold c - D* with D* <= 1.8e-14, uniform in N; (L5) the normalization identity in symbolic (all-sigma) strength; (L6) box-uniform normalization enclosure with conversion margin >= 0.0124722278 (FLOOR) over the whole sweep range.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/seam_exponent/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_exponent/SEAM_EXPONENT.md`<br>`154d69a36c20bb1d374be058d214e233a10509ab4841b18d8ee1a8c2952086b4` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_exponent/verify_seam_exponent.py`<br>`f87200aa29cbf2d9840e57afdb1720bf5bb5778e0c30d3b90eb8a9a1843aadaa` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 120 + sympy exact + exact rationals; no disk reads |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 42`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/seam_exponent && /usr/bin/python3 verify_seam_exponent.py )` |

### `seam_exponent_secondline` — stage-1 second line (prec 320 vs 120; direct two-sided subtraction of the 1e-15-scale gap)

**Statement proved (exact).** Independent re-derivation of the stage-1 statements with symbolic sign atoms re-derived and the exponent gap additionally resolved by DIRECT two-sided subtraction (a consistency check structurally unavailable to the first line); all stage-1 quoted digit strings machine-reproduced.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/seam_exponent_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_exponent_secondline/SEAMEXP_SECONDLINE.md`<br>`40c0e12397e5e1f4e1c751dd22ca8fa48ccc45ce2ae26750a40cf7f5d6fd2d52` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_exponent_secondline/verify.sh`<br>`d286f8aa4555c5828b478375d0bdead31aea9afbbc75db185585c85ff18953fd` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 320 + sympy exact; zero shared code |
| expected stdout (frozen key lines) | `TOTAL GATES RUN: 47`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/seam_exponent_secondline && bash verify.sh )` |

### `seam_kappa` — conversion stage 2: normalization / leak accounting (numerator recovery from production certificates)

**Statement proved (exact).** (K1) domain gate; (K2) leak positivity: the production evaluator's subtracted correction (kappa-leak) term is certified nonnegative on its entire domain, so certificate face values are conservative; (K3) numerator-recovery lemma: every production certificate >= 3/100 on the sweep range yields a numerator bound >= 0.0424722278 (FLOOR), and >= 0.2617557548 at the certified grid minimum 0.184889586327; the mollifier normalization factor is exactly the binding theorem's conversion-constant shape (symbolic polynomial identity, all real exponents at once); the pinned gp source ltest_bundled.gp (md5 6205e2aabbb6564a9780c00d18dac6a7) is byte-identical to the grid toolchain's.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/seam_kappa/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_kappa/SEAM_KAPPA.md`<br>`6b93fe08bf732b1964d0665abf749b36586910d96e39b79fa049c69bb7c089cc` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_kappa/verify_seam_kappa.py`<br>`58d119690d161095f3f02241a5c8652976132c237b36aa5a55355363c1c2cc30` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 120 + sympy exact + exact rationals; reads only the bundled gp source |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 31`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/seam_kappa && /usr/bin/python3 verify_seam_kappa.py )` |

### `seam_kappa_secondline` — stage-2 second line (zero shared code)

**Statement proved (exact).** Independent re-derivation of the stage-2 statements (leak positivity, normalization identity, numerator recovery) on this line's own endpoints; stage-2 quoted digit strings machine-reproduced.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/seam_kappa_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_kappa_secondline/SEAMKAPPA_SECONDLINE.md`<br>`8ccd1e492bf0a378bd831338a5fdf9b29cb63f7ae8f232668d6df85231c614dc` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_kappa_secondline/verify.sh`<br>`3ef6622ad07dfff06d13c994c0563fbaf0dd64972672ef2cee39c733e4b1d5dd` |
| toolchain pins | /usr/bin/python3; mpmath.iv + sympy exact; zero shared code |
| expected stdout (frozen key lines) | `TOTAL GATES RUN: 24`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/seam_kappa_secondline && bash verify.sh )` |

### `seam_ytransfer` — conversion stage 3: y-transfer routing (kernel-order negative + reduction-theorem route; line 1)

**Statement proved (exact).** (Y2) the OPTIMAL uniform constant comparing the L-type sharp kernel with the crude-majorant kernel is c in [0.8681942568, 0.8681942569] at the stretch row (equality attained); (Y3) quantified NEGATIVE: termwise conversion of an L-type certificate into a crude-class floor is positive ONLY for L > L* in [0.0945520619, 0.0945520620] -- 3.1517x the 3/100 design threshold and strictly above the pinned box minimum 0.085215888792 -- so the pinned L-type grid certificates can NOT be converted termwise at face value; (Y4) ROUTING: the crude-class T-type box certificate (t in [0.1770, 0.1775], N in [690988, 5e6], y = y0, margin >= 6.066621000e-3) IS a standard window majorant, the transfer gates are re-certified at t0 = 177/1000 (Y1(N0) enclosed two-sidedly in [-6.7029388683, -6.7029388682]), and the y-quantifier transfers to ALL y in [y0, y_max]: composite y-uniform floor m - E_max >= 0.0060665140 (FLOOR) for all N in [690988, 5e6].

| field | value |
|---|---|
| bundle path | `certificates/certified1965/seam_ytransfer/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_ytransfer/SEAM_YTRANSFER.md`<br>`c4bda6f9f10a36efbcca9844d4426e46e1a29b1c323b003e282dc6cd827bed2e` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_ytransfer/verify_seam_ytransfer.py`<br>`415579dd55861cde81cd14d69496800f866000ece5363f340245add8e6146863` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 120 + sympy exact + exact rationals; reads only the bundled gp source |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 46`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/seam_ytransfer && /usr/bin/python3 verify_seam_ytransfer.py )` |

### `seam_ytransfer_secondline` — stage-3 second line (exhaustive symbolic sign case-split of the kernel-order lemma)

**Statement proved (exact).** Independent zero-shared-code line on stage 3: the kernel-order lemma's universal quantifier re-derived by an exhaustive symbolic sign case-split, the conversion-threshold identity and its monotonicity re-proved symbolically, and the stage-3 quoted digit strings machine-reproduced; NO DISCREPANCY FOUND.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/seam_ytransfer_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_ytransfer_secondline/SEAMYTR_SECONDLINE.md`<br>`20633652b0780e01d686bd14bba212993828eb4383d9e9ea364627be421ffc8e` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/seam_ytransfer_secondline/verify.sh`<br>`0ed183c28cebf9f187cce3412e943a2b22fc90e013ea3ee6a91fad69765b0496` |
| toolchain pins | /usr/bin/python3; mpmath.iv + sympy exact; zero shared code |
| expected stdout (frozen key lines) | `TOTAL GATES RUN: 31`<br>`RESULT: ALL PASS -- VERIFY OK` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/seam_ytransfer_secondline && bash verify.sh )` |

### `tail_bound_box` — box-uniform Euler-2 mollified unbounded tail (line 1)

**Statement proved (exact).** For every t in [0.1760, 0.1810], every y in [0.1809, sqrt(0.648)] (a range containing the full hypothesis-(ii) y-interval of every row in play), and all x with N(x) >= N1 = 5e6 (closed box): |f_t| >= 0.0834187152 and |H_t/B_t| >= 0.0833079015 (FLOOR-truncated), with box-uniform monotonicity gates; margin 1 - D_box >= 0.1055.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/tail_bound_box/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_bound_box/TAIL_BOUND_BOX.md`<br>`2f81a74528e8e460b2a1fa621e52e181c529bd9f90d7132b1d4d09399ecae20a` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_bound_box/verify_tail_box.py`<br>`c5eca62c201f944bcc0fcad3169569f30cb76bb8e0099c76491a5dbeff943434` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 220 + exact rationals; no disk reads |
| expected stdout (frozen key lines) | `35/35 checks passed`<br>`ALL CHECKS PASSED` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/tail_bound_box && /usr/bin/python3 verify_tail_box.py )` |

### `tail_box_anchor` — anchor validation of tail_bound_box (independent line; known-anchor reproduction in two regimes)

**Statement proved (exact).** Independent-line anchor validation of the box-tail machinery: the parameterized engine exactly reproduces the pinned regime-1 (0.197 row) and regime-2 (0.1965 stretch row) certified values, box constants reproduced, dominance and cross-freeze gates certified; md5-pins anchor_machinery.py and re-runs it live.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/tail_box_anchor/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_box_anchor/ANCHOR_VALIDATION.md`<br>`0e197a31da5b2a43bfc4f60b552b6bbbbd26ff85153625b89e15514e8acb6c6c` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_box_anchor/verify.sh`<br>`bf29ad0e0bfe64fb020f6444584591165afa98fcafb9d41c0faa2ede3de16b44` |
| toolchain pins | /usr/bin/python3; mpmath + stdlib only; no reads outside the directory |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 79`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/tail_box_anchor && bash verify.sh )` |

### `tail_bound_e3box` — box-uniform Euler-3 mollified unbounded tail, wide box (line 1)

**Statement proved (exact).** For every t in [0.1620, 0.1810], every y in [0.1809, sqrt(0.676)], and all x with N(x) >= N1 = 5e6 (closed box), with the Euler-3 mollifier: |H_t/B_t| >= 0.0062457711 (FLOOR-truncated) uniformly.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/tail_bound_e3box/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_bound_e3box/TAIL_BOUND_E3BOX.md`<br>`cee190b6c08aabc2cefeb2438cbe3ee74dfdcc5182c8c8e64faee44795343a91` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_bound_e3box/verify_tail_e3box.py`<br>`a7495a4a097f3a14c9759895a8330083de44e77840ffb7f1cab9d3a6180d9b9e` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 220 + sympy exact + exact rationals; no disk reads |
| expected stdout (frozen key lines) | `150/150 checks passed`<br>`ALL CHECKS PASSED` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/tail_bound_e3box && /usr/bin/python3 verify_tail_e3box.py )` |

### `tail_e3box_secondline` — Euler-3 box-tail second line (zero shared code; independent Euler-3 branch line)

**Statement proved (exact).** Independent second line on tail_bound_e3box: rung-(a) anchors in two pinned regimes (Euler-2 box strings 0.0834187152 / 0.0833079015 and 0.197-row strings 0.2477133542 / 0.2476158451 byte-reproduced) plus a full independent Euler-3 branch line: all six slice constants, error caps and the final |H/B| floor reproduced on this line's independent endpoints.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/tail_e3box_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_e3box_secondline/WRITEUP.md`<br>`ce76fb29f49288f9c432689282a1e23cf40ef36dbaca5f010a361f3ca9f88ddc` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/tail_e3box_secondline/verify.sh`<br>`45d7aa656ea9e3fec501e2b0c36f7539cf27e1b01c2999ae7ea9dd5eba0da711` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 220; zero shared code |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 84`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/tail_e3box_secondline && bash verify.sh )` |

### `site_glue` — site-uniform window gluing + 0.1965-row precondition instantiation (line 1)

**Statement proved (exact).** The sweep-window gluing inequalities hold t0-UNIFORMLY over the ENTIRE certified-barrier slab t-range [0, 1809/10000] (closed) at X = 6000000185827, N0 = 690988; the Lambda <= 0.1965 stretch row (t0 = 1770/10000, y0^2 = 39/1000) is instantiated with margins >= 5377393.0179 and >= 11989041.1446 and the exact identities t0 + y0^2/2 = 1965/10000 and y0^2 + 2 t0 = 393/1000 <= 1.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/site_glue/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/site_glue/SITE_GLUE.md`<br>`691073c7998a6cea6c3a63cc7a49adbd207d8cc5609802c0e9db801815ee1b33` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/site_glue/verify_site_glue.py`<br>`f9b31ca72ab20cb05393aca7c5a583a066dfeeeb4ea856e433fdd01d1b16e082` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic + exact rationals |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 19`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/site_glue && /usr/bin/python3 verify_site_glue.py )` |

### `site_glue_secondline` — site-glue second line (pure-integer toolchain; zero shared code)

**Statement proved (exact).** Independent pure-integer re-derivation of the site-uniform gluing lemma and the 0.1965-row instantiation (Fraction + isqrt; pi enclosed from scratch by two intersecting Machin-type brackets; no interval library); also re-anchors the point-row margins and N-constancy robustness strings of the record row.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/site_glue_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/site_glue_secondline/SECOND_LINE.md`<br>`ac6aa45217784e82314f968e1d8b260005fabd1ae84739932321d79071cb2a26` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/site_glue_secondline/verify.sh`<br>`fdbd392db11986110a41212b3d32cb9627a49f8fe69e147307f4935f66599538` |
| toolchain pins | /usr/bin/python3; fractions.Fraction + math.isqrt only (no interval library) |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 30`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/site_glue_secondline && bash verify.sh )` |

### `assembly_1965` — combined assembly manifest: the record statement Lambda <= 0.1965 (line 1)

**Statement proved (exact).** Lambda <= t0 + y0^2/2 = 177/1000 + 39/2000 = 393/2000 = 0.1965 exactly, UNCONDITIONALLY (sole RH input: PT2021's verified height T_PT = 3000175332800 >= X/2, through hypothesis (i) only, exact slack 350479773/2), at X = 6000000185827, t0 = 177/1000, y0 = sqrt(39/1000), N0 = 690988, N1 = 5e6, y_max = sqrt(646/1000): every JOINT of the assembly (containments, construction identities, gap-free window tiling of [X, infinity) with certified splice overlap >= 125663718.7099, composite finite-leg floor >= 0.0060665140 FLOOR-truncated, margins) gated in exact rational or outward-rounded interval arithmetic.

| field | value |
|---|---|
| bundle path | `certificates/certified1965/assembly_1965/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/assembly_1965/ASSEMBLY_1965.md`<br>`3eaef10305648c3586af2fa6362a4ed4c1e85da9965b1542490937015cd470cb` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/assembly_1965/verify_assembly_1965.py`<br>`510fa5aa5fbf29dd57f0c865c2532b65a001283fba88be2f193044e9fe8c7fc1` |
| toolchain pins | /usr/bin/python3; mpmath interval arithmetic prec 220 + sympy exact + exact rationals; no disk reads outside the directory |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 52`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/assembly_1965 && /usr/bin/python3 verify_assembly_1965.py )` |

### `assembly_secondline` — record-binding second line on the assembled 0.1965 statement (zero shared code; the second of the two record-binding second lines)

**Statement proved (exact).** Independent sign-off on the assembled statement: re-establishes the exact record arithmetic (Lambda <= 393/2000 = 0.1965) and every joint on its own line, machine-reproduces the certified anchor values in two distinct parameter regimes, and adds a falsification probe at an in-window point; NO DISCREPANCY; RH consumed ONLY via PT2021 T = 3000175332800 >= X/2 (gate J2a).

| field | value |
|---|---|
| bundle path | `certificates/certified1965/assembly_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1965/assembly_secondline/RECBIND1965_SECONDLINE.md`<br>`fe8180dfe333f831fece7ea39bff32510bfb7724d20d6cdc627a7c72e74c014a` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1965/assembly_secondline/verify.sh`<br>`fa357b6f1180acf7202ca9a9968d879bd06a83e87ceab05744246835812b5e99` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 220 + sympy exact + exact Fraction rationals; no disk reads; zero shared code |
| expected stdout (frozen key lines) | `TOTAL GATES RUN: 42`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1965/assembly_secondline && bash verify.sh )` |

## The Λ ≤ 0.1875 record ladder (window-tiling assemblies: Λ ≤ 0.1891 and Λ ≤ 3/16 = 0.1875)

### `assembly_1875` — THE RECORD assembly: Lambda <= 3/16 = 0.1875 exactly (window-tiling route; the tail leg re-derived LIVE in-script)

**Statement proved (exact).** Lambda <= t0 + y0^2/2 = 1680/10^4 + 39/2000 = 1875/10^4 = 3/16 = 0.1875 EXACTLY, UNCONDITIONALLY, at X = 6000000185827, t0 = 1680/10^4, y0 = sqrt(39/1000), N0 = 690988, Nmid = 2745000; hypothesis (i): T_PT = 3000175332800 >= X/2 = 3000000092913.5, exact margin 350479773/2 (PT2021, the sole RH input); hypothesis (iii): the windslab165_v2 winding certificate + N-constancy re-derived at prec 220 (anchors 5377392.8789 / 11989041.1415); hypothesis (ii) tiled at the single split Nmid = 2745000 covered by BOTH legs: lwin2_compose tile k=8 (closed tile [1680/10^4, 1685/10^4], composite floor 0.0134320455) and the LIVE in-script P1113 tail at cutoff N1' = 2745000 (D CEIL10 0.9854851520 < 1, tail slack FLOOR10 0.0091331201 > 0, anchored bit-identically at the banked reference regime).

| field | value |
|---|---|
| bundle path | `certificates/certified1875/assembly_1875/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/assembly_1875/ASSEMBLY_1875.md`<br>`f1a60c19c9c5f632512b9466042d3aef4089b49e9d9670de7a8bffb22894d596` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/assembly_1875/verify_assembly_1875.py`<br>`d17b68ca0bc94e4f0e26cb009e4cc3974aa76e43b74568b20c1a17c0d87465ae` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 220 + sympy exact + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 58`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/assembly_1875 && /usr/bin/python3 verify_assembly_1875.py )` |

### `assembly_1891` — the intermediate rung: Lambda <= 0.1891 exactly (citation-arithmetic assembly over the same certified inventory)

**Statement proved (exact).** Lambda <= t0 + y0^2/2 = 1696/10^4 + 39/2000 = 1891/10^4 = 0.1891 EXACTLY, UNCONDITIONALLY, at X = 6000000185827, t0 = 1696/10^4, y0 = sqrt(39/1000); three-leg window tiling meeting at Nmid = 2745000 and N1 = 5000000 (both split points covered by both adjacent legs): lresid_compose (composite floor 0.0110533245), the windowleft WYBOX middle window composed with the finwin_ybind y-extension (composite y-uniform floor 0.0002669533), and the optcoeff_ytail_down1690 tail (final slack 0.0279753143); the in-bundle fill-attempt artifacts additionally certify the honesty block (gate S5 FAIL, exit 1, on the deeper 0.18634552 fill at claim time).

| field | value |
|---|---|
| bundle path | `certificates/certified1875/assembly_1891/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/assembly_1891/ASSEMBLY_1891.md`<br>`67e9dde9f25aeac5a3dd4aabc9594c38db882ab23751b341ab5da3e585041bbf` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/assembly_1891/verify_assembly_1891.py`<br>`ca875cd2448752c48468ca839ceb1604c3542b7b4bb734d3924ec5c100ea1e56` |
| toolchain pins | /usr/bin/python3; mpmath.iv prec 220 + sympy exact + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 58`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/assembly_1891 && /usr/bin/python3 verify_assembly_1891.py )` |

### `assembly_1875_secondline` — independent dual second-line sign-off on BOTH assembled statements (zero shared code; the live tail leg RE-PROVED)

**Statement proved (exact).** Zero-shared-code sign-off (AST-audited: no file IO / exec / eval) on both assemblies: record arithmetic Lambda(1875) = 3/16 and Lambda(1891) = 1891/10^4 re-established exactly; every composition/joint/window gate re-derived; the LIVE tail leg re-proved on this line's own exact-convolution engine with strictly sharper endpoints (D_ub CEIL10 0.9845628509 <= producer 0.9854851520; flow FLOOR10 0.0097134705); five FLOOR4 window strings and both N-constancy anchors (5377392.8789 / 11989041.1415) reproduced; NO DISCREPANCY.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/assembly_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/assembly_secondline/run_log.txt`<br>`900d3ca9a47d8152fb3b1381d47b9e8a6fb67c0731b46a90ea97ff8e73cf7fc4` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/assembly_secondline/verify.sh`<br>`68ebef92df11484319a4e9bae88c0a958dd4d5d6dbb2d1aed9fc95e27ff3176f` |
| toolchain pins | /usr/bin/python3; mpmath.iv + sympy exact + exact Fraction rationals; zero shared code; md5-pinned script, AST-audited |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 76`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/assembly_secondline && bash verify.sh )` |

### `lwin2_compose` — finite-window certificate: N in [690988, 2745000] on closed tiles (the 0.1875 finite leg at tile k=8)

**Statement proved (exact).** Closed-tile staircase composition over t in [1680/10^4, 1760/10^4]: on tile k=8 = [1680/10^4, 1685/10^4] the block bottom equals N0 = 690988 (no uncovered sub-block) and the composite floor is 0.0134320455 (FLOOR10), full y-range [sqrt(39/1000), sqrt(1-2t)] via the certified composition chain.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/lwin2_compose/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/lwin2_compose/LWIN2_COMPOSE.md`<br>`d10488fc50322e47c10c768a1f39cb325deed5e9e5d7bed798221b9933ec35de` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/lwin2_compose/verify_lwin2_compose.py`<br>`450ee33e9dcbbb0162a30696aff4dbe9382c464bed6db0ed790a4c8318a75839` |
| toolchain pins | /usr/bin/python3; mpmath.iv + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 58`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/lwin2_compose && /usr/bin/python3 verify_lwin2_compose.py )` |

### `lresid_compose` — finite-window certificate: N in [690988, 2745000] on the hull [1695/10^4, 1760/10^4] (the 0.1891 finite leg)

**Statement proved (exact).** Composite finite-window certificate on the closed hull t in [1695/10^4, 1760/10^4] (contains t0 = 1696/10^4), y-floor equal to sqrt(39/1000) by equal squares, composite floor 0.0110533245 (FLOOR10) > 0, with the residual rectangle below the y-floor stated exactly (gate R2; the honesty-block source for the deeper-fill negative).

| field | value |
|---|---|
| bundle path | `certificates/certified1875/lresid_compose/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/lresid_compose/LRESID_COMPOSE.md`<br>`eab3ad81c03460a023ee896ce3ce86076b36eaac004f9a219dd8e03f5e1d7d53` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/lresid_compose/verify_lresid_compose.py`<br>`205e850cfb628eac25a5b5278314e5c0f4226c2df45cff60b615d065a6b19de8` |
| toolchain pins | /usr/bin/python3; mpmath.iv + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 58`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/lresid_compose && /usr/bin/python3 verify_lresid_compose.py )` |

### `windowleft_wybox` — middle-window WYBOX certificate: N in [2745000, 5000000] (consumed by the 0.1891 assembly)

**Statement proved (exact).** T-type certified window certificate with t-hull [1696/10^4, 1770/10^4] CLOSED (t0 = 1696/10^4 at its left endpoint, membership exact), y in [33/200, sqrt(39/1000)]; WYBOX certified margin >= 2.669692513e-4 (FLOOR); md5-pinned engine, AST-audited.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/windowleft/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/windowleft/run_log.txt`<br>`4ce79ae7ec2d4d30416f014fcf38a6522b50ea1fbd1da762e708b1905f9957ae` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/windowleft/verify.sh`<br>`f0728dd98e39f143187e0e1747af138dc7a955e069352620aeb9fbded06be6ee` |
| toolchain pins | /usr/bin/python3; mpmath.iv; md5-pinned script; block-march reproduction gates |
| expected stdout (frozen key lines) | `ALL GATES PASS: 35/35` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/windowleft && bash verify.sh )` |

### `finwin_ybind` — y-extension of the middle window to the full hypothesis ceiling (consumed by the 0.1891 assembly)

**Statement proved (exact).** SITE-W y-extension binding the WYBOX window to the full hypothesis-(ii) ceiling ymax^2 = 6608/10^4: composite y-uniform floor 0.0002669533 (FLOOR10) > 0 in exact rationals, consumed through the standard-majorant routing exactly as staged by its scope clause.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/finwin_ybind/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/finwin_ybind/FINWIN_YBIND.md`<br>`5efb247119125eaac40e8c63a5ca60aeb5bbd1b7293a647f1e153c82c15ef390` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/finwin_ybind/verify_finwin_ybind.py`<br>`0dbdd36a72c291c978acf54bea50f218c888aad73e90be748bffac383a99f453` |
| toolchain pins | /usr/bin/python3; mpmath.iv + sympy + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 102`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/finwin_ybind && /usr/bin/python3 verify_finwin_ybind.py )` |

### `optcoeff_ytail_nmid1680` — the N-cutoff descent tail device at N1' = 2745000 (standalone sibling of the 0.1875 live leg)

**Statement proved (exact).** P1113 tail closure with the tail cutoff lowered 5000000 -> 2745000 on the band t in [1680/10^4, 1696/10^4], full y-range: all monotonicity constants and cap side conditions re-derived at the new cutoff (D CEIL10 0.9854851520 < 1, tail slack FLOOR10 0.0091331201 > 0), anchored bit-identically at the banked cutoff regime.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/optcoeff_ytail_nmid1680/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/optcoeff_ytail_nmid1680/OPTCOEFF_YTAIL_NMID1680.md`<br>`e0d92db993d27462b23ce6fcbbd9b66e5c8db19c09ea3e0f33159691881b3c01` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/optcoeff_ytail_nmid1680/verify_optcoeff_ytail_nmid1680.py`<br>`c262f7a46693f46d0637a5cce3b227229894de750fbc1cd6445a03dfc9ecfd1e` |
| toolchain pins | /usr/bin/python3; mpmath.iv + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 29`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/optcoeff_ytail_nmid1680 && /usr/bin/python3 verify_optcoeff_ytail_nmid1680.py )` |

### `optcoeff_ytail_down1690` — tail certificate N >= 5000000 on the band [1690/10^4, 1700/10^4] (the 0.1891 tail leg)

**Statement proved (exact).** P1113 tail certificate on the band t in [1690/10^4, 1700/10^4] (contains t0 = 1696/10^4), y-floor 33/200 with the full y-range by the certified termwise-monotonicity device; final slack 0.0279753143 (FLOOR10) > 0.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/optcoeff_ytail_down1690/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/optcoeff_ytail_down1690/OPTCOEFF_YTAIL_DOWN1690.md`<br>`605f8fc0cf459651992044ae34c23f2d2b4c1e956cb760a89d698c69ac78e3b9` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/optcoeff_ytail_down1690/verify_optcoeff_ytail_down1690.py`<br>`25e6d5875e69e069c4a72f4122633fd14e8fdc46db6d18955b92942e7d0aa9b7` |
| toolchain pins | /usr/bin/python3; mpmath.iv + exact rationals; reads NO files |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 64`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/optcoeff_ytail_down1690 && /usr/bin/python3 verify_optcoeff_ytail_down1690.py )` |

### `windslab165_v2` — hypothesis-(iii) winding slab: boundary-winding 0 on [X, X+1] x [33/200, 1], ALL real t in [0, 1809/10^4] (line 1)

**Statement proved (exact).** Certified boundary-winding-0 certificate on the slab x in [X, X+1], y in [33/200, 1], uniform over ALL real t in [0, 1809/10^4] at X = 6000000185827 -- the slab consumed by BOTH new assemblies for strictly smaller t-ranges (the slab-to-hypothesis-(iii) binding is the one accepted by the published deeper-chain assemblies).

| field | value |
|---|---|
| bundle path | `certificates/certified1875/windslab165_v2/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/windslab165_v2/verify_run_log_tmpcopy.txt`<br>`70a481df0f489573fdb5b90104ebe1d15529931ed4dd463aa25e4edaedbada11` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/windslab165_v2/verify_windslab165.py`<br>`6aa808ecf34cc90d4b06fc6395b648b4208cfac8b1a8b6f6fbff7903f366c518` |
| toolchain pins | /usr/bin/python3 + the bundled C producer source (TloopthreadedV4.c) and pinned stored-sums inputs |
| expected stdout (frozen key lines) | `TOTAL CHECKS RUN: 34`<br>`RESULT: ALL PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/windslab165_v2 && /usr/bin/python3 verify_windslab165.py )` |

### `windslab165_corner_secondline` — hypothesis-(iii) second line: independent corner audit of the y >= 33/200 slab (zero shared code)

**Statement proved (exact).** Independent interval recomputation of corner rectangles of the [X, X+1] x [33/200, 1] slab with live chunk re-runs gated against pinned endpoints; containment checks re-derived; zero shared code with the producer line.

| field | value |
|---|---|
| bundle path | `certificates/certified1875/windslab165_corner_secondline/` |
| writeup (sha256, per MANIFEST.sha256) | `certificates/certified1875/windslab165_corner_secondline/check_containment.py`<br>`febd1a6ae41f743c340e2ab58503a4cfb3bf388eb2901f95c71f04cc3570add5` |
| verifier (sha256, per MANIFEST.sha256) | `certificates/certified1875/windslab165_corner_secondline/verify.sh`<br>`e32be2620849065c42fb83a080abcd85ddf65c72e88827fc691ea030087e516e` |
| toolchain pins | /usr/bin/python3; mpmath.iv; zero shared code; live chunk re-run gated against pinned endpoints |
| expected stdout (frozen key lines) | `ALL GATES PASS` |
| verification lines | 2 |
| run | `( cd certificates/certified1875/windslab165_corner_secondline && bash verify.sh )` |

---

43 rows: 3 binding-spine theorem packages shared by all chains (`criterion_theorem`,
`error_terms_audit`, `y_reduction`) + 10 legs of the Λ ≤ 0.197 chain + 19 legs of the Λ ≤ 0.1965 chain
+ 11 legs of the Λ ≤ 0.1875 record ladder (the window-tiling assemblies `assembly_1875` and
`assembly_1891`, their dual zero-shared-code sign-off `assembly_1875_secondline`, and every cited leg
certificate). The three FLINT/Arb packages (`record_package_197`, `grid_full`, `grid_tbox`) run live
where gcc + FLINT/Arb is present and are otherwise digest-checked here and re-runnable on any
FLINT-capable machine (they were re-run from a clean copy of this bundle on Linux on 2026-06-13, all
exit 0). Every other row — including all three binding-spine packages and the entire Λ ≤ 0.1875
ladder — is pure Python (Python 3 + mpmath + sympy). `bash check_bundle.sh` re-runs the entire
pure-Python set (now 42 verifiers) plus the bundle-wide manifest check.
