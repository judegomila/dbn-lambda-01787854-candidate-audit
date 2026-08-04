#!/usr/bin/env python3
"""Fail-closed assembly audit for the exploratory 0.1782354 row."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

if sys.flags.optimize:
    raise SystemExit(
        "error: Python optimization would disable load-bearing assertions"
    )

X = 6_000_000_185_827
T_PT = 3_000_175_332_800
T0 = F(1607, 10_000)
Y0_SQUARED = F(87_677, 2_500_000)
YMAX_SQUARED = F(3393, 5000)
BOUND = F(891_177, 5_000_000)
BARRIER_TOP = F(129, 800)
BARRIER_Y_FLOOR = F(1809, 10_000)
N0 = 690_988
NMID = 4_050_000

checks = 0
failures = 0

BARRIER_ENVIRONMENT_KEYS = (
    "BARRIER_SOURCE",
    "BARRIER_LOG",
    "BARRIER_TAIL_LOG",
    "BARRIER_PROVENANCE_LOG",
    "BARRIER_REGENERATED",
    "BARRIER_UNIFORM_ERROR_LOG",
)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    suffix = f"  {detail}" if detail else ""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")
    return ok


def prerequisite(
    name: str,
    command: list[str],
    sentinels: tuple[str, ...],
    extra_environment: dict[str, str] | None = None,
) -> bool:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for variable in ("PYTHONOPTIMIZE", "PYTHONPATH", "PYTHONHOME"):
        environment.pop(variable, None)
    for variable in BARRIER_ENVIRONMENT_KEYS:
        environment.pop(variable, None)
    if extra_environment:
        environment.update(extra_environment)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    ok = completed.returncode == 0 and all(
        output.count(sentinel) >= 1 for sentinel in sentinels
    )
    result_lines = [
        line for line in output.splitlines()
        if line.startswith("RESULT") or "CONCLUSION:" in line
    ]
    detail = (
        f"exit={completed.returncode}; "
        + ("; ".join(result_lines[-2:]) if result_lines else "no result line")
    )
    recorded = check(name, ok, detail)
    if not ok:
        print(f"--- prerequisite output: {name}", file=sys.stderr)
        print(output, file=sys.stderr)
    return recorded


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("finite_logs", type=Path)
    parser.add_argument("direct_log", type=Path)
    args = parser.parse_args()
    finite_logs = args.finite_logs.resolve()
    direct_log = args.direct_log.resolve()

    print("--- P: executed prerequisite certificates")
    p_finite = prerequisite(
        "P1 all 3,359,013 lower-time finite rows",
        [PYTHON, "verifiers/verify_finite_01782354.py", str(finite_logs)],
        ("RESULT PASS: full finite Triangle weld",),
    )
    p_direct = prerequisite(
        "P2 direct singleton seam audit",
        [
            PYTHON,
            "verifiers/verify_direct_singletons_01782354.py",
            str(direct_log),
            str(finite_logs),
        ],
        ("RESULT: LOWER-TIME DIRECT SINGLETON CERTIFICATES PASS",),
    )
    p_native = prerequisite(
        "P3 native P13 Triangle-to-|f_t| binding",
        [PYTHON, "verifiers/verify_native_binding_01782354.py"],
        ("TOTAL CHECKS RUN: 15", "RESULT: ALL PASS"),
    )
    p_window = prerequisite(
        "P4 continuous lower-time window freeze and tail seam",
        [
            PYTHON,
            "verifiers/verify_window_freeze_01782354.py",
            "--repo",
            str(ROOT),
        ],
        ("TOTAL CHECKS RUN: 46", "CERTIFIED WINDOW-FREEZE CONCLUSION:"),
    )
    p_normalizer = {}
    for precision in (180, 256):
        p_normalizer[precision] = prerequisite(
            f"P5 native normalizer/correction at {precision} bits",
            [
                PYTHON,
                "verifiers/verify_triangle_normalizer_corr_01782354.py",
                "--prec",
                str(precision),
            ],
            (f"RESULT ALL PASS precision {precision}",),
        )
    p_dini = prerequisite(
        "P6 five-leg direct upper-Dini certificate at 256 bits",
        [str(ROOT / "scripts" / "run_triangle_y_dini_p13.sh"), "256"],
        (
            "LEG P13 N=690988..728999",
            "LEG P11 N=729000..774999",
            "LEG P7 N=775000..849999",
            "LEG P5 N=850000..1074999",
            "LEG P23 N=1075000..4050000",
            "RESULT PASS: exact lower-time five-leg Triangle y-Dini schedule",
        ),
    )
    with tempfile.TemporaryDirectory(prefix="tail_01782354_assembly_") as tmp:
        tail_output = Path(tmp) / "replay"
        p_tail = prerequisite(
            "P7 standalone 256/512-bit lower-time Arb tail",
            [
                str(ROOT / "scripts" / "run_tail_01782354_arb.sh"),
                str(tail_output),
            ],
            ("RESULT: LOWER-TIME INDEPENDENT ARB TAIL REPLAY PASS",),
        )
    p_barrier_linux = prerequisite(
        "P8 stronger Linux 883-prism barrier certificate",
        [PYTHON, "verifiers/verify_barrier_binding.py"],
        ("RESULT: ALL PASS", "BARRIER CONCLUSION:"),
    )
    p_barrier_macos = prerequisite(
        "P9 stronger macOS 883-prism barrier cross-check",
        [PYTHON, "verifiers/verify_barrier_binding.py"],
        ("RESULT: ALL PASS", "BARRIER CONCLUSION:"),
        {
            "BARRIER_LOG": str(
                ROOT / "barrier" / "certificates"
                / "barrier_target_closed_macos_arm64_flint36.log"
            )
        },
    )
    p_sign = prerequisite(
        "P10 exact H0-to-zeta symmetry/sign map",
        [PYTHON, "verifiers/verify_criterion_sign_map.py"],
        ("RESULT: CRITERION SIGN MAP PASS",),
    )

    print("--- A: exact candidate and criterion domain")
    a1 = check("A1 exact candidate identity", T0 + Y0_SQUARED / 2 == BOUND)
    a2 = check("A2 exact decimal", BOUND == F(1_782_354, 10_000_000))
    a3 = check("A3 theorem time domain", 0 < T0 < F(1, 2))
    a4 = check(
        "A4 final-height interval",
        0 < Y0_SQUARED < 1 - 2 * T0 == YMAX_SQUARED < 1,
    )
    a5 = check(
        "A5 curved canopy",
        Y0_SQUARED + 2 * T0 == F(891_177, 2_500_000) < 1,
    )
    a6 = check("A6 theorem abscissa domain", X > 0)

    print("--- I: Theorem 1.2 hypothesis (i)")
    print(
        "[CITED THEOREM INPUT] Platt--Trudgian verifies RH through "
        "T_PT=3000175332800."
    )
    i1 = check("I1 X/2 is within verified height", F(X, 2) <= T_PT)
    i2 = check(
        "I2 exact verified-height margin",
        T_PT - F(X, 2) == F(350_479_773, 2) > 0,
    )

    print("--- II: hypothesis (ii), final-time right half-line")
    ii1 = check("II1 finite row count", NMID - N0 + 1 == 3_359_013)
    y_lo = F(1_872_719, 10**7)
    y_hi = F(23_409, 125_000)
    y_ext_previous = F(8_237_718, 10_000_000)
    y_ext_top = F(8_237_719, 10_000_000)
    ii2 = check("II2 tail lower box straddles y0", y_lo**2 < Y0_SQUARED < y_hi**2)
    ii3 = check(
        "II3 tail extended box minimally covers final height",
        y_ext_previous**2 < YMAX_SQUARED <= y_ext_top**2,
    )
    ii4 = check(
        "II4 finite and tail overlap at N=4050000",
        NMID == 4_050_000,
        "finite=[x*,x_4050001), tail=[x_4050000,infinity)",
    )

    print("--- III: hypothesis (iii), inherited closed barrier")
    iii1 = check(
        "III1 barrier floor lies below y0",
        BARRIER_Y_FLOOR**2 < Y0_SQUARED,
    )
    iii2 = check(
        "III2 exact barrier-floor margin",
        Y0_SQUARED - BARRIER_Y_FLOOR**2
        == F(234_599, 100_000_000) > 0,
    )
    iii3 = check("III3 new time lies in stronger barrier", T0 < BARRIER_TOP)
    iii4 = check(
        "III4 new curved barrier is a strict subset",
        Y0_SQUARED + 2 * T0 < Y0_SQUARED + 2 * BARRIER_TOP < 1,
    )

    print("--- W: canonical criterion weld")
    w1 = check("W1 hypothesis (i)", all((p_sign, a3, a4, a6, i1, i2)))
    w2 = check(
        "W2 hypothesis (ii)",
        all((
            p_finite, p_direct, p_native, p_window,
            p_normalizer[180], p_normalizer[256], p_dini, p_tail,
            a3, a4, ii1, ii2, ii3, ii4,
        )),
    )
    w3 = check(
        "W3 hypothesis (iii)",
        all((
            p_barrier_linux, p_barrier_macos,
            a3, a4, a5, a6, iii1, iii2, iii3, iii4,
        )),
    )
    check("W4 final rational substitution", all((w1, w2, w3, a1, a2)))

    print(f"TOTAL CHECKS RUN: {checks}")
    if failures:
        print(f"RESULT: {failures} FAILED")
        raise SystemExit(1)
    print("RESULT: LOWER-TIME UNCONDITIONAL CANDIDATE ASSEMBLY PASS")
    print("CONCLUSION: Lambda <= 891177/5000000 = 0.1782354.")
    print(
        "STATUS: unreviewed computer-assisted proof candidate; "
        "not an established theorem."
    )


if __name__ == "__main__":
    main()
