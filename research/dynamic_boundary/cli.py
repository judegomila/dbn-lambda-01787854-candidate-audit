"""Command-line reports for the dynamic-boundary research lane."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from pathlib import Path

from .analysis import rank_targets
from .certificates import (
    load_l12_series,
    repository_certificate_paths,
)
from .core import (
    CANDIDATE,
    certify_published_landing,
    certify_steered_landing,
    published_fixed_anchor,
    steered_terminal_anchor,
)
from .exact import decimal_text, sqrt_bounds
from .steering import smoothstep5_path
from .steering import minimum_average_speed, smoothstep5_peak_speed


STATUS = (
    "STATUS: UNSEALED RESEARCH ONLY; no improved Lambda bound certified."
)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def geometry_report() -> None:
    row = CANDIDATE
    width_lower, width_upper = sqrt_bounds(row.curved_width_sq)
    published_lower, published_upper = sqrt_bounds(
        row.published_width_sq
    )
    checks = 0
    for time_step in range(9):
        time = row.t0 * F(time_step, 8)
        if row.upper_y_sq(time) - row.lower_y_sq(time) != row.curved_width_sq:
            raise AssertionError("nonconstant squared collar width")
        for radial_step in range(9):
            radial = F(radial_step, 8)
            for transverse_step in range(9):
                transverse = F(transverse_step, 8)
                if row.cone_slack(time, radial, transverse) < 0:
                    raise AssertionError("negative cone slack")
                if row.ceiling_slack(time, radial) < 0:
                    raise AssertionError("negative ceiling slack")
                checks += 2

    print(f"lambda_row={row.lambda_bound}")
    print(f"curved_width_sq={row.curved_width_sq}")
    print(
        "curved_width=["
        f"{decimal_text(width_lower, 18)},"
        f"{decimal_text(width_upper, 18)}]"
    )
    print(
        "published_width=["
        f"{decimal_text(published_lower, 18)},"
        f"{decimal_text(published_upper, 18)}]"
    )
    print(f"RESULT: {checks} EXACT CURVED-GEOMETRY CHECKS PASS")
    print(STATUS)


def landing_report(index: int) -> None:
    row = CANDIDATE
    fixed_anchor = published_fixed_anchor(index, row)
    terminal_anchor = steered_terminal_anchor(index, row)
    fixed = certify_published_landing(index, fixed_anchor, row)
    terminal = certify_steered_landing(index, terminal_anchor, row)
    path = smoothstep5_path(F(row.anchor), F(terminal_anchor), row.t0)
    average_speed = minimum_average_speed(
        path.start, path.end, path.t0
    )
    peak_speed = smoothstep5_peak_speed(
        path.start, path.end, path.t0
    )

    print(f"window={index}")
    print(f"published_fixed_anchor={fixed_anchor}")
    print(f"published_fixed_reachable={fixed.certified}")
    print(
        "published_left_margin_lower="
        f"{decimal_text(fixed.left_margin_lower, 12)}"
    )
    print(
        "published_right_margin_lower="
        f"{decimal_text(fixed.right_margin_lower, 12)}"
    )
    print(f"steered_terminal_anchor={terminal_anchor}")
    print(
        "steered_left_margin_lower="
        f"{decimal_text(terminal.left_margin_lower, 12)}"
    )
    print(f"verified_anchor_slack={terminal.verified_anchor_slack}")
    print(f"shift_from_current={terminal_anchor-row.anchor}")
    print(f"minimum_average_speed={decimal_text(average_speed, 6)}")
    print(f"smoothstep5_peak_speed={decimal_text(peak_speed, 6)}")
    if fixed.certified:
        print("RECOMMENDATION: test a new fixed barrier before steering.")
    else:
        print(
            "RECOMMENDATION: fixed verified-height budget is exhausted; "
            "a moving-wall theorem and certificate would be required."
        )
    print(STATUS)


def rank_report(first: int, last: int) -> None:
    if first > last:
        raise ValueError("first target exceeds last target")
    root = repository_root()
    paths = repository_certificate_paths(root)
    series = load_l12_series(paths, CANDIDATE.t0)
    if series.start_n != 690_988 or series.end_n != 3_840_000:
        raise ValueError("unexpected complete finite-series endpoints")
    records = rank_targets(series, range(first, last + 1))

    print(
        "N suffix_floor argmin finite_margin global_margin gain "
        "fixed_reachable fixed_X fixed_site_shift steered_a1 "
        "steered_shift_from_X steered_shift_from_PT_cap"
    )
    for record in records:
        print(
            f"{record.index} "
            f"{record.suffix_floor_picounits/10**12:.12f} "
            f"{record.suffix_argmin} "
            f"{decimal_text(record.finite_margin, 18)} "
            f"{decimal_text(record.global_margin_lower, 18)} "
            f"{decimal_text(record.gain_over_current, 6)} "
            f"{'yes' if record.fixed_reachable else 'no'} "
            f"{record.fixed_anchor} "
            f"{record.fixed_site_shift} "
            f"{record.steered_anchor} "
            f"{record.steered_shift_from_current} "
            f"{record.steered_shift_from_verified_cap}"
        )
    print(STATUS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unsealed dynamic-boundary research tools"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("geometry")

    landing = subparsers.add_parser("landing")
    landing.add_argument("index", type=int)

    ranking = subparsers.add_parser("rank")
    ranking.add_argument("--first", type=int, default=690_988)
    ranking.add_argument("--last", type=int, default=691_020)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        if arguments.command == "geometry":
            geometry_report()
        elif arguments.command == "landing":
            landing_report(arguments.index)
        elif arguments.command == "rank":
            rank_report(arguments.first, arguments.last)
        else:
            raise AssertionError("unknown command")
    except (AssertionError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"RESULT FAIL: {exc}")
        return 1
    return 0
