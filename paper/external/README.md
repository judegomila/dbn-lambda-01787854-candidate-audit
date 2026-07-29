# Repository cross-check of the supplied proof exposition

## Status

[`gomila-proof-exposition.pdf`](gomila-proof-exposition.pdf) is a useful
22-page theorem-style exposition supplied for review on 28 July 2026. It is
preserved here byte-for-byte, but it is **not** the repository's
authoritative proof record and is **not** an external acceptance report.

The supplied PDF contains several correctable mathematical and provenance
defects. It must be read with this cross-check. Where the PDF conflicts with
the sealed repository evidence, the repository evidence controls.

Adding this draft does not change the project's status: this remains an
**unreviewed computer-assisted candidate for an unconditional proof**, not
an established theorem.

## Artifact identity and safety

| Item | Value |
|---|---|
| SHA-256 | `fd98f4e91dea6c02c7705665aaa95d0cb0b0cf46f8a22276e2c693a56a489313` |
| Size | 442,088 bytes |
| Format | PDF 1.5, 22 US-letter pages |
| Producer | pdfTeX 1.40.25 |
| Visible date | 27 July 2026 |
| Baseline repository snapshot audited | tag `review-01787854-v3` |
| Baseline commit audited | `2e9976c4becbf97e31c56fe75fce07cdff5dd4ea` |

The PDF has no embedded files, JavaScript, forms, encryption, unembedded
fonts, local filesystem paths, credentials, or restricted sibling-project
references. Its PDF metadata has blank Author and Title fields, and the
visible byline is `Authors TBD`.

No LaTeX source, bibliography source, independent finite-scan program,
external run logs, or signed referee statement accompanied the PDF.

## Corrections required in a revised exposition

### 1. The effective-error dependency is stated backwards

Page 6, Remark 2.2 says:

> Accordingly, the current proof relies on (24)

It should say that the candidate **does not rely on the displayed equation
(24)** or its `10.44`. The target path uses the conservative `10.50`
corollary derived directly from Polymath Proposition 6.6(vi), as documented
in [`ERROR_CONSTANT_WELD.md`](../../ERROR_CONSTANT_WELD.md).

The nearby phrase "enlarging the denominator \(x-8.52\) to \(x-12\)" is also
misleading: \(x-12\) is the smaller denominator. What is enlarged is the
reciprocal upper bound.

### 2. Two finite certified floors disagree with the sealed corpus

Page 9, Table 1 reports two values stronger than the values in the sealed
certificate:

| Finite family | Supplied PDF | Sealed repository |
|---|---:|---:|
| \(729000\le N\le818999\), primes \(2,3,5,7\) | `0.000315112481` | `0.000315112459` |
| \(819000\le N\le1027999\), primes \(2,3,5\) | `0.000305788816` | `0.000305788807` |

The other two family floors and the global floor agree. The discrepancy
does not affect the load-bearing global minimum or the final finite margin,
but the stronger numbers cannot be used without the missing external
program and logs. A revised PDF should use the sealed values unless that
supplement is supplied and bound by hashes.

Page 9 should also replace "the global bound \(T_{\min}\) is attained at
\(N=690988\)" with "the smallest certified floor occurs at \(N=690988\)."
The stored value is a directed, floor-truncated lower enclosure; it is not
an equality claim for the exact value of \(L_N\).

The controlling evidence is
[`logs/finite_and_binding.log`](../../logs/finite_and_binding.log) and
[`CANDIDATE_PARAMETERS.md`](../../CANDIDATE_PARAMETERS.md).

### 3. The finite error total does not follow from the rounded components

Page 11 states

\[
e_A+e_B\le2.06\times10^{-12},\qquad
e_{C,0}\le0.000000233492848188649183,
\]

and then says "hence"

\[
E_{\max}\le0.000000233494905212337849.
\]

The displayed rounded component bounds add to
`0.000000233494908188649183`, not the displayed \(E_{\max}\).
The repository's precise certified first component is

`0.000000000002057023688667`,

and this does give the stated total. A revision should print the precise
component or say that all three inequalities were separately certified.
The final finite margin in the PDF is nevertheless the correct sealed
value.

### 4. The tail contraction inequality is reversed twice

Page 15, Gap / review point 6, and page 21, Category A item 6, state
\(1-D<0.000279\). The sealed corridor is

\[
0.999719<D<0.999721,
\qquad
0.000279<1-D<0.000281.
\]

The load-bearing direction is \(1-D>0.000279\). See
[`logs/tail_arb_256.log`](../../logs/tail_arb_256.log) and
[`logs/tail_arb_512.log`](../../logs/tail_arb_512.log).

### 5. The displayed proof of Theorem 5.6 uses insufficient rounded bounds

Page 16 claims

\[
\frac{1-0.999721}{M_{\max}}>0.0001735
\]

after stating only \(M_{\max}<1.608290\). Those displayed coarse bounds give

\[
\frac{1-0.999721}{1.608290}
=0.00017347617656\ldots,
\]

which is not greater than `0.0001735`.

The underlying repository certificate does close the theorem. The common
directed 512-bit bounds are

\[
\frac{1-D}{M_{\max}}>0.0001735326089372,
\]

\[
\frac{1-D}{M_{\max}}-(e_A+e_B+e_{C,0})
>0.0001735209373337.
\]

A revision should invoke these directly certified inequalities rather than
derive the conclusion from the rounded \(D\) and \(M_{\max}\) summaries.

### 6. The endpoint-cap admissibility premise is omitted

Lemma 5.1 requires

\[
\sigma>\frac t2\log c
\]

