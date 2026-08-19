#!/usr/bin/env python3
"""Strictly parse the sealed authoritative FLINT/Arb Prop 4.10 certificates.

The transcripts logs/prop410_arb_256.log and logs/prop410_arb_512.log are
the authoritative machine evidence for Proposition 4.10 (the uniform
finite-region effective-error budget).  This parser rejects a transcript
with a missing, duplicated, reordered, or renamed gate; a malformed or
nonfinite Arb ball; an unexpected or altered exact parameter; insufficient
precision; any FAIL/UNCERT/indeterminate marker; a missing or non-unique
terminal success line; or decisive endpoints that do not establish the
published Proposition 4.10 bounds.  It also binds the sealed Arb source
and PROOF_NOTE.md to the fixed problem statement, so the certificate
cannot silently drift from the documents or fall back to the derived
mpmath cross-check.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
getcontext().prec = 100

BALL_RE = re.compile(
    r"^\[(?P<mid>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?) "
    r"\+/- (?P<rad>(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)\]$",
    re.IGNORECASE,
)

PARAM_LINES = (
    "PARAM t0 = 129/800",
    "PARAM tbox_lo = 161250000/1000000000",
    "PARAM tbox_hi = 161250001/1000000000",
    "PARAM y0^2 = 87677/2500000",
    "PARAM ymax^2 = 271/400",
    "PARAM N0 = 690988",
    "PARAM m0 = 2000",
    "PARAM Tmin = 791366/1000000000000",
    "PARAM budget_Emax = 234/1000000000",
    "PARAM stated_eAB = 206/100000000000000",
    "PARAM stated_eC0 = 233492848188649183/10^24",
    "PARAM stated_Emax = 233494905212337849/10^24",
)

PASS_LINES = (
    "[PASS] exact candidate identity t0+y0^2/2 = 893927/5000000",
    "[PASS] exact t-box: t0 = tbox_lo < tbox_hi <= 1/4",
    "[PASS] exact y0^2 identity 87677/2500000 = 350708/10^7",
    "[PASS] exact floor exceeds coarse budget: 791366/10^12 > 234/10^9",
    "[PASS] domain: 0 < t/(16 N0^2) < 1 and 1 - t/(16 N0^2) > 0",
    "[PASS] domain: x0 > 12, x0 > 6.66, x0 > 6",
    "[PASS] domain: log N0 - log m0 > 0",
    "[PASS] domain: N0 - 1/8 > 0",
    "[PASS] gate G0_positive_part: 8/x0^2 < 3 y0",
    "[PASS] gate sigma1_positive: sigma1 > 0",
    "[PASS] gate Y1_negative: Y1 < 0",
    "[PASS] gate kappa_domain: 0 < kappa < 1",
    "[PASS] gate G2a_ratio: N0^2/(N0^2-t/16) > 1",
    "[PASS] gate U1_log_domain: log(N0^2-t/16) > 2",
    "[PASS] gate U2_logN: log N0 > 1/2",
    "[PASS] gate U3a_tail_decrease: (1+y0)/2 - delta1 > 0",
    "[PASS] gate Y_range (exact): 0 < y0^2 < ymax^2 <= 1",
    "[PASS] gate U3b_first_endpoint: g_t1 < 0",
    "[PASS] gate U3c_second_endpoint: g_t2 < 0",
    "[PASS] gate U5_last_factor (exact): 3/10.50 < 1",
    "[PASS] majorant domain: log n > 0 for all head terms, log m0 > 0",
    "[PASS] majorant domain: tlo > 0 and lower(log0^2) > 0",
    "[PASS] eAB corridor 2.057e-12 < eAB < 2.058e-12",
    "[PASS] eC0 corridor 2.33492848e-7 < eC0 < 2.33492849e-7",
    "[PASS] Emax corridor 2.33494905e-7 < Emax < 2.33494906e-7",
    "[PASS] decisive eAB < 206/10^14",
    "[PASS] decisive eC0 < 233492848188649183/10^24",
    "[PASS] decisive Emax < 233494905212337849/10^24",
    "[PASS] decisive coarse budget Emax < 234/10^9",
    "[PASS] decisive finite margin Tmin - Emax > 0",
    "[PASS] decisive binding floor Tmin - Emax > 557/10^9",
)

STATED_EAB = Decimal("0.00000000000206")
STATED_EC0 = Decimal("0.000000233492848188649183")
STATED_EMAX = Decimal("0.000000233494905212337849")
BUDGET_EMAX = Decimal("0.000000234")
BINDING_FLOOR = Decimal("0.000000557")
TMIN = Decimal("0.000000791366")


def ball(text: str) -> tuple[Decimal, Decimal]:
    match = BALL_RE.fullmatch(text.strip())
    if match is None:
        raise AssertionError(f"malformed Arb ball: {text!r}")
    midpoint = Decimal(match.group("mid"))
    radius = Decimal(match.group("rad"))
    if not (midpoint.is_finite() and radius.is_finite()) or radius < 0:
        raise AssertionError(f"nonfinite or invalid Arb ball: {text!r}")
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


def check_transcript(path: Path, bits: int) -> tuple[Decimal, Decimal]:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{path.name}: not a regular non-symlink file")
    text = path.read_text(encoding="utf-8")
    if (
        "[FAIL]" in text
        or "RESULT: ARB PROP410 CHECK FAILURE" in text
        or "UNCERT" in text
    ):
        raise AssertionError(f"{path.name}: failure marker present")
    if re.search(r"FAILURES: (?!0\b)\d+", text):
        raise AssertionError(f"{path.name}: nonzero failure count")
    if re.search(r"(?i)\b(nan|inf|indet)\b", text):
        raise AssertionError(f"{path.name}: nonfinite or indeterminate token")

    lines = text.splitlines()
    banner = f"Prop410 Arb verifier: precision={bits}, N0=690988, m0=2000"
    if not lines or lines[0] != banner:
        raise AssertionError(f"{path.name}: wrong domain banner")
    if tuple(lines[1 : 1 + len(PARAM_LINES)]) != PARAM_LINES:
        raise AssertionError(f"{path.name}: unexpected exact-parameter block")
    param_count = sum(1 for line in lines if line.startswith("PARAM "))
    if param_count != len(PARAM_LINES):
        raise AssertionError(f"{path.name}: unexpected extra PARAM record")

    passes = tuple(line for line in lines if line.startswith("[PASS]"))
    if passes != PASS_LINES:
        raise AssertionError(
            f"{path.name}: PASS gates missing, duplicated, or reordered"
        )
    if f"TOTAL CHECKS: {len(PASS_LINES)}; FAILURES: 0" not in lines:
        raise AssertionError(f"{path.name}: wrong check total")
    if not text.rstrip().endswith("RESULT: ALL ARB PROP410 CHECKS PASS"):
        raise AssertionError(f"{path.name}: missing unique terminal result")
    if text.count("RESULT:") != 1:
        raise AssertionError(f"{path.name}: non-unique result marker")

    y1 = named_ball(text, "Y1 enclosure")
    g_t1 = named_ball(text, "g_t1 enclosure")
    g_t2 = named_ball(text, "g_t2 enclosure")
    eab = named_ball(text, "eAB upper point")
    ec0 = named_ball(text, "eC0 upper point")
    emax = named_ball(text, "Emax upper point")
    margin = named_ball(text, "Tmin-Emax lower point")

    if not (y1[1] < Decimal("-6.4")):
        raise AssertionError(f"{path.name}: Y1 room gate failed")
    if not (g_t1[1] < 0 and g_t2[1] < 0):
        raise AssertionError(f"{path.name}: endpoint rate gate failed")
    if not (
        0 < eab[1] <= STATED_EAB
        and 0 < ec0[1] <= STATED_EC0
        and 0 < emax[1] <= STATED_EMAX
        and emax[1] < BUDGET_EMAX
        and margin[0] > BINDING_FLOOR
        and emax[1] + margin[0] <= TMIN
    ):
        raise AssertionError(f"{path.name}: decisive directed gate failed")
    print(
        f"[PASS] {path.name}: {len(PASS_LINES)}/{len(PASS_LINES)}, "
        f"Emax<={emax[1]}, margin>{margin[0]}"
    )
    return emax[1], margin[0]


def check_bindings() -> None:
    source = (ROOT / "verifiers" / "verify_prop410_arb.c").read_text(
        encoding="utf-8"
    )
    required_source = (
        "#define N0 690988UL",
        "#define M0 2000",
        "set_q(tlo, 161250000, 1000000000UL);",
        "set_q(thi, 161250001, 1000000000UL);",
        'report("decisive Emax < 233494905212337849/10^24"',
        'report("decisive finite margin Tmin - Emax > 0"',
        "refusing precision below 256 bits",
        "usage: %s precision_bits",
    )
    if any(token not in source for token in required_source):
        raise AssertionError(
            "Arb prop410 source lacks a fixed-domain fail-closed gate"
        )

    note = (ROOT / "PROOF_NOTE.md").read_text(encoding="utf-8")
    required_note = (
        "verify_prop410_arb.c",
        "prop410_arb_256.log",
        "prop410_arb_512.log",
        "same-backend replay",
    )
    if any(token not in note for token in required_note):
        raise AssertionError(
            "PROOF_NOTE.md does not record the authoritative Arb backend"
        )


def main(log_dir: Path) -> None:
    if log_dir.is_symlink() or not log_dir.is_dir():
        raise AssertionError("--log-dir must be a real directory")
    log_dir = log_dir.resolve()

    for bits in (256, 512):
        check_transcript(log_dir / f"prop410_arb_{bits}.log", bits)
    check_bindings()
    print(
        "[PASS] authoritative Arb prop410 source and document bindings hold"
    )
    print("RESULT: SEALED ARB PROP410 CERTIFICATES PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=ROOT / "logs",
        help="directory containing prop410_arb_256.log and prop410_arb_512.log",
    )
    try:
        main(parser.parse_args().log_dir)
    except AssertionError as exc:
        print(f"RESULT FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
