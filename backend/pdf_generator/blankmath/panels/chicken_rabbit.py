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
        inset = 0.2 * inch
        right_edge = self.width - inset
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
        prompt_width = self.width - (inset * 2)
        _, prompt_height = prompt.wrap(prompt_width, 0.78 * inch)
        prompt.drawOn(canvas, inset, self.height - 0.18 * inch - prompt_height)

        label_y = self.height - 1.12 * inch
        canvas.setFont("Helvetica", 11.5)
        canvas.setFillColor(colors.HexColor("#111827"))
        middle_gap = 0.28 * inch
        column_width = (self.width - inset * 2 - middle_gap) / 2
        second_column_x = inset + column_width + middle_gap
        self._draw_answer_blank(canvas, f"{self.problem.item_a}:", inset, label_y, column_width)
        self._draw_answer_blank(canvas, f"{self.problem.item_b}:", second_column_x, label_y, column_width)

        work_top = label_y - 0.34 * inch
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.HexColor("#5b616e"))
        canvas.drawString(inset, work_top, "Work:")
        canvas.setStrokeColor(colors.HexColor("#c6ceda"))
        for index in range(4):
            y = work_top - (0.25 + index * 0.26) * inch
            canvas.line(inset, y, right_edge, y)

        canvas.restoreState()

    def _draw_answer_blank(self, canvas, label: str, x: float, y: float, width: float) -> None:
        font_size = 11.5
        canvas.setFont("Helvetica", font_size)
        label_width = canvas.stringWidth(label, "Helvetica", font_size)
        min_line_width = 0.58 * inch
        max_label_width = max(0.8 * inch, width - min_line_width - 0.12 * inch)
        if label_width > max_label_width:
            for candidate in range(11, 8, -1):
                candidate_width = canvas.stringWidth(label, "Helvetica", candidate)
                if candidate_width <= max_label_width:
                    font_size = candidate
                    label_width = candidate_width
                    break
        canvas.setFont("Helvetica", font_size)
        canvas.drawString(x, y, label)

        line_start = x + min(label_width, max_label_width) + 0.12 * inch
        line_end = x + width
        canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
        canvas.setLineWidth(1.0)
        canvas.line(line_start, y - 0.03 * inch, line_end, y - 0.03 * inch)
