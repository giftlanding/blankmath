import re
from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable

NUMBER_FONT = "Helvetica"
TEXT_FONT = "Helvetica"
MONO_FONT = "Courier"
NUMBER_FONT_SIZE = 8
EXPRESSION_FONT_SIZE = 18
STEP_FONT_SIZE = 15
PANEL_WIDTH = 7.1 * inch
PANEL_HEIGHT = 2.22 * inch


@dataclass(frozen=True)
class DistributivePropertyProblem:
    factor: int
    target: int
    base: int
    offset: int
    operation: str

    @property
    def sign(self) -> str:
        return "+" if self.operation == "+" else "-"

    @property
    def first_partial(self) -> int:
        return self.factor * self.base

    @property
    def second_partial(self) -> int:
        return self.factor * self.offset

    @property
    def answer(self) -> int:
        if self.operation == "+":
            return self.first_partial + self.second_partial
        return self.first_partial - self.second_partial


class DistributivePropertyPanel(Flowable):
    def __init__(self, problem_number: int, problem: DistributivePropertyProblem):
        super().__init__()
        self.problem_number = problem_number
        self.problem = problem
        self.width = PANEL_WIDTH
        self.height = PANEL_HEIGHT

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        left = 0.08 * inch
        content_left = 0.36 * inch
        expression_y = self.height - 0.34 * inch
        step_1_y = self.height - 0.86 * inch
        step_2_y = self.height - 1.26 * inch
        combine_y = self.height - 1.78 * inch

        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#5f6b7a"))
        canvas.setFont(NUMBER_FONT, NUMBER_FONT_SIZE)
        canvas.drawString(left, expression_y + 0.08 * inch, f"{self.problem_number}.")

        canvas.setFillColor(colors.black)
        canvas.setFont(TEXT_FONT, EXPRESSION_FONT_SIZE)
        canvas.drawString(content_left, expression_y, self._expression())

        canvas.setFont(MONO_FONT, STEP_FONT_SIZE)
        canvas.drawString(content_left + 0.18 * inch, step_1_y, f"{self.problem.factor} x {self.problem.base} =")
        self._draw_blank(canvas, content_left + 2.0 * inch, step_1_y - 0.02 * inch, 1.12 * inch)

        canvas.drawString(content_left + 0.18 * inch, step_2_y, f"{self.problem.factor} x {self.problem.offset} =")
        self._draw_blank(canvas, content_left + 2.0 * inch, step_2_y - 0.02 * inch, 1.12 * inch)

        canvas.drawString(content_left + 0.18 * inch, combine_y, f"Then:")
        self._draw_blank(canvas, content_left + 1.08 * inch, combine_y - 0.02 * inch, 0.9 * inch)
        canvas.drawString(content_left + 2.08 * inch, combine_y, self.problem.sign)
        self._draw_blank(canvas, content_left + 2.36 * inch, combine_y - 0.02 * inch, 0.9 * inch)
        canvas.drawString(content_left + 3.38 * inch, combine_y, "=")
        self._draw_blank(canvas, content_left + 3.72 * inch, combine_y - 0.02 * inch, 1.08 * inch)

        canvas.restoreState()

    def _expression(self) -> str:
        return (
            f"{self.problem.factor} x {self.problem.target} = "
            f"{self.problem.factor} x ({self.problem.base} {self.problem.sign} {self.problem.offset})"
        )

    def _draw_blank(self, canvas, x: float, y: float, width: float) -> None:
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#8b96a8"))
        canvas.setLineWidth(1.0)
        canvas.line(x, y, x + width, y)
        canvas.restoreState()


def parse_distributive_property_problem(prompt: str) -> DistributivePropertyProblem | None:
    match = re.fullmatch(r"(\d+) x (\d+) = \1 x \((\d+) ([+-]) (\d+)\)", prompt)
    if not match:
        return None

    factor_text, target_text, base_text, operation, offset_text = match.groups()
    factor = int(factor_text)
    target = int(target_text)
    base = int(base_text)
    offset = int(offset_text)
    expected_target = base + offset if operation == "+" else base - offset
    if target != expected_target:
        return None

    return DistributivePropertyProblem(
        factor=factor,
        target=target,
        base=base,
        offset=offset,
        operation=operation,
    )
