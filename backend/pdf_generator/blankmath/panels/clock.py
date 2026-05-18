import math

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable


FONT = "Helvetica"


class ClockPanel(Flowable):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem
        self.width = 3.45 * inch
        self.height = 2.15 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        center_x = self.width / 2
        center_y = 1.14 * inch
        radius = 0.58 * inch

        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setStrokeColor(colors.HexColor("#111827"))
        canvas.setLineWidth(1.2)
        canvas.circle(center_x, center_y, radius, stroke=1, fill=0)

        for number in range(1, 13):
            angle = math.radians(90 - number * 30)
            tick_outer_x = center_x + math.cos(angle) * radius
            tick_outer_y = center_y + math.sin(angle) * radius
            tick_inner_x = center_x + math.cos(angle) * (radius - 0.08 * inch)
            tick_inner_y = center_y + math.sin(angle) * (radius - 0.08 * inch)
            canvas.line(tick_inner_x, tick_inner_y, tick_outer_x, tick_outer_y)

        canvas.setFont(FONT, 8)
        for number in (12, 3, 6, 9):
            angle = math.radians(90 - number * 30)
            canvas.drawCentredString(
                center_x + math.cos(angle) * (radius - 0.18 * inch),
                center_y + math.sin(angle) * (radius - 0.2 * inch) - 3,
                str(number),
            )

        if self.problem.mode == "read":
            self._draw_hands(canvas, center_x, center_y)
            canvas.setFont(FONT, 11)
            canvas.drawString(0.28 * inch, 0.25 * inch, "Time:")
            canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
            canvas.line(0.88 * inch, 0.25 * inch, self.width - 0.28 * inch, 0.25 * inch)
        else:
            canvas.setFont(FONT, 11)
            canvas.drawCentredString(center_x, 0.27 * inch, f"Draw {self.problem.answer}")

        canvas.restoreState()

    def _draw_hands(self, canvas, center_x: float, center_y: float) -> None:
        minute_angle = math.radians(90 - self.problem.minute * 6)
        hour_angle = math.radians(90 - ((self.problem.hour % 12) * 30 + self.problem.minute * 0.5))
        canvas.setStrokeColor(colors.HexColor("#111827"))
        canvas.setLineWidth(2.0)
        canvas.line(
            center_x,
            center_y,
            center_x + math.cos(hour_angle) * 0.32 * inch,
            center_y + math.sin(hour_angle) * 0.32 * inch,
        )
        canvas.setLineWidth(1.4)
        canvas.line(
            center_x,
            center_y,
            center_x + math.cos(minute_angle) * 0.47 * inch,
            center_y + math.sin(minute_angle) * 0.47 * inch,
        )
        canvas.circle(center_x, center_y, 0.025 * inch, stroke=1, fill=1)
