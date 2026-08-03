"""Rank fixed and steered terminal-window candidates."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Iterable

from .certificates import L12Series
from .core import (
    CANDIDATE,
    ERROR_MAX,
    TAIL_MARGIN_LOWER,
    CriterionRow,
    certify_published_landing,
    certify_steered_landing,
    published_fixed_anchor,
    steered_terminal_anchor,
)
from .steering import (
    minimum_average_speed,
    smoothstep5_peak_speed,
)


@dataclass(frozen=True)
class WindowTarget:
    index: int
    suffix_floor_picounits: int
    suffix_argmin: int
    finite_margin: F
    global_margin_lower: F
    gain_over_current: F
    fixed_anchor: int
    fixed_reachable: bool
    fixed_site_shift: int
    steered_anchor: int
    steered_shift_from_current: int
    steered_shift_from_verified_cap: int
    minimum_average_speed: F
    smoothstep5_peak_speed: F


def rank_targets(
    series: L12Series,
    targets: Iterable[int],
    row: CriterionRow = CANDIDATE,
    error_max: F = ERROR_MAX,
    tail_margin_lower: F = TAIL_MARGIN_LOWER,
) -> list[WindowTarget]:
    requested = sorted(set(targets))
    suffix = series.suffix_records(requested)
    current_floor, _current_argmin = series.suffix_records(
        [series.start_n]
    )[series.start_n]
    current_finite = F(current_floor, 10**12) - error_max
    current_global = min(current_finite, tail_margin_lower)
    if current_global <= 0:
        raise ValueError("current stored margin is not positive")

    records: list[WindowTarget] = []
    for index in requested:
        suffix_floor, suffix_argmin = suffix[index]
        finite_margin = F(suffix_floor, 10**12) - error_max
        global_margin = min(finite_margin, tail_margin_lower)

        fixed_anchor = published_fixed_anchor(index, row)
        fixed_landing = certify_published_landing(
            index, fixed_anchor, row
        )
        fixed_reachable = fixed_landing.certified
        fixed_site_shift = max(0, fixed_anchor - row.anchor)

        terminal_anchor = steered_terminal_anchor(index, row)
        steered_landing = certify_steered_landing(
            index, terminal_anchor, row
        )
        if steered_landing.left_margin_lower <= 0:
            raise AssertionError("terminal anchor is not right of x_N")

        shift_current = max(0, terminal_anchor - row.anchor)
        shift_cap = max(
            0, terminal_anchor - row.maximum_verified_anchor
        )
        average = minimum_average_speed(
            F(row.anchor), F(terminal_anchor), row.t0
        )
        peak = smoothstep5_peak_speed(
            F(row.anchor), F(terminal_anchor), row.t0
        )

        records.append(
            WindowTarget(
                index=index,
                suffix_floor_picounits=suffix_floor,
                suffix_argmin=suffix_argmin,
                finite_margin=finite_margin,
                global_margin_lower=global_margin,
                gain_over_current=global_margin / current_global,
                fixed_anchor=fixed_anchor,
                fixed_reachable=fixed_reachable,
                fixed_site_shift=fixed_site_shift,
                steered_anchor=terminal_anchor,
                steered_shift_from_current=shift_current,
                steered_shift_from_verified_cap=shift_cap,
                minimum_average_speed=average,
                smoothstep5_peak_speed=peak,
            )
        )
    return records
