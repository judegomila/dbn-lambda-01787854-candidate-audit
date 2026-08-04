#!/usr/bin/env python3
"""Compare lower-time direct singleton rows with the amortized replay."""

from __future__ import annotations

import argparse
from decimal import Decimal
import gzip
from pathlib import Path
import re


ROW = re.compile(r"N (\d+) L12 ([0-9.]+) GT089 ([01])")
UNCERT = re.compile(r"N (\d+) UNCERT GT089 ([01])")
TIMING_ONE = re.compile(r"TIMING [0-9]+(?:\.[0-9]+)? 1")
TIMING_ANY = re.compile(r"TIMING [0-9]+(?:\.[0-9]+)? [1-9][0-9]*")
TBOX = "TBOX 16070/100000 16070/100000"
WEIGHT = "WEIGHT TRIANGLE"

FINITE_FILES = (
    "p23571113_690988_728999.log",
    "p235711_729000_774999.log",
    "p2357_775000_849999.log",
    "p235_850000_1074999.log",
    "p23_1075000_1100000.log",
    "p23_1100001_1300000.log",
    "p23_1300001_1700000.log",
    "p23_1700001_2200000.log",
    "p23_2200001_2800000.log",
    "p23_2800001_3300000.log",
    "p23_3300001_4050000.log",
)

EXPECTED = {
    690988, 728999,
    729000, 774999,
    775000, 849999,
    850000, 1074999,
    1075000, 1100000,
    1100001, 1300000,
    1300001, 1700000,
    1700001, 2200000,
    2200001, 2800000,
    2800001, 3300000,
    3300001, 4050000,
}

SHARD_STARTS = {
    690988, 729000, 775000, 850000, 1075000,
    1100001, 1300001, 1700001, 2200001, 2800001, 3300001,
}


def require_regular(path: Path, label: str) -> Path:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{label} must be a regular non-symlink file")
    return path.resolve()


def finite_evidence_path(directory: Path, filename: str) -> Path:
    plain = directory / filename
    compressed = directory / f"{filename}.gz"
    matches = [path for path in (plain, compressed) if path.is_file()]
    if len(matches) != 1:
        raise AssertionError(
            f"need exactly one of {plain.name}, {compressed.name}"
        )
    return require_regular(matches[0], filename)


def parse_finite(log_dir: Path) -> dict[int, tuple[Decimal, int]]:
    if log_dir.is_symlink() or not log_dir.is_dir():
        raise AssertionError("finite log directory must be real")
    result: dict[int, tuple[Decimal, int]] = {}
    for name in FINITE_FILES:
        path = finite_evidence_path(log_dir, name)
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line_number, raw in enumerate(stream, 1):
                line = raw.rstrip("\n")
                if line != line.strip():
                    raise AssertionError(
                        f"{name}:{line_number}: noncanonical whitespace"
                    )
                match = ROW.fullmatch(line)
                if match:
                    n = int(match.group(1))
                    if n in result:
                        raise AssertionError(f"duplicate finite N={n}")
                    result[n] = (Decimal(match.group(2)), int(match.group(3)))
                elif UNCERT.fullmatch(line):
                    raise AssertionError(f"{name}:{line_number}: UNCERT")
                elif line in {TBOX, WEIGHT} or TIMING_ANY.fullmatch(line):
                    continue
                else:
                    raise AssertionError(
                        f"{name}:{line_number}: unknown record {line!r}"
                    )
    return result


def parse_direct(path: Path) -> dict[int, tuple[Decimal, int]]:
    path = require_regular(path, "direct log")
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            lines = stream.read().splitlines()
    else:
        lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) % 4:
        raise AssertionError("direct log must have four lines per singleton")
    result: dict[int, tuple[Decimal, int]] = {}
    for offset in range(0, len(lines), 4):
        tbox, weight, row, timing = lines[offset:offset + 4]
        if tbox != TBOX or weight != WEIGHT:
            raise AssertionError(f"bad direct header at record {offset // 4}")
        match = ROW.fullmatch(row)
        if not match or not TIMING_ONE.fullmatch(timing):
            raise AssertionError(f"bad direct record at line {offset + 1}")
        n = int(match.group(1))
        if n in result:
            raise AssertionError(f"duplicate direct N={n}")
        result[n] = (Decimal(match.group(2)), int(match.group(3)))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("direct_log", type=Path)
    parser.add_argument("finite_logs", type=Path)
    args = parser.parse_args()

    finite = parse_finite(args.finite_logs.resolve())
    direct = parse_direct(args.direct_log)
    if set(direct) != EXPECTED:
        raise AssertionError(
            f"direct set mismatch: missing={EXPECTED - set(direct)}, "
            f"extra={set(direct) - EXPECTED}"
        )

    for n in sorted(EXPECTED):
        if n not in finite:
            raise AssertionError(f"finite replay lacks N={n}")
        direct_lower, direct_gate = direct[n]
        finite_lower, finite_gate = finite[n]
        if direct_lower < finite_lower:
            raise AssertionError(
                f"N={n}: direct {direct_lower} < amortized {finite_lower}"
            )
        if direct_gate < finite_gate:
            raise AssertionError(f"N={n}: direct gate weaker")
        if n in SHARD_STARTS and direct[n] != finite[n]:
            raise AssertionError(
                f"N={n}: shard-start singleton was not reproduced exactly"
            )

    if direct[850000][0] != Decimal("0.000444808402"):
        raise AssertionError("unexpected global finite minimum anchor")
    if direct[4050000][0] <= 0:
        raise AssertionError("nonpositive finite/tail overlap anchor")

    print(
        "[PASS] 22 direct singletons dominate the amortized seam rows"
    )
    print("[PASS] all 11 shard starts reproduce exactly")
    print(
        "[PASS] global finite floor anchor N=850000 is "
        f"{direct[850000][0]}"
    )
    print(
        "[PASS] finite/tail overlap N=4050000 direct="
        f"{direct[4050000][0]} finite={finite[4050000][0]}"
    )
    print("RESULT: LOWER-TIME DIRECT SINGLETON CERTIFICATES PASS")


if __name__ == "__main__":
    main()
