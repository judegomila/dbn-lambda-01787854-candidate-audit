#!/usr/bin/env python3
"""Fail-closed parser for the coupled scalar obstruction logs."""
from __future__ import annotations
import argparse
import pathlib
import re
import sys

REQUIRED = [
    "[PASS] exact target identity and containment in existing barrier time",
    "[PASS] two-ladder center lower bound 1-G is positive",
    "[PASS] current scalar gate is rigorously impossible at this cutoff/head",
    "[PASS] the sufficient nonvanishing gate does not pass",
    "RESULT: CERTIFIED SCALAR OBSTRUCTION FOR 0.14 PHASE-FREEZE LANE",
]

def parse_ball(text: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)} = (.+)$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing ball: {label}")
    return match.group(1).strip()

def check(path: pathlib.Path) -> None:
    text = path.read_text(encoding="utf-8")
    for item in REQUIRED:
        if text.count(item) != 1:
            raise ValueError(f"{path}: required marker count != 1: {item!r}")
    match = re.search(r"TOTAL CHECKS: (\d+); FAILURES: (\d+)", text)
    if not match or int(match.group(1)) < 9 or int(match.group(2)) != 0:
        raise ValueError(f"{path}: malformed or failing check total")
    for label in ["center 1-G lower point", "residual majorant", "residual lower point"]:
        parse_ball(text, label)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--log-dir", type=pathlib.Path, required=True)
    args = p.parse_args()
    logs = [args.log_dir / "coupled_scalar_256.log", args.log_dir / "coupled_scalar_512.log"]
    for log in logs:
        check(log)
        print(f"[PASS] parsed {log}")
    # Rejection at 255 bits is part of the certificate interface.
    reject = (args.log_dir / "coupled_scalar_reject_255.log").read_text(encoding="utf-8")
    if "refusing precision below 256 bits" not in reject:
        raise ValueError("missing precision rejection")
    print("RESULT: COUPLED SCALAR LOG BINDING PASS")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
