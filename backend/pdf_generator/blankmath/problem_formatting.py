import html
import re


def problem_markup(problem_number: int, prompt: str, layout: str) -> str:
    if layout == "vertical":
        vertical_markup = vertical_problem_markup(prompt)
        if vertical_markup:
            return f"{problem_number}.<br/>{vertical_markup}"

    return f"{problem_number}. {horizontal_problem_markup(prompt)}"


def vertical_problem_markup(prompt: str) -> str | None:
    match = re.fullmatch(r"(\d+) ([+\-x/]) (\d+) = \?", prompt)
    if not match:
        return None

    left, operator, right = match.groups()
    operator_markup = operator_markup_for(operator)
    return f"{html.escape(left)}<br/>{operator_markup} {html.escape(right)}<br/>____"


def horizontal_problem_markup(prompt: str) -> str:
    return html.escape(prompt).replace(" x ", " &times; ").replace(" / ", " &divide; ")


def operator_markup_for(operator: str) -> str:
    if operator == "x":
        return "&times;"
    if operator == "/":
        return "&divide;"
    return html.escape(operator)
