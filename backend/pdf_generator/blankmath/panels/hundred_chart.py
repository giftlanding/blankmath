from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable


FONT = "Helvetica"


class HundredChartPanel(Flowable):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem
        self.width = 7.1 * inch
        self.height = 5.95 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        top = self.height - 0.34 * inch
        left = 0.32 * inch
        grid_size = min(self.width - 0.64 * inch, self.height - 0.72 * inch)
        cell = grid_size / 10

        canvas.saveState()
        canvas.setFont(FONT, 10)
        canvas.setFillColor(colors.HexColor("#5b616e"))
        canvas.drawString(left, self.height - 0.18 * inch, self.problem.prompt)

        canvas.setStrokeColor(colors.HexColor("#c6ceda"))
        canvas.setLineWidth(0.6)
        for row in range(11):
            y = top - row * cell
            canvas.line(left, y, left + grid_size, y)
        for column in range(11):
            x = left + column * cell
            canvas.line(x, top, x, top - grid_size)

        canvas.setFont(FONT, 9)
        canvas.setFillColor(colors.black)
        for index, value in enumerate(self.problem.values):
            row = index // 10
            column = index % 10
            cell_x = left + column * cell
            cell_y = top - (row + 1) * cell
            if value is None:
                canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
                canvas.line(cell_x + 0.12 * cell, cell_y + 0.32 * cell, cell_x + 0.88 * cell, cell_y + 0.32 * cell)
            else:
                canvas.drawCentredString(cell_x + cell / 2, cell_y + 0.35 * cell, str(value))

        canvas.restoreState()
