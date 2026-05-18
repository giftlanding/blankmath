from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable


FONT = "Helvetica"
FRACTION_FONT_SIZE = 16
LABEL_FONT_SIZE = 9


class FractionPanel(Flowable):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem
        self.width = 3.45 * inch
        self.height = 1.05 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        left_numerator = getattr(self.problem, "left_numerator", None)
        left_denominator = getattr(self.problem, "left_denominator", None)
        right_numerator = getattr(self.problem, "right_numerator", None)
        right_denominator = getattr(self.problem, "right_denominator", None)
        operator = getattr(self.problem, "operator", "")
        if left_numerator is None or left_denominator is None:
            left_numerator, left_denominator = _parse_first_fraction(getattr(self.problem, "prompt", str(self.problem)))

        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
        canvas.setLineWidth(1.0)

        center_y = 0.55 * inch
        if operator == "compare":
            self._draw_fraction(canvas, 0.62 * inch, center_y, left_numerator, left_denominator)
            self._draw_blank(canvas, self.width / 2 - 0.23 * inch, center_y - 0.02 * inch, 0.46 * inch)
            self._draw_fraction(canvas, self.width - 0.62 * inch, center_y, right_numerator, right_denominator)
        else:
            self._draw_fraction(canvas, 0.72 * inch, center_y, left_numerator, left_denominator)
            canvas.setFont(FONT, FRACTION_FONT_SIZE)
            canvas.drawCentredString(1.5 * inch, center_y - 0.07 * inch, "=")
            self._draw_blank(canvas, 1.92 * inch, center_y - 0.02 * inch, self.width - 2.18 * inch)

        canvas.restoreState()

    def _draw_fraction(self, canvas, center_x: float, center_y: float, numerator: int, denominator: int) -> None:
        numerator_text = str(numerator)
        denominator_text = str(denominator)
        canvas.setFont(FONT, FRACTION_FONT_SIZE)
        fraction_width = max(
            canvas.stringWidth(numerator_text, FONT, FRACTION_FONT_SIZE),
            canvas.stringWidth(denominator_text, FONT, FRACTION_FONT_SIZE),
            0.28 * inch,
        ) + 0.12 * inch
        canvas.drawCentredString(center_x, center_y + 0.14 * inch, numerator_text)
        canvas.line(center_x - fraction_width / 2, center_y + 0.08 * inch, center_x + fraction_width / 2, center_y + 0.08 * inch)
        canvas.drawCentredString(center_x, center_y - 0.14 * inch, denominator_text)

    def _draw_blank(self, canvas, x: float, y: float, width: float) -> None:
        canvas.line(x, y, x + width, y)


def _parse_first_fraction(text: str) -> tuple[int, int]:
    token = text.split()[0]
    numerator, denominator = token.split("/")
    return int(numerator), int(denominator)
