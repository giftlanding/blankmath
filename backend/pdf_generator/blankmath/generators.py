import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Problem:
    prompt: str
    answer: str


NEAR_10_BASES = (10, 20, 30, 40, 50, 60, 70, 80, 90)
NEAR_100_BASES = (100, 200, 300, 400, 500, 600, 700, 800, 900)


def generate_problems(worksheet_type: str, options: dict[str, Any]) -> list[Problem]:
    count = int(options.get("problemCount", 20))
    sheets = int(options.get("sheetCount", 1))
    total = count * sheets
    generator = _generator_for(worksheet_type)

    problems: list[Problem] = []
    seen: set[str] = set()
    attempts = 0

    while len(problems) < total:
        attempts += 1
        if attempts > total * 100:
            raise ValueError("Unable to generate enough unique problems.")
        problem = generator(options)
        if problem.prompt in seen:
            continue
        seen.add(problem.prompt)
        problems.append(problem)

    return problems


def _generator_for(worksheet_type: str):
    return {
        "addition": _addition,
        "minus": _subtraction,
        "mixed_add_minus": _mixed_add_subtract,
        "additionmn": _addition_missing_number,
        "minusmn": _subtraction_missing_number,
        "mixed_add_minus_mn": _mixed_add_subtract_missing_number,
        "add_three_numbers": _add_three_numbers,
        "add_minus_three_numbers": _add_subtract_three_numbers,
        "add_three_numbers_mn": _add_three_numbers_missing_number,
        "multiplication": _multiplication,
        "division": _division,
        "mixed_times_divide": _mixed_multiply_divide,
        "multiplicationmn": _multiplication_missing_number,
        "division_mn": _division_missing_number,
        "mixed_times_divide_mn": _mixed_multiply_divide_missing_number,
        "greater_than_less_than": _comparison,
        "distributive_property_near_numbers": _distributive_property_near_numbers,
    }[worksheet_type]


def _range(options: dict[str, Any]) -> tuple[int, int]:
    return int(options.get("from", 0)), int(options.get("to", 20))


def _number_for_digits(options: dict[str, Any]) -> int:
    mode = str(options.get("digits", "1d"))
    if mode == "2d":
        return random.randint(10, 99)
    if mode == "3d":
        return random.randint(100, 999)
    if mode == "l12":
        return random.randint(0, 11)
    if mode == "l20":
        return random.randint(0, 20)
    return random.randint(1, 9)


def _addition(options: dict[str, Any]) -> Problem:
    low, high = _range(options)
    total = random.randint(low, high)
    left = random.randint(0, total)
    right = total - left
    if options.get("smallOperandLessThan10"):
        left, right = _force_small_operand(left, right)
    return Problem(f"{left} + {right} = ?", str(total))


def _subtraction(options: dict[str, Any]) -> Problem:
    low, high = _range(options)
    result = random.randint(low, high)
    right = random.randint(0, max(0, high - result))
    left = result + right
    if options.get("smallOperandLessThan10") and right >= 10:
        right = random.randint(0, 9)
        left = result + right
    return Problem(f"{left} - {right} = ?", str(result))


def _mixed_add_subtract(options: dict[str, Any]) -> Problem:
    return random.choice([_addition, _subtraction])(options)


def _addition_missing_number(options: dict[str, Any]) -> Problem:
    low, high = _range(options)
    total = random.randint(low, high)
    left = random.randint(0, total)
    right = total - left
    hidden = random.choice(["left", "right", "result"])
    if hidden == "left":
        return Problem(f"____ + {right} = {total}", str(left))
    if hidden == "right":
        return Problem(f"{left} + ____ = {total}", str(right))
    return Problem(f"{left} + {right} = ____", str(total))


def _subtraction_missing_number(options: dict[str, Any]) -> Problem:
    low, high = _range(options)
    result = random.randint(low, high)
    right = random.randint(0, max(0, high - result))
    left = result + right
    hidden = random.choice(["left", "right", "result"])
    if hidden == "left":
        return Problem(f"____ - {right} = {result}", str(left))
    if hidden == "right":
        return Problem(f"{left} - ____ = {result}", str(right))
    return Problem(f"{left} - {right} = ____", str(result))


def _mixed_add_subtract_missing_number(options: dict[str, Any]) -> Problem:
    return random.choice([_addition_missing_number, _subtraction_missing_number])(options)


def _add_three_numbers(options: dict[str, Any]) -> Problem:
    values = [_number_for_digits(options) for _ in range(3)]
    if str(options.get("digits", "1d")) == "l20":
        while sum(values) > 20:
            values = [random.randint(0, 9) for _ in range(3)]
    return Problem(f"{values[0]} + {values[1]} + {values[2]} = ?", str(sum(values)))


