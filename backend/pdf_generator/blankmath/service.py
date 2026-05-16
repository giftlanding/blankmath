from typing import Any

from blankmath.generators import generate_problems
from blankmath.renderer import render_pdf
from blankmath.storage import upload_pdf


WORKSHEET_TITLES = {
    "addition": "Addition",
    "minus": "Subtraction",
    "mixed_add_minus": "Mixed Addition and Subtraction",
    "additionmn": "Addition Missing Number",
    "minusmn": "Subtraction Missing Number",
    "mixed_add_minus_mn": "Mixed Addition and Subtraction Missing Number",
    "add_three_numbers": "Add Three Numbers",
    "add_minus_three_numbers": "Add and Subtract Three Numbers",
    "add_three_numbers_mn": "Add Three Numbers Missing Number",
    "multiplication": "Multiplication",
    "division": "Division",
    "mixed_times_divide": "Mixed Multiplication and Division",
    "multiplicationmn": "Multiplication Missing Number",
    "division_mn": "Division Missing Number",
    "mixed_times_divide_mn": "Mixed Multiplication and Division Missing Number",
    "greater_than_less_than": "Greater Than or Less Than",
    "distributive_property_near_numbers": "Distributive Property",
    "breaking_parentheses": "Breaking Parentheses Practice",
}


def generate_worksheet_pdf(request: dict[str, Any]) -> str:
    worksheet_type = request["worksheetType"]
    options = request["options"]
    count_per_page = int(options.get("problemCount", 20))
    include_answer_key = bool(options.get("includeAnswerKey", False))
    layout = str(options.get("layout", default_layout_for(worksheet_type)))
    problems = generate_problems(worksheet_type, options)
    pdf = render_pdf(
        title=WORKSHEET_TITLES[worksheet_type],
        problems=problems,
        count_per_page=count_per_page,
        include_answer_key=include_answer_key,
        layout=layout,
    )
    return upload_pdf(pdf)


def default_layout_for(worksheet_type: str) -> str:
    if worksheet_type == "distributive_property_near_numbers":
        return "distributive_property"
    if worksheet_type == "breaking_parentheses":
        return "breaking_parentheses"
    return "horizontal"
