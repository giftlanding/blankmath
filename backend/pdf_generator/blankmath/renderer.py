from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from blankmath.generators import Problem
from blankmath.problem_formatting import problem_markup


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

    for page_number, start in enumerate(range(0, len(problems), count_per_page), start=1):
        page_problems = problems[start:start + count_per_page]
        if page_number > 1:
            story.append(PageBreak())
        story.append(Paragraph("BlankMath.com", styles["Title"]))
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Spacer(1, 0.16 * inch))
        story.append(_problem_table(page_problems, worksheet_style, layout))

    if include_answer_key:
        story.append(PageBreak())
        story.append(Paragraph("Answer Key", styles["Title"]))
        story.append(Spacer(1, 0.16 * inch))
        story.append(_answer_table(problems, styles["Normal"]))

    document.build(story)
    return buffer.getvalue()


def _problem_table(problems: list[Problem], style, layout: str) -> Table:
    if layout == "vertical":
        columns = 4 if len(problems) <= 20 else 5
    else:
        columns = 2 if len(problems) <= 20 else 3

    rows = []
    for index in range(0, len(problems), columns):
        row = []
        for offset in range(columns):
            problem_index = index + offset
            if problem_index < len(problems):
                problem = problems[problem_index]
                text = problem_markup(problem_index + 1, problem.prompt, layout)
            else:
                text = ""
            row.append(Paragraph(text, style))
        rows.append(row)

    table = Table(rows, colWidths=[7.4 * inch / columns] * columns)
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.15, colors.HexColor("#d9dee8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
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
