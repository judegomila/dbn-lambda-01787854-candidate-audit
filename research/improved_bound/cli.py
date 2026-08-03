"""Command line for the improved-bound lane."""

from __future__ import annotations

import argparse
import sys

from .core import ReductionError, compare_to_certified, certified_bound
from .report import STATUS, invocation_line, write_report


def cmd_status(_args: argparse.Namespace) -> int:
    """Report what this lane currently certifies, which is nothing yet."""

    lines = [
        f"certified bound (repository): {certified_bound()}"
        f" = {float(certified_bound()):.7f}",
        "improved bound (this lane):   NOT IMPLEMENTED",
        "",
        "RESULT: NO IMPROVED BOUND CERTIFIED",
    ]
    print(invocation_line())
    print()
    for line in lines:
        print(line)
    print(STATUS)
    path = write_report("status_report.txt", lines)
    print(f"(report written to {path})")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    """Position a candidate bound against the certified one, exactly."""

    from fractions import Fraction as F

    result = compare_to_certified(F(args.candidate))
    verdict = "STRICTLY BETTER" if result["strictly_better"] else "NOT AN IMPROVEMENT"
    lines = [
        f"candidate: {result['candidate']}",
        f"certified: {result['certified']}",
        f"margin:    {result['margin']}",
        "",
        f"RESULT: {verdict}",
    ]
    print(invocation_line())
    print()
    for line in lines:
        print(line)
    print(STATUS)
    path = write_report("compare_report.txt", lines)
    print(f"(report written to {path})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="improved_bound",
        description="Improved-bound research lane (unsealed).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status").set_defaults(func=cmd_status)
    compare = subparsers.add_parser("compare")
    compare.add_argument("candidate", help="exact rational, e.g. 893000/5000000")
    compare.set_defaults(func=cmd_compare)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ReductionError as exc:
        print(f"RESULT FAIL: {exc}", file=sys.stderr)
        return 1
