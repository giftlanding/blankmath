from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable

from blankmath.problem_formatting import VerticalProblemParts

NUMBER_FONT = "Helvetica"
OPERAND_FONT = "Courier"
NUMBER_FONT_SIZE = 8
OPERAND_FONT_SIZE = 20


class VerticalArithmeticPanel(Flowable):
    def __init__(self, problem_number: int, problem: VerticalProblemParts):
        super().__init__()
        self.problem_number = problem_number
        self.problem = problem
        self.width = 1.55 * inch
        self.height = 0.98 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        line_y = 0.25 * inch
        second_y = 0.48 * inch
        first_y = 0.72 * inch
        operand_right = self.width - 0.12 * inch

        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#5f6b7a"))
        canvas.setFont(NUMBER_FONT, NUMBER_FONT_SIZE)
        canvas.drawString(0, first_y + 0.08 * inch, f"{self.problem_number}.")

        canvas.setFillColor(colors.black)
        canvas.setFont(OPERAND_FONT, OPERAND_FONT_SIZE)
        operand_width = max(
            canvas.stringWidth(self.problem.left, OPERAND_FONT, OPERAND_FONT_SIZE),
            canvas.stringWidth(self.problem.right, OPERAND_FONT, OPERAND_FONT_SIZE),
        )
        operator_x = max(0.32 * inch, operand_right - operand_width - 0.28 * inch)

        canvas.drawRightString(operand_right, first_y, self.problem.left)
        canvas.drawString(operator_x, second_y, operator_text(self.problem.operator))
        canvas.drawRightString(operand_right, second_y, self.problem.right)
        canvas.setLineWidth(1.2)
        canvas.line(operator_x, line_y, operand_right, line_y)
        canvas.restoreState()


def operator_text(operator: str) -> str:
    if operator == "x":
        return "x"
    if operator == "/":
        return chr(247)
    return operator
