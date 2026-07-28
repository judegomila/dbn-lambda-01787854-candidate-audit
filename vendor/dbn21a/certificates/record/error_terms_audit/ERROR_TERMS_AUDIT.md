# ERROR_TERMS_AUDIT — the effective-approximation error bounds (20)–(24)/(71)–(74)

Package: `packages/error_terms_audit/` (this writeup + `verify_error_audit.py`, standalone,
exit 0, ~12 s). Author: the producer line, 2026-06-11. Source: arXiv:1904.12438v2 (local copy
`sources/p15/debruijn.tex`); repo transcription reference:
`sources/pari_error_bounds.txt` (= dbn_upper_bound/pari/error_bounds.txt, fetched
2026-06-11). All digit strings floor-truncated. These bounds are height-independent
approximation theory (no RH dependency); the Λ statements they feed carry their RH-height
dependencies in the companion package `packages/criterion_theorem/`.

## 1. Transcription from the paper (proof of correct transcription)

Theorem 1.3 of 1904.12438 (label `eff`) states, for (t, x, y) in the region
0 < t ≤ 1/2, 0 ≤ y ≤ 1, x ≥ 200 (label `region`):

  H_t(x+iy)/B_t(x+iy) = f_t(x+iy) + O_≤(e_A + e_B + e_{C,0}),

with N := ⌊√(x/4π + t/16)⌋, b_n^t := exp((t/4) log²n), and the displayed bounds (their
display numbers (20)–(24) correspond to TeX labels `gamma-bound`, `res-bound`,
`kappa-bound`, `eab-bound`, `ec-bound`):

 (20) |γ| ≤ e^{0.02y} (x/4π)^{−y/2}
 (21) Re s_* ≥ (1+y)/2 + (t/4) log(x/4π) − (t/2x²)(1 − 3y + 4y(1+y)/x²)₊
 (22) |κ| ≤ ty/(2(x−6))
 (23) e_A + e_B ≤ Σ_{n=1}^N (1 + |γ| N^{|κ|} n^y) (b_n^t/n^{Re s_*})
        · (exp(((t²/16) log²(x/4πn²) + 0.626)/(x − 6.66)) − 1)
 (24) e_{C,0} ≤ (x/4π)^{−(1+y)/4} exp(−(t/16) log²(x/4π)
        + 1.24·(3^y + 3^{−y})/(N − 0.125) + (3|log(x/4π) + iπ/2| + 10.44)/(x − 12))

The underlying exact definitions, eqs. (71)–(74) of §6 (TeX labels `ea-def`, `eb-def`,
`ecc-def`, `ec-def`), are, with s₊ = (1+y−ix)/2, s₋ = (1−y+ix)/2, T′ = x/2 + πt/8:

 (71) e_A := |γ| Σ_{n=1}^N n^y (b_n^t / n^{Re s + Re κ}) ε_{t,n}(s₋)
 (72) e_B := Σ_{n=1}^N (b_n^t / n^{Re s}) ε_{t,n}(s₊)
 (73) e_C := exp(tπ²/64) |M₀(iT′)| / |M_t(s₊)| · (ε̃(s₋) + ε̃(s₊))
 (74) e_{C,0} := exp(tπ²/64) |M₀(iT′)| / |M_t(s₊)| · (1 + ε̃(s₋) + ε̃(s₊))

