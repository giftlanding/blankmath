from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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
    story = []
    problems_per_page = page_problem_count(count_per_page, layout)

    for page_number, start in enumerate(range(0, len(problems), problems_per_page), start=1):
        page_problems = problems[start:start + problems_per_page]
        if page_number > 1:
            story.append(PageBreak())
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
        story.append(_problem_table(page_problems, worksheet_style, layout, start_number=start + 1))

    if include_answer_key:
        story.append(PageBreak())
        story.append(Paragraph("Answer Key", styles["Title"]))
        story.append(Spacer(1, 0.16 * inch))
        story.append(_answer_table(problems, styles["Normal"]))

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
    if layout not in {"breaking_parentheses", "chicken_rabbit", "place_value", "fraction"}:
        table_style_commands = [
            ("BOX", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
            ("INNERGRID", (0, 0), (-1, -1), 0.15, colors.HexColor("#d9dee8")),
            *table_style_commands,
        ]
    table.setStyle(TableStyle(table_style_commands))
    return table


def _answer_table(problems: list[Problem], style) -> Table:
    columns = 4
    rows = []
    for index in range(0, len(problems), columns):
        row = []
        for offset in range(columns):
            problem_index = index + offset
            if problem_index < len(problems):
                problem = problems[problem_index]
                text = f"{problem_index + 1}. {problem.answer}"
            else:
                text = ""
            row.append(Paragraph(text, style))
        rows.append(row)

    table = Table(rows, colWidths=[7.4 * inch / columns] * columns)
    table.setStyle(TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table