def _add_subtract_three_numbers(options: dict[str, Any]) -> Problem:
    a = _number_for_digits(options)
    b = random.randint(0, a)
    c = _number_for_digits(options)
    result = a - b + c
    if random.choice([True, False]):
        return Problem(f"{a} - {b} + {c} = ?", str(result))
    result = a + c - b
    return Problem(f"{a} + {c} - {b} = ?", str(result))


def _add_three_numbers_missing_number(options: dict[str, Any]) -> Problem:
    values = [_number_for_digits(options) for _ in range(3)]
    if str(options.get("digits", "1d")) == "l20":
        while sum(values) > 20:
            values = [random.randint(0, 9) for _ in range(3)]
    total = sum(values)
    hidden = random.randint(0, 3)
    parts = [str(value) for value in values]
    if hidden < 3:
        answer = parts[hidden]
        parts[hidden] = "____"
        return Problem(f"{parts[0]} + {parts[1]} + {parts[2]} = {total}", answer)
    return Problem(f"{parts[0]} + {parts[1]} + {parts[2]} = ____", str(total))


def _multiplication(options: dict[str, Any]) -> Problem:
    left = _number_for_digits(options)
    right = _number_for_digits(options)
    return Problem(f"{left} x {right} = ?", str(left * right))


def _division(options: dict[str, Any]) -> Problem:
    divisor = max(1, _number_for_digits(options))
    quotient = _number_for_digits(options)
    dividend = divisor * quotient
    return Problem(f"{dividend} / {divisor} = ?", str(quotient))


def _mixed_multiply_divide(options: dict[str, Any]) -> Problem:
    return random.choice([_multiplication, _division])(options)


def _multiplication_missing_number(options: dict[str, Any]) -> Problem:
    left = _number_for_digits(options)
    right = _number_for_digits(options)
    product = left * right
    hidden = random.choice(["left", "right", "result"])
    if hidden == "left":
        return Problem(f"____ x {right} = {product}", str(left))
    if hidden == "right":
        return Problem(f"{left} x ____ = {product}", str(right))
    return Problem(f"{left} x {right} = ____", str(product))


def _division_missing_number(options: dict[str, Any]) -> Problem:
    divisor = max(1, _number_for_digits(options))
    quotient = _number_for_digits(options)
    dividend = divisor * quotient
    hidden = random.choice(["dividend", "divisor", "quotient"])
    if hidden == "dividend":
        return Problem(f"____ / {divisor} = {quotient}", str(dividend))
    if hidden == "divisor":
        return Problem(f"{dividend} / ____ = {quotient}", str(divisor))
    return Problem(f"{dividend} / {divisor} = ____", str(quotient))


def _mixed_multiply_divide_missing_number(options: dict[str, Any]) -> Problem:
    return random.choice([_multiplication_missing_number, _division_missing_number])(options)


def _comparison(options: dict[str, Any]) -> Problem:
    left = _number_for_digits(options)
    right = _number_for_digits(options)
    if left < right:
        answer = "<"
    elif left > right:
        answer = ">"
    else:
        answer = "="
    return Problem(f"{left} ____ {right}", answer)


def _distributive_property_near_numbers(options: dict[str, Any]) -> Problem:
    base = _distributive_base(options)
    operation = _distributive_operation(options)
    offset = _distributive_offset(base)
    target = base + offset if operation == "+" else base - offset
    factor = _distributive_factor(options)
    first_partial = factor * base
    second_partial = factor * offset
    answer = first_partial + second_partial if operation == "+" else first_partial - second_partial
    return Problem(
        f"{factor} x {target} = {factor} x ({base} {operation} {offset})",
        str(answer),
    )


def _distributive_base(options: dict[str, Any]) -> int:
    mode = str(options.get("base", "near_100"))
    if mode == "mixed":
        mode = random.choice(["near_10", "near_100"])
    if mode == "near_10":
        return random.choice(NEAR_10_BASES)
    return random.choice(NEAR_100_BASES)


def _distributive_operation(options: dict[str, Any]) -> str:
    direction = str(options.get("direction", "subtraction"))
    if direction == "mixed":
        direction = random.choice(["addition", "subtraction"])
    return "+" if direction == "addition" else "-"


def _distributive_offset(base: int) -> int:
    if base < 100:
        return random.randint(1, 3)
    return random.randint(1, 5)


def _distributive_factor(options: dict[str, Any]) -> int:
    difficulty = str(options.get("difficulty", "multiples_of_10"))
    if difficulty == "mixed":
        difficulty = random.choice(["one_digit", "two_digit", "multiples_of_10"])
    if difficulty == "one_digit":
        return random.randint(2, 9)
    if difficulty == "two_digit":
        return random.randint(10, 99)
    return random.choice([20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900])


def _force_small_operand(left: int, right: int) -> tuple[int, int]:
    total = left + right
    if min(left, right) < 10:
        return left, right
    if random.choice([True, False]):
        small = random.randint(0, 9)
        return small, total - small
    small = random.randint(0, 9)
    return total - small, small
