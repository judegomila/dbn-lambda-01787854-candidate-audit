# Open mathematical review questions

These are the questions on which an external referee is asked to make an
independent judgment. They are not a list of acknowledged missing
hypotheses. The repository presently contains a candidate proof of each
item, but an adverse answer to any load-bearing question may invalidate the
conclusion.

The package's status remains: **unreviewed computer-assisted candidate for
an unconditional proof**, not an established or peer-reviewed theorem.

## Priority 1: canonical Theorem 1.2 weld

Please compare `PROOF_NOTE.md` directly with Theorem 1.2 of
arXiv:1904.12438v2.

- Is hypothesis (i) exactly the zeta zero-free region consumed by the
  Platt--Trudgian height, with the correct \(x=2T\) normalization?
- Is hypothesis (ii) exactly the final-time right region, with lower endpoint
  \(X+\sqrt{1-y_0^2}\) and the stated closed \(y\)-range?
- Is hypothesis (iii) exactly the curved intermediate-time barrier, including
  both endpoints \(t=0,t_0\)?
- Do these hypotheses yield
  \(\Lambda\le t_0+y_0^2/2\) with no additional premise?

Please check the cited theorem itself rather than relying solely on the
transcribed upstream criterion note.

## Priority 2: closed barrier certificate

Please audit `BARRIER_CERTIFICATE.md` and
`barrier/src/TloopSinglemat_closed_cert.c`, with the derivative theorem in
`DERIVATIVE_BOX_LEMMA.md`.

1. Do the endpoint-separated factors and strict monotonicity gates turn
   pointwise Polymath Lemma 8.4 into uniform \(D_z,D_t\) bounds on the
   complete closed box?
2. Does the exact 16-term head plus decreasing-tail integral rigorously
   majorize each discrete Lemma 8.4 sum, and do the complex analytic
   callbacks satisfy FLINT's quadrature contract?
3. Does the nearer-endpoint convex-disk argument on each half-subedge
   justify the spatial term \(D_z/[2(\mathrm{num}-1)]\) for the complete
   zero-avoiding polygon homotopy?
4. Is \(D_t\) interval-evaluated on each complete closed proposed prism, and
   does the strict prism inequality give a zero-avoiding homotopy for every
   intermediate time?
5. Do zero-free endpoint balls, argument increments in \((-\pi,\pi)\), and a
   winding enclosure inside \((-1/4,1/4)\) rigorously force winding number
   zero?
6. Are the exact dyadic seams consecutive and is every failure or
   indeterminate interval comparison fatal?
7. Is the passage from the polygon for \(f_t\) to \(H_t/B_t\), followed by
   the argument principle, valid on the closed rectangle?
8. Is the proof that \(B_t\ne0\) on this domain complete?
9. Is the compact continuity argument extending Theorem 1.3 to \(t=0\)
   valid, including continuity of the fixed-window \(f_t\) and its error
   majorant?

The target uses this new 883-prism certificate. The historical winding
artifacts in `vendor/` are provenance only and should not be mistaken for a
premise of the new certificate.

## Priority 3: barrier coefficient and error provenance

Please check:

- whether adding
  \(10^{-20}\max(1,|\text{component}|)\) to each printed component safely
  restores the 20-decimal coefficient matrix;
- whether all \(7,688\) regenerated Arb components are derived from the
  intended source formula and contained in those restored balls;
- whether the factorial Taylor-tail estimate is complete and its
  \(10^{-20}\) allowance is propagated into every value;
- whether equations (20)--(23) and the conservative Proposition 6.6(vi)
  corollary are evaluated on the entire closed barrier box;
- whether `ERROR_CONSTANT_WELD.md` correctly derives
  \(3.58+6.92=10.50\) after the denominator enlargement and therefore
  removes all reliance on displayed equation (24)'s \(10.44\);
- whether the proof of the uniform \(|\gamma|n^y\) bound is valid for every
  \(1\le n\le N\); and
- whether \(0.00125\) is therefore a valid common approximation allowance.

The target path uses \(x-6.66\) for \(e_A+e_B\) and \(x-12,\ 10.50\) for
\(e_{C,0}\). The historical \(10.44\) and denominator-transcription issues
are not consumed by the target implementation; the review task is to verify
the conservative weld and its six numerical consumers.

## Priority 4: native Triangle-to-\(|f_t|\) lemma

Please check `NATIVE_BINDING.md` against equation (14) and the definitions in
Polymath Theorem 1.3.

- Are the two exact convolution identities correct, particularly
  \(\overline E C_0=\sum A_{N,n}n^{-\overline{s_*}}\)?
- Are all mollifier coefficients real in every producer branch?
- Does the complex-\(\kappa\) estimate
  \(|m^{-\kappa}-1|\le m^{|\kappa|}-1\) supply exactly the implemented
  correction?
- Does positivity of \(L_N\) imply \(Q_N>0\), rule out \(E=0\), and give the
  correct inequality direction when \(1/|E|\) is replaced by \(1/M_N\)?
