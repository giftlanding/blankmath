from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, Paragraph


class ChickenRabbitPanel(Flowable):
    def __init__(self, problem):
        super().__init__()
        self.problem = problem
        self.width = 7.1 * inch
        self.height = 2.35 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#d9dee8"))
        canvas.setLineWidth(0.6)
        canvas.roundRect(0, 0, self.width, self.height, 5, stroke=1, fill=0)

        prompt_style = ParagraphStyle(
            "ChickenRabbitPrompt",
            fontName="Helvetica",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#111827"),
        )
        prompt = Paragraph(self.problem.prompt, prompt_style)
        prompt_width = self.width - 0.36 * inch
        _, prompt_height = prompt.wrap(prompt_width, 0.78 * inch)
        prompt.drawOn(canvas, 0.18 * inch, self.height - 0.18 * inch - prompt_height)

        label_y = self.height - 1.12 * inch
        canvas.setFont("Helvetica", 11.5)
        canvas.setFillColor(colors.HexColor("#111827"))
        first_label = f"{self.problem.item_a}:"
        second_label = f"{self.problem.item_b}:"
        canvas.drawString(0.22 * inch, label_y, first_label)
        canvas.drawString(3.65 * inch, label_y, second_label)

        canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
        canvas.setLineWidth(1.0)
        canvas.line(1.45 * inch, label_y - 0.03 * inch, 3.1 * inch, label_y - 0.03 * inch)
        canvas.line(4.9 * inch, label_y - 0.03 * inch, self.width - 0.22 * inch, label_y - 0.03 * inch)

        work_top = label_y - 0.34 * inch
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.HexColor("#5b616e"))
        canvas.drawString(0.22 * inch, work_top, "Work:")
        canvas.setStrokeColor(colors.HexColor("#c6ceda"))
        for index in range(4):
            y = work_top - (0.25 + index * 0.26) * inch
            canvas.line(0.22 * inch, y, self.width - 0.22 * inch, y)

        canvas.restoreState()
