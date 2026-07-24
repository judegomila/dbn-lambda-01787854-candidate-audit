#!/usr/bin/env python3
"""Fail-closed checks for the native Triangle-to-|f_t| binding.

The proof is NATIVE_BINDING.md.  This verifier does two independent jobs:

1. pin the load-bearing producer/error-source structure used by that proof;
2. stress-test the two exact convolutions and final lower bound with complex
   phases and complex kappa on 216 deterministic finite examples.

The numerical stress test is a falsification check, not a replacement for
the algebraic proof.
"""

from __future__ import annotations

import cmath
import itertools
import math
from pathlib import Path
import random
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
PRODUCER = ROOT / "src" / "lemma_sweep_p235711.c"
FULL_SWEEP = ROOT / "scripts" / "run_full_sweep.sh"
ERROR_CHECK = ROOT / "verifiers" / "verify_finite_and_binding.py"

checks = 0
failures = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    print(
        f"[{'PASS' if ok else 'FAIL'}] {name}"
        + (f"  {detail}" if detail else "")
    )


def require_order(text: str, name: str, fragments: tuple[str, ...]) -> None:
    position = -1
    for fragment in fragments:
        next_position = text.find(fragment, position + 1)
        if next_position < 0:
            check(name, False, f"missing {fragment!r}")
            return
        position = next_position
    check(name, True)


producer = PRODUCER.read_text(encoding="utf-8")
full_sweep = FULL_SWEEP.read_text(encoding="utf-8")
error_check = ERROR_CHECK.read_text(encoding="utf-8")

print("--- A: structural source contract")
check(
    "A1 full replay compiles the direct Triangle branch",
    "-DTRIANGLE_WEIGHT" in full_sweep,
)
check(
    "A2 bt definition is exp((t/4) log^2 n)",
    all(
        fragment in producer
        for fragment in (
            "static void bt_eval",
            "arb_mul(u, lnm, lnm, prec);",
            "arb_mul(u, u, t, prec);",
            "arb_mul_2exp_si(u, u, -2);",
            "arb_exp(res, u, prec);",
        )
    ),
)
check(
    "A3 real Euler coefficients include every supported prime",
    all(
        re.search(
            rf"if\(mask&{1 << index}\).*?arb_mul\("
            rf"ms\.moll\[mask\].*?b{prime}.*?arb_neg\(",
            producer,
            re.DOTALL,
        )
        for index, prime in enumerate((2, 3, 5, 7, 11))
    ),
)
require_order(
    producer,
    "A4 bA0 forms the two exact real convolutions",
    (
        "static ulong bA0",
        "arb_addmul(b, bb, ms->moll[i], prec);",
        "arb_mul(e, lnnd, y, prec);",
        "arb_exp(e, e, prec);",
        "arb_mul(bb, bb, e, prec);",
        "arb_addmul(a0, bb, ms->moll[i], prec);",
    ),
)
require_order(
    producer,
    "A5 direct weight is |B| + gamma |A|",
    (
        "#ifdef TRIANGLE_WEIGHT",
        "arb_abs(t1, b);",
        "arb_abs(t2, a0);",
        "arb_mul(t2, t2, ga, prec);",
        "arb_add(W, t1, t2, prec);",
    ),
)
require_order(
    producer,
    "A6 mollifier bound is sum |lambda_d| d^-sigma",
    (
        "arb_zero(modmoll);",
        "arb_abs(tmp, ms.moll[i]);",
        "arb_mul(tmp2, ms.lnd[i], sigma, prec);",
        "arb_neg(tmp2, tmp2);",
        "arb_exp(tmp2, tmp2, prec);",
        "arb_addmul(modmoll, tmp, tmp2, prec);",
    ),
)
require_order(
    producer,
    "A7 final value has exactly one division then correction subtraction",
    (
        "/* lbound = (1 - modgamma - Ssum)/modmoll - corr */",
        "arb_set_ui(lbound, 1);",
        "arb_sub(lbound, lbound, modgamma, prec);",
        "arb_sub(lbound, lbound, Ssum, prec);",
        "arb_div(lbound, lbound, modmoll, prec);",
        "arb_sub(lbound, lbound, corr, prec);",
    ),
)
check(
    "A8 target error path uses x-6.66 for equation (23)",
    '/ (x0 - iv.mpf("6.66"))' in error_check,
)
check(
    "A9 target e_C0 path uses x-12 for equation (24)",
    "/ (x0 - 12)" in error_check,
)

print("--- B: deterministic complex convolution and inequality stress test")
random.seed(1_787_854)
t = 129 / 800


def bt(n: int) -> float:
    return math.exp((t / 4) * math.log(n) ** 2)


