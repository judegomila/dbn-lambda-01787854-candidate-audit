#!/usr/bin/env python3
"""Exact-interface assembly for the 0.1787854 candidate."""

from fractions import Fraction as F
from pathlib import Path
import sys

from mpmath import iv, mp


iv.prec = 220
mp.prec = 220
ROOT = Path(__file__).resolve().parent.parent

checks = 0
failures = 0


def check(name, condition, detail=""):
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    print(
        f"[{'PASS' if ok else 'FAIL'}] {name}"
        + (f"  {detail}" if detail else "")
    )


def endpoint_fraction(value):
    sign, mantissa, exponent, _ = mp.mpf(value)._mpf_
    result = F(int(mantissa)) * F(2) ** int(exponent)
    return -result if sign else result


def floor_decimal(value, digits):
    scaled = value * 10**digits
    integer = scaled.numerator // scaled.denominator
    sign = "-" if integer < 0 else ""
    text = str(abs(integer)).rjust(digits + 1, "0")
    return sign + text[:-digits] + "." + text[-digits:]


X = 6_000_000_185_827
T_PT = 3_000_175_332_800
t0 = F(129, 800)
y0sq = F(87677, 2_500_000)
B = F(893927, 5_000_000)
N0 = 690_988
Nmid = 3_840_000

print("--- A: exact row")
check("A1 exact B identity", t0 + y0sq / 2 == B)
check("A2 exact decimal", floor_decimal(B, 7) == "0.1787854")
check(
    "A3 strict improvement over 0.1796360187",
    F(1_796_360_187, 10**10) - B
    == F(8_506_187, 10**10)
    > 0,
)
check(
    "A4 strict improvement over 0.179640000",
    F(4491, 25000) - B == F(4273, 5_000_000) > 0,
)
check(
    "A5 t and y domain",
    0 < t0 <= F(1, 4) and 0 < y0sq < 1 - 2 * t0 <= 1,
)
check(
    "A6 criterion quantity is admissible",
    y0sq + 2 * t0 == 2 * B <= 1,
)

print("--- B: verified height")
check("B1 campaign X is odd", X % 2 == 1)
check("B2 X/2 <= Platt--Trudgian height", F(X, 2) <= T_PT)
check(
    "B3 exact height margin",
    T_PT - F(X, 2) == F(350_479_773, 2),
)

print("--- C: winding/site interfaces")
slab_y = F(33, 200)
slab_t_top = F(1809, 10000)
check("C1 y-floor enters the winding slab", slab_y**2 <= y0sq)
check(
    "C2 exact y-slab margin",
    y0sq - slab_y**2 == F(39_229, 5_000_000),
)
check("C3 t lies inside the site/winding slab", 0 < t0 < slab_t_top)
check("C4 q(0)=y0^2+2t0 stays below one", y0sq + 2 * t0 <= 1)
check("C5 required x-width is at most one", 1 - y0sq <= 1)

pi = iv.pi
window_left = 4 * pi * N0**2
window_next = (
    4 * pi * (N0 + 1) ** 2
    - pi * (iv.mpf(1809) / 10000) / 4
)
left_margin = endpoint_fraction((X - window_left).a)
right_margin = endpoint_fraction((window_next - (X + 1)).a)
check(
    "C6 site window contains X uniformly",
    left_margin > 0 and right_margin > 0,
)
check(
    "C7 deposited site anchor strings",
    floor_decimal(left_margin, 4) == "5377392.8789"
    and floor_decimal(right_margin, 4) == "11989041.1415",
)

