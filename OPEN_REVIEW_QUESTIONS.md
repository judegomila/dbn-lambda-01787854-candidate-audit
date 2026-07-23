# Open mathematical review questions

These are known questions, not hidden caveats.  A reviewer is specifically
asked to decide whether each item is valid, repairable, or fatal to the
candidate implication.

## Priority 1: native Triangle binding

`provenance/TRIANGLE_NORMALIZER_CORR_MONOTONICITY.md` sections 3--4 claims
that

\[
L_N(y)=\frac{1-\mathcal F_N(y)}{M_N(y)}-K_N(y)
\]

is the producer's native lower bound for \(|f_t|\), so that the final finite
gate is \(T_{\min}-E_{\max}>0\), with no second Euler conversion factor.

Please check this directly against the definitions and error terms in
arXiv:1904.12438v2 and the finite producer.  The package's numerical checks
do not by themselves prove that this functional is bound to the paper's
\(f_t\) in the asserted units.

## Priority 2: winding slab rigor

The consumed upstream slab is vendored at
`vendor/dbn21a/certificates/certified1875/windslab165_v2/`.
Its stored region contains the target point, but its producer/log interface
needs theorem-level scrutiny:

- key quantities are printed as midpoint decimal values rather than complete
  interval endpoints;
- the production C path contains comparisons whose failure behavior should be
  checked for fail-closed semantics;
- the argument from the recorded rectangles to a closed real \(t\)-prism
  should be verified, not inferred from sample points;
- the corner second line spot-checks only part of the 492-rectangle chain and
  is not a complete independent proof of the slab.

Please determine whether the primary stored certificate is nevertheless
rigorous, and if not, specify the smallest interval-output or coverage repair.

## Priority 3: direct Dini reduction

Check the proof in
`provenance/TRIANGLE_Y_DINI_THEOREM.independent.md`, especially:

- the upper-right Dini derivative at zeros of \(A_{N,n}\);
- retention of the negative \(\gamma g|A|\) term;
- the composite-divisor factor
  \(\sum_{p\mid d}\log^2p\);
- exhaustion of all active divisor patterns by \(3^{|P|}\) cells;
- one-sided replacement of \(N\) by the smallest feasible value;
- padded binary64 endpoints and the passage from pointwise upper-Dini
  inequalities to global monotonicity.

The earlier multi-prime `standard-majorant` route is invalid and is not
consumed.

## Priority 4: error-term transcription

`provenance/ERROR_TERMS_AUDIT.upstream.md` section 4 records an
`x-6.66` implementation denominator where Proposition 6.6(vi) displays
`x-12`.  The stored audit argues that the discrepancy is numerically
negligible and absorbed by later slack.  Please check the direction and the
claimed absorption from the paper, preferably by rerunning the target bound
with `x-12` throughout.

## Priority 5: tail theorem and implementation

The target tail block is a patch to a deposited 0.1875/0.1891 engine.
`verifiers/verify_tail_patch_provenance.py` proves the source transformation,
but a reviewer should still check that the generic `run_band` theorem applies
at \(N_{\rm mid}=3840000\), \(M=153814\), the target \(t\)-box, and the full
extended \(y\)-box.

## Priority 6: interval independence

The decisive tail, effective-error, and normalizer checks use `mpmath.iv`.
Changing precision within the same implementation is not an independent
interval library.  An Arb/FLINT or MPFI reproduction of the smallest decisive
margins would materially strengthen the result.

## Priority 7: finite producer spot checks

The complete stored sweep is structurally checked and sealed.  Please add or
request direct non-amortized producer checks at:

- the weakest row \(N=690988\);
- every prime-set joint;
- every compressed-shard boundary;
- the finite/tail overlap \(N=3840000\).

The first P11 row is expensive and is not part of the quick container path.

## Priority 8: criterion weld

Finally, check that the verified-height, full right-half-line nonvanishing,
winding, endpoint, and site hypotheses match Theorem 1.2 of
arXiv:1904.12438v2 with no swapped hypothesis labels or open-endpoint gaps.
