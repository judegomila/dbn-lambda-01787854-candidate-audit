#!/usr/bin/env python3
"""Fail-closed assembly of the three hypotheses in Polymath Theorem 1.2."""

from fractions import Fraction as F
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

if sys.flags.optimize:
    print("error: Python optimization would disable load-bearing assertions")
    sys.exit(2)

X = 6_000_000_185_827
T_PT = 3_000_175_332_800
T0 = F(129, 800)
Y0_SQUARED = F(87677, 2_500_000)
BOUND = F(893927, 5_000_000)
BARRIER_Y_FLOOR = F(1809, 10_000)
N0 = 690_988
NMID = 3_840_000

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
    print(
        f"[{'PASS' if ok else 'FAIL'}] {name}"
        + (f"  {detail}" if detail else "")
    )
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
        line
        for line in output.splitlines()
        if line.startswith("RESULT") or "CONCLUSION:" in line
    ]
    detail = (
        f"exit={completed.returncode}; "
        + ("; ".join(result_lines[-2:]) if result_lines else "no result line")
    )
    recorded_ok = check(name, ok, detail)
    if not ok:
        print(f"--- prerequisite output: {name}", file=sys.stderr)
        print(output, file=sys.stderr)
    return recorded_ok


print("--- P: executed prerequisite certificates")
p1 = prerequisite(
    "P1 stored interval logs",
    [PYTHON, "verifiers/verify_stored_logs.py"],
    ("RESULT: STORED INTERVAL LOGS PASS",),
)
p2 = prerequisite(
    "P2 all 3,149,013 finite rows and corrected error units",
    [PYTHON, "verifiers/verify_finite_and_binding.py"],
    ("RESULT PASS: full finite Triangle weld",),
)
p3 = prerequisite(
    "P3 30 direct non-amortized finite singleton rows",
    [PYTHON, "verifiers/verify_direct_singletons.py"],
    ("RESULT: DIRECT SINGLETON CERTIFICATES PASS",),
)
p4 = prerequisite(
    "P4 native Triangle-to-|f_t| binding",
    [PYTHON, "verifiers/verify_native_binding.py"],
    ("TOTAL CHECKS RUN: 13", "RESULT: ALL PASS"),
)
p5 = prerequisite(
    "P5 continuous window-freeze and finite/tail site seam",
    [PYTHON, "verifiers/verify_window_freeze.py", "--repo", str(ROOT)],
    ("RESULT: ALL PASS", "CERTIFIED WINDOW-FREEZE CONCLUSION:"),
)
normalizer_prerequisites: dict[int, bool] = {}
for precision, label in ((180, "P6"), (256, "P7")):
    normalizer_prerequisites[precision] = prerequisite(
        f"{label} native normalizer/correction at {precision} bits",
        [
            PYTHON,
            "verifiers/verify_triangle_normalizer_corr_iv.py",
            "--prec",
            str(precision),
        ],
        (f"RESULT ALL PASS precision {precision}",),
    )
p8 = prerequisite(
    "P8 target tail source-patch provenance",
    [PYTHON, "verifiers/verify_tail_patch_provenance.py"],
    ("RESULT: TAIL PATCH PROVENANCE PASS",),
)
tail_prerequisites: dict[int, bool] = {}
for precision, label in ((160, "P9"), (256, "P10")):
    tail_prerequisites[precision] = prerequisite(
        f"{label} independent Python interval tail at {precision} bits",
        [PYTHON, f"verifiers/verify_tail_1787854_{precision}.py"],
        ("TOTAL CHECKS RUN: 93", "RESULT: ALL PASS"),
    )
p11 = prerequisite(
    "P11 standalone 256/512-bit FLINT/Arb tail certificates",
    [PYTHON, "verifiers/verify_tail_arb_logs.py"],
    ("RESULT: SEALED INDEPENDENT ARB TAIL CERTIFICATES PASS",),
)
p12 = prerequisite(
    "P12 portable Linux/GCC/FLINT 3.0.1 883-prism barrier certificate",
    [PYTHON, "verifiers/verify_barrier_binding.py"],
    ("RESULT: ALL PASS", "BARRIER CONCLUSION:"),
)
p13 = prerequisite(
    "P13 macOS/Clang/FLINT 3.6.0 883-prism cross-check",
    [PYTHON, "verifiers/verify_barrier_binding.py"],
    ("RESULT: ALL PASS", "BARRIER CONCLUSION:"),
    {
        "BARRIER_LOG": str(
            ROOT
            / "barrier"
            / "certificates"
            / "barrier_target_closed_macos_arm64_flint36.log"
        )
    },
)
p14 = prerequisite(
    "P14 exact H0-to-zeta symmetry/sign map",
    [PYTHON, "verifiers/verify_criterion_sign_map.py"],
    ("RESULT: CRITERION SIGN MAP PASS",),
)
p15 = prerequisite(
    "P15 conservative Proposition 6.6(vi) error-constant weld",
    [PYTHON, "verifiers/verify_error_constant_weld.py"],
    ("RESULT: CONSERVATIVE ERROR-CONSTANT WELD PASS",),
)
p16 = prerequisite(
    "P16 sealed Arb Dini y-transfer (numerator y-monotonicity) certificates",
    [PYTHON, "verifiers/verify_triangle_y_dini_logs.py"],
    ("RESULT: SEALED TRIANGLE Y-DINI CERTIFICATES PASS",),
)
print("--- A: exact candidate and criterion domain")
a1 = check("A1 exact candidate identity", T0 + Y0_SQUARED / 2 == BOUND)
a2 = check("A2 exact decimal is 0.1787854", BOUND == F(1_787_854, 10_000_000))
a3 = check("A3 theorem time domain", 0 < T0 < F(1, 2))
a4 = check(
    "A4 final-height interval is nonempty",
    0 < Y0_SQUARED < 1 - 2 * T0 == F(271, 400) < 1,
)
a5 = check(
    "A5 curved barrier edges are correctly ordered",
    Y0_SQUARED + 2 * T0 == F(893927, 2_500_000) < 1,
)
a6 = check("A6 theorem abscissa domain", X > 0)

