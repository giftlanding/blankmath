import random
from dataclasses import dataclass
from typing import Any


PLACE_VALUE_DIGITS = {
    "2d": 2,
    "3d": 3,
    "4d": 4,
    "5d": 5,
}


@dataclass(frozen=True)
class PlaceValueProblem:
    prompt: str
    answer: str


def expanded_form(options: dict[str, Any]) -> PlaceValueProblem:
    number = _place_value_number(options)
    return PlaceValueProblem(f"{_format_number(number)} =", _expanded_form(number))


def standard_form(options: dict[str, Any]) -> PlaceValueProblem:
    number = _place_value_number(options)
    return PlaceValueProblem(f"{_expanded_form(number)} =", _format_number(number))


def digit_value(options: dict[str, Any]) -> PlaceValueProblem:
    number = _place_value_number(options)
    digits = [int(digit) for digit in str(number)]
    non_zero_indexes = [index for index, digit in enumerate(digits) if digit != 0]
    digit_index = random.choice(non_zero_indexes)
    digit = digits[digit_index]
    place_power = len(digits) - digit_index - 1
    value = digit * (10 ** place_power)
    return PlaceValueProblem(
        f"In {_format_number(number)}, what is the value of {digit}?",
        _format_number(value),
    )


def _place_value_number(options: dict[str, Any]) -> int:
    digit_count = PLACE_VALUE_DIGITS[str(options.get("placeValueDigits", "3d"))]
    zero_mode = str(options.get("zeroMode", "mixed"))
    if zero_mode == "mixed":
        zero_mode = random.choice(["avoid", "allow"])

    first_digit = random.randint(1, 9)
    if zero_mode == "avoid":
        remaining_digits = [random.randint(1, 9) for _ in range(digit_count - 1)]
    else:
        remaining_digits = [random.randint(0, 9) for _ in range(digit_count - 1)]
        if all(digit != 0 for digit in remaining_digits):
            remaining_digits[random.randrange(len(remaining_digits))] = 0

    digits = [first_digit, *remaining_digits]
    return int("".join(str(digit) for digit in digits))


def _expanded_form(number: int) -> str:
    digits = [int(digit) for digit in str(number)]
    terms = []
    for index, digit in enumerate(digits):
        if digit == 0:
            continue
        place_power = len(digits) - index - 1
        terms.append(_format_number(digit * (10 ** place_power)))
    return " + ".join(terms)


def _format_number(number: int) -> str:
    return f"{number:,}"
