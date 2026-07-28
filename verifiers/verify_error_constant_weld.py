#!/usr/bin/env python3
"""Fail-closed source and exact-arithmetic check for the 10.50 error weld."""

from fractions import Fraction as F
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent

if sys.flags.optimize:
    raise SystemExit("error: Python optimization is not permitted")

checks = 0
failures = 0


def check(name: str, condition: bool) -> None:
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def source(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


x_min = F(200)
old_denominator_shift = F(852, 100)
target_denominator_shift = F(12)
prop_constant = F(358, 100)
remainder_constant = F(692, 100)
target_constant = F(1050, 100)

check(
    "W1 theorem-domain denominators are strictly positive",
    x_min - target_denominator_shift > 0,
)
check(
    "W2 denominator enlargement is conservative",
    x_min - old_denominator_shift > x_min - target_denominator_shift,
)
check(
    "W3 Proposition 6.6(vi) constants sum exactly to 21/2",
    prop_constant + remainder_constant == F(21, 2),
)
check("W4 target decimal is exactly 10.50", target_constant == F(21, 2))

python_finite = source("verifiers/verify_finite_and_binding.py")
python_barrier = source("verifiers/verify_barrier_binding.py")
python_tail_160 = source("verifiers/verify_tail_1787854_160.py")
python_tail_256 = source("verifiers/verify_tail_1787854_256.py")
arb_tail = source("verifiers/verify_tail_arb.c")
arb_barrier = source("barrier/src/verify_uniform_error_01787854.c")
assembly = source("verifiers/verify_assembly_1787854.py")
proof = source("ERROR_CONSTANT_WELD.md")

check(
    "W5 finite Python lane consumes 10.50 and not 10.44",
    'iv.mpf("10.50")' in python_finite and 'iv.mpf("10.44")' not in python_finite,
)
check(
    "W6 barrier Python lane consumes 10.50 and not 10.44",
    'iv.mpf("10.50")' in python_barrier and 'iv.mpf("10.44")' not in python_barrier,
)
check(
    "W7 Python tail lanes consume 10.50 and not 10.44",
    all(
        "itv(F(1050, 100))" in text and "itv(F(1044, 100))" not in text
        for text in (python_tail_160, python_tail_256)
    ),
)
check(
    "W8 standalone Arb tail consumes exact 21/2 and not 1044/100",
    "set_q(tmp2, 21, 2);" in arb_tail and "set_q(tmp2, 1044, 100);" not in arb_tail,
)
check(
    "W9 barrier Arb lane consumes exact 21/2 and not decimal 10.44",
    "arb_set_ui(tmp2, 21);" in arb_barrier
    and "arb_div_ui(tmp2, tmp2, 2, prec);" in arb_barrier
    and '"10.44"' not in arb_barrier,
)
check(
    "W10 final assembly executes this weld",
    '"verifiers/verify_error_constant_weld.py"' in assembly
    and "RESULT: CONSERVATIVE ERROR-CONSTANT WELD PASS" in assembly,
)
check(
    "W11 proof note records the exact conservative derivation",
    "3.58+6.92" in proof and "10.50" in proof and "x-8.52>x-12>0" in proof,
)

print(f"TOTAL CHECKS RUN: {checks}")
if failures:
    print(f"RESULT: {failures} FAILED")
    raise SystemExit(1)
print("RESULT: CONSERVATIVE ERROR-CONSTANT WELD PASS")