for every cap to which it is applied. Sections 5.4-5.6 state the
all-\(N\) decrease conditions but do not include this separate
cap-admissibility obligation in Proposition 5.5.

The repository's standalone Arb transcripts explicitly certify it as
`SC1` and `SC2` over both required hulls. A revised Proposition 5.5 should
state those gates before Lemma 5.1 is used in Lemma 5.2.

### 7. The claimed external finite supplement is absent

Pages 9-10 say that all of the following accompany the manuscript:

- `code/prop43/prop43_proof.c`;
- `runs/*_summary.txt`; and
- `runs/*_sweep.out`.

They were not supplied, are not embedded in the PDF, and are not present in
this repository. Therefore the PDF's claims that Proposition 4.3 was
independently replayed and its program reviewed line-by-line are not
auditable from the supplied materials.

The repository instead contains its own producers under [`src/`](../../src),
the 15 sealed shards under [`certificates/`](../../certificates), the
stored verifier
[`verifiers/verify_finite_and_binding.py`](../../verifiers/verify_finite_and_binding.py),
and the full regeneration path
[`scripts/run_full_sweep.sh`](../../scripts/run_full_sweep.sh).

Moreover, a program "derived from Gomila's source" can support external
source review and a clean-toolchain replay, but it is not a clean-room
independent implementation under
[`ADVERSARIAL_REVIEW_PROTOCOL.md`](../../ADVERSARIAL_REVIEW_PROTOCOL.md).

### 8. The barrier winding orientation differs from the implementation

Page 18 writes the polygon increments as

\[
\arg\!\left(\frac{f(z_{j+1})}{f(z_j)}\right).
\]

The C implementation accumulates the reciprocal
\(f(z_j)/f(z_{j+1})\), which negates the winding orientation. This does not
affect either the strict \((-\pi,\pi)\) increment gate or the only
load-bearing conclusion, winding number zero. The distinction should still
be documented to avoid needless referee ambiguity.

The remainder of the barrier exposition agrees with the stored evidence:
883 consecutive prisms, 7,688 contained scalar coefficient components, a
minimum recomputed prism margin above
`0.519849894613872543`, and the stated uniform-error and Taylor-tail
bounds. The derivative-box transcription and coefficient-formula
provenance remain genuine human-review obligations.

### 9. Attribution and status language need tightening

Before this document can function as a referee report or publication
manuscript, a revised edition should:

- replace `Authors TBD` and fill the PDF Author/Title metadata;
- identify the exact audited tag and commit;
- identify the author or reviewer responsible for each claimed check;
- supply the promised source, logs, build commands, toolchain description,
  and hashes;
- reconcile the abstract's claim that no computation was independently
  confirmed with the later claimed Proposition 4.3 exception;
- qualify "the theorem inputs are settled" as the named expositor's
  assessment unless and until it is a signed referee finding;
- replace "self-contained" with "review-oriented" unless the missing
  computational supplement is included; and
- describe the title as an exposition of a **candidate** or **claimed**
  proof.

The citation to Csordas-Norfolk-Varga in the sentence about a sequence of
upper bounds should also be corrected: that cited paper concerns a lower
bound. The time-sensitive phrase "current record" is better written as
"the published Platt-Trudgian corollary \(\Lambda\le0.2\)" unless a current
literature search is recorded.

## What this audit did confirm

The following parts of the supplied exposition agree with the cited primary
papers and the sealed repository:

- the exact candidate parameters and
  \(893927/5000000=0.1787854\);
- the three-hypothesis Polymath Theorem 1.2 weld;
- the Platt-Trudgian height and exact surplus \(350479773/2\);
- the \(H_0\)-to-\(\xi\) sign map and the \(T=0\) eta-function argument;
- the conservative `10.50` derivation from Proposition 6.6(vi);
- the complete finite row count, endpoints, and global limiting floor;
- the native mollifier binding and finite/tail full-window overlap;
- the underlying tail certificate and its positive post-error margin;
- the barrier rectangle containment, \(t=0\) continuity argument, and
  convex half-subedge prism homotopy; and
- all stored barrier counts and directed numerical margins.

The repository's complete stored verifier was rerun after this audit. It
passed all 15 prerequisites and all 38 assembly gates, ending with:

```text
RESULT: UNCONDITIONAL CANDIDATE ASSEMBLY PASS
CONCLUSION: Lambda <= 893927/5000000 = 0.1787854.
STATUS: unreviewed computer-assisted unconditional proof candidate; not an established theorem.
RESULT: STORED UNCONDITIONAL-CANDIDATE REVIEW PASS
```

No fatal counterexample to the repository candidate was found in this
cross-check. That is not independent peer acceptance: the analytic
reductions, proof-to-code correspondence, and clean-room recomputation
requirements listed in
[`OPEN_REVIEW_QUESTIONS.md`](../../OPEN_REVIEW_QUESTIONS.md) remain open.

## Recommended reading order

1. Read this cross-check.
2. Read the supplied exposition PDF for its theorem-level narrative and ten
   clearly identified review points.
3. Use [`PROOF_NOTE.md`](../../PROOF_NOTE.md) and the theorem-level notes as
   the controlling repository statements.
4. Use [`REVIEW_SCOPE.md`](../../REVIEW_SCOPE.md) and
   [`ADVERSARIAL_REVIEW_PROTOCOL.md`](../../ADVERSARIAL_REVIEW_PROTOCOL.md)
   for independent sign-off.

For a corrected edition, request the LaTeX source, bibliography source,
finite-scan supplement, reproducible compile command, author identity,
audited commit, toolchain record, artifact hashes, and redistribution
permission from the expositor.
