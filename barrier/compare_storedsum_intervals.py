#!/usr/bin/env python3
"""Check that regenerated Arb intervals fit inside archived-decimal balls."""

from __future__ import annotations

import argparse
import re
from decimal import Decimal, getcontext
from pathlib import Path


INTERVAL_RE = re.compile(r"^\[(.+) \+/- (.+)\]$")


def read_matrix(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text().splitlines()
    if not lines:
        raise ValueError(f"empty stored-sum file: {path}")
    header = [field.strip() for field in lines[0].split(",")]
    if len(header) != 4:
        raise ValueError(f"invalid header in {path}: {lines[0]!r}")
    values = [
        field.strip()
        for line in lines[1:]
        if not line.startswith("cpu/wall")
        for field in line.split(",")
    ]
    return header, values


def parse_ball(text: str) -> tuple[Decimal, Decimal]:
    match = INTERVAL_RE.fullmatch(text)
    if match:
        return Decimal(match.group(1)), Decimal(match.group(2))
    return Decimal(text), Decimal(0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archived", type=Path)
    parser.add_argument("regenerated", type=Path)
    args = parser.parse_args()

    getcontext().prec = 100
    archived_header, archived = read_matrix(args.archived)
    regenerated_header, regenerated = read_matrix(args.regenerated)

    if archived_header != regenerated_header:
        raise SystemExit(
            f"header mismatch: {archived_header!r} != {regenerated_header!r}"
        )
    rows = int(archived_header[1])
    columns = int(archived_header[2])
    digits = int(archived_header[3])
    expected = 2 * rows * columns
    if len(archived) != expected or len(regenerated) != expected:
        raise SystemExit(
            f"component count mismatch: expected {expected}, "
            f"archived {len(archived)}, regenerated {len(regenerated)}"
        )

    scale = Decimal(10) ** (-digits)
    worst_ratio = Decimal(0)
    worst_index = 0
    worst_radius_scale = Decimal(0)
    failures: list[tuple[int, Decimal]] = []
    interval_components = 0

    for index, (old_text, new_text) in enumerate(
        zip(archived, regenerated), start=1
    ):
        old_value = Decimal(old_text)
        midpoint, radius = parse_ball(new_text)
        interval_components += radius != 0
        allowed = scale * max(Decimal(1), abs(old_value))
        ratio = (abs(midpoint - old_value) + radius) / allowed
        radius_scale = radius / max(Decimal(1), abs(midpoint))
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_index = index
        if radius_scale > worst_radius_scale:
            worst_radius_scale = radius_scale
        if ratio > 1:
            failures.append((index, ratio))

    print(f"components: {expected}")
    print(f"components with nonzero printed Arb radii: {interval_components}")
    print(f"containment failures: {len(failures)}")
    print(f"worst total-to-widening ratio: {worst_ratio}")
    print(f"worst component index: {worst_index}")
    print(f"maximum regenerated radius scale: {worst_radius_scale}")

    if interval_components == 0:
        raise SystemExit("regenerated file did not retain Arb radii")
    if failures:
        raise SystemExit(f"first containment failure: {failures[0]}")
    print("RESULT: STORED-SUM PROVENANCE PASS")


if __name__ == "__main__":
    main()