def divisors_and_lambdas(
    primes: tuple[int, ...],
) -> list[tuple[int, float]]:
    result = []
    for mask in range(1 << len(primes)):
        divisor = 1
        coefficient = 1.0
        for index, prime in enumerate(primes):
            if mask & (1 << index):
                divisor *= prime
                coefficient *= -bt(prime)
        result.append((divisor, coefficient))
    return result


def stress_case(
    primes: tuple[int, ...],
    cutoff: int,
    y: float,
    sigma: float,
    phase: float,
) -> tuple[float, float, float]:
    terms = divisors_and_lambdas(primes)
    max_divisor = math.prod(primes)
    s = complex(sigma + 0.11, phase)

    mollifier = sum(
        coefficient * divisor ** (-s)
        for divisor, coefficient in terms
    )
    first = sum(bt(m) * m ** (-s) for m in range(1, cutoff + 1))
    second_zero = sum(
        m**y * bt(m) * m ** (-s.conjugate())
        for m in range(1, cutoff + 1)
    )

    b_coefficients = [0.0] * (max_divisor * cutoff + 1)
    a_coefficients = [0.0] * (max_divisor * cutoff + 1)
    for n in range(1, max_divisor * cutoff + 1):
        for divisor, coefficient in terms:
            if n % divisor == 0 and n // divisor <= cutoff:
                m = n // divisor
                b_coefficients[n] += coefficient * bt(m)
                a_coefficients[n] += coefficient * bt(m) * m**y

    first_convolution = sum(
        b_coefficients[n] * n ** (-s)
        for n in range(1, max_divisor * cutoff + 1)
    )
    second_convolution = sum(
        a_coefficients[n] * n ** (-s.conjugate())
        for n in range(1, max_divisor * cutoff + 1)
    )
    first_error = abs(mollifier * first - first_convolution)
    second_error = abs(
        mollifier.conjugate() * second_zero - second_convolution
    )

    gamma_bound = 0.008
    kappa_bound = 0.002
    gamma = 0.73 * gamma_bound * cmath.exp(
        1j * random.uniform(-math.pi, math.pi)
    )
    kappa = 0.81 * kappa_bound * cmath.exp(
        1j * random.uniform(-math.pi, math.pi)
    )
    second_kappa = sum(
        m**y * bt(m) * m ** (-s.conjugate() - kappa)
        for m in range(1, cutoff + 1)
    )
    f_value = first + gamma * second_kappa

    mollifier_upper = sum(
        abs(coefficient) * divisor ** (-sigma)
        for divisor, coefficient in terms
    )
    triangle_mass = sum(
        (
            abs(b_coefficients[n])
            + gamma_bound * abs(a_coefficients[n])
        )
        * n ** (-sigma)
        for n in range(2, max_divisor * cutoff + 1)
    )
    numerator = 1 - gamma_bound - triangle_mass
    correction = sum(
        bt(m)
        * (m**kappa_bound - 1)
        * m ** (y - sigma)
        for m in range(2, cutoff + 1)
    )
    lower_bound = (
        numerator / mollifier_upper - gamma_bound * correction
    )
    if numerator <= 0:
        raise AssertionError("stress parameters unexpectedly lost Q>0")
    binding_slack = abs(f_value) - lower_bound
    return first_error, second_error, binding_slack


case_count = 0
max_first_error = 0.0
max_second_error = 0.0
min_binding_slack = math.inf
for prime_list in (
    (2, 3),
    (2, 3, 5),
    (2, 3, 5, 7),
    (2, 3, 5, 7, 11),
):
    for cutoff, y, sigma, phase in itertools.product(
        (3, 5, 8),
        (0.18, 0.42, 0.81),
        (4.0, 5.5),
        (-11.2, -0.7, 8.9),
    ):
        first_error, second_error, binding_slack = stress_case(
            prime_list, cutoff, y, sigma, phase
        )
        case_count += 1
        max_first_error = max(max_first_error, first_error)
        max_second_error = max(max_second_error, second_error)
        min_binding_slack = min(min_binding_slack, binding_slack)

check("B1 expected stress-case count", case_count == 216)
check(
    "B2 first exact convolution in all cases",
    max_first_error < 2e-11,
    f"max floating residual={max_first_error:.3e}",
)
check(
    "B3 conjugated second exact convolution in all cases",
    max_second_error < 2e-11,
    f"max floating residual={max_second_error:.3e}",
)
check(
    "B4 derived lower bound survives complex gamma and kappa",
    min_binding_slack > -2e-12,
    f"minimum floating slack={min_binding_slack:.3e}",
)

print(f"TOTAL CHECKS RUN: {checks}")
if failures:
    print(f"RESULT: {failures} FAILED")
    sys.exit(1)
print("RESULT: ALL PASS")
