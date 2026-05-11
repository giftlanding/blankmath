import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.problem_formatting import horizontal_problem_markup, problem_markup, vertical_problem_markup


class ProblemFormattingTest(unittest.TestCase):
    def test_horizontal_markup_uses_math_symbols(self):
        self.assertEqual(horizontal_problem_markup("8 x 9 = ?"), "8 &times; 9 = ?")
        self.assertEqual(horizontal_problem_markup("8 / 2 = ?"), "8 &divide; 2 = ?")

    def test_vertical_markup_formats_standard_binary_problem(self):
        self.assertEqual(vertical_problem_markup("12 + 9 = ?"), "12<br/>+ 9<br/>____")
        self.assertEqual(vertical_problem_markup("8 x 9 = ?"), "8<br/>&times; 9<br/>____")

    def test_vertical_markup_falls_back_for_missing_number_problem(self):
        self.assertIsNone(vertical_problem_markup("8 x ____ = 72"))
        self.assertEqual(problem_markup(1, "8 x ____ = 72", "vertical"), "1. 8 &times; ____ = 72")


if __name__ == "__main__":
    unittest.main()
