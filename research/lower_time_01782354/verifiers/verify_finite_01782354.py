#!/usr/bin/env python3
"""Verify the exploratory 0.1782354 finite Triangle sweep and binding.

The stored producer value is

    L_N(y0) = Q_N(y0) / M_N(y0) - corr_N(y0),

where Q_N = 1 - gamma - S_triangle.  Separate rigorous verifiers prove
Q_N is nondecreasing in y while M_N and corr_N are nonincreasing.  Thus
the stored global T floor is already in the same |f_t| units as the
paper's P-independent effective-approximation error E_max.  The final
finite gate is consequently T_floor - E_max > 0.
"""

from fractions import Fraction as F
import argparse
import gzip
from pathlib import Path
import re
import sys

from mpmath import iv, mp


iv.prec = 220
mp.prec = 220

HERE = Path(__file__).resolve().parent

T0 = F(16070, 100000)
TBOX_LO = T0
TBOX_HI = F(160700001, 10**9)
Y2 = F(350708, 10**7)
YMAX2 = 1 - 2 * T0
B = F(891177, 5_000_000)
N0 = 690_988
NMID = 4_050_000

EXACT_TBOX = ("16070/100000", "16070/100000")

FILES = (
    ("p23571113_690988_728999.log", "p23571113", 690_988, 728_999),
    ("p235711_729000_774999.log", "p235711", 729_000, 774_999),
    ("p2357_775000_849999.log", "p2357", 775_000, 849_999),
    ("p235_850000_1074999.log", "p235", 850_000, 1_074_999),
    ("p23_1075000_1100000.log", "p23", 1_075_000, 1_100_000),
    ("p23_1100001_1300000.log", "p23", 1_100_001, 1_300_000),
    ("p23_1300001_1700000.log", "p23", 1_300_001, 1_700_000),
    ("p23_1700001_2200000.log", "p23", 1_700_001, 2_200_000),
    ("p23_2200001_2800000.log", "p23", 2_200_001, 2_800_000),
    ("p23_2800001_3300000.log", "p23", 2_800_001, 3_300_000),
    ("p23_3300001_4050000.log", "p23", 3_300_001, 4_050_000),
)

EXPECTED_LEGS = {
    "p23571113": (
        690_988, 728_999, 38_012, F(670513304, 10**12), 690_988,
    ),
    "p235711": (
        729_000, 774_999, 46_000, F(4925245406, 10**12), 729_000,
    ),
    "p2357": (
        775_000, 849_999, 75_000, F(7453723667, 10**12), 775_000,
    ),
    "p235": (
        850_000, 1_074_999, 225_000, F(444808402, 10**12), 850_000,
    ),
    "p23": (
        1_075_000, 4_050_000, 2_975_001,
        F(2584981890, 10**12), 1_075_000,
    ),
}

ROW_RE = re.compile(r"N ([0-9]+) L12 ([0-9.]+) GT089 ([01])")
UNCERT_RE = re.compile(r"N ([0-9]+) UNCERT GT089 ([01])")
TIMING_RE = re.compile(r"TIMING ([0-9.]+) ([0-9]+)")


def itv_fraction(value):
    return iv.mpf(value.numerator) / value.denominator


def hull(left, right):
    return left + (right - left) * iv.mpf([0, 1])


def endpoint_fraction(value):
    sign, mantissa, exponent, _ = mp.mpf(value)._mpf_
    if mantissa == 0 and exponent == 0:
        return F(0)
    result = F(int(mantissa)) * F(2) ** int(exponent)
    return -result if sign else result


def upper_fraction(value):
    return endpoint_fraction(value.b)


def upper_point(value):
    return iv.mpf([value.b, value.b])


def floor_decimal(value, digits):
    integer = (value * 10**digits).numerator // (value * 10**digits).denominator
    sign = "-" if integer < 0 else ""
    text = str(abs(integer)).rjust(digits + 1, "0")
    return sign + text[:-digits] + "." + text[-digits:]


