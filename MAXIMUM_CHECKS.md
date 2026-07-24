# Maximum pre-handoff checks

## Scope and interpretation

This file records the strongest computational and software checks performed
while preparing the \(0.1787854\) referee package. These checks materially
raise confidence in reproducibility and catch many classes of implementation
error. They do not replace mathematical review of the analytic reductions.

The repository's status after every successful check remains:
**unreviewed computer-assisted unconditional proof candidate**, not an
established or peer-reviewed theorem.

Some expensive finite-replay checks were first completed against sealed
commit

```text
5c4d7a7ba14f9933ca604d18b2e5bf70a104b3b3
```

before the new native-binding, window-freeze, tail-Arb, and barrier materials
were integrated. The only subsequent edit to the finite producer is a
cleanup/fail-closed patch: it validates the mode before allocation, frees all
Arb/FLINT objects on every exit, and silences two branch-specific unused
parameters. Both producer branches and both evaluation modes were checked
for numerical output invariance under that patch. The final integrated
commit must nevertheless pass the final-seal checklist at the end of this
file before handoff.

## 1. Complete finite regeneration

A fresh producer run regenerated every row

\[
N=690988,\ldots,3840000
\]

for a total of

\[
3149013
\]

rows.

Results:

- all fresh `(N,L12,GT089)` tuples matched the 15 sealed certificate shards;
- there were no missing, duplicate, overlapping, nonpositive, or `UNCERT`
  rows;
- after removing only nondeterministic `TIMING` values and the explicit
  `WEIGHT TRIANGLE` banner, every other line matched its stored counterpart;
- all 15 gzip members passed integrity checks; and
- the all-row comparison itself completed in 1.89 seconds.

On the audit machine the producer replay took about 16 minutes 45 seconds.
Runtime is hardware-dependent and is not part of the certificate.

During integration, a second cleanup-patched run generated all 15 output
logs and the strict comparator again matched all \(3,149,013\) canonical
rows. That driver process is deliberately not counted as a release replay:
the shell script was edited while its already-open process was running and
exited afterward with `691011: command not found`, so it never emitted the
required terminal success or final metadata. The finalized runner and the
GitHub `complete-finite-replay` job must execute from the clean final commit.

The freshly parsed decisive finite values were

\[
T_{\min}=0.000000791366,
\]

\[
E_{\max}\le0.000000233494905212335514,
\]

and

\[
T_{\min}-E_{\max}
\ge0.000000557871094787>0.
\]

## 2. Direct non-amortized finite checks

Thirty direct 256-bit singleton evaluations were run independently of the
amortized shard accumulation.

The selected rows include:

- the global weakest row \(N=690988\);
- both sides of every auxiliary-prime-set transition;
- both sides of every compressed P11 and P23 shard boundary; and
- the closed finite/tail overlap \(N=3840000\).

Every direct lower bound dominated the corresponding stored bound. The
weakest row was reproduced exactly:

```text
N 690988 L12 0.000000791366 GT089 0
```

At the far endpoint, the direct result was

```text
N=3840000  direct=0.301900093765  stored=0.299655457299
```

The direct weakest-row path was also run under UBSan and reproduced the same
output with no diagnostic.

## 3. Direct all-height and normalizer checks

The primary direct Arb upper-Dini verifier passed at 180, 256, and 384 bits.
It exhausted all active divisor-cell patterns

\[
243,\ 81,\ 27,\ 9
\]

for the four finite auxiliary-prime families. Its smallest strict ratio
margin was

\[
1-\text{ratio}_{\rm ub}
=0.00000139232724905>0.
\]

The 256-bit Dini verifier also passed under ASan+UBSan with leak detection
enabled and emitted no sanitizer diagnostic.

The separate native normalizer/correction verifier passed at 180 and 256
bits. Its decisive correction logarithmic-rate upper bound was

\[
-1.3631121547576400<0.
\]

## 4. Native binding stress tests

`verifiers/verify_native_binding.py` passed all 13 structural and algebraic
gates.

In addition to checking the source-to-formula contract, it ran 216
deterministic complex-phase tests of:

- the \(EA\) convolution;
- the \(\overline E C_0\) convolution;
- complex \(\kappa\) correction bounds; and
- the final normalized inequality.

The largest convolution residual was at ordinary floating-roundoff scale,
and the smallest tested final slack exceeded \(0.03056\). These tests are
not a proof of the symbolic lemma; they are an independent attempt to catch
sign, conjugation, and normalization mistakes.

