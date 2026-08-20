#!/usr/bin/env python3
"""Bind the supplied exposition draft to its repository cross-check.

This verifier establishes artifact identity and checks that the repository
evidence cited by the cross-check still contains the controlling directed
values. It does not validate the exposition's mathematics or upgrade the
candidate's review status.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "paper" / "external" / "gomila-proof-exposition.pdf"
CROSSCHECK = ROOT / "paper" / "external" / "README.md"

EXPECTED_SHA256 = (
    "fd98f4e91dea6c02c7705665aaa95d0cb0b0cf46f8a22276e2c693a56a489313"
)
EXPECTED_SIZE = 442_088
BASELINE_TAG = "review-01787854-v3"
BASELINE_COMMIT = "2e9976c4becbf97e31c56fe75fce07cdff5dd4ea"

checks = 0
failures = 0


def check(label: str, condition: bool) -> None:
    global checks, failures
    checks += 1
    if condition:
        print(f"[PASS] {label}")
    else:
        failures += 1
        print(f"[FAIL] {label}", file=sys.stderr)


def contains(path: Path, fragment: str) -> bool:
    return fragment in path.read_text(encoding="utf-8")


def main() -> int:
    check("external exposition PDF exists", PDF.is_file() and not PDF.is_symlink())
    if not PDF.is_file():
        return 1

    payload = PDF.read_bytes()
    check("external exposition exact byte size", len(payload) == EXPECTED_SIZE)
    check(
        "external exposition exact SHA-256",
        hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256,
    )
    check("external exposition is the expected PDF generation", payload.startswith(b"%PDF-1.5"))

    check("cross-check exists", CROSSCHECK.is_file() and not CROSSCHECK.is_symlink())
    if not CROSSCHECK.is_file():
        return 1

    crosscheck = CROSSCHECK.read_text(encoding="utf-8")
    normalized_crosscheck = crosscheck.replace(" ", "")
    for label, fragment in (
        ("cross-check binds PDF SHA-256", EXPECTED_SHA256),
        ("cross-check binds baseline tag", BASELINE_TAG),
        ("cross-check binds baseline commit", BASELINE_COMMIT),
        ("cross-check records sealed P7 floor", "0.000315112459"),
        ("cross-check records sealed P5 floor", "0.000305788807"),
        ("cross-check records tail lower direction", "0.000279<1-D<0.000281"),
        (
            "cross-check preserves proof status",
            "computer-assisted unconditional proof, not yet peer reviewed",
        ),
    ):
        check(label, fragment.replace(" ", "") in normalized_crosscheck)

    finite_log = ROOT / "logs" / "finite_and_binding.log"
    check(
        "sealed finite log retains P7 floor",
        contains(finite_log, "minimum=0.000315112459@729000"),
    )
    check(
        "sealed finite log retains P5 floor",
        contains(finite_log, "minimum=0.000305788807@819000"),
    )

    for precision in (256, 512):
        tail_log = ROOT / "logs" / f"tail_arb_{precision}.log"
        check(
            f"{precision}-bit tail log retains cap admissibility",
            contains(tail_log, "[PASS] SC1:")
            and contains(tail_log, "[PASS] SC2:"),
        )
        check(
            f"{precision}-bit tail log retains two-sided D corridor",
            contains(tail_log, "[PASS] D corridor 0.999719 < D < 0.999721"),
        )
        check(
            f"{precision}-bit tail log retains positive normalized margin",
            contains(tail_log, "[PASS] decisive normalized margin flow > error > 0"),
        )

    print(f"TOTAL CHECKS RUN: {checks}")
    if failures:
        print(f"RESULT: EXTERNAL EXPOSITION CROSS-CHECK FAIL ({failures} failures)")
        return 1

    print("RESULT: EXTERNAL EXPOSITION INTEGRITY AND CROSS-CHECK PASS")
    print(
        "STATUS: supplied draft with required corrections; "
        "not an external acceptance report."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