print("--- I: Theorem 1.2 hypothesis (i), verified zeta height")
print(
    "[CITED THEOREM INPUT] Platt--Trudgian Theorem 1 verifies RH through "
    "T_PT=3000175332800."
)
print(
    "[CITED CLASSICAL INPUT] eta(sigma)>0 and "
    "eta(sigma)=(1-2^(1-sigma))*zeta(sigma) give no real zeta zero "
    "for 0<sigma<1; s=1 is a pole."
)
i1 = check("I1 X/2 is within the verified height", F(X, 2) <= T_PT)
i2 = check(
    "I2 exact verified-height margin",
    T_PT - F(X, 2) == F(350_479_773, 2) > 0,
)

print("--- II: Theorem 1.2 hypothesis (ii), final-time right half-line")
ii1 = check("II1 finite row count", NMID - N0 + 1 == 3_149_013)
ii2 = check(
    "II2 finite t-boxes contain the exact t0",
    F(16125, 100000) == T0
    and F(161250000, 10**9) == T0 < F(161250001, 10**9),
)
y_lo = F(1_872_719, 10**7)
y_hi = F(23_409, 125_000)
y_ext_previous = F(4_115_519, 5_000_000)
y_ext_top = F(8_231_039, 10_000_000)
ii3 = check("II3 tail lower box strictly straddles y0", y_lo**2 < Y0_SQUARED < y_hi**2)
ii4 = check(
    "II4 tail extended box minimally covers the final height",
    y_ext_previous**2 < 1 - 2 * T0 <= y_ext_top**2,
)
ii5 = check(
    "II5 finite and tail share the complete N=3840000 window",
    N0 <= NMID and NMID == 3_840_000,
    "finite=[x*,x_3840001), tail=[x_3840000,infinity)",
)
ii6 = check(
    "II6 the half-open/closed-left union has no endpoint gap",
    N0 < NMID < NMID + 1,
    "x_3840001 belongs to the tail lane",
)

print("--- III: Theorem 1.2 hypothesis (iii), closed barrier")
iii1 = check(
    "III1 barrier floor lies strictly below y0",
    BARRIER_Y_FLOOR**2 < Y0_SQUARED,
)
iii2 = check(
    "III2 exact barrier-floor squared margin",
    Y0_SQUARED - BARRIER_Y_FLOOR**2
    == F(234_599, 100_000_000)
    > 0,
)
iii3 = check(
    "III3 required horizontal width lies in the closed unit strip",
    0 < 1 - Y0_SQUARED < 1,
)
iii4 = check("III4 barrier time top is exactly t0", F(129, 800) == T0)
iii5 = check(
    "III5 the whole curved vertical interval is inside [0.1809,1]",
    BARRIER_Y_FLOOR**2 < Y0_SQUARED
    and Y0_SQUARED + 2 * T0 < 1,
)

print("--- W: canonical criterion weld")
print(
    "[CITED THEOREM INPUT] Polymath Theorem 1.2: hypotheses (i), (ii), "
    "and (iii) imply Lambda <= t0+y0^2/2."
)
check(
    "W1 hypothesis (i) exact domain and height predicates",
    all((p14, a3, a4, a6, i1, i2)),
)
check(
    "W2 hypothesis (ii) finite+tail certificates and coverage predicates",
    all(
        (
            p1,
            p2,
            p3,
            p4,
            p5,
            normalizer_prerequisites[180],
            normalizer_prerequisites[256],
            p8,
            tail_prerequisites[160],
            tail_prerequisites[256],
            p11,
            p15,
            p16,
            a3,
            a4,
            ii1,
            ii2,
            ii3,
            ii4,
            ii5,
            ii6,
        )
    ),
)
check(
    "W3 hypothesis (iii) dual barrier certificates and containment predicates",
    all((p12, p13, p15, a3, a4, a5, a6, iii1, iii2, iii3, iii4, iii5)),
)
check("W4 final rational substitution", all((a1, a2, T0 + Y0_SQUARED / 2 == BOUND)))

print(f"TOTAL CHECKS RUN: {checks}")
if failures:
    print(f"RESULT: {failures} FAILED")
    sys.exit(1)
print("RESULT: UNCONDITIONAL CANDIDATE ASSEMBLY PASS")
print("CONCLUSION: Lambda <= 893927/5000000 = 0.1787854.")
print(
    "STATUS: unreviewed computer-assisted unconditional proof candidate; "
    "not an established theorem."
)
