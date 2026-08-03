"""Exact geometry and Riemann--Siegel landing calculations."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .exact import (
    floor_fraction,
    pi_bounds,
    sqrt_bounds,
)


ERROR_MAX = F(233_494_905_212_337_849, 10**24)
TAIL_MARGIN_LOWER = F(1_735_209_373_337, 10**16)


@dataclass(frozen=True)
class CriterionRow:
    """One exact de Bruijn--Newman criterion row."""

    t0: F
    y0_sq: F
    anchor: int
    verified_height: int

    def __post_init__(self) -> None:
        if not F(0) < self.t0 < F(1, 2):
            raise ValueError("need 0 < t0 < 1/2")
        if self.y0_sq <= 0:
            raise ValueError("need y0_sq > 0")
        if self.y0_sq + 2 * self.t0 >= 1:
            raise ValueError("need y0_sq + 2*t0 < 1")
        if self.anchor <= 0 or self.verified_height <= 0:
            raise ValueError("anchor and verified height must be positive")

    @property
    def lambda_bound(self) -> F:
        return self.t0 + self.y0_sq / 2

    @property
    def canopy_sq(self) -> F:
        return self.y0_sq + 2 * self.t0

    @property
    def curved_width_sq(self) -> F:
        return 1 - self.canopy_sq

    @property
    def published_width_sq(self) -> F:
        return 1 - self.y0_sq

    @property
    def maximum_verified_anchor(self) -> int:
        return 2 * self.verified_height

    def lower_y_sq(self, time: F) -> F:
        self._check_time(time)
        return self.y0_sq + 2 * (self.t0 - time)

    def upper_y_sq(self, time: F) -> F:
        self._check_time(time)
        return 1 - 2 * time

    def collar_y_sq(self, time: F, radial: F) -> F:
        self._check_unit(radial, "radial")
        return self.lower_y_sq(time) + radial * radial * self.curved_width_sq

    def collar_offset_sq(self, radial: F, transverse: F) -> F:
        self._check_unit(radial, "radial")
        self._check_unit(transverse, "transverse")
        return (
            radial
            * radial
            * transverse
            * transverse
            * self.curved_width_sq
        )

    def cone_slack(self, time: F, radial: F, transverse: F) -> F:
        """Return y^2-Y(t)^2-(x-a(t))^2 for the box parameterization."""

        return (
            self.collar_y_sq(time, radial)
            - self.lower_y_sq(time)
            - self.collar_offset_sq(radial, transverse)
        )

    def ceiling_slack(self, time: F, radial: F) -> F:
        return self.upper_y_sq(time) - self.collar_y_sq(time, radial)

    def _check_time(self, time: F) -> None:
        if not F(0) <= time <= self.t0:
            raise ValueError("time outside [0,t0]")

    @staticmethod
    def _check_unit(value: F, name: str) -> None:
        if not F(0) <= value <= 1:
            raise ValueError(f"{name} outside [0,1]")


CANDIDATE = CriterionRow(
    t0=F(129, 800),
    y0_sq=F(87_677, 2_500_000),
    anchor=6_000_000_185_827,
    verified_height=3_000_175_332_800,
)


def x_window_bounds(
    index: int,
    row: CriterionRow = CANDIDATE,
    pi_terms: int = 64,
) -> tuple[F, F]:
    """Enclose x_N(t)=4*pi*(N^2-t/16) exactly."""

    if index < 1:
        raise ValueError("window index must be positive")
    pi_lower, pi_upper = pi_bounds(pi_terms)
    factor = F(index * index) - row.t0 / 16
    if factor <= 0:
        raise ValueError("window factor must be positive")
    return 4 * pi_lower * factor, 4 * pi_upper * factor


def steered_terminal_anchor(
    index: int,
    row: CriterionRow = CANDIDATE,
) -> int:
    """Smallest certified integer a with a>x_N.

    This is the safe endpoint for the height-dependent terminal exterior,
    whose left edge equals a at y=y0.
    """

    _lower, upper = x_window_bounds(index, row)
    return floor_fraction(upper) + 1


def published_fixed_anchor(
    index: int,
    row: CriterionRow = CANDIDATE,
) -> int:
    """Smallest integer X whose published constant start is past x_N."""

    _x_lower, x_upper = x_window_bounds(index, row)
    width_lower, _width_upper = sqrt_bounds(row.published_width_sq)
    return floor_fraction(x_upper - width_lower) + 1


@dataclass(frozen=True)
class LandingCertificate:
    """Exact interval checks for one terminal Riemann--Siegel landing."""

    index: int
    anchor: int
    left_margin_lower: F
    right_margin_lower: F
    verified_anchor_slack: int

    @property
    def certified(self) -> bool:
        return (
            self.left_margin_lower > 0
            and self.right_margin_lower > 0
            and self.verified_anchor_slack >= 0
        )


def certify_steered_landing(
    index: int,
    anchor: int,
    row: CriterionRow = CANDIDATE,
) -> LandingCertificate:
    """Certify a lies strictly inside W_N and below the RH height cap."""

    x_lower, x_upper = x_window_bounds(index, row)
    next_lower, _next_upper = x_window_bounds(index + 1, row)
    return LandingCertificate(
        index=index,
        anchor=anchor,
        left_margin_lower=F(anchor) - x_upper,
        right_margin_lower=next_lower - F(anchor),
        verified_anchor_slack=row.maximum_verified_anchor - anchor,
    )


def certify_published_landing(
    index: int,
    anchor: int,
    row: CriterionRow = CANDIDATE,
) -> LandingCertificate:
    """Certify X+sqrt(1-y0^2) lies strictly inside W_N."""

    x_lower, x_upper = x_window_bounds(index, row)
    next_lower, _next_upper = x_window_bounds(index + 1, row)
    width_lower, width_upper = sqrt_bounds(row.published_width_sq)
    return LandingCertificate(
        index=index,
        anchor=anchor,
        left_margin_lower=F(anchor) + width_lower - x_upper,
        right_margin_lower=next_lower - F(anchor) - width_upper,
        verified_anchor_slack=row.maximum_verified_anchor - anchor,
    )
