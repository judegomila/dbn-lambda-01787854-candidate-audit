# SITE-UNIFORM window gluing at X = 6000000185827 (all t0 ≤ 0.1809) + 0.1965-row instantiation

Prepared 2026-06-12. Strict extension of the VERIFIED the auxiliary line
lemma (claims/nconst_gap_v2/, memory #57), which certified the sweep-window
gluing margins ONLY at the single point t0 = 1775/10000. This bundle certifies
the gluing inequalities t0-UNIFORMLY over the ENTIRE certified-barrier slab
t-range [0, 1809/10000], and instantiates the precondition row for the
Λ ≤ 0.1965 campaign target (t0 = 1770/10000) the system is converging on.

## 1. Direction note: future-proof the P10/P11 preconditions

DIRECTION. The previously verified precondition audit identified P10 (slab
N-constancy) and P11 (sweep-window/slab gluing) as the record-chain
preconditions that "live between legs and default to nobody". an earlier run pinned them
at the 0.197 row's t0 = 0.1775 only. The system's active queue is now rows at
OTHER t0 at the SAME site X = 6000000185827, N0 = 690988:

- Λ ≤ 0.1965 (t0 = 1770/10000): the survey line's verified aim197 fact (#20)
  certifies the row is grid-sharp for Euler-2 but the the producer host/the producer host deliverys
  (two external producer-host imports) supply
  Euler-3 selection > 0.18 at exactly this row, and the producer line's a pinned earlier run
  journal lead #1 is "adopt the external stretch-row tail import (t0=0.1770,
  Lambda <= 0.1965)". When that chain assembles, it needs P10/P11 at
  t0 = 0.1770 — covered by NO pinned fact (the earlier run covers t0 = 0.1775 only).
- Rung menu t0 = 162/1000, 161/1000, 160/1000 (the survey line, memory #52):
  same site, same N0, same future P10/P11 need.

Rather than re-certify per row (one rejected-claim-risk per row, forever),
certify ONCE, t0-uniformly: evaluate the exact window-start formula
ws(N,t) = 4πN² − πt/4 over the whole t-interval [0, 0.1809] in directed-rounded
interval arithmetic and compare endpoints to X and X+1 as exact rationals. Any
row with t0 ≤ 0.1809 at this site — every row the certified barrier artifact
can ever serve, since the winding slab tops at t = 0.1809 — inherits the
margins by containment (one exact-rational comparison, gated per rung in G).

NON-DUPLICATION (checked against the campaign policies + all 58 verified results,
2026-06-12 ~02:35 UTC):
- the auxiliary line (#57, my own): point t0 = 1775/10000 margins only; the fact
  text says "the t0=0.1775 sweep windows glue". The uniform statement, the
  uniform margins 5377392.8789 / 11989041.1415, the 0.1965-row point margins
  5377393.0179 / 11989041.1446, and the 0.1965-row criterion arithmetic
  (R1–R5) appear in no pinned fact.
- the producer line (lemma packages): record_binding (#55) proves the window-TILING
  identity (windows N, N+1 abut as formulas) — an algebraic identity, not the
  site-anchored gluing margins at X; criterion_theorem's B9 is N-constancy at
  the 0.2-row X = 5e12+194858. Neither touches X = 6000000185827 gluing.
- the survey line (frontier/params): aim197 (#20) certifies the 0.1965 row's
  selection grid-sharpness; rungmap/rung178 (#37/#52) certify Dirichlet
  anchors; ybridge (#54) is the y-transfer of the sweep functional. None
  states a window-gluing or N-constancy precondition.
- the producer (production campaigns): its winding fact and record-package
  attempts gate constancy at t ∈ [0, 0.1775] only (the earlier audits, and
  the 01:51 UTC rejection, confirm).
- the independent verifier (second lines on pinned statements): no pinned fact on
  window gluing; its windrect second line covers mesh values.
- approximation_designer: scheme boxes have t ∈ [0.12125, 0.18375] and state
  N-constancy only on those boxes; no gluing content.

CHEAPEST DECISIVE TEST. One interval evaluation of ws(N0, ·) and ws(N0+1, ·)
over the t-hull at prec 250, exact-rational endpoint comparison vs X, X+1.
Cost < 5 s. Decisive both ways.

KILL CRITERION. (a) If sup_t ws(N0,t) ≥ X or inf_t ws(N0+1,t) ≤ X+1 the
uniform lemma is FALSE and per-row gluing certificates become mandatory
(bankable negative: it would mean some admissible row's sweep indexing does
NOT cover [X, X+1]). (b) The direction dies if a pinned fact already states
t0-uniform gluing at this site (re-checked: none does; nearest facts named
above). (c) single-pass direction; if a production line wants per-row
re-statements beyond the containment gate, that is their lane.

## 2. What is certified (verify_site_glue.py, 19 checks)

All endpoint extraction via the independently verified exact `_mpi_` binary-tuple path
(self-test C0). All printed decimals are FLOOR truncations machine-derived
from exact endpoint rationals; certified threshold strings are gated to EQUAL
the machine-printed truncations (U3, R8).

- U1: X − sup_{t∈[0,0.1809]} ws(N0, t) ≥ 5377392.8789 — window N0 starts
  strictly below X at EVERY t0 in the slab range.
- U2: inf_{t∈[0,0.1809]} ws(N0+1, t) − (X+1) ≥ 11989041.1415 — window N0+1
  starts strictly past X+1 at every such t0.
  (Together: for every t0 ≤ 0.1809, the per-N sweep indexing at N0 covers all
  x ∈ [X, X+1] with no window boundary inside the slab. The t-spread of ws
  over the whole range is ≤ π·0.1809/4 < 0.15, so the two margins differ from
  the earlier point values only in the 4th decimal — stated for context, the
  certificates are the endpoint comparisons.)
- S1: re-assertion of the pinned N-constancy (N = 690988 on
  [X, X+1] × [0, 0.1809]) so the bundle is self-supporting: U1+U2+S1 retire
  P10/P11 for ANY row at this site with t0 ≤ 0.1809.
- S2: window-identity sanity at both t-extremes (N just past ws(N0,t) is N0).
- R1–R8: the Λ ≤ 0.1965 row (t0 = 1770/10000, y0² = 39/1000): functional
  arithmetic t0 + y0²/2 = 1965/10000 EXACTLY, criterion validity
  y0² + 2t0 = 393/1000 ≤ 1, range condition, slab containment
  (y0² = 39/1000 ≥ (1809/10000)², t0 ≤ 1809/10000), PT2021 admissibility
  X/2 ≤ T_PT exact, and the row's own sharper point gluing margins
  ≥ 5377393.0179 / ≥ 11989041.1446.
- G: the three rung-menu t0 values (162/1000, 161/1000, 160/1000) lie in
  [0, 1809/10000], so U1/U2/S1 apply to each by containment.

RH-height dependency: NONE in U/S/G/R6–R8 (finite interval arithmetic at
fixed X); R5 is the exact PT2021 height comparison the chains consume; any Λ
chain these preconditions serve is unconditional via PT2021.

## 3. Verify

Copy claims/site_glue_v1/ anywhere, run `/usr/bin/python3 verify_site_glue.py`.
No disk reads, imports mpmath + stdlib only. Machine-prints
"TOTAL CHECKS RUN: 19" and "RESULT: ALL PASS", exit 0 in < 5 s.
