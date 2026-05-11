import html
import re


def problem_markup(problem_number: int, prompt: str, layout: str) -> str:
    number = problem_number_markup(problem_number)
    if layout == "vertical":
        vertical_markup = vertical_problem_markup(prompt)
        if vertical_markup:
            return f"{number}<br/>{vertical_markup}"

    return f"{number}&nbsp;{horizontal_problem_markup(prompt)}"


def problem_number_markup(problem_number: int) -> str:
    return f'<font size="8" color="#5f6b7a">{problem_number}.</font>'


def vertical_problem_markup(prompt: str) -> str | None:
    match = re.fullmatch(r"(\d+) ([+\-x/]) (\d+) = \?", prompt)
    if not match:
        return None

    left, operator, right = match.groups()
    operator_markup = operator_markup_for(operator)
    return f"{html.escape(left)}<br/>{operator_markup} {html.escape(right)}<br/>{answer_blank_markup()}"


def horizontal_problem_markup(prompt: str) -> str:
    rendered = html.escape(prompt).replace(" x ", " &times; ").replace(" / ", " &divide; ")
    if rendered.endswith(" = ?"):
        return rendered[:-4] + f" = {answer_blank_markup()}"
    return rendered


def answer_blank_markup() -> str:
    return '<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>'


def operator_markup_for(operator: str) -> str:
    if operator == "x":
        return "&times;"
    if operator == "/":
        return "&divide;"
    return html.escape(operator)
