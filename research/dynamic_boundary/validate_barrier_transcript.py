"""Strict smoke parser for an experimental re-anchor barrier transcript.

This checks that the existing C program reports a successful closed-slab
calculation at the requested Riemann--Siegel index, with consecutive closed
time prisms, strict margins, and a complete time cover.  It does not supply
the new-site Taylor-tail or uniform-error proofs and therefore cannot promote
the transcript into proof evidence.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
from pathlib import Path
import re


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?"
# Arb transcript endpoints can carry substantially more than the default
# 28 decimal digits.  This parser is only a structural smoke check, but its
# endpoint and seam comparisons should still retain the printed precision.
getcontext().prec = 200
BALL_RE = re.compile(
    rf"^\[(?:(?P<mid>{NUMBER}) )?\+/- (?P<rad>{NUMBER})\]$",
    re.IGNORECASE,
)
PRISM_RE = re.compile(
    r"^Prism\((\d+)\) t=\[(.*?),(.*?)\] "
    r"winding=(.*?) min_mesh=(.*?) Dz=(.*?) Dt=(.*?) "
    r"spatial=(.*?) time=(.*?) eps=(.*?) margin=(.*?) "
    r"mesh=(\d+) PASS$"
)


def finite_decimal(text: str) -> Decimal:
    value = Decimal(text.strip())
    if not value.is_finite():
        raise ValueError(f"nonfinite decimal token: {text!r}")
    return value


def decimal_ball(text: str) -> tuple[Decimal, Decimal]:
    text = text.strip()
    match = BALL_RE.fullmatch(text)
    if match:
        midpoint = finite_decimal(match.group("mid") or "0")
        radius = finite_decimal(match.group("rad"))
        if radius < 0:
            raise ValueError("negative ball radius")
        return midpoint - radius, midpoint + radius
    value = finite_decimal(text)
    return value, value


def validate(path: Path, expected_n: int) -> int:
    text = path.read_text(encoding="utf-8")
    if "FAIL:" in text or "aborted" in text.lower():
        raise ValueError("barrier transcript contains a failure marker")
    n_corner_token = f"N-corners={expected_n},{expected_n}"
    if text.count(n_corner_token) != 1:
        raise ValueError("wrong or missing N-corner record")
    if text.count("Closed target enclosure: ") != 1:
        raise ValueError("wrong number of closed-target headers")
    if text.count("RESULT: CLOSED SLAB CERTIFIED") != 1:
        raise ValueError("wrong number of closed-slab success markers")

    identifiers = []
    previous_end_text: str | None = None
    first_start_text: str | None = None
    last_end: tuple[Decimal, Decimal] | None = None
    for line in text.splitlines():
        if not line.startswith("Prism("):
            continue
        match = PRISM_RE.fullmatch(line)
        if not match:
            raise ValueError(f"unparsed prism record: {line!r}")
        (
            identifier_text,
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
        ) = match.groups()
        identifier = int(identifier_text)
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
        dz = finite_decimal(dz_text)
        dt = finite_decimal(dt_text)
        mesh = int(mesh_text)

        if not start[1] < end[0]:
            raise ValueError(f"prism {identifier}: nonpositive time width")
        if minimum[0] <= 0 or margin[0] <= 0:
            raise ValueError(f"prism {identifier}: nonpositive margin")
        if spatial[0] <= 0 or time_motion[0] <= 0:
            raise ValueError(
                f"prism {identifier}: nonpositive displacement allowance"
            )
        if dz <= 0 or dt <= 0 or mesh < 4:
            raise ValueError(
                f"prism {identifier}: invalid derivative/mesh record"
            )
        if not winding[0] > Decimal("-0.25") or not winding[1] < Decimal(
            "0.25"
        ):
            raise ValueError(
                f"prism {identifier}: winding does not certify zero"
            )
        allowance = Decimal("0.00125")
        if not epsilon[0] <= allowance <= epsilon[1]:
            raise ValueError(
                f"prism {identifier}: wrong approximation allowance"
            )
        if previous_end_text is not None and start_text != previous_end_text:
            raise ValueError(
                f"prism {identifier}: nonidentical closed-prism seam"
            )

        identifiers.append(identifier)
        first_start_text = (
            start_text if first_start_text is None else first_start_text
        )
        previous_end_text = end_text
        last_end = end

    if not identifiers:
        raise ValueError("no prism records")
    if identifiers != list(range(1, len(identifiers) + 1)):
        raise ValueError("prism identifiers are not consecutive")
    if first_start_text != "0":
        raise ValueError("first prism does not start at exact token 0")
    t0 = Decimal(129) / Decimal(800)
    if last_end is None or not last_end[0] <= t0 <= last_end[1]:
        raise ValueError("final prism does not cover t0")

    print(
        f"RESULT: EXPERIMENTAL RE-ANCHOR TRANSCRIPT SMOKE PASS "
        f"(N={expected_n}, prisms={len(identifiers)})"
    )
    print(
        "STATUS: UNSEALED RESEARCH ONLY; new-site Taylor-tail, "
        "uniform-error, proof-to-code, and theorem-assembly checks remain "
        "outstanding."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("--expected-n", required=True, type=int)
    arguments = parser.parse_args()
    try:
        return validate(arguments.log, arguments.expected_n)
    except (OSError, ValueError) as exc:
        print(f"RESULT FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
