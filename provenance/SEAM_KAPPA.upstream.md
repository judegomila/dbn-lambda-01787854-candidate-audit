# SEAM_KAPPA — the κ-leak accounting lemma (stage 2 of the convention-conversion chain)

Package: `packages/seam_kappa/` (this writeup + `verify_seam_kappa.py` +
`ltest_bundled.gp`, standalone, /usr/bin/python3, mpmath interval arithmetic
prec 120 + sympy exact + exact rationals, reads ONLY the bundled gp source
inside its own directory, 31/31 checks, exit 0 in ≈ 2 s; logs `verify_log.txt`
and `verify_clean_copy_log.txt`, the latter from a standalone /tmp copy).
Author: the producer line, 2026-06-12.

**Provenance and staging.** Stage 2 of the pari-T-type → hypothesis-(S)
convention-conversion lemma chain: stage 1 (`packages/seam_exponent/`, this
run) pinned the exponent leg (one-sided seam, mass-inflation cost
D* ≤ 1.8·10⁻¹⁴) and the symbolic normalization identity; the chain was named
by the verified the auxiliary line fact (note `convseam_v1`); the staging is the
the 2026-06-12 intake order. This stage verifies the remaining
TRANSCRIPTION-CLASS leg note lists: the **κ-leak accounting** — the pari
T-type bound subtracts a per-N leak term, and the conversion needs to know
that recovering the numerator from a pari certificate loses nothing to it.

**The pari functional, pinned.** `ltest_bundled.gp`
(md5 `6205e2aabbb6564a9780c00d18dac6a7`, byte-identical to the source inside
the adoption-gate line's verified load-bearing bundle
`claims/ltbox_native_grid/lsweep_package/ltest.gp` — the toolchain of the
pinned full-grid certificates at this row) defines, for integer N ≥ 1,
y > 0, t > 0 (gp lines pinned verbatim by checks T2a–T2g):

- x_N = 4πN² − πt/4;
- sig = (1+y)/2 + (t/4)log(x_N/4π) − (t/(2x_N²))·max(0, 1−3y+4y(1+y)/x_N²);
- modK = t·y/(2(x_N − 6));
- modgamma = e^{0.02y}(x_N/4π)^{−y/2};
- modmoll = Σ_d |moll_d| d^{−sig} (the d = 1 term is the bare 1);
- Num := 1 − modgamma − Σ_{n=2}^{DN} max(|b−a|, common·|b+a|)/n^{sig};
- lbound = (1/modmoll)·Num − κ_leak, with
  **κ_leak = modgamma · Σ_{n=1}^{N} bt(n,t)·(n^{modK} − 1)/n^{sig−y}**,
  bt(n,t) = n^{(t/4)ln n} = e^{(t/4)ln²n}.

`abbeff_largex_ep_bound(N, y, t, ·, mtype)` returns lbound; the pinned grid
facts certify lbound > 3/100 per N.

**RH-height dependency: NONE.** Elementary positivity of finite sums plus
exp/log interval arithmetic; no zero of ζ consumed.

**Digit law.** Every decimal machine-derived in-script from exact binary
interval endpoints, lower bounds FLOOR-truncated, upper bounds
CEILING-truncated, labeled; self-test E0.

---

## 1. (K1) The domain gate

**Lemma K1.** For all integer N ≥ 1 and all t ∈ (0, 1/4]:
x_N − 6 ≥ 4π − π/16 − 6 > 6.37 > 0. Hence modK = t·y/(2(x_N−6)) > 0 for all
y > 0 on the whole domain.

*Proof.* x_N is strictly increasing in N (∂x_N/∂N = 8πN > 0, symbolic SY1a)
and strictly decreasing in t (∂x_N/∂t = −π/4, SY1b), so the infimum over
the domain is at (N, t) = (1, 1/4): x_N − 6 ≥ 4π − π/16 − 6, certified
> 6.37 (gate K1a, lower FLOOR10 = 6.3700210735). modK is then a product of
the positives t, y and 1/(2(x_N−6)) (gate K1b: positive lower endpoint at
the worst corner). ∎

(The campaign rows have t ≤ 0.181 ≤ 1/4 and N ≥ N₀ = 690988, deep inside
this domain; K1 is stated on the WHOLE gp-functional domain so every future
row inherits it.)

## 2. (K2) Leak positivity

**Lemma K2.** κ_leak(N, y, t) ≥ 0 for all integer N ≥ 1, all t ∈ (0, 1/4],
all y > 0, and every real sig. Moreover the n = 1 summand is exactly 0.

*Proof.* Each summand is modgamma · bt(n,t) · (n^{modK} − 1) · n^{−(sig−y)}.
The factors modgamma = e^{0.02y}(x_N/4π)^{−y/2}, bt(n,t) = e^{(t/4)ln²n} and
n^{−(sig−y)} = e^{−(sig−y)ln n} are exponentials, hence strictly positive
for every real argument (no condition on sig needed). The remaining factor
n^{modK} − 1 = e^{modK·ln n} − 1 ≥ 0 because modK > 0 (K1) and ln n ≥ 0 for
n ≥ 1, and e^u ≥ 1 for u ≥ 0 (atom SY3: e is increasing with e⁰ = 1). At
n = 1: bt(1) = 1 and 1^{modK} − 1 = 0 exactly (symbolic SY2), so the first
summand vanishes identically. Sum of nonnegatives is nonnegative. ∎

