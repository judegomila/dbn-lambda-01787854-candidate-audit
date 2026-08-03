"""Strict parser for the stored finite Triangle certificate rows."""

from __future__ import annotations

from array import array
from dataclasses import dataclass
from fractions import Fraction as F
import gzip
from pathlib import Path
import re
from typing import Iterable, TextIO


TBOX_RE = re.compile(r"TBOX ([^ ]+) ([^ ]+)")
ROW_RE = re.compile(
    r"N ([0-9]+) L12 ([0-9]+\.[0-9]{12}) GT089 ([01])"
)
UNCERT_RE = re.compile(r"N ([0-9]+) UNCERT GT089 ([01])")
TIMING_RE = re.compile(r"TIMING ([0-9.]+) ([0-9]+)")


P11_TBOX = (F(16_125, 100_000), F(16_125, 100_000))
LATER_TBOX = (
    F(161_250_000, 10**9),
    F(161_250_001, 10**9),
)

# This is intentionally the same finite-file contract as
# verifiers/verify_finite_and_binding.py at the audited source commit.
# filename, family, first N, last N, exact TBOX, WEIGHT tag required
FINITE_FILE_SPECS = (
    (
        "p235711_690988_690995.log.gz",
        "p235711",
        690_988,
        690_995,
        P11_TBOX,
        False,
    ),
    (
        "p235711_690996_691500.log.gz",
        "p235711",
        690_996,
        691_500,
        P11_TBOX,
        False,
    ),
    (
        "p235711_691501_697000.log.gz",
        "p235711",
        691_501,
        697_000,
        P11_TBOX,
        False,
    ),
    (
        "p235711_697001_728999.log.gz",
        "p235711",
        697_001,
        728_999,
        P11_TBOX,
        False,
    ),
    (
        "p2357_729000_818999.log.gz",
        "p2357",
        729_000,
        818_999,
        LATER_TBOX,
        True,
    ),
    (
        "p235_819000_1027999.log.gz",
        "p235",
        819_000,
        1_027_999,
        LATER_TBOX,
        True,
    ),
    (
        "p23_1028000_1030000.log.gz",
        "p23",
        1_028_000,
        1_030_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_1030001_1050000.log.gz",
        "p23",
        1_030_001,
        1_050_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_1050001_1100000.log.gz",
        "p23",
        1_050_001,
        1_100_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_1100001_1300000.log.gz",
        "p23",
        1_100_001,
        1_300_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_1300001_1700000.log.gz",
        "p23",
        1_300_001,
        1_700_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_1700001_2200000.log.gz",
        "p23",
        1_700_001,
        2_200_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_2200001_2800000.log.gz",
        "p23",
        2_200_001,
        2_800_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_2800001_3300000.log.gz",
        "p23",
        2_800_001,
        3_300_000,
        LATER_TBOX,
        True,
    ),
    (
        "p23_3300001_3840000.log.gz",
        "p23",
        3_300_001,
        3_840_000,
        LATER_TBOX,
        True,
    ),
)

FILE_SPEC_BY_NAME = {
    spec[0]: spec for spec in FINITE_FILE_SPECS
}


def decimal_picounits(text: str) -> int:
    whole, fractional = text.split(".")
    if len(fractional) != 12:
        raise ValueError("L12 must have exactly 12 fractional digits")
    return int(whole) * 10**12 + int(fractional)


@dataclass(frozen=True)
class L12Segment:
    start_n: int
    values: array

    @property
    def end_n(self) -> int:
        return self.start_n + len(self.values) - 1


@dataclass(frozen=True)
class L12Series:
    start_n: int
    values: array

    @property
    def end_n(self) -> int:
        return self.start_n + len(self.values) - 1

    def value(self, index: int) -> int:
        offset = index - self.start_n
        if offset < 0 or offset >= len(self.values):
            raise ValueError("index outside stored series")
        return self.values[offset]

    def suffix_records(
        self,
        targets: Iterable[int],
    ) -> dict[int, tuple[int, int]]:
        """Return target -> (suffix floor picounits, argmin)."""

        requested = set(targets)
        if not requested:
            return {}
        if min(requested) < self.start_n or max(requested) > self.end_n:
            raise ValueError("target outside stored series")

        result: dict[int, tuple[int, int]] = {}
        minimum: int | None = None
        argmin: int | None = None
        for offset in range(len(self.values) - 1, -1, -1):
            index = self.start_n + offset
            value = self.values[offset]
            if minimum is None or value <= minimum:
                minimum = value
                argmin = index
            if index in requested:
                if minimum is None or argmin is None:
                    raise AssertionError("internal suffix state failure")
                result[index] = minimum, argmin
        if result.keys() != requested:
            raise AssertionError("not every suffix target was visited")
        return result


