#!/usr/bin/env python3
"""Strict structural checks for stored interval-verifier logs."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"


def read(name):
    text = (LOGS / name).read_text(encoding="utf-8")
    if "FAIL" in text or "UNCERT" in text:
        raise AssertionError(f"{name}: failure marker present")
    return text


for precision in (180, 256):
    name = f"triangle_y_dini_{precision}.log"
    text = read(name)
    required = (
        "patterns=243",
        "patterns=81",
        "patterns=27",
        "patterns=9",
        "ratio_ub=0.99999860767275095",
        "RESULT PASS: direct-Triangle mass is nonincreasing",
    )
    missing = [token for token in required if token not in text]
    if missing:
        raise AssertionError(f"{name}: missing {missing}")
    if text.count("\nPASS P=") != 4:
        raise AssertionError(f"{name}: expected four leg passes")
    print(f"[PASS] {name}: four legs and strict ratio")

for precision in (180, 256):
    name = f"triangle_normalizer_corr_{precision}.log"
    text = read(name)
    required = (
        "Xi",
        "M-P11",
        "M-P7",
        "M-P5",
        "M-P23",
        f"RESULT ALL PASS precision {precision}",
    )
    missing = [token for token in required if token not in text]
    if missing:
        raise AssertionError(f"{name}: missing {missing}")
    print(f"[PASS] {name}: normalizer/correction gates")

head = read("triangle_y_monotonicity_independent_head_120.log")
tail = read("triangle_y_monotonicity_independent_tail_120.log")
if "RESULT ALL PASS" not in head or "RESULT ALL PASS" not in tail:
    raise AssertionError("independent Python monotonicity logs lack PASS")
print("[PASS] independent corrected Python head/tail logs")

cell = read("p11_triangle_tail_cells_independent.log")
if (
    "RESULT ALL PASS" not in cell
    or "932073" not in cell
    or "0.999999303929656" not in cell
):
    raise AssertionError("independent P11 cell log lacks decisive markers")
print("[PASS] independent P11 cell decomposition log")

for precision in (160, 256):
    name = f"tail_1787854_{precision}.log"
    text = read(name)
    required = (
        "TRI178785400SAFE-D upper bound is below one",
        "TRI178785400SAFE-final flow exceeds error",
        "TRI178785400SAFE-hulls contain y0",
        "TOTAL CHECKS RUN: 93",
        "RESULT: ALL PASS",
    )
    missing = [token for token in required if token not in text]
    if missing:
        raise AssertionError(f"{name}: missing {missing}")
    print(f"[PASS] {name}: 93/93 and candidate tail gates")

print("RESULT: STORED INTERVAL LOGS PASS")