## 5. Exact window-freeze and site coverage

The window-freeze verifier used:

- exact rational algebra;
- a rational Machin-series enclosure for \(\pi\) narrower than
  \(10^{-100}\);
- exact integer-square-root brackets; and
- an independent 400-bit `mpmath.iv` calculation.

It proved

\[
x_{690988}
<X+\sqrt{1-y_0^2}
<x_{690989}
\]

with strict lower margins exceeding \(5.37\times10^6\) and
\(1.19\times10^7\), respectively. It also checked the producer formula
fragments, half-open window convention, all finite leg joints, and the
closed finite/tail overlap.

The final criterion assembly separately executes a six-check exact-rational
audit of the \(H_0\)-to-\(\xi\) sign map. It records that
\(H_0(x+iy)=0\) first maps to \((1-y+ix)/2\), and that the functional
equation followed by conjugation produces the required
\((1+y+ix)/2\) representative. This closes an easy-to-miss sign shorthand
without modifying the byte-preserved upstream package.

## 6. Standalone tail checks

### Independent FLINT/Arb path

The standalone tail implementation, which reads no stored numerical data,
passed all 36 fail-closed gates at both 256 and 512 bits.

The more conservative 512-bit transcript gives directed values implying

\[
D<0.999721,
\]

\[
\frac{1-D}{M_{\max}}>0.0001735326089372,
\]

\[
e_A+e_B+e_{C,0}<0.000000011671604,
\]

and

\[
\frac{1-D}{M_{\max}}-(e_A+e_B+e_{C,0})
>0.0001735209373337.
\]

The strict parser rejects malformed balls, duplicate results, wrong domains,
failure markers, and loss of any decisive directed inequality.

### Corroborating Python interval path

The older full tail verifier passed all 93 gates at 160, 256, and 384 bits.
After elapsed-time fields were removed, all 107 semantic output lines were
identical across the three precisions.

A separate 384-bit Arb recombination of the printed conservative component
ceilings certified

```text
D     <= 0.999720909379941957210435553228
flow  >= 0.0001735326144143072119838702800138
error <= 0.00000001167160258920
slack >= 0.0001735209428117180119838702800138
```

The new standalone lemma and Arb program are the primary proof path; the
Python runs provide source-lineage and cross-implementation corroboration.

## 7. Closed barrier checks

The target barrier replay completed all 883 consecutive closed prisms on

\[
[X,X+1]\times[0.1809,1]\times[0,0.16125].
\]

The strict parser verified:

- exact initial time \(0\);
- final endpoint enclosing \(129/800\);
- byte-identical adjacent seam serializations;
- the complete-prism derivative products and mesh formula for every prism;
- one and only one record for each consecutive prism;
- zero-free endpoint balls and permitted argument increments;
- every winding enclosure strictly inside \((-1/4,1/4)\);
- aggregate winding consistent with the integer zero;
- positive independently recomputed margins; and
- the unique terminal line `RESULT: CLOSED SLAB CERTIFIED`.

The minimum independently recomputed prism margin was

\[
>0.519849894613872543374989997.
\]

The aggregate winding enclosure was contained in

\[
[-8.95,8.95]\times10^{-13}.
\]

The full run was independently repeated across two toolchains from the same
sealed source.  The canonical Linux/GCC/FLINT 3.0.1 transcript has SHA-256
`2d010f70902dca1627f40ddcd68f3954b37fd9596f7840787415eeafb20805f4`
and minimum recomputed margin ending in `...997`.  The corroborating
macOS/Clang/FLINT 3.6.0 transcript has SHA-256
`4d5ec355fb51b834b99ec48662eae200ecb125297e62b757d7d7f1b3737378f4`
and minimum recomputed margin ending in `...999`.  Both independently pass
all 54 parser checks and all 883 prisms.  The macOS `cpu` profiler field is a
non-mathematical platform artifact and is deliberately not consumed; the
recorded wall time is sane.

### Barrier data provenance

The stored-sum generator independently regenerated all \(7,688\) real
components of the \(62\times62\) complex matrix as Arb balls.

- components checked: \(7688\);
- components with nonzero printed radii: \(7688\);
- containment failures: \(0\);
- largest regenerated-radius use of the restored allowance: below \(0.018\).

The independent Taylor checker gave

\[
\text{omitted tail}
<1.954234593244762\times10^{-22}<10^{-20}.
\]

The separate 256-bit uniform-error checker evaluated the complete barrier
box and certified

