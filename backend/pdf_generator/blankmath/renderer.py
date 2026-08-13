from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from blankmath.generators import Problem
from blankmath.panels.problem import page_problem_count, panel_grid, problem_panel

HEADER_IMAGE_PATH = Path(__file__).resolve().parent / "assets" / "logo.jpg"
PAGE_WIDTH, PAGE_HEIGHT = letter
HEADER_WIDTH = PAGE_WIDTH
HEADER_HEIGHT = 1.0 * inch
BODY_TOP_GAP = 0.12 * inch


def render_pdf(
    title: str,
    problems: list[Problem],
    count_per_page: int,
    include_answer_key: bool,
    layout: str = "horizontal",
    include_name_date: bool = False,
    include_class_period: bool = False,
    memo_text: str = "",
) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=HEADER_HEIGHT + BODY_TOP_GAP,
        bottomMargin=0.45 * inch,
    )
    styles = getSampleStyleSheet()
    worksheet_style = styles["Normal"].clone("WorksheetProblem")
    worksheet_style.fontSize = 18
    worksheet_style.leading = 22
    title_style = styles["Title"].clone("WorksheetTitle")
    title_style.fontSize = 20
    title_style.leading = 24
    instruction_style = styles["Normal"].clone("WorksheetInstruction")
    instruction_style.fontSize = 12
    instruction_style.leading = 15
    instruction_style.textColor = colors.HexColor("#394150")
    version_style = styles["Normal"].clone("WorksheetVersion")
    version_style.fontSize = 10
    version_style.leading = 12
    version_style.textColor = colors.HexColor("#5f6b7a")
    version_style.alignment = 2
    story = []
    problems_per_page = page_problem_count(count_per_page, layout)
    version_chunks = [
        problems[start:start + problems_per_page]
        for start in range(0, len(problems), problems_per_page)
    ]
    version_count = len(version_chunks)

    for page_number, page_problems in enumerate(version_chunks, start=1):
        if page_number > 1:
            story.append(PageBreak())
        if include_name_date or include_class_period or memo_text:
            story.append(_worksheet_info_table(include_name_date, include_class_period, memo_text))
            story.append(Spacer(1, 0.12 * inch))
        if version_count > 1:
            story.append(Paragraph(f"Version {page_number}", version_style))
            story.append(Spacer(1, 0.08 * inch))
        if layout == "breaking_parentheses":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Rewrite each expression without parentheses. Do not solve.", instruction_style))
            story.append(Spacer(1, 0.14 * inch))
        if layout == "chicken_rabbit":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Use drawing, guess-and-check, or equations. Show your work.", instruction_style))
            story.append(Spacer(1, 0.12 * inch))
        if layout == "place_value":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Write the missing place-value form.", instruction_style))
            story.append(Spacer(1, 0.14 * inch))
        if layout == "fraction":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Write the missing fraction answer.", instruction_style))
            story.append(Spacer(1, 0.14 * inch))
        if layout == "number_line":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Fill in the missing numbers on each number line.", instruction_style))
            story.append(Spacer(1, 0.14 * inch))
        if layout == "clock":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Read the clock or draw the clock hands.", instruction_style))
            story.append(Spacer(1, 0.14 * inch))
        if layout == "hundred_chart":
            story.append(Paragraph(title, title_style))
            story.append(Paragraph("Fill in the missing numbers on the chart.", instruction_style))
            story.append(Spacer(1, 0.14 * inch))
        story.append(_problem_table(page_problems, worksheet_style, layout))

    if include_answer_key:
        for page_number, page_problems in enumerate(version_chunks, start=1):
            story.append(PageBreak())
            answer_title = "Answer Key" if version_count == 1 else f"Answer Key - Version {page_number}"
            story.append(Paragraph(answer_title, styles["Title"]))
            story.append(Spacer(1, 0.16 * inch))
            story.append(_answer_table(page_problems, styles["Normal"], layout))

    document.build(story, onFirstPage=_draw_page_header, onLaterPages=_draw_page_header)
    return buffer.getvalue()


def _draw_page_header(canvas, document) -> None:
    canvas.drawImage(
        str(HEADER_IMAGE_PATH),
        0,
        PAGE_HEIGHT - HEADER_HEIGHT,
        width=HEADER_WIDTH,
        height=HEADER_HEIGHT,
        preserveAspectRatio=False,
        mask="auto",
    )