def _parse_stream(
    stream: TextIO,
    source: str,
    requested_t0: F,
    *,
    expected_range: tuple[int, int] | None = None,
    expected_tbox: tuple[F, F] | None = None,
    require_weight: bool | None = None,
) -> L12Segment:
    first: int | None = None
    previous: int | None = None
    values = array("q")
    run_open = False
    run_rows = 0
    weight_seen = False
    weight_policy: bool | None = None

    for line_number, raw in enumerate(stream, 1):
        line = raw.strip()
        if not line:
            continue

        tbox_match = TBOX_RE.fullmatch(line)
        if tbox_match:
            if run_open:
                raise ValueError(
                    f"{source}:{line_number}: TBOX before prior TIMING"
                )
            lower = F(tbox_match.group(1))
            upper = F(tbox_match.group(2))
            if expected_tbox is not None and (
                lower,
                upper,
            ) != expected_tbox:
                raise ValueError(
                    f"{source}:{line_number}: wrong exact TBOX"
                )
            if not lower <= requested_t0 <= upper:
                raise ValueError(
                    f"{source}:{line_number}: t0 outside stored TBOX"
                )
            run_open = True
            run_rows = 0
            weight_seen = False
            continue

        if line == "WEIGHT TRIANGLE":
            if (
                not run_open
                or weight_seen
                or run_rows
                or require_weight is False
            ):
                raise ValueError(
                    f"{source}:{line_number}: misplaced WEIGHT TRIANGLE"
                )
            weight_seen = True
            continue

        row_match = ROW_RE.fullmatch(line)
        if row_match:
            if not run_open:
                raise ValueError(
                    f"{source}:{line_number}: row outside a run"
                )
            index = int(row_match.group(1))
            if previous is not None and index != previous + 1:
                raise ValueError(
                    f"{source}:{line_number}: gap/overlap "
                    f"after N={previous}"
                )
            first = index if first is None else first
            previous = index
            values.append(decimal_picounits(row_match.group(2)))
            run_rows += 1
            continue

        uncert_match = UNCERT_RE.fullmatch(line)
        if uncert_match:
            raise ValueError(
                f"{source}:{line_number}: UNCERT N="
                f"{uncert_match.group(1)}"
            )

        timing_match = TIMING_RE.fullmatch(line)
        if timing_match:
            if not run_open:
                raise ValueError(
                    f"{source}:{line_number}: TIMING outside a run"
                )
            if run_rows == 0:
                raise ValueError(
                    f"{source}:{line_number}: empty certificate run"
                )
            if int(timing_match.group(2)) != run_rows:
                raise ValueError(
                    f"{source}:{line_number}: TIMING row-count mismatch"
                )
            if require_weight is True and not weight_seen:
                raise ValueError(
                    f"{source}:{line_number}: missing WEIGHT TRIANGLE"
                )
            if require_weight is None and weight_policy is None:
                weight_policy = weight_seen
            elif (
                require_weight is None
                and weight_seen != weight_policy
            ):
                raise ValueError(
                    f"{source}:{line_number}: inconsistent WEIGHT "
                    "TRIANGLE headers"
                )
            run_open = False
            continue

        raise ValueError(
            f"{source}:{line_number}: unparsed record {line!r}"
        )

    if run_open:
        raise ValueError(f"{source}: unterminated run")
    if first is None or not values:
        raise ValueError(f"{source}: no certified rows")
    segment = L12Segment(first, values)
    if expected_range is not None and (
        segment.start_n,
        segment.end_n,
    ) != expected_range:
        raise ValueError(
            f"{source}: range {segment.start_n}..{segment.end_n}, "
            f"expected {expected_range[0]}..{expected_range[1]}"
        )
    return segment


def parse_l12_file(path: Path, requested_t0: F) -> L12Segment:
    try:
        (
            _filename,
            _family,
            expected_lo,
            expected_hi,
            expected_tbox,
            require_weight,
        ) = FILE_SPEC_BY_NAME[path.name]
    except KeyError as exc:
        raise ValueError(
            f"unrecognized finite certificate filename: {path.name}"
        ) from exc
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return _parse_stream(
            stream,
            str(path),
            requested_t0,
            expected_range=(expected_lo, expected_hi),
            expected_tbox=expected_tbox,
            require_weight=require_weight,
        )


def load_l12_series(
    paths: Iterable[Path],
    requested_t0: F,
) -> L12Series:
    segments = sorted(
        (parse_l12_file(path, requested_t0) for path in paths),
        key=lambda segment: segment.start_n,
    )
    if not segments:
        raise ValueError("no certificate paths supplied")

    values = array("q")
    expected = segments[0].start_n
    for segment in segments:
        if segment.start_n != expected:
            raise ValueError(
                f"certificate gap/overlap: expected N={expected}, "
                f"got N={segment.start_n}"
            )
        values.extend(segment.values)
        expected = segment.end_n + 1
    return L12Series(segments[0].start_n, values)


def repository_certificate_paths(repository_root: Path) -> tuple[Path, ...]:
    directory = repository_root / "certificates"
    paths = tuple(
        directory / spec[0] for spec in FINITE_FILE_SPECS
    )
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "missing finite certificate files: " + ", ".join(missing)
        )
    return paths
