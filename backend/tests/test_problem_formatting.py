import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.problem_formatting import (
    VerticalProblemParts,
    horizontal_problem_markup,
    parse_vertical_problem,
    problem_markup,
    vertical_problem_markup,
)


class ProblemFormattingTest(unittest.TestCase):
    def test_horizontal_markup_uses_math_symbols(self):
        self.assertEqual(
            horizontal_problem_markup("8 x 9 = ?"),
            "8 &times; 9 = <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>",
        )
        self.assertEqual(
            horizontal_problem_markup("8 / 2 = ?"),
            "8 &divide; 2 = <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>",
        )
        self.assertEqual(
            problem_markup(1, "8 / 2 = ?", "horizontal"),
            '<font size="8" color="#5f6b7a">1.</font>&nbsp;<font size="18">8 &divide; 2 = <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></font>',
        )
        self.assertEqual(
            problem_markup(1, "8 / 2 = ?", "equation"),
            '<font size="8" color="#5f6b7a">1.</font>&nbsp;<font size="18">8 &divide; 2 = <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></font>',
        )

    def test_vertical_markup_formats_standard_binary_problem(self):
        self.assertEqual(
            vertical_problem_markup("12 + 9 = ?"),
            '<font size="18">12</font><br/><font size="18">+ 9</font><br/><font size="18"><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></font>',
        )
        self.assertEqual(
            vertical_problem_markup("8 x 9 = ?"),
            '<font size="18">8</font><br/><font size="18">&times; 9</font><br/><font size="18"><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></font>',
        )

    def test_parses_standard_vertical_problem_parts(self):
        self.assertEqual(parse_vertical_problem("120 / 12 = ?"), VerticalProblemParts("120", "/", "12"))
        self.assertIsNone(parse_vertical_problem("8 x ____ = 72"))

    def test_vertical_markup_falls_back_for_missing_number_problem(self):
        self.assertIsNone(vertical_problem_markup("8 x ____ = 72"))
        self.assertEqual(
            problem_markup(1, "8 x ____ = 72", "vertical"),
            '<font size="8" color="#5f6b7a">1.</font>&nbsp;<font size="18">8 &times; ____ = 72</font>',
        )


if __name__ == "__main__":
    unittest.main()
