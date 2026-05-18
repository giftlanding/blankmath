from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable


FONT = "Helvetica"
FONT_SIZE = 16
MIN_FONT_SIZE = 12
PANEL_HEIGHT = 0.72 * inch
INSET = 0.1 * inch
BLANK_GAP = 0.14 * inch
MIN_BLANK_WIDTH = 1.55 * inch


class PlaceValuePanel(Flowable):
    def __init__(self, prompt: str):
        super().__init__()
        self.prompt = prompt
        self.width = 7.1 * inch
        self.height = PANEL_HEIGHT

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        baseline_y = 0.28 * inch
        font_size = self._font_size_for(canvas)
        text_width = canvas.stringWidth(self.prompt, FONT, font_size)
        line_start = INSET + text_width + BLANK_GAP
        line_end = self.width - INSET

        if line_end - line_start < MIN_BLANK_WIDTH:
            line_start = line_end - MIN_BLANK_WIDTH

        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setFont(FONT, font_size)
        canvas.drawString(INSET, baseline_y, self.prompt)

        canvas.setStrokeColor(colors.HexColor("#5f6b7a"))
        canvas.setLineWidth(1.0)
        canvas.line(line_start, baseline_y - 0.03 * inch, line_end, baseline_y - 0.03 * inch)
        canvas.restoreState()

    def _font_size_for(self, canvas) -> int:
        for font_size in range(FONT_SIZE, MIN_FONT_SIZE - 1, -1):
            text_width = canvas.stringWidth(self.prompt, FONT, font_size)
            if self.width - INSET - text_width - BLANK_GAP >= MIN_BLANK_WIDTH:
                return font_size
        return MIN_FONT_SIZE