def _problem_table(problems: list[Problem], style, layout: str, start_number: int = 1) -> Table:
    grid = panel_grid(layout, len(problems))

    rows = []
    for index in range(0, len(problems), grid.columns):
        row = []
        for offset in range(grid.columns):
            problem_index = index + offset
            if problem_index < len(problems):
                problem = problems[problem_index]
                cell = problem_panel(start_number + problem_index, problem, style, layout)
            else:
                cell = ""
            row.append(cell)
        rows.append(row)

    table = Table(rows, colWidths=[7.4 * inch / grid.columns] * grid.columns, rowHeights=grid.row_height)
    table_style_commands = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), grid.left_padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), grid.right_padding),
        ("TOPPADDING", (0, 0), (-1, -1), grid.top_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), grid.bottom_padding),
    ]
    if layout not in {"breaking_parentheses", "chicken_rabbit", "place_value", "fraction", "number_line", "clock", "hundred_chart"}:
        table_style_commands = [
            ("BOX", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
            ("INNERGRID", (0, 0), (-1, -1), 0.15, colors.HexColor("#d9dee8")),
            *table_style_commands,
        ]
    table.setStyle(TableStyle(table_style_commands))
    return table


def _worksheet_info_table(include_name_date: bool, include_class_period: bool, memo_text: str = "") -> Table:
    style = getSampleStyleSheet()["Normal"]
    style.fontSize = 10
    style.leading = 12
    rows = []
    table_style_commands = [
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ]
    if include_name_date:
        rows.append([Paragraph("Name:", style), "", Paragraph("Date:", style), ""])
        row_index = len(rows) - 1
        table_style_commands.extend([
            ("LINEBELOW", (1, row_index), (1, row_index), 0.8, colors.HexColor("#5f6b7a")),
            ("LINEBELOW", (3, row_index), (3, row_index), 0.8, colors.HexColor("#5f6b7a")),
        ])
    if include_class_period:
        rows.append([Paragraph("Class/Period:", style), "", "", ""])
        row_index = len(rows) - 1
        table_style_commands.append(("LINEBELOW", (1, row_index), (3, row_index), 0.8, colors.HexColor("#5f6b7a")))
    if memo_text:
        rows.append([Paragraph("Memo:", style), Paragraph(memo_text, style), "", ""])
        row_index = len(rows) - 1
        table_style_commands.append(("SPAN", (1, row_index), (3, row_index)))

    table = Table(
        rows,
        colWidths=[0.88 * inch, 2.95 * inch, 0.48 * inch, 2.8 * inch],
        rowHeights=[0.28 * inch] * len(rows),
    )
    table.setStyle(TableStyle(table_style_commands))
    return table


class FractionAnswer(Flowable):
    def __init__(self, problem_number: int, answer: str):
        super().__init__()
        self.problem_number = problem_number
        self.answer = answer
        self.width = 1.6 * inch
        self.height = 0.34 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setStrokeColor(colors.black)
        canvas.setFont("Helvetica", 10)
        label = f"{self.problem_number}."
        label_width = canvas.stringWidth(label, "Helvetica", 10)
        canvas.drawString(0, 0.13 * inch, label)
        self._draw_answer(canvas, label_width + 0.08 * inch, 0.17 * inch)
        canvas.restoreState()

    def _draw_answer(self, canvas, x: float, center_y: float) -> None:
        whole, numerator, denominator = _parse_fraction_answer(self.answer)
        if numerator is None or denominator is None:
            canvas.drawString(x, center_y - 0.04 * inch, self.answer)
            return

        fraction_x = x
        if whole is not None:
            whole_text = str(whole)
            canvas.drawString(x, center_y - 0.04 * inch, whole_text)
            fraction_x += canvas.stringWidth(whole_text, "Helvetica", 10) + 0.07 * inch

        numerator_text = str(numerator)
        denominator_text = str(denominator)
        fraction_width = max(
            canvas.stringWidth(numerator_text, "Helvetica", 10),
            canvas.stringWidth(denominator_text, "Helvetica", 10),
            0.18 * inch,
        ) + 0.06 * inch
        center_x = fraction_x + fraction_width / 2
        canvas.drawCentredString(center_x, center_y + 0.07 * inch, numerator_text)
        canvas.line(fraction_x, center_y + 0.035 * inch, fraction_x + fraction_width, center_y + 0.035 * inch)
        canvas.drawCentredString(center_x, center_y - 0.09 * inch, denominator_text)


def _parse_fraction_answer(answer: str) -> tuple[int | None, int | None, int | None]:
    parts = answer.split()
    if len(parts) == 1 and "/" in parts[0]:
        numerator, denominator = parts[0].split("/", 1)
        return None, int(numerator), int(denominator)
    if len(parts) == 2 and "/" in parts[1]:
        numerator, denominator = parts[1].split("/", 1)
        return int(parts[0]), int(numerator), int(denominator)
    return None, None, None


def _answer_table(problems: list[Problem], style, layout: str = "horizontal") -> Table:
    columns = 4
    rows = []
    for index in range(0, len(problems), columns):
        row = []
        for offset in range(columns):
            problem_index = index + offset
            if problem_index < len(problems):
                problem = problems[problem_index]
                if layout == "fraction":
                    row.append(FractionAnswer(problem_index + 1, problem.answer))
                    continue
                text = f"{problem_index + 1}. {problem.answer}"
            else:
                text = ""
            row.append(Paragraph(text, style))
        rows.append(row)

    row_heights = [0.46 * inch] * len(rows) if layout == "fraction" else None
    table = Table(rows, colWidths=[7.4 * inch / columns] * columns, rowHeights=row_heights)
    table.setStyle(TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table
