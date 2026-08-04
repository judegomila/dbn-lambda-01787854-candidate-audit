"""Tests for the improved-bound lane scaffold.

These assert the lane's *conventions*, not its mathematics -- there is no
mathematics yet.  They exist so the conventions cannot quietly regress
while the reduction is being written.
"""

from __future__ import annotations

from fractions import Fraction as F
import os
from pathlib import Path
import tempfile
import unittest

from . import cli, core, report


class TestInvocationIsRecorded(unittest.TestCase):
    """The prop43 lesson, enforced."""

    def test_invocation_line_quotes_arguments(self) -> None:
        line = report.invocation_line(["prog", "a b", "c'd"])
        self.assertTrue(line.startswith("INVOCATION: "))
        self.assertIn("'a b'", line)

    def test_report_first_line_is_the_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            os.environ[report.OUTPUT_DIR_ENV] = name
            try:
                path = report.write_report("t.txt", ["body"], argv=["prog", "--x", "1"])
                first = path.read_text(encoding="utf-8").splitlines()[0]
            finally:
                del os.environ[report.OUTPUT_DIR_ENV]
        self.assertEqual(first, "INVOCATION: prog --x 1")

    def test_report_carries_the_unsealed_status(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            os.environ[report.OUTPUT_DIR_ENV] = name
            try:
                path = report.write_report("t.txt", ["body"], argv=["prog"])
                text = path.read_text(encoding="utf-8")
            finally:
                del os.environ[report.OUTPUT_DIR_ENV]
        self.assertIn("UNSEALED RESEARCH ONLY", text)


class TestOutputIsRedirectable(unittest.TestCase):
    """The prop410 lesson: the container mounts the repo read-only."""

    def test_env_var_redirects_the_report(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            os.environ[report.OUTPUT_DIR_ENV] = name
            try:
                path = report.write_report("t.txt", [], argv=["prog"])
            finally:
                del os.environ[report.OUTPUT_DIR_ENV]
            self.assertEqual(path.parent, Path(name))

    def test_default_is_the_lane_runs_directory(self) -> None:
        os.environ.pop(report.OUTPUT_DIR_ENV, None)
        self.assertEqual(report.output_dir().name, "runs")


class TestFailClosed(unittest.TestCase):
    """An unimplemented result must raise, never return a placeholder."""

    def test_improved_bound_raises_until_implemented(self) -> None:
        with self.assertRaises(core.ReductionError):
            core.improved_bound()

    def test_compare_rejects_inexact_input(self) -> None:
        with self.assertRaises(core.ReductionError):
            core.compare_to_certified(0.1787854)  # type: ignore[arg-type]


class TestComparisonIsExact(unittest.TestCase):
    def test_certified_bound_value(self) -> None:
        self.assertEqual(core.certified_bound(), F(893927, 5000000))

    def test_equal_is_not_an_improvement(self) -> None:
        result = core.compare_to_certified(F(893927, 5000000))
        self.assertFalse(result["strictly_better"])
        self.assertEqual(result["margin"], F(0))

    def test_smaller_is_an_improvement(self) -> None:
        result = core.compare_to_certified(F(893000, 5000000))
        self.assertTrue(result["strictly_better"])
        self.assertGreater(result["margin"], F(0))


class TestCli(unittest.TestCase):
    def test_status_exits_zero_and_certifies_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            os.environ[report.OUTPUT_DIR_ENV] = name
            try:
                self.assertEqual(cli.main(["status"]), 0)
            finally:
                del os.environ[report.OUTPUT_DIR_ENV]

    def test_compare_runs(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            os.environ[report.OUTPUT_DIR_ENV] = name
            try:
                self.assertEqual(cli.main(["compare", "893000/5000000"]), 0)
            finally:
                del os.environ[report.OUTPUT_DIR_ENV]


if __name__ == "__main__":
    unittest.main()
