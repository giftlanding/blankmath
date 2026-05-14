from io import BytesIO
from pathlib import Path

from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate

from blankmath.panels.long_division import (
    DIVIDEND_Y as LONG_DIVISION_DIVIDEND_Y,
    OPERAND_FONT_SIZE as LONG_DIVISION_OPERAND_FONT_SIZE,
    PANEL_HEIGHT as LONG_DIVISION_PANEL_HEIGHT,
    PANEL_WIDTH as LONG_DIVISION_PANEL_WIDTH,
    QUOTIENT_LINE_Y,
    WORK_LINE_YS as LONG_DIVISION_WORK_LINE_YS,
    LongDivisionPanel,
)
from blankmath.panels.vertical_arithmetic import (
    FIRST_OPERAND_Y,
    LINE_Y,
    OPERAND_FONT_SIZE,
    PANEL_HEIGHT,
    PANEL_WIDTH,
    SECOND_OPERAND_Y,
    WORK_LINE_YS,
    VerticalArithmeticPanel,
    operator_text,
)


def render_panel_pdf(panel, width: float = 2 * inch, height: float = 2 * inch) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=(width, height),
        rightMargin=0,
        leftMargin=0,
        topMargin=0,
        bottomMargin=0,
    )
    document.build([panel])
    return buffer.getvalue()


def render_panel_png(panel, path: str | Path, scale: int = 4) -> None:
    if isinstance(panel, LongDivisionPanel):
        _render_long_division_panel_png(panel, path, scale)
        return
    if isinstance(panel, VerticalArithmeticPanel):
        _render_vertical_arithmetic_panel_png(panel, path, scale)
        return
    raise TypeError(f"PNG preview is not implemented for {type(panel).__name__}.")


def _render_vertical_arithmetic_panel_png(panel: VerticalArithmeticPanel, path: str | Path, scale: int) -> None:
    from PIL import Image, ImageDraw, ImageFont

    width = int(PANEL_WIDTH * scale)
    height = int(PANEL_HEIGHT * scale)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    operand_font = _font("DejaVuSansMono.ttf", OPERAND_FONT_SIZE * scale)
    number_font = _font("DejaVuSans.ttf", 8 * scale)

    operand_right = width - int(0.12 * inch * scale)
    operand_width = max(
        draw.textlength(panel.problem.left, font=operand_font),
        draw.textlength(panel.problem.right, font=operand_font),
    )
    operator_x = max(int(0.32 * inch * scale), int(operand_right - operand_width - 0.28 * inch * scale))

    draw.text(
        (0, _baseline_to_image_top(FIRST_OPERAND_Y + 0.08 * inch, height, scale, number_font)),
        f"{panel.problem_number}.",
        fill="#5f6b7a",
        font=number_font,
    )
    _draw_right_text(
        draw,
        (operand_right, _baseline_to_image_top(FIRST_OPERAND_Y, height, scale, operand_font)),
        panel.problem.left,
        operand_font,
    )
    draw.text(
        (operator_x, _baseline_to_image_top(SECOND_OPERAND_Y, height, scale, operand_font)),
        operator_text(panel.problem.operator),
        fill="black",
        font=operand_font,
    )
    _draw_right_text(
        draw,
        (operand_right, _baseline_to_image_top(SECOND_OPERAND_Y, height, scale, operand_font)),
        panel.problem.right,
        operand_font,
    )

    line_width = max(1, int(1.2 * scale))
    draw.line(
        (operator_x, _to_image_y(LINE_Y, height, scale), operand_right, _to_image_y(LINE_Y, height, scale)),
        fill="black",
        width=line_width,
    )
    for work_line_y in WORK_LINE_YS:
        draw.line(
            (operator_x, _to_image_y(work_line_y, height, scale), operand_right, _to_image_y(work_line_y, height, scale)),
            fill="#d8dde6",
            width=max(1, int(0.6 * scale)),
        )

    image.save(path)


def _render_long_division_panel_png(panel: LongDivisionPanel, path: str | Path, scale: int) -> None:
    from PIL import Image, ImageDraw

    width = int(LONG_DIVISION_PANEL_WIDTH * scale)
    height = int(LONG_DIVISION_PANEL_HEIGHT * scale)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    operand_font = _font("DejaVuSansMono.ttf", LONG_DIVISION_OPERAND_FONT_SIZE * scale)
    number_font = _font("DejaVuSans.ttf", 8 * scale)

    bracket_x = int(1.0 * inch * scale)
    dividend_x = bracket_x + int(0.22 * inch * scale)
    dividend_right = min(width - int(0.18 * inch * scale), dividend_x + int(1.45 * inch * scale))
    divisor_right = bracket_x - int(0.08 * inch * scale)

    draw.text((0, int(0.08 * inch * scale)), f"{panel.problem_number}.", fill="#5f6b7a", font=number_font)
    _draw_right_text(
        draw,
        (divisor_right, _baseline_to_image_top(LONG_DIVISION_DIVIDEND_Y, height, scale, operand_font)),
        panel.problem.right,
        operand_font,
    )
    draw.text(
        (bracket_x, _baseline_to_image_top(LONG_DIVISION_DIVIDEND_Y, height, scale, operand_font)),
        ")",
        fill="black",
        font=operand_font,
    )
    draw.text(
        (dividend_x, _baseline_to_image_top(LONG_DIVISION_DIVIDEND_Y, height, scale, operand_font)),
        panel.problem.left,
        fill="black",
        font=operand_font,
    )
    draw.line(
        (
            dividend_x - int(0.02 * inch * scale),
            _to_image_y(QUOTIENT_LINE_Y, height, scale),
            dividend_right,
            _to_image_y(QUOTIENT_LINE_Y, height, scale),
        ),
        fill="black",
        width=max(1, int(1.2 * scale)),
    )
    for work_line_y in LONG_DIVISION_WORK_LINE_YS:
        draw.line(
            (dividend_x, _to_image_y(work_line_y, height, scale), dividend_right, _to_image_y(work_line_y, height, scale)),
            fill="#d8dde6",
            width=max(1, int(0.6 * scale)),
        )

    image.save(path)


def _to_image_y(reportlab_y: float, height: int, scale: int) -> int:
    return height - int(reportlab_y * scale)


def _baseline_to_image_top(reportlab_y: float, height: int, scale: int, font) -> int:
    try:
        ascent, _ = font.getmetrics()
    except AttributeError:
        ascent = font.size
    return _to_image_y(reportlab_y, height, scale) - ascent


def _draw_right_text(draw, position: tuple[int, int], text: str, font) -> None:
    x, y = position
    draw.text((x - draw.textlength(text, font=font), y), text, fill="black", font=font)


def _font(name: str, size: int):
    from PIL import ImageFont

    candidates = [
        name,
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Courier.ttc",
        "/System/Library/Fonts/Geneva.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()
