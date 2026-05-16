import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

try:
    from reportlab.lib.styles import getSampleStyleSheet
except ModuleNotFoundError:
    getSampleStyleSheet = None

try:
    from blankmath.panels.distributive_property import DistributivePropertyPanel
    from blankmath.panels.long_division import LongDivisionPanel
    from blankmath.panels.problem import page_problem_count, problem_panel
except ModuleNotFoundError:
    DistributivePropertyPanel = None
    LongDivisionPanel = None
    page_problem_count = None
    problem_panel = None


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


if __name__ == "__main__":
    unittest.main()
