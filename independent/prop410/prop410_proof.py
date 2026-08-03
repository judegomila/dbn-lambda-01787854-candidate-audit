#!/usr/bin/env python3
"""prop410_proof.py

The computation constituting the computer-assisted proof of
Proposition 4.10 of the review manuscript
(dan-reworking/latex/exposition/gomila-proof-exposition.tex): the uniform bound
on the effective-approximation error terms of Theorem 1.3 over the
finite region, at t = t_0, bounded using equation (23) of [Polymath]
for e_A + e_B and the conservative corollary (eq:ec0) for e_C0:

    e_A + e_B <= 2.06e-12,
    e_C0      <= 0.000000233492848188649183,
    e_A + e_B + e_C0 <= E_max := 0.000000233494905212337849.

The bound is computed in effective_error_budget() by interval
arithmetic (mpmath.iv at 220 bits).  The majorants are decreasing in
x, so the enclosure at the left endpoint x_* (window index
N_0 = 690988), over a closed rational t-box containing t_0 and over
the full height range [y_0, sqrt(1 - 2 t_0)], controls the whole
finite region.

The program reads no input files.  It calculates the enclosures,
checks them against the three displayed bounds by exact rational
comparison of outward-rounded endpoints, prints the result, and
writes a human-readable report of all intermediate quantities to
runs/prop410_report.txt for inspection.

The report directory may be redirected by setting PROP410_OUTPUT_DIR.
The sealed review container mounts the repository read-only, so the
default location is unwritable there; verify_independent_crosscheck.py
points this at the container scratch area.  The certified arithmetic
and the exit status do not depend on the report at all.

PROVENANCE AND MODIFICATIONS
----------------------------
Derived from verifiers/verify_finite_and_binding.py in the candidate
repository (dbn-lambda-01787854-candidate-audit).  That program did
three things: (1) parse the stored logs of the window sweep and
re-derive their minimum; (2) compute the effective error budget;
(3) certify a numerical rate bound for the correction-term
monotonicity.  Only (2) is the proof of Proposition 4.10, and only
(2) is retained:
  - the stored-log parsing (the manifest FILES/EXPECTED_LEGS, the
    function parse_file, and the coverage/minimum/binding checks in
    main) is removed: the window sweep is Proposition 4.3 of the
    manuscript, proved by the standalone program
    ../prop43/prop43_proof.c, which recomputes it from scratch;
  - corr_rate_gate() is removed: the statement it certified
    numerically (correction-term decay rate < 0; the manuscript
    derives rate < -1.36) is proved analytically in Lemma 4.5(c)
    ("Monotone normalizer and correction") of the manuscript;
  - main() is rewritten as described above, and the helper
    floor_decimal (used only for the removed sweep minimum) is
    dropped.
The retained constants, the helpers itv_fraction, hull,
endpoint_fraction, upper_fraction, upper_point, ceil_decimal, and
the entire function effective_error_budget() are line-for-line
identical to the original; diff against
verifiers/verify_finite_and_binding.py to audit.
"""

from fractions import Fraction as F
import os
from pathlib import Path
import sys

from mpmath import iv, mp


iv.prec = 220
mp.prec = 220

HERE = Path(__file__).resolve().parent

T0 = F(16125, 100000)
TBOX_LO = F(161250000, 10**9)
TBOX_HI = F(161250001, 10**9)
Y2 = F(350708, 10**7)
YMAX2 = 1 - 2 * T0
N0 = 690_988

# The three bounds displayed in Proposition 4.10, as exact rationals.
STATED_EAB = F(206, 10**14)
STATED_EC0 = F(233492848188649183, 10**24)
STATED_EMAX = F(233494905212337849, 10**24)


def itv_fraction(value):
    return iv.mpf(value.numerator) / value.denominator


def hull(left, right):
    return left + (right - left) * iv.mpf([0, 1])