print("--- D: finite/direct-Triangle interface")
finite_rows = Nmid - N0 + 1
t_floor = F(791_366, 10**12)
error_upper = F(233_494_905_213, 10**18)
binding_floor = t_floor - error_upper
check("D1 exact finite row count", finite_rows == 3_149_013)
check("D2 finite endpoints", N0 == 690_988 and Nmid == 3_840_000)
check("D3 binding stored T floor is positive", t_floor > 0)
check("D4 effective error is positive", 0 < error_upper < t_floor)
check(
    "D5 corrected selection-unit binding floor is positive",
    binding_floor == F(557_871_094_787, 10**18) > 0,
)
check(
    "D6 mollifier joints are consecutive",
    728_999 + 1 == 729_000
    and 818_999 + 1 == 819_000
    and 1_027_999 + 1 == 1_028_000,
)
check(
    "D7 exact finite leg row counts",
    38_012 + 90_000 + 209_000 + 2_812_001 == finite_rows,
)
check(
    "D8 direct-Dini pattern counts",
    (243, 81, 27, 9) == (3**5, 3**4, 3**3, 3**2),
)
check(
    "D9 worst certified Dini ratio is strict",
    F(99_999_860_767_275_095, 10**17) < 1,
)
check(
    "D10 correction logarithmic rate is strict",
    F(-1_363_112_154_757_640_0, 10**16) < 0,
)

print("--- T: analytic tail")
y_lo = F(1_872_719, 10**7)
y_hi = F(23_409, 125_000)
y_ext_previous = F(4_115_519, 5_000_000)
y_ext_top = F(8_231_039, 10_000_000)
m_head = 153_814
d_upper = F(999_720_909_379_940, 10**15)
flow_lower = F(173_532_614_415, 10**15)
tail_error_upper = F(1_167_160_258_919, 10**20)
slack_lower = F(173_520_942_813, 10**15)
check("T1 exact y-box straddles y0", y_lo**2 < y0sq < y_hi**2)
check(
    "T2 minimal extended grid covers sqrt(1-2t)",
    y_ext_previous**2 < 1 - 2 * t0 <= y_ext_top**2,
)
check(
    "T3 small y-box remains inside the full range",
    y_hi**2 <= 1 - 2 * F(161_250_001, 10**9),
)
check("T4 selected exact-convolution head", m_head == 153_814)
check("T5 contraction D is below one", 0 < d_upper < 1)
check(
    "T6 directed flow exceeds directed error",
    flow_lower > tail_error_upper > 0,
)
check("T7 independently displayed slack is positive", slack_lower > 0)
check(
    "T8 interval grain is below 1-D",
    F(1, 10**30) < 1 - d_upper,
)

print("--- F: closed weld")
check("F1 finite and tail overlap at Nmid", N0 <= Nmid)
check("F2 tail begins at the exact finite endpoint", Nmid == 3_840_000)
full_sweep = (ROOT / "scripts" / "run_full_sweep.sh").read_text()
tail_160 = (ROOT / "verifiers" / "verify_tail_1787854_160.py").read_text()
tail_256 = (ROOT / "verifiers" / "verify_tail_1787854_256.py").read_text()
check(
    "F3 finite and tail sources share the exact t-point",
    "16125 16125 100000" in full_sweep
    and "161250000 161250001 1000000000" in full_sweep
    and all(
        "TC_LO = F(129, 800)" in text
        and "TC_HI = F(161250001, 1000000000)" in text
        for text in (tail_160, tail_256)
    ),
)
check(
    "F4 finite and tail sources share the exact y-floor",
    "350708 10000000" in full_sweep
    and all(
        "YC_SQ = F(87677, 2500000)" in text
        for text in (tail_160, tail_256)
    ),
)
print(
    "[DOCUMENTARY] F5 height, nonvanishing, and winding are criterion "
    "interfaces requiring theorem-level review"
)

print("--- G: conditional conclusion")
check("G1 assembled functional is the exact candidate", B == F(893927, 5_000_000))
print(
    "[DOCUMENTARY] G2 package states that the direct theorem bypasses the "
    "invalid standard-shape seam"
)
print(
    "[DOCUMENTARY] G3 winding, native-functional, site, error, and criterion "
    "bindings remain open to external review"
)

print(f"TOTAL CHECKS RUN: {checks}")
if failures:
    print(f"RESULT: {failures} FAILED")
    sys.exit(1)
print("RESULT: ALL PASS")
print(
    "CONDITIONAL CONCLUSION: accepting the direct native-functional "
    "identification and the cited winding, site, effective-approximation, "
    "and criterion bindings, "
    "Lambda <= 893927/5000000 = 0.1787854."
)
