import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

try:
    from reportlab.lib.styles import getSampleStyleSheet
except ModuleNotFoundError:
    getSampleStyleSheet = None

try:
    from blankmath.panels.breaking_parentheses import BreakingParenthesesPanel
    from blankmath.panels.chicken_rabbit import ChickenRabbitPanel
    from blankmath.panels.clock import ClockPanel
    from blankmath.panels.distributive_property import DistributivePropertyPanel
    from blankmath.panels.fraction import FractionPanel
    from blankmath.panels.long_division import LongDivisionPanel
    from blankmath.panels.number_line import NumberLinePanel
    from blankmath.panels.place_value import PlaceValuePanel
    from blankmath.panels.problem import page_problem_count, problem_panel
    from blankmath.worksheets.chicken_rabbit import generate_chicken_rabbit_problem
    from blankmath.worksheets.number_lines import missing_labels
    from blankmath.worksheets.time import read_clock
except ModuleNotFoundError:
    BreakingParenthesesPanel = None
    ChickenRabbitPanel = None
    ClockPanel = None
    DistributivePropertyPanel = None
    FractionPanel = None
    LongDivisionPanel = None
    NumberLinePanel = None
    PlaceValuePanel = None
    page_problem_count = None
    problem_panel = None
    generate_chicken_rabbit_problem = None
    missing_labels = None
    read_clock = None


class PanelsTest(unittest.TestCase):
    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_long_division_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]

        panel = problem_panel(1, "120 / 12 = ?", style, "long_division")

        self.assertIsInstance(panel, LongDivisionPanel)
        self.assertEqual(page_problem_count(20, "long_division"), 6)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_distributive_property_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]

        panel = problem_panel(1, "600 x 99 = 600 x (100 - 1)", style, "distributive_property")

        self.assertIsInstance(panel, DistributivePropertyPanel)
        self.assertEqual(page_problem_count(20, "distributive_property"), 3)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_breaking_parentheses_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]

        panel = problem_panel(1, "21 - (8 + 9)", style, "breaking_parentheses")

        self.assertIsInstance(panel, BreakingParenthesesPanel)
        self.assertEqual(page_problem_count(20, "breaking_parentheses"), 12)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_chicken_rabbit_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]
        problem = generate_chicken_rabbit_problem({"numberSize": "small"})

        panel = problem_panel(1, problem, style, "chicken_rabbit")

        self.assertIsInstance(panel, ChickenRabbitPanel)
        self.assertEqual(page_problem_count(10, "chicken_rabbit"), 3)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_place_value_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]

        panel = problem_panel(1, "4,582 =", style, "place_value")

        self.assertIsInstance(panel, PlaceValuePanel)
        self.assertEqual(page_problem_count(20, "place_value"), 10)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_fraction_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]

        panel = problem_panel(1, "2/3 =", style, "fraction")

        self.assertIsInstance(panel, FractionPanel)
        self.assertEqual(page_problem_count(20, "fraction"), 12)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_number_line_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]
        problem = missing_labels({"numberLineSize": "small"})

        panel = problem_panel(1, problem, style, "number_line")

        self.assertIsInstance(panel, NumberLinePanel)
        self.assertEqual(page_problem_count(8, "number_line"), 5)

    @unittest.skipIf(getSampleStyleSheet is None, "ReportLab is not installed")
    def test_clock_layout_uses_dedicated_panel(self):
        style = getSampleStyleSheet()["Normal"]
        problem = read_clock({"timeIncrement": "five_minutes"})

        panel = problem_panel(1, problem, style, "clock")

        self.assertIsInstance(panel, ClockPanel)
        self.assertEqual(page_problem_count(8, "clock"), 6)


if __name__ == "__main__":
    unittest.main()
