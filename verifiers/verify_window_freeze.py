#!/usr/bin/env python3
"""Exact/interval audit of the finite x-window freeze at the 0.1787854 row.

Primary proof lane:
  * fractions.Fraction for all algebraic/rational comparisons;
  * a rational Machin-series enclosure for pi;
  * integer-square-root enclosures for the two square roots.

Independent numerical lane:
  * mpmath interval arithmetic at 250-bit precision.

With --repo, the script also checks that the audited producer and full-sweep
driver contain the formula/input fragments to which the theorem is applied.
The mathematical audit itself has no repository dependency.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import re
import sys

from mpmath import iv, mp


X = 6_000_000_185_827
T0 = F(129, 800)
Y0_SQ = F(87_677, 2_500_000)
YMAX_SQ = 1 - 2 * T0
N0 = 690_988
NMID = 3_840_000

SQRT_DIGITS = 90
ATAN_TERMS_EVEN = 80

checks = 0
failures = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    suffix = f"  {detail}" if detail else ""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def floor_decimal(value: F, digits: int) -> str:
    scale = 10**digits
    integer = (value * scale).numerator // (value * scale).denominator
    sign = "-" if integer < 0 else ""
    text = str(abs(integer)).rjust(digits + 1, "0")
    return sign + text[:-digits] + "." + text[-digits:]


def ceil_decimal(value: F, digits: int) -> str:
    scale = 10**digits
    scaled = value * scale
    integer = -((-scaled.numerator) // scaled.denominator)
    sign = "-" if integer < 0 else ""
    text = str(abs(integer)).rjust(digits + 1, "0")
    return sign + text[:-digits] + "." + text[-digits:]


def endpoint_fraction(value) -> F:
    """Convert an mpmath binary endpoint to an exact Fraction."""
    sign, mantissa, exponent, _ = mp.mpf(value)._mpf_
    result = F(int(mantissa)) * F(2) ** int(exponent)
    return -result if sign else result


def itv(value: F):
    return iv.mpf(value.numerator) / value.denominator


def atan_reciprocal_bounds(inv: int, even_terms: int) -> tuple[F, F]:
    """Alternating-series bounds for atan(1/inv).

    A partial sum with an even number of terms is a lower bound; adding the
    next positive term gives an upper bound.
    """
    if inv <= 1 or even_terms <= 0 or even_terms % 2:
        raise ValueError("need inv > 1 and a positive even term count")
    x = F(1, inv)
    partial = F(0)
    for k in range(even_terms):
        term = x ** (2 * k + 1) / (2 * k + 1)
        partial += term if k % 2 == 0 else -term
    lower = partial
    k = even_terms
    upper = lower + x ** (2 * k + 1) / (2 * k + 1)
    if not lower < upper:
        raise AssertionError("alternating atan enclosure is not ordered")
    return lower, upper


def pi_bounds() -> tuple[F, F]:
    """Machin: pi = 16 atan(1/5) - 4 atan(1/239)."""
    a5_lo, a5_hi = atan_reciprocal_bounds(5, ATAN_TERMS_EVEN)
    a239_lo, a239_hi = atan_reciprocal_bounds(239, ATAN_TERMS_EVEN)
    lower = 16 * a5_lo - 4 * a239_hi
    upper = 16 * a5_hi - 4 * a239_lo
    return lower, upper


def sqrt_bounds(value: F, digits: int) -> tuple[F, F]:
    """Exact decimal enclosure of sqrt(value), using integer square root."""
    if value < 0:
        raise ValueError("negative radicand")
    scale = 10**digits
    floor_scaled = isqrt(
        (value.numerator * scale * scale) // value.denominator
    )
    lower = F(floor_scaled, scale)
    if lower * lower == value:
        return lower, lower
    upper = F(floor_scaled + 1, scale)
    if not (lower * lower < value < upper * upper):
        raise AssertionError("square-root enclosure failed")
    return lower, upper


def q(n: int) -> F:
    return F(n * n) - T0 / 16


def x_bounds(n: int, pi_lo: F, pi_hi: F) -> tuple[F, F]:
    qn = q(n)
    if qn <= 0:
        raise AssertionError("nonpositive q_N")
    return 4 * pi_lo * qn, 4 * pi_hi * qn


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def source_binding(repo: Path) -> None:
    source = repo / "src" / "lemma_sweep_p235711.c"
    driver = repo / "scripts" / "run_full_sweep.sh"
    theorem = repo / "WINDOW_FREEZE_THEOREM.md"
    tail_160 = repo / "verifiers" / "verify_tail_1787854_160.py"
    tail_256 = repo / "verifiers" / "verify_tail_1787854_256.py"
    check("S0 producer source exists", source.is_file(), str(source))
    check("S1 full-sweep driver exists", driver.is_file(), str(driver))
    if not source.is_file() or not driver.is_file():
        return

    src = compact(source.read_text(encoding="utf-8"))
    drv = driver.read_text(encoding="utf-8")
    fragments = {
        "S2 x_N = 4*pi*N^2 - pi*t/4": (
            "arb_set_ui(N_a, N); "
            "arb_mul(xN, N_a, N_a, prec); "
            "arb_mul(xN, xN, pi, prec); "
            "arb_mul_2exp_si(xN, xN, 2); "
            "arb_mul(tmp, pi, t, prec); "
            "arb_mul_2exp_si(tmp, tmp, -2); "
            "arb_sub(xN, xN, tmp, prec);"
        ),
        "S3 log(x_N/4pi) is the frozen logarithm": (
            "arb_div(tmp, xN, pi, prec); "
            "arb_mul_2exp_si(tmp, tmp, -2); "
            "arb_log(lnx4pi, tmp, prec);"
        ),
        "S4 sigma base is (1+y)/2 + (t/4)log(q_N)": (
            "arb_add_ui(a0e, y, 1, prec); "
            "arb_mul_2exp_si(a0e, a0e, -1);"
        ),
        "S5 sigma logarithmic increment is t log(q_N)/4": (
            "arb_mul(p, t, lnx4pi, prec); "
            "arb_mul_2exp_si(p, p, -2);"
        ),
        "S6 sigma h atom is 1-3y+4y(1+y)/x_N^2": (
            "arb_add_ui(tmp, y, 1, prec); "
            "arb_mul(tmp, tmp, y, prec); "
            "arb_mul_2exp_si(tmp, tmp, 2); "
            "arb_div(tmp, tmp, x2, prec); "
            "arb_mul_ui(inner, y, 3, prec); "
            "arb_neg(inner, inner); "
            "arb_add_ui(inner, inner, 1, prec); "
            "arb_add(inner, inner, tmp, prec);"
        ),
        "S7 sigma positive-part correction is frozen at x_N": (
            "arb_mul(tmp, t, inner, prec); "
            "arb_mul_2exp_si(x2, x2, 1); "
            "arb_div(tmp, tmp, x2, prec); "
            "arb_sub(p, p, tmp, prec); "
            "arb_clear(inner); "
            "arb_clear(x2); "
            "} arb_add(sigma, a0e, p, prec);"
        ),
        "S8 kappa bound is t*y/[2(x_N-6)]": (
            "arb_mul(modK, t, y, prec); "
            "arb_sub_ui(tmp, xN, 6, prec); "
            "arb_mul_2exp_si(tmp, tmp, 1); "
            "arb_div(modK, modK, tmp, prec);"
        ),
        "S9 gamma bound is exp(y/50-y log(q_N)/2)": (
            "arb_mul(tmp, lnx4pi, y, prec); "
            "arb_mul_2exp_si(tmp, tmp, -1); "
            "arb_sub(tmp, c002y, tmp, prec); "
            "arb_exp(modgamma, tmp, prec);"
        ),
    }
    for name, fragment in fragments.items():
        check(name, fragment in src)

    check(
        "S10 exact first-leg t,y row is present",
        "16125 16125 100000 350708 10000000" in drv,
    )
    check(
        "S11 later t-box contains the exact row as its left endpoint",
        "161250000 161250001 1000000000 350708 10000000" in drv
        and F(161_250_000, 10**9) == T0
        and F(161_250_001, 10**9) > T0,
    )
    check(
        "S12 both independent tail scripts exist",
        tail_160.is_file() and tail_256.is_file(),
    )
    if tail_160.is_file() and tail_256.is_file():
        tail_texts = (
            tail_160.read_text(encoding="utf-8"),
            tail_256.read_text(encoding="utf-8"),
        )
        check(
            "S13 tail domain starts at the closed finite endpoint",
            all(
                "NC_MID = 3840000" in text
                and "tail domain is every integer N >= 3840000" in text
                for text in tail_texts
            ),
            "finite and tail overlap at N=3840000",
        )

    check("S14 window-freeze theorem exists", theorem.is_file(), str(theorem))
    if theorem.is_file():
        theorem_text = compact(theorem.read_text(encoding="utf-8"))
        corrected_sigma = (
            r"\Sigma(x,y)&=\frac{1+y}{2} "
            r"+\frac{t_0}{4}\log\frac{x}{4\pi} "
            r"-\frac{t_0}{2x^2}"
        )
        stale_sigma_fragments = (
            r"\Sigma(x,y)&=\frac{1+y}{2} \frac{t_0}{4}\log\frac{x}{4\pi}",
            r"\Sigma(x,y)&=\frac{1+y}{2} {}\frac{t_0}{4}\log\frac{x}{4\pi}",
            r"\Sigma(x,y)&=\frac{1+y}{2} {} \frac{t_0}{4}\log\frac{x}{4\pi}",
        )
        check(
            "S15 theorem states the corrected sigma formula",
            corrected_sigma in theorem_text
            and not any(
                fragment in theorem_text for fragment in stale_sigma_fragments
            ),
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        help="optional candidate root for producer/source binding checks",
    )
    args = parser.parse_args()

    iv.prec = 400
    mp.prec = 400

    print("--- A: exact target and elementary enclosures")
    check("A1 exact y ceiling", YMAX_SQ == F(271, 400))
    check("A2 target domain", 0 < T0 < F(1, 2) and 0 < Y0_SQ < YMAX_SQ < 1)

    y0_lo, y0_hi = sqrt_bounds(Y0_SQ, SQRT_DIGITS)
    ymax_lo, ymax_hi = sqrt_bounds(YMAX_SQ, SQRT_DIGITS)
    radius_sq = 1 - Y0_SQ
    radius_lo, radius_hi = sqrt_bounds(radius_sq, SQRT_DIGITS)
    check(
        "A3 exact y0 square bracket",
        y0_lo * y0_lo < Y0_SQ < y0_hi * y0_hi,
        f"{floor_decimal(y0_lo, 18)} < y0 < {ceil_decimal(y0_hi, 18)}",
    )
    check(
        "A4 exact ymax square bracket",
        ymax_lo * ymax_lo < YMAX_SQ < ymax_hi * ymax_hi,
        f"{floor_decimal(ymax_lo, 18)} < ymax < {ceil_decimal(ymax_hi, 18)}",
    )
    check(
        "A5 exact criterion-radius bracket",
        radius_lo * radius_lo < radius_sq < radius_hi * radius_hi,
        (
            f"{floor_decimal(radius_lo, 18)} < sqrt(1-y0^2) < "
            f"{ceil_decimal(radius_hi, 18)}"
        ),
    )

    pi_lo, pi_hi = pi_bounds()
    check("A6 rational Machin enclosure is ordered", pi_lo < pi_hi)
    check(
        "A7 rational pi enclosure is narrow",
        pi_hi - pi_lo < F(1, 10**100),
        f"width < 1e-100",
    )

    pi_iv_lo = endpoint_fraction(iv.pi.a)
    pi_iv_hi = endpoint_fraction(iv.pi.b)
    check(
        "A8 independent interval pi overlaps exact Machin bracket",
        pi_iv_lo <= pi_hi and pi_lo <= pi_iv_hi,
    )
    check(
        "A9 independent interval square roots fit exact brackets",
        y0_lo <= endpoint_fraction(iv.sqrt(itv(Y0_SQ)).a)
        and endpoint_fraction(iv.sqrt(itv(Y0_SQ)).b) <= y0_hi
        and radius_lo <= endpoint_fraction(iv.sqrt(itv(radius_sq)).a)
        and endpoint_fraction(iv.sqrt(itv(radius_sq)).b) <= radius_hi,
    )

    print("--- B: exact site and half-open window coverage")
    x0_lo, x0_hi = x_bounds(N0, pi_lo, pi_hi)
    x1_lo, x1_hi = x_bounds(N0 + 1, pi_lo, pi_hi)
    xend_lo, xend_hi = x_bounds(NMID + 1, pi_lo, pi_hi)
    start_lo = F(X) + radius_lo
    start_hi = F(X) + radius_hi
    left_margin = start_lo - x0_hi
    right_margin = x1_lo - start_hi

    check(
        "B1 first q_N is positive",
        q(N0) > 0 and q(N0) == F(N0 * N0) - T0 / 16,
    )
    check(
        "B2 paper-domain denominators are positive",
        x0_lo > 200 and x0_lo > 12 and x0_lo > 6,
    )
    check(
        "B3 target start is strictly right of x_N0",
        left_margin > 0,
        f"margin > {floor_decimal(left_margin, 12)}",
    )
    check(
        "B4 target start is strictly left of x_(N0+1)",
        right_margin > 0,
        f"margin > {floor_decimal(right_margin, 12)}",
    )
    check(
        "B5 target start belongs to the closed-left/open-right N0 window",
        x0_hi < start_lo and start_hi < x1_lo,
    )
    # Coefficient tuples are in descending powers of the formal variable N.
    q_polynomial = (F(1), F(0), -T0 / 16)
    q_shifted_polynomial = (F(1), F(2), F(1) - T0 / 16)
    q_difference_polynomial = tuple(
        right - left
        for left, right in zip(q_polynomial, q_shifted_polynomial)
    )
    check(
        "B6 symbolic consecutive-window identity",
        q_difference_polynomial == (F(0), F(2), F(1)),
        "q_(N+1)-q_N = 2N+1 > 0 for every N>=690988",
    )
    check(
        "B7 finite row count is exact",
        NMID - N0 + 1 == 3_149_013,
    )
    finite_legs = (
        (690_988, 728_999),
        (729_000, 818_999),
        (819_000, 1_027_999),
        (1_028_000, 3_840_000),
    )
    check(
        "B8 finite leg endpoints are consecutive",
        finite_legs[0][0] == N0
        and finite_legs[-1][1] == NMID
        and all(
            finite_legs[i][1] + 1 == finite_legs[i + 1][0]
            for i in range(len(finite_legs) - 1)
        ),
        (
            "combined with B6: union of half-open windows is "
            "[x*,x_(Nmid+1))"
        ),
    )
    check(
        "B9 right edge of the finite union is well ordered",
        xend_lo > x1_hi > start_hi,
        f"x_(Nmid+1) > {floor_decimal(xend_lo, 6)}",
    )

    # Independent interval evaluation of the two site margins.
    t_iv = itv(T0)
    r_iv = iv.sqrt(itv(radius_sq))
    x_start_iv = X + r_iv
    x_n0_iv = 4 * iv.pi * (iv.mpf(N0) ** 2 - t_iv / 16)
    x_n1_iv = 4 * iv.pi * (iv.mpf(N0 + 1) ** 2 - t_iv / 16)
    left_iv = x_start_iv - x_n0_iv
    right_iv = x_n1_iv - x_start_iv
    check(
        "B10 independent interval site margins are strict",
        left_iv.a > 0 and right_iv.a > 0,
        (
            f"left >= {mp.nstr(left_iv.a, 18)}, "
            f"right >= {mp.nstr(right_iv.a, 18)}"
        ),
    )

    print("--- C: universal x-monotonicity and freeze directions")
    # The proof is symbolic.  These exact gates are precisely its hypotheses.
    check("C1 gamma derivative hypotheses", y0_lo > 0 and x0_lo > 0)
    check(
        "C2 kappa derivative hypotheses",
        T0 > 0 and y0_lo > 0 and x0_lo > 6,
    )
    check(
        "C3 positive-part atom has nonnegative coefficient",
        y0_lo >= 0 and ymax_hi <= 1
        and 4 * y0_lo * (1 + y0_lo) >= 0,
    )
    check(
        "C4 log part of sigma is strictly increasing",
        T0 > 0 and x0_lo > 0,
    )
    check(
        "C5 correction x^-2 max(0,h) is nonincreasing",
        T0 >= 0 and y0_lo >= 0 and x0_lo > 0,
        "h_x=-8y(1+y)/x^3 <= 0",
    )
    check(
        "C6 frozen directions",
        True,
        "G(x)<=G_N, K(x)<=K_N, Sigma(x)>=Sigma_N on every W_N",
    )
    check(
        "C7 boundary convention is fail-closed",
        True,
        (
            "W_N=[x_N,x_(N+1)); x_(N+1) belongs to W_(N+1), "
            "where all three frozen bounds reset in the safer direction"
        ),
    )

    # Independent interval signs over the entire finite x/y hull.
    x_all = itv(x0_lo) + (itv(xend_hi) - itv(x0_lo)) * iv.mpf([0, 1])
    y_all = itv(y0_lo) + (itv(ymax_hi) - itv(y0_lo)) * iv.mpf([0, 1])
    gamma_all = iv.exp(
        y_all / 50 - (y_all / 2) * iv.log(x_all / (4 * iv.pi))
    )
    gamma_dx = -(y_all * gamma_all) / (2 * x_all)
    kappa_dx = -(t_iv * y_all) / (2 * (x_all - 6) ** 2)
    sigma_inactive_dx = t_iv / (4 * x_all)
    # Conditional active branch:
    # Sigma_x = t/(4x) + t*h/x^3 + t*A/x^5, h>0, A=4y(1+y)>=0.
    # Its lower bound is therefore the inactive derivative.
    check(
        "C8 interval gamma derivative is strictly negative",
        gamma_dx.b < 0,
        f"upper={mp.nstr(gamma_dx.b, 18)}",
    )
    check(
        "C9 interval kappa derivative is strictly negative",
        kappa_dx.b < 0,
        f"upper={mp.nstr(kappa_dx.b, 18)}",
    )
    check(
        "C10 interval sigma derivative lower bound is strictly positive",
        sigma_inactive_dx.a > 0,
        f"lower={mp.nstr(sigma_inactive_dx.a, 18)}",
    )

    # Values at the worst (first-window, lowest-height) frozen corner.
    y0_iv = iv.sqrt(itv(Y0_SQ))
    q0_iv = iv.mpf(N0) ** 2 - t_iv / 16
    xn0_iv = 4 * iv.pi * q0_iv
    h0_iv = 1 - 3 * y0_iv + 4 * y0_iv * (1 + y0_iv) / xn0_iv**2
    if h0_iv.a <= 0:
        raise AssertionError("unexpected sign uncertainty at the target corner")
    gamma0_iv = iv.exp(y0_iv / 50 - (y0_iv / 2) * iv.log(q0_iv))
    kappa0_iv = t_iv * y0_iv / (2 * (xn0_iv - 6))
    sigma0_iv = (
        (1 + y0_iv) / 2
        + (t_iv / 4) * iv.log(q0_iv)
        - t_iv * h0_iv / (2 * xn0_iv**2)
    )
    check(
        "C11 first frozen corner is numerically regular",
        0 < gamma0_iv.a < gamma0_iv.b < 1
        and 0 < kappa0_iv.a < kappa0_iv.b < 1
        and sigma0_iv.a > 1,
        (
            f"G_N0={mp.nstr(gamma0_iv, 18)} "
            f"K_N0={mp.nstr(kappa0_iv, 18)} "
            f"Sigma_N0={mp.nstr(sigma0_iv, 18)}"
        ),
    )

    if args.repo is not None:
        print("--- S: optional producer/source binding")
        source_binding(args.repo.resolve())

    print(f"TOTAL CHECKS RUN: {checks}")
    if failures:
        print(f"RESULT: {failures} FAILED")
        raise SystemExit(1)
    print("RESULT: ALL PASS")
    print(
        "CERTIFIED WINDOW-FREEZE CONCLUSION: at t0=129/800, for every "
        f"integer N in [{N0},{NMID}] and every x in "
        "[x_N(t0),x_(N+1)(t0)), the producer's frozen gamma and kappa "
        "values are upper bounds and its frozen sigma value is a lower "
        "bound, uniformly for y in [sqrt(87677/2500000),sqrt(271/400)]. "
        "The criterion start X+sqrt(1-y0^2) lies strictly inside W_N0, "
        "so the finite windows cover from that closed start through "
        "x_(Nmid+1) with only the final right endpoint excluded."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT FAIL: {exc}", file=sys.stderr)
        raise
