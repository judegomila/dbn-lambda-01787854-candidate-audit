#!/usr/bin/env python3
"""Verify the closed barrier certificate's analytic and stored interfaces.

The C replay is the primary interval certificate.  This script independently
checks:

* exact containment of the curved criterion barrier in the certified box;
* constancy of the Riemann--Siegel window index;
* a coarse uniform bound for equations (23)--(24) of Theorem 1.3;
* the fail-closed structural contract of the C verifier; and
* continuity, margins, and completion markers in the sealed prism log.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction as F
import os
from pathlib import Path
import re
import sys

from mpmath import iv, mp


iv.prec = 256
mp.prec = 256
getcontext().prec = 100

ROOT = Path(__file__).resolve().parent.parent


def selected_path(variable: str, default: Path) -> Path:
    return Path(os.environ.get(variable, str(default))).resolve()


SOURCE = selected_path(
    "BARRIER_SOURCE",
    ROOT / "barrier" / "src" / "TloopSinglemat_closed_cert.c",
)
LOG = selected_path(
    "BARRIER_LOG",
    ROOT / "barrier" / "certificates" / "barrier_target_closed.log",
)
TAIL_LOG = selected_path(
    "BARRIER_TAIL_LOG",
    ROOT / "barrier" / "certificates" / "storedsum_taylor_tail.log",
)
PROVENANCE_LOG = selected_path(
    "BARRIER_PROVENANCE_LOG",
    ROOT / "barrier" / "certificates" / "storedsum_provenance.log",
)
REGENERATED = selected_path(
    "BARRIER_REGENERATED",
    ROOT
    / "barrier"
    / "certificates"
    / "storedsum_interval_regenerated.txt",
)
UNIFORM_ERROR_LOG = selected_path(
    "BARRIER_UNIFORM_ERROR_LOG",
    ROOT / "barrier" / "certificates" / "uniform_error_256.log",
)
DERIVATIVE_NOTE = ROOT / "DERIVATIVE_BOX_LEMMA.md"

X = 6_000_000_185_827
T0 = F(129, 800)
Y0_SQUARED = F(87677, 2_500_000)
SLAB_T = F(129, 800)
SLAB_Y = F(1809, 10_000)
N0 = 690_988
ERROR_ALLOWANCE = F(1, 800)  # 0.00125

checks = 0
failures = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global checks, failures
    checks += 1
    ok = bool(condition)
    failures += 0 if ok else 1
    print(
        f"[{'PASS' if ok else 'FAIL'}] {name}"
        + (f"  {detail}" if detail else "")
    )


def upper(value) -> mp.mpf:
    return mp.mpf(value.b)


def lower(value) -> mp.mpf:
    return mp.mpf(value.a)


def require_order(text: str, name: str, fragments: tuple[str, ...]) -> None:
    position = -1
    for fragment in fragments:
        next_position = text.find(fragment, position + 1)
        if next_position < 0:
            check(name, False, f"missing {fragment!r}")
            return
        position = next_position
    check(name, True)


print("--- A: exact criterion containment")
check("A1 exact candidate row", T0 + Y0_SQUARED / 2 == F(893927, 5_000_000))
check(
    "A2 certified y-floor is below the target y0",
    SLAB_Y**2 < Y0_SQUARED,
    f"squared margin={Y0_SQUARED - SLAB_Y**2}",
)
check("A3 certified t-top contains target t0", T0 <= SLAB_T)
check("A4 required x-width is below one", 0 < 1 - Y0_SQUARED < 1)
check(
    "A5 curved lower edge remains above slab floor",
    SLAB_Y**2
    <= Y0_SQUARED
    <= Y0_SQUARED + 2 * T0
    <= 1,
)
check(
    "A6 curved upper edge remains inside slab",
    0 < 1 - 2 * T0 <= 1,
)

print("--- B: constant N on the complete closed slab")
x_box = iv.mpf([X, X + 1])
t_box = iv.mpf(129) / 800 * iv.mpf([0, 1])
n_box = iv.sqrt(x_box / (4 * iv.pi) + t_box / 16)
n_lo = int(mp.floor(lower(n_box)))
n_hi = int(mp.floor(upper(n_box)))
check(
    "B1 floor(sqrt(x/4pi+t/16)) is constant",
    n_lo == n_hi == N0,
    f"sqrt-box={n_box}",
)

print("--- C: independent uniform Theorem 1.3 error majorant")
x_left = iv.mpf(X)
x_right = iv.mpf(X + 1)
t_max = iv.mpf(129) / 800
y_min = iv.mpf(1809) / 10_000
one = iv.mpf(1)
nn = iv.mpf(N0)
pi = iv.pi
q_left = x_left / (4 * pi)
q_right = x_right / (4 * pi)

# The positive-part correction in (21) is at most
# t/(2x^2) * (1 + 8/x^2) for 0 <= y <= 1.
delta = t_max / (2 * x_left**2) * (1 + 8 / x_left**2)

# Equation (22), using t<=t0, y<=1, x>=X.
kappa_upper = t_max / (2 * (x_left - 6))

# For n<=N, N^2<q makes the heat exponent in b_n n^{-sigma}
# nonpositive after the +(t/4)log(q) part of sigma is retained.  Only
# n^delta remains.  The same inequality gives
# |gamma| n^y <= exp(.02y)(n^2/q)^(y/2) <= exp(.02).
check(
    "C1 N^2<q gives both heat cancellation and the gamma*n^y bound",
    lower(q_left) > N0**2,
)
check(
    "C2 2*log(N)<log(q) independently confirms N^2<q",
    2 * iv.log(nn).b < iv.log(q_left).a,
)
delta_factor = iv.exp(delta * iv.log(nn))
gamma_ny_upper = iv.exp(iv.mpf("0.02"))

# For equation (23), |log(q/n^2)| <= log(q) on 1<=n<=N.  Bound all N
# summands by the worst retained powers; this is deliberately coarse.
u_max = (
    (t_max**2 / 16) * iv.log(q_right) ** 2 + iv.mpf("0.626")
) / (x_left - iv.mpf("6.66"))
e_ab = (
    nn
    * delta_factor
    * (
        1
        + gamma_ny_upper
        * iv.exp(kappa_upper * iv.log(nn))
    )
    * (iv.exp(u_max) - 1)
)

# For equation (24), drop the favorable negative heat term.  The first
# factor is largest at (X,y_min), the cosh factor at y=1, and the last
# factor is bounded using its largest numerator and smallest denominator.
e_c0 = iv.exp(
    -(1 + y_min) / 4 * iv.log(q_left)
    + iv.mpf("1.24") * (3 + one / 3) / (nn - iv.mpf("0.125"))
    + (
        3 * iv.sqrt(iv.log(q_right) ** 2 + (pi / 2) ** 2)
        + iv.mpf("10.44")
    )
    / (x_left - 12)
)
error_total = e_ab + e_c0
check("C3 equation (23) coarse bound is below 4.3e-7", upper(e_ab) < mp.mpf("4.3e-7"))
check("C4 equation (24) coarse bound is below 3.57e-4", upper(e_c0) < mp.mpf("3.57e-4"))
check(
    "C5 total error is below the C verifier's 0.00125 allowance",
    upper(error_total) < mp.mpf(ERROR_ALLOWANCE.numerator) / ERROR_ALLOWANCE.denominator,
    f"uniform upper={mp.nstr(upper(error_total), 24)}",
)

print("--- D: fail-closed C source contract")
source = SOURCE.read_text(encoding="utf-8")
check(
    "D1 both numerical quadratures check their return status",
    source.count("quadrature did not converge") == 2
    and source.count("acb_calc_integrate(") == 2,
)
check("D2 minimum modulus uses interval min", "arb_min(minmodabb, minmodabb, ab, prec);" in source)
check(
    "D3 serialized coefficients receive relative-or-absolute 1e-20 balls",
    'arb_set_str(serialization_scale, "1e-20", prec)' in source
    and source.count("arb_add_error(re, serialization_error);") == 1
    and source.count("arb_add_error(im, serialization_error);") == 1,
)
check(
    "D4 the independently bounded Taylor remainder enters every value",
    'arb_set_str(truncation_error, "1e-20", prec)' in source
    and "acb_add_error_arb(a, truncation_error);" in source,
)
require_order(
    source,
    "D5 spatial interpolation uses Dz/[2(num-1)]",
    (
        "arb_set_si(a, 2 * (num - 1));",
        "arb_div(spatial_error, dzabb, a, prec);",
    ),
)
require_order(
    source,
    "D6 time derivative is enclosed on each complete closed prism",
    (
        "arb_union(t_box, t, t_next, prec);",
        "generate_ddtbound(dtabb_prism",
        "arb_get_ubound_arf(candidate_arf, dtabb_prism, prec);",
        "arf_ceil(candidate_arf, candidate_arf);",
        "arb_set_arf(dtabb, candidate_arf);",
    ),
)
require_order(
    source,
    "D7 decisive inequality includes space, time, and H/B error",
    (
        "arb_mul(time_error, dtabb, delta, prec);",
        "arb_add(proof_lhs, spatial_error, time_error, prec);",
        "arb_add(proof_lhs, proof_lhs, approximation_error, prec);",
        "arb_sub(proof_margin, minmodabb, proof_lhs, prec);",
        "!arb_is_positive(proof_margin)",
    ),
)
check(
    "D8 full winding intervals must prove the integer zero",
    "winding interval does not certify the integer zero" in source
    and "arb_mul_2exp_si(b, b, -2);" in source,
)
check(
    "D9 C allowance is the independently discharged 0.00125",
    'arb_set_str(approximation_error, "0.00125", prec)' in source,
)
check(
    "D10 success is impossible without terminal coverage",
    "if (!covered || !arb_lt(a, b))" in source
    and "return certified;" in source,
)

ddz_callback = (
    source.split("f_ddzbound(acb_ptr res", 1)[1].split(
        "\nvoid\ngenerate_ddzbound", 1
    )[0]
    if "f_ddzbound(acb_ptr res" in source
    and "\nvoid\ngenerate_ddzbound" in source
    else ""
)
ddt_callback = (
    source.split("f_ddtbound(acb_ptr res", 1)[1].split(
        "\nvoid\ngenerate_ddtbound", 1
    )[0]
    if "f_ddtbound(acb_ptr res" in source
    and "\nvoid\ngenerate_ddtbound" in source
    else ""
)
check(
    "D11 quadrature callbacks preserve the complex variable",
    bool(ddz_callback)
    and bool(ddt_callback)
    and "acb_get_real(" not in ddz_callback
    and "acb_get_real(" not in ddt_callback,
)
check(
    "D12 quadrature callbacks use fail-closed analytic log and powers",
    all(
        callback.count("acb_log_analytic(logNu, Nu, analytic, prec);") == 1
        and callback.count("acb_pow_analytic(") == 2
        and "analytic = (order != 0);" in callback
        and "if (order > 1)" in callback
        for callback in (ddz_callback, ddt_callback)
    ),
)
check(
    "D13 every integral exercises order=1 while finite-head calls use order=0",
    source.count("analytic_calls == 0") == 2
    and source.count("never requested an analytic enclosure") == 2
    and source.count("f_ddzbound(tmp, ai, param, 0, prec)") == 1
    and source.count("f_ddtbound(tmp, ai, param, 0, prec)") == 1,
)
check(
    "D14 Lemma 8.4 sums use an exact 16-term head and decreasing-tail integral",
    "#define DERIVATIVE_HEAD 16" in source
    and source.count("head_n <= DERIVATIVE_HEAD") == 2
    and source.count("arb_set_si(a, DERIVATIVE_HEAD);") == 2
    and source.count("acb_mul_arb(est, est, Narb, prec);") == 2
    and "arb_add(esta, esta, estinit, prec);" not in source,
)
require_order(
    source,
    "D15 increasing and decreasing spatial factors use conservative endpoints",
    (
        "arb_add_si(x_upper, X, 1, prec);",
        "arb_one(y_upper);",
        "arb_log(logxdiv4pi_upper, xdiv4pi_upper, prec);",
        "generate_ddzbound(dzabb, X, y0, x_upper, y_upper, t,",
        "logxdiv4pi_upper, onedivxmin6, prec);",
        "generate_ddtbound(dtabb_prism, X, y0, t_box,",
        "logxdiv4pi_upper,",
    ),
)
check(
    "D16 every derivative-envelope theorem gate is fail-closed",
    all(
        source.count(message) == 1
        for message in (
            "derivative-box c derivative prerequisite failed",
            "derivative-box c x-monotonicity gate is not strict",
            "A-core y-monotonicity gate is not strict",
            "derivative-bracket positivity gate failed",
            "sigma y-monotonicity gate is not strict",
            "derivative-tail exponent gate is not strict",
            "derivative-tail monotonicity gate is not strict",
            "time-derivative logarithmic bracket is not positive",
        )
    ),
)
try:
    derivative_note = DERIVATIVE_NOTE.read_text(encoding="utf-8")
except (OSError, UnicodeError):
    derivative_note = ""
check(
    "D17 derivative-box theorem documents endpoints, discrete tail, and analytic quadrature",
    all(
        fragment in derivative_note
        for fragment in (
            "Endpoint-separated upper bound",
            "Certified discrete-sum majorant",
            "Holomorphic quadrature contract",
            "K=16",
            "acb_log_analytic",
            "acb_pow_analytic",
        )
    ),
)


BALL_RE = re.compile(
    r"^\[(?:(?P<mid>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?) )?"
    r"\+/- (?P<rad>(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)\]$",
    re.IGNORECASE,
)
PRISM_RE = re.compile(
    r"^Prism\((\d+)\) t=\[(.*?),(.*?)\] "
    r"winding=(.*?) min_mesh=(.*?) Dz=(.*?) Dt=(.*?) "
    r"spatial=(.*?) time=(.*?) eps=(.*?) margin=(.*?) "
    r"mesh=(\d+) PASS$"
)


def decimal_ball(text: str) -> tuple[Decimal, Decimal]:
    text = text.strip()
    match = BALL_RE.fullmatch(text)
    if match:
        midpoint = Decimal(match.group("mid") or "0")
        radius = Decimal(match.group("rad"))
        return midpoint - radius, midpoint + radius
    value = Decimal(text)
    return value, value


def read_evidence(path: Path, name: str) -> str:
    try:
        value = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        check(name, False, f"{path}: {exc}")
        return ""
    check(name, bool(value.strip()), str(path))
    return value


print("--- E: sealed closed-prism evidence")
log = read_evidence(LOG, "E1 barrier log exists and is nonempty")
check("E2 log contains no failure marker", "FAIL:" not in log and "aborted" not in log)
check("E3 log records constant N corners", "N-corners=690988,690988" in log)
allowance_matches = re.findall(
    r"H/B approximation allowance=(\[[^\]]+\])$",
    log,
    re.MULTILINE,
)
allowance_ball = (
    decimal_ball(allowance_matches[0])
    if len(allowance_matches) == 1
    else (Decimal(1), Decimal(-1))
)
allowance_exact = Decimal(1) / Decimal(800)
check(
    "E4 log encloses the exact 0.00125 allowance with negligible radius",
    allowance_ball[0] <= allowance_exact <= allowance_ball[1]
    and allowance_ball[1] - allowance_ball[0] < Decimal("1e-25"),
)

prisms = []
prism_lines = []
for line in log.splitlines():
    if line.startswith("Prism("):
        prism_lines.append(line)
        match = PRISM_RE.fullmatch(line)
        if match:
            prisms.append(match.groups())

check(
    "E5 every prism line parses and the deterministic cover has 883 prisms",
    len(prism_lines) == len(prisms) == 883,
    f"lines={len(prism_lines)} parsed={len(prisms)}",
)
sequential = all(int(row[0]) == index for index, row in enumerate(prisms, 1))
check("E6 prism identifiers are consecutive", sequential)

seams_exact = True
numeric_ok = True
formula_ok = True
first_start = None
first_start_text = None
last_end = None
last_end_text = None
first_dz = None
first_dt = None
minimum_margin = None
maximum_winding = Decimal(0)
epsilon_reference = None
for row in prisms:
    (
        _number,
        start_text,
        end_text,
        winding_text,
        minimum_text,
        dz_text,
        dt_text,
        spatial_text,
        time_text,
        epsilon_text,
        margin_text,
        mesh_text,
    ) = row
    start_text = start_text.strip()
    end_text = end_text.strip()
    start = decimal_ball(start_text)
    end = decimal_ball(end_text)
    winding = decimal_ball(winding_text)
    minimum = decimal_ball(minimum_text)
    spatial = decimal_ball(spatial_text)
    time_motion = decimal_ball(time_text)
    epsilon = decimal_ball(epsilon_text)
    margin = decimal_ball(margin_text)
    dz = Decimal(dz_text)
    dt = Decimal(dt_text)
    mesh = int(mesh_text)
    num = (mesh + 4) // 4

    if first_start is None:
        first_start = start
        first_start_text = start_text
        first_dz = dz
        first_dt = dt
    if epsilon_reference is None:
        epsilon_reference = epsilon_text.strip()
    if last_end_text is not None and last_end_text != start_text:
        seams_exact = False
    last_end = end
    last_end_text = end_text

    maximum_winding = max(
        maximum_winding, abs(winding[0]), abs(winding[1])
    )
    recomputed_margin = (
        minimum[0] - spatial[1] - time_motion[1] - epsilon[1]
    )
    recomputed_margin_upper = (
        minimum[1] - spatial[0] - time_motion[0] - epsilon[0]
    )
    minimum_margin = (
        recomputed_margin
        if minimum_margin is None
        else min(minimum_margin, recomputed_margin)
    )

    exact_integers = (
        dz > 0
        and dt > 0
        and dz == dz.to_integral_value()
        and dt == dt.to_integral_value()
    )
    mesh_relation = num >= 2 and mesh == 4 * num - 4
    spatial_expected = dz / (2 * Decimal(num - 1))
    delta_lower = end[0] - start[1]
    delta_upper = end[1] - start[0]
    time_lower = dt * delta_lower
    time_upper = dt * delta_upper
    formula_ok &= (
        exact_integers
        and mesh_relation
        and spatial[0] <= spatial_expected <= spatial[1]
        and time_motion[0] <= time_lower
        and time_upper <= time_motion[1]
        and recomputed_margin > 0
        and margin[0] <= recomputed_margin_upper
        and recomputed_margin <= margin[1]
    )
    numeric_ok &= (
        start[1] < end[0]
        and minimum[0] > 0
        and spatial[0] > 0
        and time_motion[0] > 0
        and epsilon_text.strip() == epsilon_reference
        and epsilon[0] <= allowance_exact <= epsilon[1]
        and epsilon[1] - epsilon[0] < Decimal("1e-25")
        and margin[0] > 0
        and mesh >= 4
    )

check("E7 every printed prism quantity passes its sign/type gate", numeric_ok)
check(
    "E8 every prism inequality is independently recomputed from printed balls",
    formula_ok,
    f"minimum recomputed lower={minimum_margin}",
)
check("E9 adjacent closed-prism seam strings are byte-identical", seams_exact)
check(
    "E10 the first prism begins at the exact t=0 token",
    first_start_text == "0" and first_start == (Decimal(0), Decimal(0)),
)
check(
    "E11 the final prism encloses t0=0.16125",
    last_end is not None
    and last_end[0]
    <= Decimal(T0.numerator) / Decimal(T0.denominator)
    <= last_end[1],
)
check(
    "E12 every per-prism winding enclosure lies in (-1/4,1/4)",
    maximum_winding < Decimal("0.25"),
    f"max abs endpoint={maximum_winding}",
)
check(
    "E13 first prism records the exact-head derivative ceilings",
    first_dz == Decimal(9600) and first_dt == Decimal(52726),
    f"Dz={first_dz} Dt={first_dt}",
)

nonblank = [line for line in log.splitlines() if line.strip()]
allowed_nonprism = (
    "Filling stored sums matrix with ",
    "Processing the barrier for X= ",
    "Closed target enclosure: ",
    "Overall winding number: ",
    "Rigorous winding interval: ",
    "Closed coverage endpoint: ",
    "RESULT: CLOSED SLAB CERTIFIED",
    "cpu/wall(s): ",
)
recognized = all(
    line.startswith("Prism(")
    or any(line.startswith(prefix) for prefix in allowed_nonprism)
    for line in nonblank
)
check("E14 log contains no unrecognized nonblank record", recognized)
check(
    "E15 unique headers, aggregate gates, result, and timing are ordered",
    len(nonblank) == 891
    and sum(line.startswith("Filling stored sums matrix with ") for line in nonblank) == 1
    and sum(line.startswith("Processing the barrier for X= ") for line in nonblank) == 1
    and sum(line.startswith("Closed target enclosure: ") for line in nonblank) == 1
    and sum(line.startswith("Overall winding number: ") for line in nonblank) == 1
    and sum(line.startswith("Rigorous winding interval: ") for line in nonblank) == 1
    and sum(line.startswith("Closed coverage endpoint: ") for line in nonblank) == 1
    and nonblank[-2] == "RESULT: CLOSED SLAB CERTIFIED"
    and nonblank[-1].startswith("cpu/wall(s): "),
)

aggregate_lines = [
    line.removeprefix("Rigorous winding interval: ").strip()
    for line in nonblank
    if line.startswith("Rigorous winding interval: ")
]
aggregate = (
    decimal_ball(aggregate_lines[0])
    if len(aggregate_lines) == 1
    else (Decimal(1), Decimal(-1))
)
check(
    "E16 aggregate winding interval certifies the integer zero",
    aggregate[0] <= 0 <= aggregate[1]
    and max(abs(aggregate[0]), abs(aggregate[1])) < Decimal("0.25"),
    f"aggregate={aggregate}",
)
coverage_lines = [
    line.removeprefix("Closed coverage endpoint: ").strip()
    for line in nonblank
    if line.startswith("Closed coverage endpoint: ")
]
check(
    "E17 aggregate coverage token equals the final prism endpoint",
    len(coverage_lines) == 1 and coverage_lines[0] == last_end_text,
)

print("--- F: coefficient, Taylor-tail, and Arb error provenance")
tail_log = read_evidence(
    TAIL_LOG, "F1 factorial Taylor-tail log exists and is nonempty"
)
tail_matches = re.findall(
    r"^Taylor truncation upper = (.+)$", tail_log, re.MULTILINE
)
tail_ball = (
    decimal_ball(tail_matches[0])
    if len(tail_matches) == 1
    else (Decimal(1), Decimal(1))
)
check(
    "F2 factorial Taylor-tail upper is strictly below 1e-20",
    "FAIL" not in tail_log
    and len(tail_matches) == 1
    and tail_ball[1] < Decimal("1e-20"),
    f"upper={tail_ball[1]}",
)

provenance_log = read_evidence(
    PROVENANCE_LOG, "F3 stored-sum provenance log exists and is nonempty"
)
check(
    "F4 all 7,688 regenerated stored components fit their archived balls",
    re.search(r"^components: 7688$", provenance_log, re.MULTILINE) is not None
    and re.search(
        r"^components with nonzero printed Arb radii: 7688$",
        provenance_log,
        re.MULTILINE,
    )
    is not None
    and re.search(r"^containment failures: 0$", provenance_log, re.MULTILINE)
    is not None
    and provenance_log.rstrip().endswith(
        "RESULT: STORED-SUM PROVENANCE PASS"
    ),
)
regenerated = read_evidence(
    REGENERATED, "F5 regenerated interval matrix exists and is nonempty"
)
check(
    "F6 regenerated matrix retains all 7,688 nonzero radii",
    regenerated.startswith("6000000185827.00000000000000000, 62, 62, 20\n")
    and regenerated.count("+/-") == 7688,
)

uniform_log = read_evidence(
    UNIFORM_ERROR_LOG, "F7 independent Arb uniform-error log exists"
)
uniform_matches = re.findall(
    r"^uniform displayed-formula total upper = (.+)$",
    uniform_log,
    re.MULTILINE,
)
uniform_ball = (
    decimal_ball(uniform_matches[0])
    if len(uniform_matches) == 1
    else (Decimal(1), Decimal(1))
)
check(
    "F8 Arb independently certifies the complete displayed error below 0.00125",
    "[PASS] N^2 < X/(4*pi)" in uniform_log
    and "[PASS] 2*log(N) < log(X/(4*pi))" in uniform_log
    and "FAIL" not in uniform_log
    and len(uniform_matches) == 1
    and uniform_ball[1] < Decimal(1) / Decimal(800)
    and "RESULT: UNIFORM NUMERICAL ERROR-FORMULA BOUND CERTIFIED"
    in uniform_log,
    f"upper={uniform_ball[1]}",
)

print(f"TOTAL CHECKS RUN: {checks}")
if failures:
    print(f"RESULT: {failures} FAILED")
    sys.exit(1)
print("RESULT: ALL PASS")
print(
    "BARRIER CONCLUSION: H_t is zero-free on the complete closed slab "
    "[X,X+1] x [0.1809,1] x [0,0.16125]."
)
