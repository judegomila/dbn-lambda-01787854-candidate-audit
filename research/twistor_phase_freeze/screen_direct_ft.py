#!/usr/bin/env python3
"""Non-rigorous direct screen for the phase/jet structure of Polymath f_t.

This program is intentionally separated from the certificate surface. It
uses IEEE double precision and samples finitely many points. Its output is
research diagnostics only; it cannot certify a de Bruijn--Newman bound.

The formulas are Theorem 1.3 / equation (14) of arXiv:1904.12438v2 in the
normalization used by this repository.
"""

from __future__ import annotations

import argparse
import cmath
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

DEFAULT_X = 6_000_000_185_827.0
DEFAULT_Y2 = 87_677 / 2_500_000
DEFAULT_PRIMES = (2, 3, 5, 7, 11, 13)
DEFAULT_N = (690_988, 850_000, 1_075_000, 2_000_000, 4_050_000)
DEFAULT_T = (0.1607, 0.1500, 0.1400, 0.1300, 0.1250, 0.1200)
DEFAULT_FRACTIONS = tuple(float(x) for x in np.linspace(0.0, 0.999, 9))


def alpha(s: complex) -> complex:
    return 1 / (2 * s) + 1 / (s - 1) + 0.5 * cmath.log(s / (2 * math.pi))


def alpha_prime(s: complex) -> complex:
    return -1 / (2 * s * s) - 1 / (s - 1) ** 2 + 1 / (2 * s)


def alpha_second(s: complex) -> complex:
    return 1 / s**3 + 2 / (s - 1) ** 3 - 1 / (2 * s * s)


def log_m0(s: complex) -> complex:
    return (
        cmath.log(s)
        + cmath.log(s - 1)
        - (s / 2) * math.log(math.pi)
        + math.log(math.sqrt(2 * math.pi) / 16)
        + (s / 2 - 0.5) * cmath.log(s / 2)
        - s / 2
    )


def log_mt(s: complex, t: float) -> complex:
    a = alpha(s)
    return log_m0(s) + (t / 4) * a * a


def beta(s: complex, t: float) -> complex:
    a = alpha(s)
    return a + (t / 2) * a * alpha_prime(s)


def beta_prime(s: complex, t: float) -> complex:
    a = alpha(s)
    ap = alpha_prime(s)
    return ap + (t / 2) * (ap * ap + a * alpha_second(s))


def x_n(n: int, t: float) -> float:
    return 4 * math.pi * (n * n - t / 16)


def p13_mollifier(s_star: complex, t: float, primes: Sequence[int]) -> complex:
    value = 1 + 0j
    for prime in primes:
        logp = math.log(prime)
        btp = math.exp((t / 4) * logp * logp)
        value *= 1 - btp * cmath.exp(-s_star * logp)
    return value


@dataclass(frozen=True)
class ScreenRow:
    t: float
    lambda_objective: float
    y: float
    n: int
    fraction: float
    x: float
    computed_n: int
    abs_f: float
    abs_ef: float
    re_ef: float
    im_ef: float
    abs_ef_x: float
    radial_first: float
    radial_second: float