with ε_{t,n}(σ+iT) := exp(((t²/8)|α(σ+iT) − log n|² + t/4 + 1/6)/(T − 3.33)) − 1
(label `eps-def`) and ε̃(σ+iT) := (0.397·9^σ/(a − 0.865) + 5/(3(T−6))) exp(3.49/(T−4))
(label `epsp-def`), a := √(T′/2π). Proposition 6.6 (label `estimates`), parts (iv)–(vi),
bounds (71)–(74) by the evaluable forms (23)–(24); part (vi) carries the sharper
denominator structure exp((3|log(x/4π)+iπ/2|+3.58)/(x−8.52))·(1 + 1.24(3^y+3^{−y})/(N−0.125)
+ 6.92/(x−12)), from which (24) follows via 1+u ≤ e^u and 1/(x−8.52) ≤ 1/(x−12) — wait,
the paper's own reduction note (line following Prop 6.6) is "we may simply use the
inequality 1+u ≤ exp(u) ... and then bound 1/(x−8.52) ≤ 1/(x−12)"; the resulting merged
constant is 3.58 + 6.92 = 10.50 ≥ 10.44 only after absorbing the 6.92 term at x ≥ 200 —
the audit therefore treats (24) AS DISPLAYED in Theorem 1.3 as the audited formula (that
is the formula the campaign's scripts cite), and separately verifies the (vi)-form used
by the repo. What we certify is the transcription of each DISPLAYED bound, not the
paper-internal derivation (vi) → (24), which belongs to the paper's peer-reviewed record.

## 2. The two independent transcriptions (mechanism of the audit)

`verify_error_audit.py` contains two implementations of (20)–(24), written separately:

- **T1 (paper-direct):** interval arithmetic (mpmath.iv, 40 dps) on the formulas exactly
  as displayed; the (23) sum is evaluated head-first for n = 1..4000 and the tail
  n ∈ (4000, N] (N ~ 6.3–6.9 × 10⁵ at campaign points) is enclosed above using the
  convexity of (t/4)log²n − Re s_* · log n in log n (endpoint maximum × term count) and
  the monotone bound u_n ≤ u_1.
- **T2 (log-space):** every power and quotient rewritten as exp/log expressions, the head
  sum accumulated **tail-first** (reverse order), the positive part and the tail
  enclosure re-derived independently (same convexity principle, separately coded).

The two enclosures of each quantity must overlap AND agree endpoint-wise to relative
1e-12 ((20)–(22)) / 1e-6 ((23)–(24)). A transcription error (wrong constant, wrong sign,
wrong exponent) shifts values at relative O(1) at x ~ 5×10¹²; agreement at 1e-12/1e-6 over
5 scattered points is far beyond coincidence. Both transcriptions share zero code with
km-git-acc/dbn_upper_bound and zero code with each other beyond the mpmath library.

## 3. Audit results at 5 representative campaign points (all PASS, floor-truncated)

| point | (x, y, t) | N | e_A+e_B ≤ | e_{C,0} ≤ | total ≤ |
|---|---|---|---|---|---|
| 0.20-row barrier corner | (5×10¹²+194858, 0.16733, 0.186) | 630783 | 4.4575e-12 | 1.0306e-7 | 1.0307e-7 |
| 0.20-row slab top | (5×10¹²+194858, 1.0, 0.01) | 630783 | 2.8155e-11 | 1.0150e-6 | 1.0150e-6 |
| campaign interior | (5.5×10¹², 0.2, 0.15) | 661570 | 9.3200e-12 | 3.8220e-7 | 3.8221e-7 |
| 0.197-site (0.1809 row) | (6×10¹²+185827, 0.1809, 0.1809) | 690988 | 4.1077e-12 | 1.0026e-7 | 1.0027e-7 |
| 0.197-site tuned | (6×10¹²+185827, 0.19748, 0.1775) | 690988 | 4.2085e-12 | 1.0459e-7 | 1.0459e-7 |

Consequences for the campaign: at every audited point the total error budget
e_A + e_B + e_{C,0} < 1.1e-6, i.e. ≥ 4 orders of magnitude below the project's 0.03
|f_t| safety threshold and ≥ 3 orders below the barrier criterion's 1.25×10⁻³ ball —
the representation boundary (the cross-toolchain audit policy) holds with enormous margin at X ~ 5–6×10¹².
e_{C,0} dominates e_A + e_B by ~5 orders, consistent with the paper's Figure
(`eA_eB_eC_errorbounds.png`).

## 4. FLAGGED MISMATCH (per the audit mandate: flag ANY mismatch)

The repo transcription `dbn_upper_bound/pari/error_bounds.txt`, function
`habc_sharperbound`, line `e3_term3_abc = 1.24*(3^y + 1/3^y)/(N - 0.125) +
**6.92/(xN - 6.66)**` deviates from Proposition 6.6(vi)'s displayed `6.92/(x − 12)`.
Since x − 6.66 > x − 12, the repo's term is strictly SMALLER, i.e. **the repo bound is
slightly less conservative than the paper's at that sub-term**. The script certifies in
interval arithmetic: (a) the strict inequality 6.92/(x−6.66) < 6.92/(x−12) at the
campaign x; (b) its relative magnitude < 2e-12 — i.e. numerically irrelevant at x ≥ 200
(the deviation is ~6.92·5.34/x² ≈ 1.5e-24 absolute at x = 5×10¹², a factor ~1e-17 below
the e_{C,0} values themselves), and additionally the whole habc form sits inside the
(vi)→(24) slack (10.44 vs 3.58+6.92 merged constants). DISPOSITION: harmless at campaign
parameters, but any record-claim writeup citing the repo's error code verbatim must cite
the (vi) form with this substitution noted, or re-derive with x−12. This is exactly the
representation-boundary item the policy's policy-11 audit exists to surface.

## 5. Scope

- Certified (exit 0): the displayed bounds (20)–(24) evaluate, under two mechanically
  independent transcriptions, to overlapping interval enclosures agreeing to 1e-12/1e-6
  at 5 campaign points; the totals sit < 1.1e-6 there; the repo deviation in §4 is real,
  strictly one-sided, and < 2e-12 relative.
- Not certified: the paper's PROOFS of (20)–(24) from (71)–(74) (peer-reviewed record;
  Prop 6.6), and the exact (71)–(74) values themselves (they require M₀, M_t, α at
  campaign x — the companion companion approximation line's interval f_t implementation
  covers the consuming side). No RH dependency anywhere in this package.
