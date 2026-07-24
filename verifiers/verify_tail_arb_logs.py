#!/usr/bin/env python3
"""Strictly parse the sealed standalone FLINT/Arb tail certificates."""

import argparse
from decimal import Decimal, getcontext
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
getcontext().prec = 100

BALL_RE = re.compile(
    r"^\[(?P<mid>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?) "
    r"\+/- (?P<rad>(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)\]$",
    re.IGNORECASE,
)


def ball(text: str) -> tuple[Decimal, Decimal]:
    match = BALL_RE.fullmatch(text.strip())
    if match is None:
        raise AssertionError(f"malformed Arb ball: {text!r}")
    midpoint = Decimal(match.group("mid"))
    radius = Decimal(match.group("rad"))
    return midpoint - radius, midpoint + radius


def named_ball(text: str, label: str) -> tuple[Decimal, Decimal]:
    matches = re.findall(
        rf"^{re.escape(label)} = (.+)$", text, re.MULTILINE
    )
    if len(matches) != 1:
        raise AssertionError(
            f"{label!r}: expected one record, found {len(matches)}"
        )
    return ball(matches[0])


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--log-dir",
    type=Path,
    default=ROOT / "logs",
    help="directory containing tail_arb_256.log and tail_arb_512.log",
)
arguments = parser.parse_args()
if arguments.log_dir.is_symlink() or not arguments.log_dir.is_dir():
    raise AssertionError("--log-dir must be a real directory")
log_dir = arguments.log_dir.resolve()

for bits in (256, 512):
    path = log_dir / f"tail_arb_{bits}.log"
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{path.name}: not a regular non-symlink file")
    text = path.read_text(encoding="utf-8")
    if (
        "[FAIL]" in text
        or "RESULT: ARB TAIL CHECK FAILURE" in text
        or "UNCERT" in text
    ):
        raise AssertionError(f"{path.name}: failure marker present")
    if not text.startswith(
        f"P1113 Arb verifier: precision={bits}, "
        "N1=3840000, M=153814\n"
    ):
        raise AssertionError(f"{path.name}: wrong domain banner")
    if text.count("[PASS]") != 36:
        raise AssertionError(f"{path.name}: expected exactly 36 PASS gates")
    if "TOTAL CHECKS: 36; FAILURES: 0" not in text:
        raise AssertionError(f"{path.name}: wrong check total")
    if not text.rstrip().endswith("RESULT: ALL ARB TAIL CHECKS PASS"):
        raise AssertionError(f"{path.name}: missing unique terminal result")
    if text.count("RESULT:") != 1:
        raise AssertionError(f"{path.name}: non-unique result marker")

    contraction = named_ball(text, "D upper point")
    flow = named_ball(text, "flow lower point")
    error = named_ball(text, "error upper point")
    margin = named_ball(text, "flow-error lower point")
    width = named_ball(text, "P enclosure width")

    if not (
        Decimal("0.999719") < contraction[0] <= contraction[1] < 1
    ):
        raise AssertionError(f"{path.name}: contraction gate failed")
    if not (
        Decimal("0.0001735") < flow[0]
        and error[1] < Decimal("0.000000011672")
        and flow[0] > error[1] > 0
        and margin[0] > Decimal("0.00017352")
        and width[1] < 1 - contraction[1]
    ):
        raise AssertionError(f"{path.name}: decisive directed gate failed")
    print(
        f"[PASS] {path.name}: 36/36, D<1, flow>error, "
        f"margin>{margin[0]}"
    )

note = (ROOT / "TAIL_LEMMA.md").read_text(encoding="utf-8")
source = (ROOT / "verifiers" / "verify_tail_arb.c").read_text(
    encoding="utf-8"
)
required_note = (
    "Tail theorem.",
    "For every",
    "N\\ge N_*",
    "No sampling in \\(N\\) is involved.",
    "Theorem 1.3 then yields",
)
if any(token not in note for token in required_note):
    raise AssertionError("TAIL_LEMMA.md lacks a quantified proof obligation")
required_source = (
    "#define MHEAD 153814",
    "#define MERR 3000",
    "#define N1 3840000UL",
    'report("decisive contraction D < 1"',
    'report("decisive normalized margin flow > error > 0"',
)
if any(token not in source for token in required_source):
    raise AssertionError("Arb source lacks a fixed-domain fail-closed gate")
print("[PASS] standalone tail lemma and fixed-domain Arb source are present")
print("RESULT: SEALED INDEPENDENT ARB TAIL CERTIFICATES PASS")
