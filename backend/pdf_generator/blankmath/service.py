from typing import Any

from blankmath.generators import generate_problems
from blankmath.renderer import render_pdf
from blankmath.storage import upload_pdf
from blankmath.worksheet_registry import worksheet_definition


def generate_worksheet_pdf(request: dict[str, Any]) -> str:
    worksheet_type = request["worksheetType"]
    definition = worksheet_definition(worksheet_type)
    options = request["options"]
    count_per_page = int(options.get("problemCount", 20))
    include_answer_key = bool(options.get("includeAnswerKey", False))
    layout = str(options.get("layout", default_layout_for(worksheet_type)))
    problems = generate_problems(worksheet_type, options)
    pdf = render_pdf(
        title=definition.title,
        problems=problems,
        count_per_page=count_per_page,
        include_answer_key=include_answer_key,
        layout=layout,
    )
    return upload_pdf(pdf)


def default_layout_for(worksheet_type: str) -> str:
    return worksheet_definition(worksheet_type).default_layout
