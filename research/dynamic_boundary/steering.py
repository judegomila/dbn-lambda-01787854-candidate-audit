"""Exact rational steering schedules and unavoidable speed costs."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F


def de_casteljau(controls: tuple[F, ...], parameter: F) -> F:
    if not F(0) <= parameter <= 1:
        raise ValueError("Bernstein parameter outside [0,1]")
    row = list(controls)
    while len(row) > 1:
        row = [
            (1 - parameter) * left + parameter * right
            for left, right in zip(row, row[1:])
        ]
    return row[0]


@dataclass(frozen=True)
class BernsteinPath:
    """A Bernstein polynomial a(t/t0) with exact rational controls."""

    t0: F
    controls: tuple[F, ...]

    def __post_init__(self) -> None:
        if self.t0 <= 0:
            raise ValueError("t0 must be positive")
        if len(self.controls) < 2:
            raise ValueError("need at least two controls")

    @property
    def degree(self) -> int:
        return len(self.controls) - 1

    @property
    def start(self) -> F:
        return self.controls[0]

    @property
    def end(self) -> F:
        return self.controls[-1]

    def evaluate(self, time: F) -> F:
        if not F(0) <= time <= self.t0:
            raise ValueError("time outside [0,t0]")
        return de_casteljau(self.controls, time / self.t0)

    def derivative_controls(self, order: int = 1) -> tuple[F, ...]:
        if order < 0 or order > self.degree:
            raise ValueError("invalid derivative order")
        controls = self.controls
        degree = self.degree
        for _ in range(order):
            scale = F(degree, 1) / self.t0
            controls = tuple(
                scale * (right - left)
                for left, right in zip(controls, controls[1:])
            )
            degree -= 1
        return controls

    def derivative_hull(self, order: int = 1) -> tuple[F, F]:
        controls = self.derivative_controls(order)
        return min(controls), max(controls)

    def derivative(self, time: F, order: int = 1) -> F:
        if not F(0) <= time <= self.t0:
            raise ValueError("time outside [0,t0]")
        return de_casteljau(
            self.derivative_controls(order),
            time / self.t0,
        )


def linear_path(start: F, end: F, t0: F) -> BernsteinPath:
    return BernsteinPath(t0=t0, controls=(start, end))


def smoothstep5_path(start: F, end: F, t0: F) -> BernsteinPath:
    """Quintic smoothstep with zero first/second endpoint derivatives."""

    return BernsteinPath(
        t0=t0,
        controls=(start, start, start, end, end, end),
    )


def minimum_average_speed(start: F, end: F, t0: F) -> F:
    if t0 <= 0:
        raise ValueError("t0 must be positive")
    return abs(end - start) / t0


def smoothstep5_peak_speed(start: F, end: F, t0: F) -> F:
    """Exact L-infinity speed of the quintic smoothstep."""

    return F(15, 8) * minimum_average_speed(start, end, t0)
