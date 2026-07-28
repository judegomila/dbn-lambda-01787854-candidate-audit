#!/usr/bin/env python3
"""Strictly parse the sealed Arb Dini y-transfer certificates.

Hypothesis (ii) of Polymath Theorem 1.2 needs the numerator y-transfer
`Num_N(y) >= Num_N(y0)` on the final-time right half-line.  Its worst
certified upper ratio is `ratio_ub` per Euler-prime leg; the direct
Triangle mass is nonincreasing in y iff every such ratio is strictly < 1.

This auditor is dependency-free (stdlib only): it re-derives the decisive
gate from the SEALED logs, exactly like verify_tail_arb_logs.py audits the
sealed FLINT/Arb tail certificates.  It never links FLINT/Arb itself.
"""

import argparse
from decimal import Decimal, getcontext
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
getcontext().prec = 100

# Bit-identical worst upper ratio in BOTH precisions (180 and 256), from the
# P=235711 leg N=690988..728999.  slack = 1 - worst ~ 1.39232724905e-6.
EXPECTED_WORST = Decimal("0.99999860767275095")
EXPECTED_SLACK = Decimal(1) - EXPECTED_WORST

BANNER = (
    "ROW t=16125/100000 y2=350708/10000000 "
    "ybox=[0.187271994702891,0.823103881657717] "
    "sigma_prime>=1/2 gamma_log_prime<0"
)
SENTINEL = (
    "RESULT PASS: direct-Triangle mass is nonincreasing "
    "on the full y interval"
)
EXPECTED_LEGS = (
    "N=690988..728999",
    "N=729000..818999",
    "N=819000..1027999",
    "N=1028000..3840000",
)

RATIO_RE = re.compile(r"ratio_ub=([-+0-9.eE]+)")


def audit_log(path: Path, bits: int) -> Decimal:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{path.name}: not a regular non-symlink file")
    text = path.read_text(encoding="utf-8")

    if (
        "UNCERT" in text
        or "RESULT FAIL" in text
        or any(
            line.startswith("FAIL") for line in text.splitlines()
        )
    ):
        raise AssertionError(f"{path.name}: failure marker present")
    if not text.startswith(BANNER + "\n"):
        raise AssertionError(f"{path.name}: wrong fixed-domain banner")

    pass_rows = [
        line for line in text.splitlines() if line.startswith("PASS P=")
    ]
    if len(pass_rows) != 4:
        raise AssertionError(
            f"{path.name}: expected exactly 4 leg gates, found {len(pass_rows)}"
        )
    for leg in EXPECTED_LEGS:
        if text.count(leg) != 1:
            raise AssertionError(f"{path.name}: missing/duplicate leg {leg}")

    ratios = []
    for row in pass_rows:
        match = RATIO_RE.search(row)
        if match is None:
            raise AssertionError(f"{path.name}: malformed row, no ratio_ub")
        value = Decimal(match.group(1))
        if not (0 < value < 1):
            raise AssertionError(
                f"{path.name}: ratio_ub {value} not strictly in (0,1)"
            )
        ratios.append(value)

    worst = max(ratios)
    if worst != EXPECTED_WORST:
        raise AssertionError(
            f"{path.name}: worst ratio {worst} != expected {EXPECTED_WORST}"
        )
    slack = Decimal(1) - worst
    if slack != EXPECTED_SLACK:
        raise AssertionError(f"{path.name}: slack {slack} != {EXPECTED_SLACK}")
    if not (Decimal("1.39e-6") < slack < Decimal("1.40e-6")):
        raise AssertionError(f"{path.name}: slack {slack} outside expected band")

    if text.count(SENTINEL) != 1:
        raise AssertionError(f"{path.name}: non-unique success sentinel")
    if not text.rstrip().endswith(SENTINEL):
        raise AssertionError(f"{path.name}: missing terminal success sentinel")

    print(
        f"[PASS] {path.name}: 4/4 legs, worst ratio {worst} < 1, "
        f"slack {slack}"
    )
    return worst


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--log-dir",
    type=Path,
    default=ROOT / "logs",
    help="directory containing triangle_y_dini_180.log and _256.log",
)
arguments = parser.parse_args()
if arguments.log_dir.is_symlink() or not arguments.log_dir.is_dir():
    raise AssertionError("--log-dir must be a real directory")
log_dir = arguments.log_dir.resolve()

worsts = {}
for bits in (180, 256):
    worsts[bits] = audit_log(log_dir / f"triangle_y_dini_{bits}.log", bits)

if worsts[180] != worsts[256] or worsts[180] != EXPECTED_WORST:
    raise AssertionError("precisions disagree on the worst Dini ratio")
print(
    f"[PASS] 180-bit and 256-bit precisions agree: worst ratio "
    f"{EXPECTED_WORST} < 1 (slack {EXPECTED_SLACK})"
)

source = (ROOT / "verifiers" / "verify_triangle_y_dini_arb.c").read_text(
    encoding="utf-8"
)
required_source = (
    "h_nonpositive=%lu ratio_ub=%.17g ",
    'ok &= audit_leg(5, 690988, 728999, t);',
    'ok &= audit_leg(2, 1028000, 3840000, t);',
    "RESULT PASS: direct-Triangle mass is nonincreasing ",
)
if any(token not in source for token in required_source):
    raise AssertionError("Arb Dini source lacks a fixed-domain fail-closed gate")
print("[PASS] fixed-domain Arb Dini source is present")
print("RESULT: SEALED TRIANGLE Y-DINI CERTIFICATES PASS")