- Does the source-to-formula map account for every term and sign in
  `src/lemma_sweep_p235711.c`?
- Are the stored \(T_N\) values consequently in the same normalized units as
  the additive Theorem 1.3 error, with no further Euler factor?

This is now an explicit theorem and stress-tested source contract, not an
assumed interface. It nevertheless remains load-bearing mathematics for the
referee to validate.

## Priority 5: complete finite height and window transfer

Please audit both the all-\(y\) and all-\(x\) reductions.

For the direct Dini proof:

- Is the upper-right Dini derivative handled correctly at zeros of
  \(A_{N,n}\)?
- Is the negative \(\gamma g|A|\) term retained with the correct sign?
- Is the composite-divisor factor
  \(\sum_{p\mid d}\log^2p\) correct?
- Do the \(3^{|\mathcal P|}\) cells exhaust every active sign pattern?
- Are the padded binary64 cell endpoints one-sided in the required
  direction?
- Does local Lipschitz continuity justify passage from pointwise upper-Dini
  bounds to global monotonicity?
- Are the normalizer and \(\kappa\)-correction monotonicity arguments
  sufficient to transfer \(L_N(y_0)\) to the full height range?

For the window freeze:

- Are \(G\) and \(K\) decreasing and \(\Sigma\) increasing in \(x\), including
  the positive-part kink?
- Is \(x_*=X+\sqrt{1-y_0^2}\) rigorously inside \(W_{690988}\)?
- Does the convention \(W_N=[x_N,x_{N+1})\) cover every endpoint exactly
  once, and do the constants reset conservatively?
- Does the finite/tail overlap at \(N=3840000\) eliminate the final endpoint
  risk?

The invalid historical multi-prime `standard-majorant` route,
`seam_ytransfer`, and exponent-inflation seam are not consumed.

## Priority 6: standalone all-\(N\) tail theorem

Please audit `TAIL_LEMMA.md` and `verifiers/verify_tail_arb.c`.

- Does the endpoint-cap lemma bound every routed sum under its checked
  monotonicity condition?
- Is equation (4.3) a disjoint and exhaustive convolution partition?
- Is `OV` genuinely optional nonnegative padding rather than a missing or
  double-counted term needed for the identity?
- Do the cap-derivative gates prove decrease for every \(N\ge3840000\), not
  merely sampled \(N\)?
- Is the moving-cap argument, including floors and \(N/(d+1)\), valid?
- Do the \(y\)-monotonicity gates cover
  \(y_0\le y\le\sqrt{1-2t}\), and is the complete \(t\)-interval evaluated
  without assuming monotonicity in \(t\)?
- Are the exact error definitions (71)--(72) and the conservative
  Proposition 6.6(vi) corollary bounded with the claimed all-\(N\)
  directions?
- Does
  \[
  |M_\lambda(s_*)f_t-1|\le D<1
  \]
  together with the \(M_{\max}\) bound yield the stated normalized
  post-error margin?
- Does nonvanishing of \(B_t\) complete the passage to \(H_t\)?

The primary certificate is one standalone FLINT/Arb implementation run at
256 and 512 bits and independently parsed. The separate 160/256-bit Python
interval implementation supplies cross-implementation corroboration and
source-lineage evidence, not the sole justification.

## Priority 7: implementation independence and reproducibility

The previously open numerical-backend blocker for Proposition 4.10 — that
both programs computing the finite-region error budget shared one
`mpmath.iv` backend, so exact endpoint comparison was conditional on that
single library's outward rounding of transcendental interval operations —
is closed: `verifiers/verify_prop410_arb.c` now certifies the budget
authoritatively in FLINT/Arb at 256 and 512 bits (assembly prerequisite
P17), and the `mpmath` path is recorded as same-backend corroboration.
The remaining referee task for that lane is the proof-to-code map of the
Arb program against the Proposition 4.10 formulas, including its directed
endpoint/majorant substitutions (documented in the program header).

Please reproduce at least the decisive small margins in a different build
environment. Ideally:

- rerun the barrier coefficient generator and all 883 prisms;
- compile the tail verifier with an independently built FLINT/Arb;
- rerun direct non-amortized finite checks at the weakest row, every
  prime-set joint, every compressed-shard joint, and \(N=3840000\);
- run the Dini and producer paths under sanitizers; and
- perform the complete finite regeneration or independently sample and
  recompute its canonical tuples.

`MAXIMUM_CHECKS.md` records the checks already performed. Agreement is strong
evidence of reproducibility but cannot establish the analytic reductions by
itself.

## Priority 8: final theorem assessment

After auditing the components, please state explicitly:

1. whether hypotheses (i), (ii), and (iii) of Polymath Theorem 1.2 are each
   established on the exact closed domains;
2. whether any step still relies on an unproved conjecture;
3. whether any software check is circular with the claim it is intended to
   validate;
4. whether a correction is local or invalidates the target bound; and
5. whether the package may properly advance beyond “unreviewed
   computer-assisted candidate for an unconditional proof.”

Until that review exists, automated `PASS` output must not be described as
peer acceptance.
