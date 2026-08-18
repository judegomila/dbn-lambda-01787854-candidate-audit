# Preliminary direct phase-orbit screen

**Status: non-rigorous sampled diagnostic only. No new bound is certified.**

The screen keeps the existing `y0^2 = 87677/2500000` so the already-certified rectangular barrier contains the lower-time curved barrier. It evaluates the exact finite Polymath approximant `f_t` and its P13 Euler-mollified value at five points in each of five representative Riemann--Siegel windows.

| t | objective if all criterion obligations closed | sampled global min | sampled global min Re | location N |
|---:|---:|---:|---:|---:|
| 0.130 | 0.1475354 | 0.915230628307 | 0.915175946913 | 850000 |
| 0.125 | 0.1425354 | 0.915337415039 | 0.915254275381 | 850000 |
| 0.120 | 0.1375354 | 0.914664398682 | 0.914612849018 | 850000 |

The sampled mollified approximant remains in the right half-plane with an order-one margin at every tested point. This is evidence that the triangle-majorant failure at lower time is not accompanied by an obvious collapse of the actual complex sum. It is not a lower bound between sample points and does not address the final tail.

Representative windows: `N = 690988, 850000, 1075000, 2000000, 4050000`; fractions `0, 0.25, 0.5, 0.75, 0.999` of each window.

The accompanying jet sample evaluates `(|E f|^2)'` and `(|E f|^2)''` at the two early windows. The derivatives are not small enough to make a coarse Lipschitz mesh competitive; phase-aware interval propagation or the sharp two-channel functional is still required.
