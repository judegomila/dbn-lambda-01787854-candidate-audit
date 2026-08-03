"""Unit tests for the unsealed dynamic-boundary research package."""

from __future__ import annotations

from fractions import Fraction as F
import io
from pathlib import Path
import tempfile
import unittest

from .analysis import rank_targets
from .certificates import (
    L12Series,
    _parse_stream,
    decimal_picounits,
)
from .core import (
    CANDIDATE,
    ERROR_MAX,
    certify_published_landing,
    certify_steered_landing,
    published_fixed_anchor,
    steered_terminal_anchor,
)
from .exact import pi_bounds, sqrt_bounds
from .steering import (
    linear_path,
    smoothstep5_path,
    smoothstep5_peak_speed,
)
from .validate_barrier_transcript import decimal_ball, validate


class ExactGeometryTests(unittest.TestCase):
    def test_candidate_identities(self) -> None:
        self.assertEqual(
            CANDIDATE.lambda_bound,
            F(893_927, 5_000_000),
        )
        self.assertEqual(
            CANDIDATE.curved_width_sq,
            F(1_606_073, 2_500_000),
        )
        for step in range(33):
            time = CANDIDATE.t0 * F(step, 32)
            self.assertEqual(
                CANDIDATE.upper_y_sq(time)
                - CANDIDATE.lower_y_sq(time),
                CANDIDATE.curved_width_sq,
            )

    def test_pi_and_sqrt_bounds(self) -> None:
        pi_lower, pi_upper = pi_bounds()
        self.assertLess(pi_lower, F(3_141_593, 1_000_000))
        self.assertGreater(pi_upper, F(3_141_592, 1_000_000))
        lower, upper = sqrt_bounds(F(2), 50)
        self.assertLessEqual(lower * lower, 2)
        self.assertGreaterEqual(upper * upper, 2)
        self.assertLess(upper - lower, F(1, 10**49))

    def test_box_parameterization_slacks(self) -> None:
        for tstep in range(9):
            time = CANDIDATE.t0 * F(tstep, 8)
            for rstep in range(9):
                radial = F(rstep, 8)
                for sstep in range(9):
                    transverse = F(sstep, 8)
                    self.assertGreaterEqual(
                        CANDIDATE.cone_slack(
                            time, radial, transverse
                        ),
                        0,
                    )
                    self.assertGreaterEqual(
                        CANDIDATE.ceiling_slack(time, radial),
                        0,
                    )
                    if transverse == 1:
                        self.assertEqual(
                            CANDIDATE.cone_slack(
                                time, radial, transverse
                            ),
                            0,
                        )


class LandingTests(unittest.TestCase):
    def test_fixed_pt_budget_reaches_691008_not_691009(self) -> None:
        anchor_008 = published_fixed_anchor(691_008)
        landing_008 = certify_published_landing(691_008, anchor_008)
        self.assertTrue(landing_008.certified)

        anchor_009 = published_fixed_anchor(691_009)
        landing_009 = certify_published_landing(691_009, anchor_009)
        self.assertFalse(landing_009.certified)
        self.assertLess(landing_009.verified_anchor_slack, 0)

    def test_steered_terminal_anchor_regression(self) -> None:
        anchor = steered_terminal_anchor(691_008)
        self.assertEqual(anchor, 6_000_342_141_913)
        landing = certify_steered_landing(691_008, anchor)
        self.assertGreater(landing.left_margin_lower, 0)
        self.assertGreater(landing.right_margin_lower, 17_000_000)
        self.assertGreater(landing.verified_anchor_slack, 8_000_000)


class SteeringTests(unittest.TestCase):
    def test_linear_and_smoothstep(self) -> None:
        start = F(CANDIDATE.anchor)
        end = F(steered_terminal_anchor(690_989))
        linear = linear_path(start, end, CANDIDATE.t0)
        self.assertEqual(linear.evaluate(0), start)
        self.assertEqual(linear.evaluate(CANDIDATE.t0), end)
        self.assertEqual(
            linear.derivative(0),
            (end - start) / CANDIDATE.t0,
        )

        smooth = smoothstep5_path(start, end, CANDIDATE.t0)
        self.assertEqual(smooth.derivative(0), 0)
        self.assertEqual(smooth.derivative(CANDIDATE.t0), 0)
        self.assertEqual(
            smooth.derivative(CANDIDATE.t0 / 2),
            smoothstep5_peak_speed(start, end, CANDIDATE.t0),
        )

    def test_next_window_steering_is_millions(self) -> None:
        target = steered_terminal_anchor(690_989)
        shift = target - CANDIDATE.anchor
        self.assertGreater(shift, 11_900_000)
        self.assertLess(shift, 12_100_000)