Interval instances at the stretch row (sanity, not the proof): modK(N₀) > 0
with CEIL20 = 2.91290·10⁻¹⁵ (gate K2b), the n = 2 summand positive (K2c),
modgamma(N₀) ∈ (0, 1) with CEIL10 = 0.0705524828 (K2d — so the gp `common`
is in (0,1) as the L-type branch assumes).

## 3. (K3) The numerator-recovery lemma

**Lemma K3.** modmoll ≥ 1 always (the d = 1 divisor contributes the bare 1,
every other term |moll_d| d^{−sig} ≥ 0; for the Euler-P mollifier the sum
equals ∏_{p∈P}(1 + b_p p^{−sig}) ≥ 1, symbolic SY4). Hence for ANY θ and any
point (N, y, t) of the domain:

  lbound_pari(N, y, t) ≥ θ ⟹ Num ≥ modmoll·(θ + κ_leak) ≥ modmoll·θ ≥ θ.

*Proof.* lbound = Num/modmoll − κ_leak ≥ θ rearranges (modmoll > 0) to
Num ≥ modmoll·(θ + κ_leak); drop κ_leak ≥ 0 (K2) and modmoll ≥ 1. ∎

**The conversion's κ-leg is therefore FREE: the subtracted leak only makes
the pari certificate stronger than its face value.** Combined with stage 1:
a pari grid certificate lbound ≥ θ at (N, t₀, y₀) yields the NUMERATOR bound
Num ≥ modmoll(N)·θ, and stage 1's L6 box enclosure turns this into the
box-uniform floor

  Num(N) ≥ modmoll_boxmin · θ ≥ 1.4157409295 · 3/100 ≥ **0.0424722278**
  (FLOOR10, gate K3e) for every N ∈ [N₀, 5·10⁶] at θ = 3/100,

and at the pinned grid minimum (the adoption-gate line `lemma_native_grid`:
min 0.184889586327 over the full grid at this row, hypothesis re-gated
> 3/100 as K3f) the floor is ≥ **0.2617557548** (FLOOR10, K3g). The
modmoll endpoints are RE-DERIVED in this package's script (K3b/K3c/K3d) —
no file of stage 1 is read; the two packages agree on the shared strings
(1.4871894818 CEIL10 / 1.4157409295 FLOOR10), which is itself a cross-check.

## 4. What remains after this stage (scope honesty)

Stages 1 + 2 together convert: pari grid certificate (lbound ≥ θ per N)
⟹ numerator bound Num ≥ modmoll·θ per N ⟹ [stage 1 L4] hypothesis-(S)-form
selection floor at threshold θ − D* at the SWEEP HEIGHT y₀. The single
remaining leg of the full conversion lemma is the **y-transfer
identification**: the pari numerator Num and the hypothesis-(S) majorant
1 − Σ m_n differ in their second-sum kernel (the gp max(|b−a|, common|b+a|)
form vs the trib2 rearrangement), and the identification of the swept
functional with the standard-window-majorant class at all y ∈ [y₀, y_max] —
record_binding R1's argument instantiated for the gp kernel — is stage 3.
Until stage 3 verifies, the full conversion lemma is NOT stated and
the auxiliary line's kill test (a) does not fire. No Λ value is claimed or
modified here.

## 5. Rung-(a) anchors (built in, two pinned regimes)

- **A1**: sig(N₀) at the stretch row FLOOR10-reproduces the pinned σ₁lo
  string 1.7887022679 (stretch_binding P2 / the auxiliary line G2d).
- **K3b**: modmoll(N₀) CEIL10 == pinned C_{2,3} string 1.4871894818
  (stretch_binding P2 / the independent verifier cross-line).
- **A2** (second regime, record row t = 71/400, Euler-2): modmoll CEIL10 ==
  pinned record_binding C_λ string 1.2949811496; **A3**: modK > 0 and
  modgamma < 1 there too.

NO discrepancy found in any anchor.

## 6. Novelty boundary

Not in any pinned fact: (a) the κ-leak positivity lemma K2 with its full
domain quantifier (note noted "κ_leak ≥ 0 (helpful direction)" as an
UNPROVED expectation and listed its accounting as a remaining ingredient;
convseam_v1's G4 simply omitted the leak); (b) the domain gate K1 (nowhere
stated; the gp source itself never checks x_N > 6); (c) the recovery
implication K3 with its box-uniform numerator floors — the object the
verified the adoption-gate line/-s4 grids and the binding packages need to
TOUCH each other; (d) the verbatim transcription pin T2a–T2g of the gp
functional against an md5-locked copy of the verified toolchain source
(the error_constants_audit discipline applied to the pari side; the audit
package covered the paper's (20)–(24), not the gp largex functional).
Stage 1 (`seam_exponent`) contains none of this — its script never reads
the gp source and proves nothing about κ_leak or Num.
