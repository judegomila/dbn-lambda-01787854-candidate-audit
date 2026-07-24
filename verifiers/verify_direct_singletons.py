#!/usr/bin/env python3
"""Compare 30 non-amortized singleton rows with the sealed finite sweep."""

from decimal import Decimal
import gzip
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
CERTIFICATES = ROOT / "certificates"
DIRECT_LOG_ARGUMENT = (
    Path(sys.argv[1])
    if len(sys.argv) == 2
    else ROOT / "logs" / "direct_singletons_256.log"
)
if len(sys.argv) > 2:
    raise SystemExit("usage: verify_direct_singletons.py [DIRECT_LOG]")
if DIRECT_LOG_ARGUMENT.is_symlink() or not DIRECT_LOG_ARGUMENT.is_file():
    raise AssertionError("direct log must be a regular, non-symlink file")
DIRECT_LOG = DIRECT_LOG_ARGUMENT.resolve()

ROW = re.compile(r"N (\d+) L12 ([0-9.]+) GT089 ([01])")
UNCERT = re.compile(r"N (\d+) UNCERT GT089 ([01])")
TIMING = re.compile(r"TIMING ([0-9]+(?:\.[0-9]+)?) 1")
TBOX_EXACT = "TBOX 16125/100000 16125/100000"
TBOX_INTERVAL = "TBOX 161250000/1000000000 161250001/1000000000"
WEIGHT = "WEIGHT TRIANGLE"


def parse_stored(lines, label: str) -> dict[int, tuple[Decimal, int]]:
    result: dict[int, tuple[Decimal, int]] = {}
    for number, raw in enumerate(lines, 1):
        line = raw[:-1] if raw.endswith("\n") else raw
        if line.endswith("\r") or line != line.strip():
            raise AssertionError(
                f"{label}:{number}: noncanonical record whitespace"
            )
        match = ROW.fullmatch(line)
        if match:
            n_text, lower, gate = match.groups()
            n = int(n_text)
            if n in result:
                raise AssertionError(f"{label}:{number}: duplicate N={n}")
            result[n] = (Decimal(lower), int(gate))
        elif UNCERT.fullmatch(line):
            raise AssertionError(f"{label}:{number}: uncertainty row")
        elif (
            line in {TBOX_EXACT, TBOX_INTERVAL, WEIGHT}
            or re.fullmatch(r"TIMING [0-9]+(?:\.[0-9]+)? [1-9][0-9]*", line)
        ):
            continue
        else:
            raise AssertionError(
                f"{label}:{number}: unrecognized record: {line!r}"
            )
    return result


def parse_direct(lines: list[str], label: str) -> dict[int, tuple[Decimal, int]]:
    if len(lines) % 4:
        raise AssertionError(
            f"{label}: incomplete record; expected four lines per singleton"
        )
    result: dict[int, tuple[Decimal, int]] = {}
    for offset in range(0, len(lines), 4):
        number = offset + 1
        records = lines[offset:offset + 4]
        for record_offset, line in enumerate(records):
            if line != line.strip():
                raise AssertionError(
                    f"{label}:{number + record_offset}: "
                    "noncanonical record whitespace"
                )
        tbox, weight, row, timing = records
        if tbox not in {TBOX_EXACT, TBOX_INTERVAL}:
            raise AssertionError(
                f"{label}:{number}: unrecognized TBOX record: {tbox!r}"
            )
        if weight != WEIGHT:
            raise AssertionError(
                f"{label}:{number + 1}: unrecognized WEIGHT record: {weight!r}"
            )
        match = ROW.fullmatch(row)
        if not match:
            if UNCERT.fullmatch(row):
                raise AssertionError(f"{label}:{number + 2}: uncertainty row")
            raise AssertionError(
                f"{label}:{number + 2}: unrecognized N record: {row!r}"
            )
        if not TIMING.fullmatch(timing):
            raise AssertionError(
                f"{label}:{number + 3}: unrecognized TIMING record: {timing!r}"
            )
        n_text, lower, gate = match.groups()
        n = int(n_text)
        if n in result:
            raise AssertionError(f"{label}:{number + 2}: duplicate N={n}")
        expected_tbox = TBOX_EXACT if n <= 728999 else TBOX_INTERVAL
        if tbox != expected_tbox:
            raise AssertionError(
                f"{label}:{number}: wrong TBOX mode for N={n}: {tbox!r}"
            )
        result[n] = (Decimal(lower), int(gate))
    return result


stored: dict[int, tuple[Decimal, int]] = {}
if CERTIFICATES.is_symlink() or not CERTIFICATES.is_dir():
    raise AssertionError("certificates must be a real directory")
for path in sorted(CERTIFICATES.glob("*.log.gz")):
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"stored certificate is not a regular file: {path}")
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        shard = parse_stored(stream, path.name)
    duplicates = set(stored).intersection(shard)
    if duplicates:
        raise AssertionError(
            f"{path.name}: duplicate stored N values: {sorted(duplicates)}"
        )
    stored.update(shard)

with DIRECT_LOG.open(encoding="utf-8") as stream:
    direct_text = stream.read()
direct = parse_direct(direct_text.splitlines(), DIRECT_LOG.name)
if "UNCERT" in direct_text or "FAIL" in direct_text:
    raise AssertionError("direct log contains a failure marker")

expected = {
    690988,
    690995,
    690996,
    691500,
    691501,
    697000,
    697001,
    728999,
    729000,
    818999,
    819000,
    1027999,
    1028000,
    1030000,
    1030001,
    1050000,
    1050001,
    1100000,
    1100001,
    1300000,
    1300001,
    1700000,
    1700001,
    2200000,
    2200001,
    2800000,
    2800001,
    3300000,
    3300001,
    3840000,
}
if set(direct) != expected:
    raise AssertionError(
        f"direct row set mismatch: missing={expected - set(direct)}, "
        f"extra={set(direct) - expected}"
    )

for n in sorted(direct):
    direct_lower, direct_gate = direct[n]
    stored_lower, stored_gate = stored[n]
    if direct_lower < stored_lower:
        raise AssertionError(
            f"N={n}: direct lower {direct_lower} < stored {stored_lower}"
        )
    if direct_gate < stored_gate:
        raise AssertionError(
            f"N={n}: direct gate {direct_gate} < stored {stored_gate}"
        )

if direct[690988] != stored[690988]:
    raise AssertionError("global weakest row was not reproduced exactly")
if direct[3840000][0] != Decimal("0.301900093765"):
    raise AssertionError("unexpected direct finite/tail overlap value")

print(
    "[PASS] 30 direct non-amortized singleton rows dominate the sealed "
    "amortized rows"
)
print("[PASS] global weakest row N=690988 is reproduced exactly")
print(
    "[PASS] finite/tail overlap N=3840000: "
    f"direct={direct[3840000][0]} stored={stored[3840000][0]}"
)
print("RESULT: DIRECT SINGLETON CERTIFICATES PASS")