def endpoint_fraction(value):
    sign, mantissa, exponent, _ = mp.mpf(value)._mpf_
    if mantissa == 0 and exponent == 0:
        return F(0)
    result = F(int(mantissa)) * F(2) ** int(exponent)
    return -result if sign else result


def upper_fraction(value):
    return endpoint_fraction(value.b)


def upper_point(value):
    return iv.mpf([value.b, value.b])


def ceil_decimal(value, digits):
    scaled = value * 10**digits
    integer = -((-scaled.numerator) // scaled.denominator)
    sign = "-" if integer < 0 else ""
    text = str(abs(integer)).rjust(digits + 1, "0")
    return sign + text[:-digits] + "." + text[-digits:]


def effective_error_budget():
    """Full upstream U1--U5 path, on a t-box containing the exact row."""
    t = hull(itv_fraction(TBOX_LO), itv_fraction(TBOX_HI))
    y0 = iv.sqrt(itv_fraction(Y2))
    ymax = iv.sqrt(itv_fraction(YMAX2))
    pi = iv.pi
    n0 = iv.mpf(N0)
    x0 = 4 * pi * (n0**2 - t / 16)
    log0 = iv.log(n0**2 - t / 16)
    logn0 = iv.log(N0)
    delta1 = upper_point(
        (t / 4) * (-iv.log(1 - t / (16 * n0**2)))
        + t / (2 * x0**2)
    )
    sigma1 = (1 + y0) / 2 + (t / 2) * logn0 - delta1
    y1 = iv.mpf("0.02") - log0 / 2 + logn0 / 2
    kappa = upper_point(t / (2 * (x0 - 6)))

    gates = {
        "G0_positive_part": (8 / x0**2).b < (3 * y0).a,
        "sigma1_positive": sigma1.a > 0,
        "Y1_negative": y1.b < 0,
        "kappa_domain": kappa.a > 0 and kappa.b < 1,
        "G2a_ratio": (n0**2 / (n0**2 - t / 16)).a > 1,
        "U1_log_domain": log0.a > 2,
        "U2_logN": logn0.a > iv.mpf("0.5").b,
        "U3a_tail_decrease": ((1 + y0) / 2 - delta1).a > 0,
        "Y_range": 0 < Y2 < YMAX2 <= 1,
    }

    u1max = upper_point(
        ((t * t / 16) * log0**2 + iv.mpf("0.626"))
        / (x0 - iv.mpf("6.66"))
    )
    pmax = upper_point(
        1
        + iv.exp(iv.mpf("0.02"))
        * (1 - t / (16 * n0**2)) ** (iv.mpf(-1) / 2)
        * iv.exp(t * logn0 / (2 * (x0 - 6)))
    )

    m0 = 2000
    logm0 = iv.log(m0)
    g_t1 = -(t / 2) * logm0 + 1 / (logn0 - logm0)
    g_t2 = (
        (1 - y0) / 2
        + delta1
        - (t / 2) * logn0
        + 1 / (logn0 - logm0)
    )
    gates["U3b_first_endpoint"] = g_t1.b < 0
    gates["U3c_second_endpoint"] = g_t2.b < 0
    gates["U5_last_factor"] = F(3, 1) / F(1050, 100) < 1

    head = iv.mpf(0)
    for n in range(2, m0 + 1):
        logn = iv.log(n)
        head += iv.exp((t / 4) * logn**2 - sigma1 * logn)
    head = upper_point(head)

    def exponential_tail(logu):
        return iv.exp(
            (1 - sigma1) * logu + (t / 4) * logu**2
        )

    term1 = upper_point(exponential_tail(logm0) * (logn0 - logm0))
    term2 = upper_point(exponential_tail(logn0) * (logn0 - logm0))
    cap_u = iv.mpf([max(term1.b, term2.b)] * 2)
    smax = upper_point(1 + head + cap_u)
    error_ab = upper_point(pmax * smax * (iv.exp(u1max) - 1))
    error_c0 = upper_point(
        iv.exp(
            -(1 + y0) / 4 * log0
            - (t / 16) * log0**2
            + iv.mpf("1.24") * (3**ymax + 3**(-ymax))
            / (n0 - iv.mpf("0.125"))
            + (
                3 * iv.sqrt(log0**2 + (pi / 2) ** 2)
                + iv.mpf("10.50")
            )
            / (x0 - 12)
        )
    )
    if len(gates) != 12:
        raise AssertionError(f"internal error-gate count {len(gates)}")
    return (
        upper_fraction(error_ab + error_c0),
        upper_fraction(error_ab),
        upper_fraction(error_c0),
        upper_fraction(y1),
        upper_fraction(g_t1),
        upper_fraction(g_t2),
        gates,
    )


def main():
    if not (TBOX_LO == T0 < TBOX_HI <= F(1, 4)):
        raise AssertionError("t-box does not contain t_0")
    if not (0 < Y2 < YMAX2 <= 1):
        raise AssertionError("invalid y range")

    (
        error_max,
        error_ab,
        error_c0,
        y1_upper,
        g_t1_upper,
        g_t2_upper,
        gates,
    ) = effective_error_budget()

    failed = [name for name, passed in gates.items() if not passed]
    if failed:
        raise AssertionError(f"error-budget gates failed: {failed}")

    checks = (
        ("e_A+e_B <= 2.06e-12", error_ab <= STATED_EAB),
        ("e_C0 <= 0.000000233492848188649183", error_c0 <= STATED_EC0),
        ("e_A+e_B+e_C0 <= E_max", error_max <= STATED_EMAX),
    )
    failed_checks = [name for name, passed in checks if not passed]
    if failed_checks:
        raise AssertionError(
            f"Proposition 4.10 bounds not established: {failed_checks}"
        )

    lines = [
        "Proposition 4.10: uniform error bound, finite region",
        "",
        "Parameters (exact rationals):",
        f"  t_0    = {T0}",
        f"  t-box  = [{TBOX_LO}, {TBOX_HI}]",
        f"  y_0^2  = {Y2}",
        f"  ymax^2 = 1 - 2 t_0 = {YMAX2}",
        f"  N_0    = {N0}",
        f"  interval precision: {iv.prec} bits",
        "",
        "Domain and sign conditions (all must hold):",
    ]
    lines += [f"  [PASS] {name}" for name in gates]
    lines += [
        "",
        "Certified upper endpoints (outward-rounded, then rounded up",
        "once more in the last printed digit):",
        f"  e_A+e_B        <= {ceil_decimal(error_ab, 24)}",
        f"  e_C0           <= {ceil_decimal(error_c0, 24)}",
        f"  e_A+e_B+e_C0   <= {ceil_decimal(error_max, 24)}",
        "",
        "Auxiliary enclosures (upper endpoints):",
        f"  Y1   <= {ceil_decimal(y1_upper, 18)}",
        f"  g_t1 <= {ceil_decimal(g_t1_upper, 18)}",
        f"  g_t2 <= {ceil_decimal(g_t2_upper, 18)}",
        "",
        "Bounds of Proposition 4.10 (exact rational comparison):",
    ]
    lines += [f"  [PASS] {name}" for name, _ in checks]
    lines += [
        "",
        "RESULT PASS: e_A+e_B+e_C0 <= E_max "
        "= 0.000000233494905212337849 on the finite region",
    ]

    report = "\n".join(lines) + "\n"
    runs = Path(os.environ.get("PROP410_OUTPUT_DIR", HERE / "runs"))
    runs.mkdir(parents=True, exist_ok=True)
    (runs / "prop410_report.txt").write_text(report, encoding="utf-8")
    print(report, end="")
    print(f"(report written to {runs / 'prop410_report.txt'})")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT FAIL: {exc}", file=sys.stderr)
        raise
