# THEOREM_LAMBDA_CRITERION — the instantiated upper-bound criterion Λ ≤ t₀ + y₀²/2

Package: `packages/criterion_theorem/` (this writeup + `verify_criterion.py`, standalone, exit 0).
Author: the producer line, 2026-06-11. Sources: arXiv:1904.12438v2 (Polymath 15; local
copy `sources/p15/debruijn.tex`, statement labels cited by TeX label), arXiv:2004.09765
(Platt–Trudgian 2021), N. G. de Bruijn, Duke Math. J. 17 (1950), Theorem 13.

All decimal digit strings below are **floor-truncated** unless marked "exactly".
Every Λ statement carries its RH-height dependency explicitly.

---

## 0. Setup and normalization

Throughout, ξ is the completed zeta function and H_t the de Bruijn heat-flow family:

  ξ(s) := (s(s−1)/2) π^{−s/2} Γ(s/2) ζ(s)          (1904.12438 eq. `sas`),
  H₀(z) := (1/8) ξ(1/2 + iz/2)                      (eq. `hoz`),
  H_t(z) := ∫₀^∞ e^{tu²} Φ(u) cos(zu) du            (eq. `htdef`),

with Φ(u) := Σ_{n≥1} (2π²n⁴e^{9u} − 3πn²e^{5u}) exp(−πn²e^{4u}) > 0 for u ≥ 0.
Λ is the de Bruijn–Newman constant: H_t has only real zeros iff t ≥ Λ.

### Lemma 0.1 (x ↔ 2·(ζ-height) normalization).
The map s ↦ z(s) := −2i(s − 1/2) = 2·Im(s) + i(1 − 2·Re(s)) is a bijection from ℂ to ℂ
under which the zero sets correspond: H₀(z(s)) = 0 ⟺ ξ(s) = 0. In coordinates: a zero
ξ(σ + iT) = 0 corresponds to the zero H₀(x + iy) = 0 with

  **x = 2T,  y = 1 − 2σ.**

Consequently: (a) RH verified to ζ-height T (all zeros ρ = β+iγ of ζ with 0 ≤ γ ≤ T have
β = 1/2) is equivalent to: all zeros of H₀ with 0 ≤ Re z ≤ 2T and |Im z| ≤ 1 are real.
(b) A barrier at abscissa X consumes RH height T_req = X/2.

*Proof.* H₀(z) = (1/8)ξ(1/2 + iz/2) by definition (eq. `hoz`); 1/8 ≠ 0, so H₀(z) = 0 iff
ξ(1/2 + iz/2) = 0. Setting s = 1/2 + iz/2 and solving, z = −2i(s − 1/2); writing s = σ+iT
gives z = −2i(σ − 1/2 + iT) = 2T + i(1 − 2σ), i.e. x = 2T, y = 1 − 2σ exactly. The strip
0 ≤ σ ≤ 1 (which contains all ξ zeros, since ξ and ζ share zeros in the strip and ξ has no
others) maps to −1 ≤ y ≤ 1; the critical line σ = 1/2 maps to y = 0. A ζ zero at height
0 ≤ γ ≤ T off the critical line (β ≠ 1/2) would give a non-real H₀ zero with 0 ≤ x ≤ 2T,
and conversely (using ξ(s) = ξ(1−s) and ξ(s̄) = conj ξ(s), zeros come in the quadruple
σ, 1−σ, conjugates, so WLOG the representative has 1/2 ≤ σ ≤ 1, T ≥ 0). ∎

(The verify script checks the algebra of Lemma 0.1 symbolically with sympy and spot-checks
numerically that H₀(2γ₁) ≈ 0 at the first zeta zero γ₁ = 14.1347251417… while H₀(2γ₁+0.5)
is not small.)

## 1. The generic criterion (Polymath 15, Thm 1.2 = TeX label `ubc-0`)

