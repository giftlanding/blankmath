from dataclasses import dataclass

from reportlab.lib.units import inch
from reportlab.platypus import Paragraph

from blankmath.panels.long_division import LongDivisionPanel
from blankmath.panels.vertical_arithmetic import VerticalArithmeticPanel
from blankmath.problem_formatting import parse_vertical_problem, problem_markup


@dataclass(frozen=True)
class PanelGrid:
    columns: int
    row_height: float | None
    left_padding: float
    right_padding: float
    top_padding: float
    bottom_padding: float


def panel_grid(layout: str, problem_count: int) -> PanelGrid:
    if layout == "long_division":
        return PanelGrid(
            columns=2,
            row_height=2.35 * inch,
            left_padding=12,
            right_padding=12,
            top_padding=6,
            bottom_padding=6,
        )

    if layout == "vertical":
        return PanelGrid(
            columns=4,
            row_height=2.0 * inch,
            left_padding=10,
            right_padding=10,
            top_padding=8,
            bottom_padding=8,
        )

    return PanelGrid(
        columns=2 if problem_count <= 20 else 3,
        row_height=None,
        left_padding=14,
        right_padding=14,
        top_padding=16,
        bottom_padding=16,
    )


def page_problem_count(count_per_page: int, layout: str) -> int:
    if layout == "long_division":
        return min(count_per_page, 6)
    if layout == "vertical":
        return min(count_per_page, 16)
    return count_per_page


def problem_panel(problem_number: int, prompt: str, style, layout: str):
    if layout == "long_division":
        division_problem = parse_vertical_problem(prompt)
        if division_problem and division_problem.operator == "/":
            return LongDivisionPanel(problem_number, division_problem)

    if layout == "vertical":
        vertical_problem = parse_vertical_problem(prompt)
        if vertical_problem:
            return VerticalArithmeticPanel(problem_number, vertical_problem)

    return Paragraph(problem_markup(problem_number, prompt, layout), style)