def evaluate_jet(
    x: float,
    y: float,
    t: float,
    logs: np.ndarray,
    primes: Sequence[int],
) -> tuple[complex, complex, complex, complex, complex, float, float, float]:
    """Return f, f_x, f_xx, E, Ef, |(Ef)_x|, (|Ef|^2)', (|Ef|^2)''."""
    n = logs.size
    computed_n = int(math.floor(math.sqrt(x / (4 * math.pi) + t / 16)))
    if computed_n != n:
        raise ValueError(f"window mismatch: expected N={n}, computed N={computed_n}")

    s0 = (1 + y - 1j * x) / 2
    aarg = (1 - y + 1j * x) / 2
    barg = (1 + y + 1j * x) / 2

    s_star = s0 + (t / 2) * alpha(s0)
    s_x = (-0.5j) * (1 + (t / 2) * alpha_prime(s0))
    s_xx = -(t / 8) * alpha_second(s0)

    kappa = (t / 2) * (alpha(aarg) - alpha(barg))
    kappa_x = 0.25j * t * (alpha_prime(aarg) - alpha_prime(barg))
    kappa_xx = -(t / 8) * (alpha_second(aarg) - alpha_second(barg))

    log_gamma = log_mt(aarg, t) - log_mt(s0, t)
    gamma = cmath.exp(log_gamma)
    log_gamma_x = 0.5j * (beta(aarg, t) + beta(s0, t))
    log_gamma_xx = 0.25 * (beta_prime(s0, t) - beta_prime(aarg, t))

    heat = (t / 4) * logs * logs

    term1 = np.exp(heat - s_star * logs)
    dlog1 = -s_x * logs
    ddlog1 = -s_xx * logs
    term1_x = term1 * dlog1
    term1_xx = term1 * (dlog1 * dlog1 + ddlog1)

    reflected = np.conj(s_star) + kappa
    reflected_x = np.conj(s_x) + kappa_x
    reflected_xx = np.conj(s_xx) + kappa_xx
    term2 = gamma * np.exp(heat + y * logs - reflected * logs)
    dlog2 = log_gamma_x - reflected_x * logs
    ddlog2 = log_gamma_xx - reflected_xx * logs
    term2_x = term2 * dlog2
    term2_xx = term2 * (dlog2 * dlog2 + ddlog2)

    f = np.sum(term1 + term2)
    f_x = np.sum(term1_x + term2_x)
    f_xx = np.sum(term1_xx + term2_xx)

    euler = 1 + 0j
    q = 0 + 0j
    rsum = 0 + 0j
    for prime in primes:
        logp = math.log(prime)
        btp = math.exp((t / 4) * logp * logp)
        ratio = btp * cmath.exp(-s_star * logp)
        euler *= 1 - ratio
        q += ratio * logp / (1 - ratio)
        rsum += ratio * logp * logp / (1 - ratio) ** 2

    elog_x = s_x * q
    elog_xx = s_xx * q - s_x * s_x * rsum
    euler_x = euler * elog_x
    euler_xx = euler * (elog_x * elog_x + elog_xx)

    ef = euler * f
    ef_x = euler_x * f + euler * f_x
    ef_xx = euler_xx * f + 2 * euler_x * f_x + euler * f_xx

    radial_first = 2 * (ef.conjugate() * ef_x).real
    radial_second = 2 * abs(ef_x) ** 2 + 2 * (ef.conjugate() * ef_xx).real
    return f, f_x, f_xx, euler, ef, abs(ef_x), radial_first, radial_second


def evaluate_value(
    x: float,
    y: float,
    t: float,
    logs: np.ndarray,
    primes: Sequence[int],
) -> tuple[complex, complex]:
    """Return the direct Polymath approximant f_t and its Euler-mollified value."""
    n = logs.size
    computed_n = int(math.floor(math.sqrt(x / (4 * math.pi) + t / 16)))
    if computed_n != n:
        raise ValueError(f"window mismatch: expected N={n}, computed N={computed_n}")

    s0 = (1 + y - 1j * x) / 2
    s_star = s0 + (t / 2) * alpha(s0)
    aarg = (1 - y + 1j * x) / 2
    barg = (1 + y + 1j * x) / 2
    kappa = (t / 2) * (alpha(aarg) - alpha(barg))
    gamma = cmath.exp(log_mt(aarg, t) - log_mt(s0, t))

    heat = (t / 4) * logs * logs
    term1 = np.exp(heat - s_star * logs)
    term2 = gamma * np.exp(heat + y * logs - (np.conj(s_star) + kappa) * logs)
    f = np.sum(term1 + term2)
    euler = p13_mollifier(s_star=s_star, t=t, primes=primes)
    return f, euler * f


def parse_csv_numbers(text: str, cast=float) -> tuple:
    return tuple(cast(part.strip()) for part in text.split(",") if part.strip())