class CertificateTests(unittest.TestCase):
    def test_strict_multi_run_parser(self) -> None:
        text = """\
TBOX 16125/100000 16125/100000
WEIGHT TRIANGLE
N 690988 L12 0.000000791366 GT089 0
TIMING 1.0 1
TBOX 16125/100000 16125/100000
WEIGHT TRIANGLE
N 690989 L12 0.000000974062 GT089 0
N 690990 L12 0.000001570095 GT089 0
TIMING 2.0 2
"""
        segment = _parse_stream(
            io.StringIO(text), "fixture", CANDIDATE.t0
        )
        self.assertEqual(segment.start_n, 690_988)
        self.assertEqual(segment.end_n, 690_990)
        self.assertEqual(
            list(segment.values),
            [791_366, 974_062, 1_570_095],
        )

    def test_parser_rejects_uncert_and_gap(self) -> None:
        uncert = """\
TBOX 16125/100000 16125/100000
N 690988 UNCERT GT089 0
TIMING 1.0 1
"""
        with self.assertRaisesRegex(ValueError, "UNCERT"):
            _parse_stream(
                io.StringIO(uncert), "uncert", CANDIDATE.t0
            )

        gap = """\
TBOX 16125/100000 16125/100000
N 690988 L12 0.000000791366 GT089 0
N 690990 L12 0.000001570095 GT089 0
TIMING 1.0 2
"""
        with self.assertRaisesRegex(ValueError, "gap/overlap"):
            _parse_stream(io.StringIO(gap), "gap", CANDIDATE.t0)

        inconsistent_weight = """\
TBOX 16125/100000 16125/100000
N 690988 L12 0.000000791366 GT089 0
TIMING 1.0 1
TBOX 16125/100000 16125/100000
WEIGHT TRIANGLE
N 690989 L12 0.000000974062 GT089 0
TIMING 1.0 1
"""
        with self.assertRaisesRegex(ValueError, "inconsistent WEIGHT"):
            _parse_stream(
                io.StringIO(inconsistent_weight),
                "weight",
                CANDIDATE.t0,
            )

        missing_required_weight = """\
TBOX 161250000/1000000000 161250001/1000000000
N 729000 L12 0.000315112459 GT089 0
TIMING 1.0 1
"""
        with self.assertRaisesRegex(ValueError, "missing WEIGHT"):
            _parse_stream(
                io.StringIO(missing_required_weight),
                "required-weight",
                CANDIDATE.t0,
                expected_tbox=(
                    F(161_250_000, 10**9),
                    F(161_250_001, 10**9),
                ),
                require_weight=True,
            )

        with self.assertRaisesRegex(ValueError, "wrong exact TBOX"):
            _parse_stream(
                io.StringIO(missing_required_weight),
                "wrong-tbox",
                CANDIDATE.t0,
                expected_tbox=(CANDIDATE.t0, CANDIDATE.t0),
                require_weight=True,
            )

    def test_suffix_floor_not_single_row(self) -> None:
        from array import array

        series = L12Series(
            690_988,
            array("q", [791_366, 2_000_000, 1_500_000, 3_000_000]),
        )
        records = series.suffix_records([690_988, 690_989, 690_990])
        self.assertEqual(records[690_989], (1_500_000, 690_990))
        self.assertEqual(records[690_990], (1_500_000, 690_990))

    def test_pilot_margin_regression(self) -> None:
        from array import array

        # Exact rows decoded from the first two sealed P11 shards at
        # repository commit 16148718742023ebf16598a3e598d7d97b08914d.
        values = [
            791_366,
            974_062,
            1_570_095,
            1_891_132,
            2_347_687,
            2_662_370,
            3_118_922,
            3_354_765,
            4_185_565,
            4_315_413,
            4_800_573,
            5_115_253,
            5_616_965,
            5_746_814,
            6_313_380,
            6_443_228,
            6_899_772,
            7_325_439,
            7_781_981,
            7_911_829,
            8_478_389,
        ]
        series = L12Series(690_988, array("q", values))
        record = rank_targets(series, [691_008])[0]
        self.assertEqual(record.suffix_floor_picounits, 8_478_389)
        self.assertEqual(
            record.finite_margin,
            F(8_478_389, 10**12) - ERROR_MAX,
        )
        self.assertTrue(record.fixed_reachable)
        self.assertGreater(record.gain_over_current, 14)

    def test_decimal_parser(self) -> None:
        self.assertEqual(decimal_picounits("0.000008478389"), 8_478_389)
        with self.assertRaises(ValueError):
            decimal_picounits("0.00000847838")


class BarrierLogTests(unittest.TestCase):
    def test_decimal_ball_rejects_nonfinite_tokens(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            decimal_ball("NaN")
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            decimal_ball("Infinity")

    def test_structural_validator(self) -> None:
        log = """\
Closed target enclosure: [0.16125 +/- 1e-40]; N-corners=691008,691008; H/B approximation allowance=[0.00125 +/- 1e-40]
Prism(1) t=[0,0.1] winding=0 min_mesh=1 Dz=1 Dt=1 spatial=0.1 time=0.1 eps=0.00125 margin=0.7 mesh=8 PASS
Prism(2) t=[0.1,0.16125] winding=0 min_mesh=1 Dz=1 Dt=1 spatial=0.1 time=0.1 eps=0.00125 margin=0.7 mesh=8 PASS
RESULT: CLOSED SLAB CERTIFIED
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "barrier.log"
            path.write_text(log, encoding="utf-8")
            self.assertEqual(validate(path, 691_008), 0)

            path.write_text(
                log.replace(
                    "Prism(2) t=[0.1,0.16125]",
                    "Prism(2) t=[0.11,0.16125]",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "seam"):
                validate(path, 691_008)

            path.write_text(
                log.replace("margin=0.7", "margin=-0.1", 1),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "nonpositive margin"):
                validate(path, 691_008)


if __name__ == "__main__":
    unittest.main()
