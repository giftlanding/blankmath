from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable


FONT = "Helvetica"
FONT_SIZE = 17
MIN_FONT_SIZE = 14
PANEL_WIDTH = 7.1 * inch
PANEL_HEIGHT = 0.58 * inch
LEFT_PADDING = 0.05 * inch
BLANK_GAP = 0.12 * inch
MIN_BLANK_WIDTH = 1.55 * inch


class BreakingParenthesesPanel(Flowable):
    def __init__(self, prompt: str):
        super().__init__()
        self.prompt = prompt
        self.width = PANEL_WIDTH
        self.height = PANEL_HEIGHT

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        text = f"{self.prompt} ="
        baseline_y = 0.22 * inch
        font_size = self._font_size_for(canvas, text)
        text_width = canvas.stringWidth(text, FONT, font_size)
        line_start = LEFT_PADDING + text_width + BLANK_GAP
        line_end = self.width - 0.08 * inch

        if line_end - line_start < MIN_BLANK_WIDTH:
            line_start = max(LEFT_PADDING + text_width + BLANK_GAP, self.width - MIN_BLANK_WIDTH)

        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setFont(FONT, font_size)
        canvas.drawString(LEFT_PADDING, baseline_y, text)

        canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
        canvas.setLineWidth(1.0)
        canvas.line(line_start, baseline_y - 0.03 * inch, line_end, baseline_y - 0.03 * inch)
        canvas.restoreState()

    def _font_size_for(self, canvas, text: str) -> int:
        for font_size in range(FONT_SIZE, MIN_FONT_SIZE - 1, -1):
            text_width = canvas.stringWidth(text, FONT, font_size)
            if self.width - LEFT_PADDING - text_width - BLANK_GAP >= MIN_BLANK_WIDTH:
                return font_size
        return MIN_FONT_SIZE