def screen(
    x_anchor: float,
    y2: float,
    t_values: Iterable[float],
    n_values: Iterable[int],
    fractions: Iterable[float],
    primes: Sequence[int],
    compute_jets: bool = False,
) -> list[ScreenRow]:
    t_values = tuple(t_values)
    n_values = tuple(n_values)
    fractions = tuple(fractions)
    if not n_values:
        raise ValueError("at least one N value is required")

    y = math.sqrt(y2)
    first_x = x_anchor + math.sqrt(1 - y2)
    first_n = min(n_values)
    rows: list[ScreenRow] = []
    logs_cache = {n: np.log(np.arange(1, n + 1, dtype=np.float64)) for n in n_values}

    for t in t_values:
        for n in n_values:
            logs = logs_cache[n]
            left = x_n(n, t)
            right = x_n(n + 1, t)
            if n == first_n:
                left = max(left, first_x)
            for fraction in fractions:
                if not 0 <= fraction < 1:
                    raise ValueError("fractions must lie in [0,1)")
                x = left + fraction * (right - left)

                # At x_N the exact expression lies in window N, but IEEE
                # evaluation can round the inverse square root down to N-1.
                computed_n = int(math.floor(math.sqrt(x / (4 * math.pi) + t / 16)))
                if computed_n < n:
                    # One unit in x is negligible relative to a window of
                    # width about 8*pi*N, but exceeds the IEEE uncertainty.
                    x = min(right, x + max(1.0, 32 * math.ulp(x)))
                    computed_n = int(math.floor(math.sqrt(x / (4 * math.pi) + t / 16)))
                if computed_n != n:
                    raise ValueError(
                        f"failed to place sample in window N={n}; computed N={computed_n}"
                    )

                if compute_jets:
                    f, _fx, _fxx, _e, ef, abs_ef_x, radial_first, radial_second = evaluate_jet(
                        x=x, y=y, t=t, logs=logs, primes=primes
                    )
                else:
                    f, ef = evaluate_value(x=x, y=y, t=t, logs=logs, primes=primes)
                    abs_ef_x = math.nan
                    radial_first = math.nan
                    radial_second = math.nan
                rows.append(
                    ScreenRow(
                        t=t,
                        lambda_objective=t + y2 / 2,
                        y=y,
                        n=n,
                        fraction=fraction,
                        x=x,
                        computed_n=computed_n,
                        abs_f=abs(f),
                        abs_ef=abs(ef),
                        re_ef=ef.real,
                        im_ef=ef.imag,
                        abs_ef_x=abs_ef_x,
                        radial_first=radial_first,
                        radial_second=radial_second,
                    )
                )
    return rows


def write_outputs(rows: Sequence[ScreenRow], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "direct_ft_screen.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    minima: list[dict] = []
    keys = sorted({(row.t, row.n) for row in rows})
    for t, n in keys:
        group = [row for row in rows if row.t == t and row.n == n]
        min_abs = min(group, key=lambda row: row.abs_ef)
        min_real = min(group, key=lambda row: row.re_ef)
        minima.append(
            {
                "t": t,
                "lambda_objective": min_abs.lambda_objective,
                "n": n,
                "sampled_min_abs_ef": min_abs.abs_ef,
                "sampled_min_abs_fraction": min_abs.fraction,
                "sampled_min_re_ef": min_real.re_ef,
                "sampled_min_re_fraction": min_real.fraction,
            }
        )
    payload = {
        "status": "NONRIGOROUS_SAMPLED_DIAGNOSTIC_ONLY",
        "warning": "Finite sampling and double precision do not certify nonvanishing or a Lambda bound.",
        "rows": len(rows),
        "minima": minima,
    }
    (output / "direct_ft_screen_summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", type=float, default=DEFAULT_X)
    parser.add_argument("--y2", type=float, default=DEFAULT_Y2)
    parser.add_argument("--t", default=",".join(str(value) for value in DEFAULT_T))
    parser.add_argument("--n", default=",".join(str(value) for value in DEFAULT_N))
    parser.add_argument(
        "--fractions", default=",".join(str(value) for value in DEFAULT_FRACTIONS)
    )
    parser.add_argument("--primes", default=",".join(str(value) for value in DEFAULT_PRIMES))
    parser.add_argument("--output", type=Path, default=Path("direct-ft-screen"))
    parser.add_argument(
        "--jets", action="store_true",
        help="also evaluate first and second x-jets (substantially slower)",
    )
    args = parser.parse_args()

    rows = screen(
        x_anchor=args.x,
        y2=args.y2,
        t_values=parse_csv_numbers(args.t, float),
        n_values=parse_csv_numbers(args.n, int),
        fractions=parse_csv_numbers(args.fractions, float),
        primes=parse_csv_numbers(args.primes, int),
        compute_jets=args.jets,
    )
    write_outputs(rows, args.output)

    print("STATUS: NONRIGOROUS SAMPLED DIAGNOSTIC ONLY")
    print(f"rows={len(rows)} output={args.output}")
    for t in sorted({row.t for row in rows}):
        group = [row for row in rows if row.t == t]
        print(
            f"t={t:.7f} bound_if_certified={t + args.y2 / 2:.7f} "
            f"sampled_min_abs_Ef={min(row.abs_ef for row in group):.12g} "
            f"sampled_min_Re_Ef={min(row.re_ef for row in group):.12g}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
