from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable

from blankmath.problem_formatting import VerticalProblemParts

NUMBER_FONT = "Helvetica"
OPERAND_FONT = "Courier"
NUMBER_FONT_SIZE = 8
OPERAND_FONT_SIZE = 24
PANEL_WIDTH = 3.35 * inch
PANEL_HEIGHT = 2.16 * inch

DIVIDEND_Y = 1.55 * inch
QUOTIENT_LINE_Y = 1.88 * inch
WORK_LINE_YS = (1.15 * inch, 0.82 * inch, 0.49 * inch, 0.16 * inch)
BRACKET_X = 1.0 * inch
DIVIDEND_X_OFFSET = 0.34 * inch
DIVISOR_GAP = 0.08 * inch
BRACKET_BOTTOM_Y = 1.18 * inch


class LongDivisionPanel(Flowable):
    def __init__(self, problem_number: int, problem: VerticalProblemParts):
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
        bracket_x = BRACKET_X
        dividend_x = bracket_x + DIVIDEND_X_OFFSET
        dividend_right = min(self.width - 0.18 * inch, dividend_x + 1.45 * inch)
        divisor_right = bracket_x - DIVISOR_GAP

        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#5f6b7a"))
        canvas.setFont(NUMBER_FONT, NUMBER_FONT_SIZE)
        canvas.drawString(0, self.height - 0.16 * inch, f"{self.problem_number}.")

        canvas.setFillColor(colors.black)
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(1.2)
        canvas.setFont(OPERAND_FONT, OPERAND_FONT_SIZE)
        canvas.drawRightString(divisor_right, DIVIDEND_Y, self.problem.right)
        canvas.drawString(dividend_x, DIVIDEND_Y, self.problem.left)
        draw_long_division_sign(canvas, bracket_x, dividend_x, dividend_right)

        canvas.setStrokeColor(colors.HexColor("#d8dde6"))
        canvas.setLineWidth(0.6)
        for work_line_y in WORK_LINE_YS:
            canvas.line(dividend_x, work_line_y, dividend_right, work_line_y)
        canvas.restoreState()


def draw_long_division_sign(canvas, bracket_x: float, dividend_x: float, dividend_right: float) -> None:
    sign_x = dividend_x - 0.14 * inch
    canvas.line(sign_x, QUOTIENT_LINE_Y, dividend_right, QUOTIENT_LINE_Y)

    path = canvas.beginPath()
    path.moveTo(sign_x, QUOTIENT_LINE_Y)
    path.curveTo(
        sign_x + 0.11 * inch,
        QUOTIENT_LINE_Y - 0.20 * inch,
        sign_x + 0.11 * inch,
        BRACKET_BOTTOM_Y + 0.20 * inch,
        sign_x,
        BRACKET_BOTTOM_Y,
    )
    canvas.drawPath(path, stroke=1, fill=0)
