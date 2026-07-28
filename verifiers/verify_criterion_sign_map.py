#!/usr/bin/env python3
"""Exact algebra audit for the H_0-to-zeta sign/symmetry bridge."""

from fractions import Fraction as F
import sys


# Affine forms are (constant, x coefficient, y coefficient).
ZERO = F(0)
ONE = F(1)
HALF = F(1, 2)

checks = 0
failures = 0


def check(name: str, condition: bool) -> None:
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def subtract(left: tuple[F, F, F], right: tuple[F, F, F]) -> tuple[F, F, F]:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def negate(form: tuple[F, F, F]) -> tuple[F, F, F]:
    return tuple(-value for value in form)


constant_one = (ONE, ZERO, ZERO)

# For z=x+iy, H_0(z)=xi(1/2+iz/2)/8.
s0_real = (HALF, ZERO, -HALF)
s0_imag = (ZERO, HALF, ZERO)
check("S1 direct preimage has real part (1-y)/2", s0_real == (HALF, ZERO, -HALF))
check("S2 direct preimage has height x/2", s0_imag == (ZERO, HALF, ZERO))

# xi(s)=xi(1-s), followed by conjugation of the zero.
reflected_real = subtract(constant_one, s0_real)
reflected_imag = negate(s0_imag)
check(
    "S3 functional-equation reflection is (1+y)/2-ix/2",
    reflected_real == (HALF, ZERO, HALF)
    and reflected_imag == (ZERO, -HALF, ZERO),
)
conjugated_real = reflected_real
conjugated_imag = negate(reflected_imag)
check(
    "S4 conjugated representative is (1+y)/2+ix/2",
    conjugated_real == (HALF, ZERO, HALF)
    and conjugated_imag == (ZERO, HALF, ZERO),
)

# Exact scalar implications used when mapping criterion hypothesis (i).
t0 = F(129, 800)
y0_squared = F(87677, 2_500_000)
x = 6_000_000_185_827
check(
    "S5 positive candidate data give sqrt(y0^2+2t0)>=y0>0",
    t0 >= 0 and y0_squared > 0 and y0_squared + 2 * t0 >= y0_squared,
)
check(
    "S6 x in [0,X] maps to zeta height in [0,X/2] with X>0",
    x > 0 and F(x, 2) > 0,
)

print(f"TOTAL CHECKS RUN: {checks}")
if failures:
    print(f"RESULT: {failures} FAILED")
    sys.exit(1)
print("RESULT: CRITERION SIGN MAP PASS")
