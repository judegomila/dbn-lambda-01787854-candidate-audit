#!/usr/bin/env python3
"""Compare a fresh uncompressed sweep with every sealed stored row."""

import gzip
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
STORED = ROOT / "certificates"
REPLAY = Path(sys.argv[1]).resolve()

FILES = (
    "p235711_690988_690995.log",
    "p235711_690996_691500.log",
    "p235711_691501_697000.log",
    "p235711_697001_728999.log",
    "p2357_729000_818999.log",
    "p235_819000_1027999.log",
    "p23_1028000_1030000.log",
    "p23_1030001_1050000.log",
    "p23_1050001_1100000.log",
    "p23_1100001_1300000.log",
    "p23_1300001_1700000.log",
    "p23_1700001_2200000.log",
    "p23_2200001_2800000.log",
    "p23_2800001_3300000.log",
    "p23_3300001_3840000.log",
)

ROW = re.compile(r"N ([0-9]+) L12 ([0-9.]+) GT089 ([01])")
UNCERT = re.compile(r"N ([0-9]+) UNCERT GT089 ([01])")


def rows(stream, label):
    result = []
    for line_number, raw in enumerate(stream, 1):
        line = raw.strip()
        match = ROW.fullmatch(line)
        if match:
            result.append(match.groups())
        elif UNCERT.fullmatch(line):
            raise AssertionError(f"{label}:{line_number}: UNCERT")
    if not result:
        raise AssertionError(f"{label}: no rows")
    return result


total = 0
previous = None
for name in FILES:
    stored_path = STORED / f"{name}.gz"
    replay_path = REPLAY / name
    if not replay_path.is_file():
        raise AssertionError(f"missing replay file: {replay_path}")
    with gzip.open(stored_path, "rt", encoding="utf-8") as stream:
        expected = rows(stream, stored_path.name)
    with replay_path.open("rt", encoding="utf-8") as stream:
        actual = rows(stream, replay_path.name)
    if actual != expected:
        for index, (left, right) in enumerate(zip(actual, expected)):
            if left != right:
                raise AssertionError(
                    f"{name}: row mismatch at local index {index}: "
                    f"{left} != {right}"
                )
        raise AssertionError(
            f"{name}: row-count mismatch {len(actual)} != {len(expected)}"
        )
    first = int(actual[0][0])
    last = int(actual[-1][0])
    if previous is not None and first != previous + 1:
        raise AssertionError(f"global replay gap: {previous}, {first}")
    previous = last
    total += len(actual)
    print(f"[PASS] {name}: rows={len(actual)} N={first}..{last}")

if total != 3_149_013 or previous != 3_840_000:
    raise AssertionError(f"global replay totals {total}, endpoint {previous}")
print(
    "RESULT PASS: fresh sweep matches all 3149013 sealed rows "
    "N=690988..3840000"
)