**Theorem 1.1** (Upper bound criterion; 1904.12438 Theorem 1.2). Suppose t₀, X > 0 and
0 < y₀ ≤ 1 obey:

 (i) *(RH at time 0)* There are no zeros ζ(σ+iT) = 0 with (1+y₀)/2 ≤ σ ≤ 1 and
     0 ≤ T ≤ X/2.
 (ii) *(Asymptotic zero-free region at time t₀)* There are no zeros H_{t₀}(x+iy) = 0 with
     x ≥ X + √(1−y₀²) and y₀ ≤ y ≤ √(1−2t₀).
 (iii) *(Barrier at intermediate times)* There are no zeros H_t(x+iy) = 0 with
     X ≤ x ≤ X + √(1−y₀²), √(y₀² + 2(t₀−t)) ≤ y ≤ √(1−2t), and 0 ≤ t ≤ t₀.

Then **Λ ≤ t₀ + y₀²/2**.

*Proof (assembled, self-contained modulo the two cited ingredients).*

**Ingredient A** (de Bruijn 1950, Thm 13 = 1904.12438 Theorem 3.2, label `debr-bound`):
if H_{t₀} has no zeros with Im z > y₀ then for t > t₀, H_t has no zeros with
Im z > max(y₀² − 2(t−t₀), 0)^{1/2}; in particular Λ ≤ t₀ + y₀²/2 (take t = t₀ + y₀²/2;
then the zero-free bound is 0, and since non-real zeros of H_t come in conjugate pairs,
H_t has only real zeros).

**Ingredient B** (zero dynamics, 1904.12438 Prop. 3.1, label `dynam`): for simple zeros,
z_k(t) moves by dz_k/dt = 2 Σ'_{j≠k} 1/(z_k − z_j) (suitably summed), and repeated zeros
release at least one zero pair into Im z > 0 backward in time.

