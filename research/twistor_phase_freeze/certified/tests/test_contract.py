from fractions import Fraction as F
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_exact_target(self):
        y = F(1809, 10000)
        t = F(24727519, 200000000)
        self.assertEqual(t + y * y / 2, F(7, 50))
        self.assertLess(t, F(129, 800))

    def test_source_is_explicitly_negative(self):
        source_dir = ROOT / "src"
        text = "".join(
            path.read_text()
            for path in sorted(source_dir.glob("coupled_scalar_obstruction_014*"))
        )
        self.assertIn("does NOT certify Lambda <= 0.14", text)
        self.assertIn("CERTIFIED SCALAR OBSTRUCTION", text)

    def test_parser_is_fail_closed(self):
        text = (ROOT / "verifiers/verify_coupled_scalar_logs.py").read_text()
        self.assertIn("required marker count != 1", text)
        self.assertIn("refusing precision below 256 bits", text)


if __name__ == "__main__":
    unittest.main()
