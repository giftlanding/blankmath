from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable


FONT = "Helvetica"


class NumberLinePanel(Flowable):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem
        self.width = 7.1 * inch
        self.height = 1.42 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        inset = 0.34 * inch
        line_y = 0.68 * inch
        label_y = 0.26 * inch
        left = inset
        right = self.width - inset
        labels = self.problem.labels
        interval = (right - left) / (len(labels) - 1)

        canvas.saveState()
        canvas.setFont(FONT, 10)
        canvas.setFillColor(colors.HexColor("#5b616e"))
        canvas.drawString(inset, self.height - 0.26 * inch, "Fill in the missing numbers.")

        canvas.setStrokeColor(colors.HexColor("#111827"))
        canvas.setLineWidth(1.3)
        canvas.line(left, line_y, right, line_y)
        canvas.line(right, line_y, right - 0.09 * inch, line_y + 0.05 * inch)
        canvas.line(right, line_y, right - 0.09 * inch, line_y - 0.05 * inch)

        for index, label in enumerate(labels):
            x = left + index * interval
            canvas.line(x, line_y - 0.08 * inch, x, line_y + 0.08 * inch)
            if label is None:
                canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
                canvas.line(x - 0.2 * inch, label_y, x + 0.2 * inch, label_y)
                canvas.setStrokeColor(colors.HexColor("#111827"))
            else:
                canvas.setFillColor(colors.black)
                canvas.setFont(FONT, 12)
                canvas.drawCentredString(x, label_y - 0.04 * inch, str(label))

        canvas.restoreState()