def ceil_decimal(value, digits):
    scaled = value * 10**digits
    integer = -((-scaled.numerator) // scaled.denominator)
    sign = "-" if integer < 0 else ""
    text = str(abs(integer)).rjust(digits + 1, "0")
    return sign + text[:-digits] + "." + text[-digits:]


def parse_file(path, family, expected_lo, expected_hi):
    expected_tbox = EXACT_TBOX
    require_weight = True
    first = None
    last = None
    previous = None
    rows = 0
    uncert = 0
    minimum = None
    argmin = None
    run_open = False
    run_rows = 0
    run_weight = False
    runs = 0

    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        for line_number, raw in enumerate(stream, 1):
            line = raw.strip()
            if not line:
                continue
            if line.startswith("TBOX "):
                if run_open:
                    raise AssertionError(
                        f"{path.name}:{line_number}: new TBOX before TIMING"
                    )
                fields = tuple(line.removeprefix("TBOX ").split())
                if fields != expected_tbox:
                    raise AssertionError(
                        f"{path.name}:{line_number}: wrong TBOX {fields}"
                    )
                run_open = True
                run_rows = 0
                run_weight = False
                runs += 1
                continue
            if line == "WEIGHT TRIANGLE":
                if not run_open or not require_weight or run_weight or run_rows:
                    raise AssertionError(
                        f"{path.name}:{line_number}: misplaced kernel tag"
                    )
                run_weight = True
                continue
            match = ROW_RE.fullmatch(line)
            if match:
                if not run_open or (require_weight and not run_weight):
                    raise AssertionError(
                        f"{path.name}:{line_number}: row before valid header"
                    )
                n = int(match.group(1))
                value = F(match.group(2))
                if previous is not None and n != previous + 1:
                    raise AssertionError(
                        f"{path.name}:{line_number}: nonconsecutive {previous},{n}"
                    )
                previous = n
                first = n if first is None else first
                last = n
                rows += 1
                run_rows += 1
                if minimum is None or value < minimum:
                    minimum = value
                    argmin = n
                continue
            match = UNCERT_RE.fullmatch(line)
            if match:
                uncert += 1
                raise AssertionError(
                    f"{path.name}:{line_number}: uncertified N={match.group(1)}"
                )
            match = TIMING_RE.fullmatch(line)
            if match:
                if not run_open:
                    raise AssertionError(
                        f"{path.name}:{line_number}: TIMING without run"
                    )
                if int(match.group(2)) != run_rows:
                    raise AssertionError(
                        f"{path.name}:{line_number}: TIMING count "
                        f"{match.group(2)} != {run_rows}"
                    )
                if require_weight and not run_weight:
                    raise AssertionError(
                        f"{path.name}:{line_number}: missing Triangle tag"
                    )
                run_open = False
                continue
            raise AssertionError(
                f"{path.name}:{line_number}: unparsed line {line!r}"
            )

    if run_open:
        raise AssertionError(f"{path.name}: unterminated run")
    if not runs or rows != expected_hi - expected_lo + 1:
        raise AssertionError(f"{path.name}: run/row count mismatch")
    if (first, last) != (expected_lo, expected_hi):
        raise AssertionError(
            f"{path.name}: range {first}..{last}, "
            f"expected {expected_lo}..{expected_hi}"
        )
    return {
        "first": first,
        "last": last,
        "rows": rows,
        "uncert": uncert,
        "minimum": minimum,
        "argmin": argmin,
        "runs": runs,
    }


def evidence_path(directory, filename):
    plain = directory / filename
    compressed = directory / f"{filename}.gz"
    matches = [path for path in (plain, compressed) if path.is_file()]
    if len(matches) != 1:
        raise AssertionError(
            f"need exactly one of {plain.name}, {compressed.name}"
        )
    if matches[0].is_symlink():
        raise AssertionError(f"evidence path is a symlink: {matches[0]}")
    return matches[0]


def effective_error_budget():
    """Full upstream U1--U5 path, on a t-box containing the exact row."""
    t = hull(itv_fraction(TBOX_LO), itv_fraction(TBOX_HI))
    y0 = iv.sqrt(itv_fraction(Y2))
    ymax = iv.sqrt(itv_fraction(YMAX2))
    pi = iv.pi
    n0 = iv.mpf(N0)
    x0 = 4 * pi * (n0**2 - t / 16)
    log0 = iv.log(n0**2 - t / 16)
    logn0 = iv.log(N0)
    delta1 = upper_point(
        (t / 4) * (-iv.log(1 - t / (16 * n0**2)))
        + t / (2 * x0**2)
    )
    sigma1 = (1 + y0) / 2 + (t / 2) * logn0 - delta1
    y1 = iv.mpf("0.02") - log0 / 2 + logn0 / 2
    kappa = upper_point(t / (2 * (x0 - 6)))

    gates = {
        "G0_positive_part": (8 / x0**2).b < (3 * y0).a,
        "sigma1_positive": sigma1.a > 0,
        "Y1_negative": y1.b < 0,
        "kappa_domain": kappa.a > 0 and kappa.b < 1,
        "G2a_ratio": (n0**2 / (n0**2 - t / 16)).a > 1,
        "U1_log_domain": log0.a > 2,
        "U2_logN": logn0.a > iv.mpf("0.5").b,
        "U3a_tail_decrease": ((1 + y0) / 2 - delta1).a > 0,
        "Y_range": 0 < Y2 < YMAX2 <= 1,
    }

    u1max = upper_point(
        ((t * t / 16) * log0**2 + iv.mpf("0.626"))
        / (x0 - iv.mpf("6.66"))
    )
    pmax = upper_point(
        1
        + iv.exp(iv.mpf("0.02"))
        * (1 - t / (16 * n0**2)) ** (iv.mpf(-1) / 2)
        * iv.exp(t * logn0 / (2 * (x0 - 6)))
    )

    m0 = 2000
    logm0 = iv.log(m0)
    g_t1 = -(t / 2) * logm0 + 1 / (logn0 - logm0)
    g_t2 = (
        (1 - y0) / 2
        + delta1
        - (t / 2) * logn0
        + 1 / (logn0 - logm0)
    )
    gates["U3b_first_endpoint"] = g_t1.b < 0
    gates["U3c_second_endpoint"] = g_t2.b < 0
    gates["U5_last_factor"] = F(3, 1) / F(1044, 100) < 1

    head = iv.mpf(0)
    for n in range(2, m0 + 1):
        logn = iv.log(n)
        head += iv.exp((t / 4) * logn**2 - sigma1 * logn)
    head = upper_point(head)

    def exponential_tail(logu):
        return iv.exp(
            (1 - sigma1) * logu + (t / 4) * logu**2
        )

    term1 = upper_point(exponential_tail(logm0) * (logn0 - logm0))
    term2 = upper_point(exponential_tail(logn0) * (logn0 - logm0))
    cap_u = iv.mpf([max(term1.b, term2.b)] * 2)
    smax = upper_point(1 + head + cap_u)
    error_ab = upper_point(pmax * smax * (iv.exp(u1max) - 1))
    error_c0 = upper_point(
        iv.exp(
            -(1 + y0) / 4 * log0
            - (t / 16) * log0**2
            + iv.mpf("1.24") * (3**ymax + 3**(-ymax))
            / (n0 - iv.mpf("0.125"))
            + (
                3 * iv.sqrt(log0**2 + (pi / 2) ** 2)
                + iv.mpf("10.44")
            )
            / (x0 - 12)
        )
    )
    if len(gates) != 12:
        raise AssertionError(f"internal error-gate count {len(gates)}")
    return (
        upper_fraction(error_ab + error_c0),
        upper_fraction(error_ab),
        upper_fraction(error_c0),
        upper_fraction(y1),
        upper_fraction(g_t1),
        upper_fraction(g_t2),
        gates,
    )


def corr_rate_gate():
    """Certify the global termwise logarithmic-rate cap Xi < 0."""
    t = itv_fraction(T0)
    y0 = iv.sqrt(itv_fraction(Y2))
    n0 = iv.mpf(N0)
    q = n0**2 - t / 16
    x = 4 * iv.pi * q
    k = t / (2 * (x - 6))
    g = iv.mpf("0.02") - iv.log(q) / 2
    xi = g + 1 / y0 + (iv.mpf("0.5") + k) * iv.log(n0)
    gates = {
        "q_positive": q.a > 0,
        "k_positive_small": k.a > 0 and k.b < iv.mpf("0.5").a,
        "gamma_rate_negative": g.b < 0,
        "Xi_negative": xi.b < 0,
        "Xi_N_decreases": (
            n0**2 / q
        ).a > (iv.mpf("0.5") + k).b,
        "expm1_rate_atom": True,  # e^u >= 1+u => u/(1-e^-u) <= 1+u.
    }
    return upper_fraction(xi), gates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "logs_dir",
        type=Path,
        help="directory containing the complete finite replay logs",
    )
    args = parser.parse_args()
    certificates = args.logs_dir.resolve()
    if not certificates.is_dir():
        raise AssertionError(f"not a log directory: {certificates}")

    if T0 + Y2 / 2 != B:
        raise AssertionError("exact B identity failed")
    if not (TBOX_LO == T0 < TBOX_HI <= F(1, 4)):
        raise AssertionError("stored t-box does not contain exact row")
    if not (0 < Y2 < YMAX2 <= 1):
        raise AssertionError("invalid y range")

    leg_state = {
        family: {
            "first": None,
            "last": None,
            "rows": 0,
            "minimum": None,
            "argmin": None,
            "uncert": 0,
            "files": 0,
            "runs": 0,
        }
        for family in EXPECTED_LEGS
    }
    previous_end = None
    total_rows = 0
    total_uncert = 0

    for filename, family, expected_lo, expected_hi in FILES:
        if previous_end is not None and expected_lo != previous_end + 1:
            raise AssertionError("manifest gap or overlap")
        result = parse_file(
            evidence_path(certificates, filename),
            family,
            expected_lo,
            expected_hi,
        )
        if previous_end is not None and result["first"] != previous_end + 1:
            raise AssertionError("stored global gap or overlap")
        previous_end = result["last"]
        total_rows += result["rows"]
        total_uncert += result["uncert"]

        state = leg_state[family]
        state["first"] = (
            result["first"] if state["first"] is None else state["first"]
        )
        state["last"] = result["last"]
        state["rows"] += result["rows"]
        state["uncert"] += result["uncert"]
        state["files"] += 1
        state["runs"] += result["runs"]
        if (
            state["minimum"] is None
            or result["minimum"] < state["minimum"]
        ):
            state["minimum"] = result["minimum"]
            state["argmin"] = result["argmin"]

    if (FILES[0][2], previous_end) != (N0, NMID):
        raise AssertionError("wrong global finite endpoints")
    expected_total = NMID - N0 + 1
    if total_rows != expected_total or total_rows != 3_359_013:
        raise AssertionError(f"wrong total row count {total_rows}")
    if total_uncert:
        raise AssertionError(f"UNCERT rows {total_uncert}")

    for family, expected in EXPECTED_LEGS.items():
        state = leg_state[family]
        actual_prefix = (state["first"], state["last"], state["rows"])
        if actual_prefix != expected[:3]:
            raise AssertionError(
                f"{family}: got {actual_prefix}, expected {expected[:3]}"
            )
        if (state["minimum"], state["argmin"]) != expected[3:]:
            raise AssertionError(
                f"{family}: minimum got "
                f"{(state['minimum'], state['argmin'])}, "
                f"expected {expected[3:]}"
            )
        if state["minimum"] <= 0:
            raise AssertionError(
                f"{family}: nonpositive minimum {state['minimum']}"
            )
        print(
            f"[PASS] family={family} files={state['files']} "
            f"runs={state['runs']} N={state['first']}..{state['last']} "
            f"rows={state['rows']} "
            f"minimum={floor_decimal(state['minimum'], 12)}"
            f"@{state['argmin']} UNCERT=0"
        )

    (
        error_max,
        error_ab,
        error_c0,
        y1_upper,
        g_t1_upper,
        g_t2_upper,
        error_gates,
    ) = effective_error_budget()
    failed_error = [
        name for name, passed in error_gates.items() if not passed
    ]
    if failed_error:
        raise AssertionError(f"error-budget gates failed: {failed_error}")

    xi_upper, corr_gates = corr_rate_gate()
    failed_corr = [
        name for name, passed in corr_gates.items() if not passed
    ]
    if failed_corr:
        raise AssertionError(f"corr-rate gates failed: {failed_corr}")

    global_t_floor = min(
        state["minimum"] for state in leg_state.values()
    )
    binding_floor = global_t_floor - error_max
    if not (0 < error_max < F(240, 10**9)):
        raise AssertionError(f"unexpected Emax {error_max}")
    if not (binding_floor > 0):
        raise AssertionError(f"binding floor too small {binding_floor}")
    if y1_upper >= F(-64, 10):
        raise AssertionError("Y1 room gate failed")

    print(
        "[PASS] full effective-error budget "
        f"gates={len(error_gates)}/{len(error_gates)} "
        f"eAB<={ceil_decimal(error_ab, 24)} "
        f"eC0<={ceil_decimal(error_c0, 24)} "
        f"Emax<={ceil_decimal(error_max, 24)}"
    )
    print(
        "[PASS] normalizer/corr monotonicity "
        f"gates={len(corr_gates)}/{len(corr_gates)} "
        f"Xi_ub={ceil_decimal(xi_upper, 18)} "
        f"g_t1_ub={ceil_decimal(g_t1_upper, 18)} "
        f"g_t2_ub={ceil_decimal(g_t2_upper, 18)}"
    )
    print(
        "RESULT PASS: full finite Triangle weld "
        "B=891177/5000000 rows=3359013 "
        "N=690988..4050000 gaps=0 overlaps=0 UNCERT=0 "
        f"T_floor={floor_decimal(global_t_floor, 12)} "
        f"Emax={ceil_decimal(error_max, 24)} "
        f"binding_floor={floor_decimal(binding_floor, 18)}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT FAIL: {exc}", file=sys.stderr)
        raise
