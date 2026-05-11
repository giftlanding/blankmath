from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from blankmath.generators import Problem
from blankmath.problem_formatting import VerticalProblemParts, parse_vertical_problem, problem_markup

WORKSHEET_FONT = "Helvetica"
VERTICAL_FONT = "Courier"


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
    page_problem_count = _page_problem_count(count_per_page, layout)

    for page_number, start in enumerate(range(0, len(problems), page_problem_count), start=1):
        page_problems = problems[start:start + page_problem_count]
        if page_number > 1:
            story.append(PageBreak())
        story.append(Paragraph("BlankMath.com", styles["Title"]))
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Spacer(1, 0.16 * inch))
        story.append(_problem_table(page_problems, worksheet_style, layout, start_number=start + 1))

    if include_answer_key:
        story.append(PageBreak())
        story.append(Paragraph("Answer Key", styles["Title"]))
        story.append(Spacer(1, 0.16 * inch))
        story.append(_answer_table(problems, styles["Normal"]))

    document.build(story)
    return buffer.getvalue()


def _page_problem_count(count_per_page: int, layout: str) -> int:
    if layout == "vertical":
        return min(count_per_page, 20)
    return count_per_page


def _problem_table(problems: list[Problem], style, layout: str, start_number: int = 1) -> Table:
    if layout == "vertical":
        columns = 4 if len(problems) <= 20 else 5
        row_height = 1.16 * inch
    else:
        columns = 2 if len(problems) <= 20 else 3
        row_height = None

    rows = []
    for index in range(0, len(problems), columns):
        row = []
        for offset in range(columns):
            problem_index = index + offset
            if problem_index < len(problems):
                problem = problems[problem_index]
                cell = _problem_cell(start_number + problem_index, problem.prompt, style, layout)
            else:
                cell = ""
            row.append(cell)
        rows.append(row)

    table = Table(rows, colWidths=[7.4 * inch / columns] * columns, rowHeights=row_height)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.2, colors.HexColor("#d9dee8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.15, colors.HexColor("#d9dee8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]
    if layout == "vertical":
        commands.extend([
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    table.setStyle(TableStyle(commands))
    return table


def _problem_cell(problem_number: int, prompt: str, style, layout: str):
    if layout == "vertical":
        vertical_problem = parse_vertical_problem(prompt)
        if vertical_problem:
            return VerticalProblemFlowable(problem_number, vertical_problem)
    return Paragraph(problem_markup(problem_number, prompt, layout), style)


class VerticalProblemFlowable(Flowable):
    def __init__(self, problem_number: int, problem: VerticalProblemParts):
        super().__init__()
        self.problem_number = problem_number
        self.problem = problem
        self.width = 1.55 * inch
        self.height = 0.98 * inch

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        number_text = f"{self.problem_number}."
        operator_text = _operator_text(self.problem.operator)
        line_y = 0.25 * inch
        second_y = 0.48 * inch
        first_y = 0.72 * inch
        operand_right = self.width - 0.12 * inch

        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#5f6b7a"))
        canvas.setFont(WORKSHEET_FONT, 8)
        canvas.drawString(0, first_y + 0.08 * inch, number_text)

        canvas.setFillColor(colors.black)
        canvas.setFont(VERTICAL_FONT, 20)
        operand_width = max(
            canvas.stringWidth(self.problem.left, VERTICAL_FONT, 20),
            canvas.stringWidth(self.problem.right, VERTICAL_FONT, 20),
        )
        operator_x = max(0.32 * inch, operand_right - operand_width - 0.28 * inch)
        canvas.drawRightString(operand_right, first_y, self.problem.left)
        canvas.drawString(operator_x, second_y, operator_text)
        canvas.drawRightString(operand_right, second_y, self.problem.right)
        canvas.setLineWidth(1.2)
        canvas.line(operator_x, line_y, operand_right, line_y)
        canvas.restoreState()


def _operator_text(operator: str) -> str:
    if operator == "x":
        return "x"
    if operator == "/":
        return chr(247)
    return operator


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
