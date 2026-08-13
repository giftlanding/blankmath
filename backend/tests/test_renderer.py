import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

try:
    from reportlab.lib.styles import getSampleStyleSheet
except ModuleNotFoundError:
    getSampleStyleSheet = None

try:
    from blankmath.renderer import FractionAnswer, _answer_table, _chunk_problems, _parse_fraction_answer, _problem_page_chunks
    from blankmath.worksheets.fractions import FractionProblem
except ModuleNotFoundError:
    FractionAnswer = None
    _answer_table = None
    _chunk_problems = None
    _parse_fraction_answer = None
    _problem_page_chunks = None
    FractionProblem = None


class RendererTest(unittest.TestCase):
    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_fraction_answer_table_uses_stacked_fraction_cells(self):
        style = getSampleStyleSheet()["Normal"]
        problems = [
            FractionProblem("1/2 + 1/3 = ?", "5/6", 1, 2, right_numerator=1, right_denominator=3, operator="add"),
            FractionProblem("10 3/5 x 4 = ?", "42 2/5", 3, 5, left_whole=10, right_whole=4, operator="multiply"),
            FractionProblem("1/2 ____ 1/3", ">", 1, 2, right_numerator=1, right_denominator=3, operator="compare"),
        ]

        table = _answer_table(problems, style, "fraction")

        self.assertTrue(all(height > 30 for height in table._rowHeights))
        self.assertIsInstance(table._cellvalues[0][0], FractionAnswer)
        self.assertIsInstance(table._cellvalues[0][1], FractionAnswer)
        self.assertIsInstance(table._cellvalues[0][2], FractionAnswer)

    def test_parse_fraction_answer_supports_simple_and_mixed_answers(self):
        self.assertEqual(_parse_fraction_answer("5/6"), (None, 5, 6))
        self.assertEqual(_parse_fraction_answer("42 2/5"), (42, 2, 5))
        self.assertEqual(_parse_fraction_answer(">"), (None, None, None))

    def test_fraction_page_capacity_does_not_create_extra_versions(self):
        problems = [
            FractionProblem("1/2 + 1/3 = ?", "5/6", 1, 2, right_numerator=1, right_denominator=3, operator="add")
            for _ in range(40)
        ]

        versions = _chunk_problems(problems, 20)
        pages = [_problem_page_chunks(version, 12) for version in versions]

        self.assertEqual([len(version) for version in versions], [20, 20])
        self.assertEqual([[len(page) for _, page in version_pages] for version_pages in pages], [[12, 8], [12, 8]])


if __name__ == "__main__":
    unittest.main()
