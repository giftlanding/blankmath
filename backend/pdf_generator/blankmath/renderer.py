from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from blankmath.generators import Problem
from blankmath.panels import page_problem_count, panel_grid, problem_panel

HEADER_IMAGE_PATH = Path(__file__).resolve().parent / "assets" / "logo.jpg"


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
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
    )
    styles = getSampleStyleSheet()
    worksheet_style = styles["Normal"].clone("WorksheetProblem")
    worksheet_style.fontSize = 18
    worksheet_style.leading = 22
    story = []
    problems_per_page = page_problem_count(count_per_page, layout)

    for page_number, start in enumerate(range(0, len(problems), problems_per_page), start=1):
        page_problems = problems[start:start + problems_per_page]
        if page_number > 1:
            story.append(PageBreak())
        story.append(_header_image())
        story.append(Spacer(1, 0.12 * inch))
        story.append(_problem_table(page_problems, worksheet_style, layout, start_number=start + 1))

    if include_answer_key:
        story.append(PageBreak())
        story.append(Paragraph("Answer Key", styles["Title"]))
        story.append(Spacer(1, 0.16 * inch))
        story.append(_answer_table(problems, styles["Normal"]))

    document.build(story)
    return buffer.getvalue()


def _header_image() -> Image:
    return Image(str(HEADER_IMAGE_PATH), width=7.6 * inch, height=0.894 * inch)


def _problem_table(problems: list[Problem], style, layout: str, start_number: int = 1) -> Table:
    grid = panel_grid(layout, len(problems))

    rows = []
    for index in range(0, len(problems), grid.columns):
        row = []
        for offset in range(grid.columns):
            problem_index = index + offset
            if problem_index < len(problems):
                problem = problems[problem_index]
                cell = problem_panel(start_number + problem_index, problem.prompt, style, layout)
            else:
                cell = ""
            row.append(cell)
        rows.append(row)

    table = Table(rows, colWidths=[7.4 * inch / grid.columns] * grid.columns, rowHeights=grid.row_height)
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.15, colors.HexColor("#d9dee8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), grid.left_padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), grid.right_padding),
        ("TOPPADDING", (0, 0), (-1, -1), grid.top_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), grid.bottom_padding),
    ]))
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
