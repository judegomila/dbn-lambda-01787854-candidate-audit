"""Small exact-arithmetic helpers used by the research lane."""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from math import isqrt


def floor_fraction(value: Fraction) -> int:
    """Return floor(value) exactly."""

    return value.numerator // value.denominator


def ceil_fraction(value: Fraction) -> int:
    """Return ceil(value) exactly."""

    return -((-value.numerator) // value.denominator)


def sqrt_bounds(
    value: Fraction,
    decimal_digits: int = 60,
) -> tuple[Fraction, Fraction]:
    """Return outward decimal-rational bounds for sqrt(value).

    The result is exact: no floating-point operation is used to construct
    either endpoint.
    """

    if value < 0:
        raise ValueError("cannot take the square root of a negative value")
    if decimal_digits < 1:
        raise ValueError("decimal_digits must be positive")
    scale = 10**decimal_digits
    scaled_square = value.numerator * scale * scale // value.denominator
    lower_integer = isqrt(scaled_square)
    lower = Fraction(lower_integer, scale)
    if lower * lower == value:
        return lower, lower
    return lower, Fraction(lower_integer + 1, scale)


def atan_reciprocal_bounds(
    denominator: int,
    terms: int,
) -> tuple[Fraction, Fraction]:
    """Bound atan(1/denominator) by an alternating Taylor series."""

    if denominator <= 1:
        raise ValueError("denominator must exceed one")
    if terms < 1:
        raise ValueError("terms must be positive")

    partial = Fraction(0)
    for index in range(terms):
        term = Fraction(
            1,
            (2 * index + 1) * denominator ** (2 * index + 1),
        )
        partial = partial + term if index % 2 == 0 else partial - term

    index = terms
    next_term = Fraction(
        1,
        (2 * index + 1) * denominator ** (2 * index + 1),
    )
    other_endpoint = (
        partial + next_term if index % 2 == 0 else partial - next_term
    )
    return min(partial, other_endpoint), max(partial, other_endpoint)


@lru_cache(maxsize=None)
def pi_bounds(terms: int = 64) -> tuple[Fraction, Fraction]:
    """Return exact rational bounds for pi using Machin's identity."""

    atan5_lo, atan5_hi = atan_reciprocal_bounds(5, terms)
    atan239_lo, atan239_hi = atan_reciprocal_bounds(239, terms)
    lower = 16 * atan5_lo - 4 * atan239_hi
    upper = 16 * atan5_hi - 4 * atan239_lo
    if not lower < upper:
        raise AssertionError("invalid pi enclosure")
    return lower, upper


def decimal_text(value: Fraction, digits: int = 18) -> str:
    """Render an exact fraction as a decimal for human-readable reports."""

    if digits < 1:
        raise ValueError("digits must be positive")
    with localcontext() as context:
        context.prec = digits + 20
        result = Decimal(value.numerator) / Decimal(value.denominator)
        return f"{result:.{digits}f}"
