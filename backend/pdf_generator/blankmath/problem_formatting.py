import html
import re
from dataclasses import dataclass

NUMBER_FONT_SIZE = 8
PROBLEM_FONT_SIZE = 18
BLANK_WIDTH = 10


@dataclass(frozen=True)
class VerticalProblemParts:
    left: str
    operator: str
    right: str


def problem_markup(problem_number: int, prompt: str, layout: str) -> str:
    number = problem_number_markup(problem_number)
    if layout == "vertical":
        vertical_markup = vertical_problem_markup(prompt)
        if vertical_markup:
            return f"{number}<br/>{vertical_markup}"

    return f"{number}&nbsp;<font size=\"{PROBLEM_FONT_SIZE}\">{horizontal_problem_markup(prompt)}</font>"


def problem_number_markup(problem_number: int) -> str:
    return f'<font size="{NUMBER_FONT_SIZE}" color="#5f6b7a">{problem_number}.</font>'


def vertical_problem_markup(prompt: str) -> str | None:
    parts = parse_vertical_problem(prompt)
    if not parts:
        return None

    operator_markup = operator_markup_for(parts.operator)
    return (
        f"<font size=\"{PROBLEM_FONT_SIZE}\">{html.escape(parts.left)}</font>"
        f"<br/><font size=\"{PROBLEM_FONT_SIZE}\">{operator_markup} {html.escape(parts.right)}</font>"
        f"<br/><font size=\"{PROBLEM_FONT_SIZE}\">{answer_blank_markup()}</font>"
    )


def parse_vertical_problem(prompt: str) -> VerticalProblemParts | None:
    match = re.fullmatch(r"(\d+) ([+\-x/]) (\d+) = \?", prompt)
    if not match:
        return None
    left, operator, right = match.groups()
    return VerticalProblemParts(left=left, operator=operator, right=right)


def horizontal_problem_markup(prompt: str) -> str:
    rendered = html.escape(prompt).replace(" x ", " &times; ").replace(" / ", " &divide; ")
    if rendered.endswith(" = ?"):
        return rendered[:-4] + f" = {answer_blank_markup()}"
    return rendered


def answer_blank_markup() -> str:
    return "<u>" + "&nbsp;" * BLANK_WIDTH + "</u>"


def operator_markup_for(operator: str) -> str:
    if operator == "x":
        return "&times;"
    if operator == "/":
        return "&divide;"
    return html.escape(operator)