**Step 1** (Prop. 3.3 of 1904.12438, label `ubc`, with its proof). Claim: hypotheses
 (i') no zeros H₀(x+iy) = 0 with 0 ≤ x ≤ X and √(y₀²+2t₀) ≤ y ≤ 1,
 (ii), (iii) as above
imply that H_{t₀} has no zeros with x ∈ ℝ, y ≥ y₀.

Proof of Step 1: ξ has no zeros outside 0 ≤ Re s ≤ 1, so (Lemma 0.1) H₀ has no zeros with
y > 1; by Ingredient A applied at t₀ = 0 with that zero-free region, the constraints
y ≤ 1, y ≤ √(1−2t₀), y ≤ √(1−2t) in (i'), (ii), (iii) can be removed. Suppose for
contradiction some 0 < t₁ ≤ t₀ is minimal with a zero of H_{t₁} in
Ω(t₁) := {0 ≤ x ≤ X, y ≥ Y(t₁)}, Y(t) := √(y₀² + 2(t₀−t)). (Minimal t₁ exists by
continuity of H_t in t and the absence of zeros with y > 1.) At t = 0 the region Ω(0) is
zero-free by (i'). By Rouché/continuity, the offending zero at t₁ lies on ∂Ω(t₁). The
side x = X is excluded by (iii); the side x = 0 is excluded because H_t(iy) =
∫₀^∞ e^{tu²}Φ(u) cosh(yu) du > 0 (positivity of Φ). So H_{t₁}(x + iY(t₁)) = 0 for some
0 < x < X. If this zero is repeated, Ingredient B produces, for t < t₁ near t₁, a zero in
Ω(t), contradicting minimality. If simple, the velocity computation in 1904.12438 (proof
of Prop 3.3) shows Im dz_j/dt(t₁) < dY/dt(t₁) = −1/Y(t₁): each zero with |Im z_k| ≤ Y(t₁)
contributes non-positively; the conjugate at x − iY(t₁) contributes exactly −1/Y(t₁); a
zero pair with y_k > Y(t₁) contributes ≤ 0 iff y_k² ≤ (x−x_k)² + Y(t₁)², which holds
because (iii) forces |x_k| ≥ X + √(1−Y(t₁)²) hence (x−x_k)² ≥ 1 − Y(t₁)², while y_k < 1
by the de Bruijn-propagated strip bound. So the zero crosses INTO Ω(t) for t < t₁ near
t₁ — contradiction. Hence H_{t₀} has no zeros with 0 ≤ x ≤ X, y ≥ Y(t₀) = y₀; combined
with (ii) (which covers x ≥ X + √(1−y₀²)), with (iii) at t = t₀ (which covers
X ≤ x ≤ X + √(1−y₀²), y ≥ y₀), and with the symmetry H_t(−z̄) = conj H_t(z) (evenness +
reality), H_{t₀} has no zeros with y ≥ y₀ at all. ∎(Step 1)

**Step 2** ((i) ⟹ (i')). By Lemma 0.1, a zero of H₀ at x + iy with 0 ≤ x ≤ X and
√(y₀²+2t₀) ≤ y ≤ 1 corresponds to a zero of ξ (hence of ζ, as Re s ∈ (0,1)) at
σ + iT with σ = (1+y)/2 ∈ [(1+√(y₀²+2t₀))/2, 1] ⊆ [(1+y₀)/2, 1] and T = x/2 ∈ [0, X/2].
(⊆ holds since √(y₀²+2t₀) ≥ y₀ for t₀ ≥ 0.) Hypothesis (i) excludes these. ∎(Step 2)

**Step 3.** Step 1 + Ingredient A give Λ ≤ t₀ + y₀²/2. ∎

**Remark 1.2 (the simplified barrier slab).** The Polymath numerics (and our campaign)
verify (iii) on the LARGER region X ≤ x ≤ X+1, y₀ ≤ y ≤ 1, 0 ≤ t ≤ t₀, which contains
the (iii)-region because √(1−y₀²) ≤ 1, √(y₀²+2(t₀−t)) ≥ y₀ and √(1−2t) ≤ 1. (Validity
needs y₀² + 2t₀ ≤ 1 so that Y(t) ≤ 1; checked per row by the script.)

## 2. Instantiation at the published 0.2 row (the row our campaign upgrades)

**Theorem 2.1** (instantiated criterion; RH-height dependency explicit). Let

  X = 5 000 000 194 858 (= 5×10¹² + 194858, exactly),  t₀ = 0.186,  y₀ = 0.16733.

Assume:
 (i) RH verified to ζ-height T = X/2 = 2 500 000 097 429 (exactly): **supplied
     unconditionally** by Platt–Trudgian 2021 (arXiv:2004.09765, Thm 1), who verify RH to
     T_PT = 3 000 175 332 800 ≥ X/2, with margin T_PT − X/2 = 500 175 235 371 (exactly).
 (ii) H_t(x+iy) ≠ 0 on the barrier slab x ∈ [X, X+1], y ∈ [y₀, 1], t ∈ [0, t₀]
     (Polymath 15 winding-number computation, Table 1 row 2, winding number 0; artifact
     `output/windingnumbers/windnum_nolemma_x5000000194858_y_0.16733_1_t_0_0.186.txt`,
     435 rectangles, all winding numbers 0).
 (iii) the zero-free right region at y₀: no zeros H_{t₀}(x+iy) = 0, x ≥ X + √(1−y₀²),
     y₀ ≤ y ≤ √(1−2t₀) (Polymath 15 Lemma-bound sweep, Table 1 row 2).

Then  **Λ ≤ t₀ + y₀²/2 = 0.19999966445 (exactly 0.186 + 0.0279993289/2) < 0.2.**

Arithmetic facts instantiating Theorem 1.1, all checked in exact rational arithmetic by
`verify_criterion.py`:

| check | value (exact) | requirement | status |
|---|---|---|---|
| Λ functional | t₀ + y₀²/2 = 0.19999966445 | ≤ 0.2 (claimed) | ✓ |
| RH height consumed | X/2 = 2500000097429 | ≤ T_PT = 3000175332800 | ✓ margin 500175235371 |
| Prop-3.3 canopy validity | y₀² + 2t₀ = 0.3999993289 | ≤ 1 | ✓ |
| (ii)-range nonempty | y₀² = 0.0279993289 | ≤ 1 − 2t₀ = 0.628 | ✓ |
| Thm-1.3 region `region` | t₀ ≤ 1/2, 0 ≤ y ≤ 1, X ≥ 200 | — | ✓ |
| slab ⊇ (iii)-region | √(1−y₀²) ≤ 1 | — | ✓ |
| N constant on slab | N = ⌊√(x/4π + t/16)⌋ = 630783 for all x ∈ [X, X+1], t ∈ [0, t₀] | f_t holomorphic on slab rectangles | ✓ (interval arithmetic) |

The constant N = 630783 (Table 1's N₀) is verified to be constant over the entire slab in
interval arithmetic, which is what makes f_t holomorphic there and the winding-number
argument (Rouché, §8.4 of 1904.12438) applicable.

## 3. Campaign parameter-substitution corollaries (policy 2)

The upgrade rows below change ONLY (X, t₀, y₀); the proof of Theorem 1.1 is untouched.
Hypotheses (ii)/(iii) for them are the campaign deliverables of the producer /
the independent verifier (the committed repo artifact at X = 6×10¹²+185827 is **unvetted**; we
state the conditionals exactly).

**Corollary 3.1** (the 0.197262405 row). Let X' = 6 000 000 185 827 (= 6×10¹² + 185827,
exactly), t₀' = y₀' = 0.1809. Then X'/2 = 3 000 000 092 913.5 ≤ T_PT (margin
175 239 886.5, exactly), so hypothesis (i) is supplied unconditionally by PT2021; and IF
(ii), (iii) hold at (X', t₀', y₀') THEN Λ ≤ 0.1809 + 0.1809²/2 = **0.197262405**
(exactly). Validity: y₀'² + 2t₀' = 0.39452481 ≤ 1; y₀'² = 0.03272481 ≤ 1 − 2t₀' = 0.6382.

**Corollary 3.2** (the tuned 0.197 row). Let X' as above (or any X' ≤ 2·T_PT =
6 000 350 665 600 with the same barrier), t₀'' = 0.1775, y₀'' = √0.039. Then IF (ii),
(iii) hold at (X', t₀'', y₀'') THEN Λ ≤ 0.1775 + 0.039/2 = **0.197 exactly**. Validity:
y₀''² + 2t₀'' = 0.394 ≤ 1; y₀''² = 0.039 ≤ 1 − 2t₀'' = 0.645. Moreover the barrier region
of Cor. 3.2, [√0.039, 1] × [0, 0.1775] (note √0.039 = 0.19748… > 0.1809), is strictly
contained in that of Cor. 3.1, [0.1809, 1] × [0, 0.1809], in both coordinates — so one
slab certification at (X', 0.1809, 0.1809) covers both corollaries. (Containment needs
y₀'' ≥ y₀' and t₀'' ≤ t₀': 0.039 ≥ 0.1809² = 0.03272481 ✓ and 0.1775 ≤ 0.1809 ✓ — but
note hypothesis (iii)'s lower y-edge √(y₀²+2(t₀−t)): at t = 0 Cor. 3.2 needs y down to
√(0.039 + 0.355) = √0.394 ≤ 1 and the slab form needs only y ≥ y₀''; both inside the
certified slab y ≥ 0.1809 since y₀'' = 0.19748… ≥ 0.1809 ✓. Hypothesis (ii) of Cor 3.2
at t₀'' = 0.1775 is NOT implied by (ii) at t₀' = 0.1809 — it is a separate sweep at
t = 0.1775; the script flags this as a campaign obligation, not a free containment.)

**Floor remark (RH-height dependency of the next rung).** Within this framework the
published Λ ≤ 0.19 row (X = 2×10¹³ + 131252) consumes T ≥ X/2 = 10 000 000 065 626
(exactly) = 3.33313… × T_PT; no choice of (t₀, y₀) at admissible X ≤ 2·T_PT changes
hypothesis (i)'s ceiling. See the companion package `packages/improvement_memo/`.

## 4. What this package does and does not certify

- It certifies (script, exit 0): every arithmetic inequality in §2–§3 in exact rational
  arithmetic; N-constancy on the slab in interval arithmetic; Lemma 0.1 symbolically and
  numerically. It makes the chain of implications explicit and self-contained modulo de
  Bruijn's Theorem 13 and Prop 3.1 of 1904.12438 (both cited, the latter's role isolated
  to Step 1).
- It does NOT certify hypotheses (ii)/(iii) themselves — those are computational
  deliverables (Polymath artifacts for §2; the producer/the independent verifier for §3).
- Λ ≤ 0.19999966445 as stated in §2 is unconditional ONLY because PT2021's
  T_PT = 3000175332800 supplies (i); every statement here names the height it consumes.