\[
e_A+e_B+e_{C,0}
<0.000356523011600037<0.00125.
\]

Negative barrier tests with an out-of-range terminal time, malformed numeric
input, and a missing coefficient file all exited nonzero.

### Adversarial derivative and winding audit

Red-team review found and repaired three theorem-level defects before the
final sealed replay:

- a pointwise Lemma 8.4 derivative bound had been frozen at one spatial
  corner without proving it dominated the complete box;
- a discrete derivative sum had been replaced by an integral even though
  its time summand initially increases; and
- the numerical quadrature callback projected complex balls to their real
  parts, violating FLINT's holomorphic `order=1` callback contract.

The final source separates conservative spatial endpoints, uses an exact
16-term Arb head plus a rigorously decreasing integral tail, and keeps the
complete complex variable in analytic logarithms and powers. A focused
exact-source probe passed at 126 and 256 bits and under ASan+UBSan,
including branch-cut failure tests, both callback orders, all 16 head
terms, scaled-tail identities, and the midpoint-disk winding homotopy. The
audited barrier source SHA-256 is

```text
3cb650af474c0908d2e94abf1e4ceefcd3f15187c54be2e6eaa3c94214313895
```

This is an internal adversarial audit, not the requested external
mathematical review.

## 8. Source robustness and hygiene

The finite producer was checked in both compile-time branches and both
evaluation modes under ASan+UBSan.

The original exit-only leak of 4,304 bytes in 91 allocations was removed by
the cleanup patch. The patched source passed:

- strict warnings-as-errors;
- ASan, UBSan, and LeakSanitizer;
- normal and early exits;
- debug output paths; and
- output-neutral comparisons with the original numerical computation.

All shell sources parsed with `bash -n`, and all Python sources present in
the audited tree compiled. The full-sweep harness correctly rejected:

- a missing output argument;
- any pre-existing, symlinked, stable-tree, or repository-ancestor output
  path; and
- an image whose identity did not match the recorded lock.

All release entry points clear `PYTHONOPTIMIZE`, `PYTHONPATH`, and
`PYTHONHOME`, and disable bytecode writes. The assembly also rejects an
optimized interpreter and scrubs all six `BARRIER_*` override variables
before selecting its two sealed transcripts. Thus ambient shell state
cannot disable assertion-based inherited checks or silently substitute
barrier evidence.

## 9. Clean-clone and integrity checks

For the original sealed audit commit:

- a clean local clone had no worktree changes;
- `SHA256SUMS` covered exactly all 313 files under the declared exclusions;
  and
- a read-only clean-clone container review passed in 43.601 seconds.

That container run included the stored seal, vendored arithmetic replay,
complete finite structural scan, regenerated 180/256-bit Dini logs,
180/256-bit normalizer checks, 160/256-bit tail reruns, and the then-current
assembly.

Because the unconditional-candidate integration adds and changes files, the
final commit requires a new seal and a new clean-clone container result. The
old clean-clone result is evidence for the inherited finite package, not a
substitute for the final integrated check.

## 10. Final-seal checklist

Before sharing the repository with the external reviewer:

1. regenerate `SHA256SUMS` from the exact final tree and verify complete
   coverage under the documented exclusions;
2. run `./verify.sh` from a clean worktree;
3. build the portable review image and run
   `./scripts/run_container_review.sh`;
4. run `./scripts/run_barrier_replay.sh` from the final integrated sources
   and compare the decisive semantics with the sealed barrier evidence;
5. run `./scripts/run_tail_arb.sh` at 256 and 512 bits;
6. rerun the complete finite sweep from the cleanup-patched producer, or
   retain a clearly labeled pre-patch full replay together with the
   output-neutral patch proof;
7. record the final commit, source hashes, exact container image ID,
   architecture, compiler/FLINT versions, commands, and start/finish times;
8. verify that the GitHub repository remains private; and
9. confirm that the landing page says “unreviewed computer-assisted
   unconditional proof candidate,” never “established theorem.”

Only results tied to the final seal should be presented as the final
handoff state.

## 11. Remaining human review boundary

Even this check set does not determine whether:

- the published theorems have been transcribed and applied correctly;
- the native binding, Dini, window-freeze, tail, and barrier proofs are
  mathematically valid;
- each implementation is a faithful realization of its proof;
- all independent paths avoid a common conceptual error; or
- the work meets the standards for peer acceptance.

Those are the central questions for the external mathematician.
