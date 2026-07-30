import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


@dataclass(frozen=True)
class FractionProblem:
    prompt: str
    answer: str
    left_numerator: int | None
    left_denominator: int | None
    left_whole: int | None = None
    right_numerator: int | None = None
    right_denominator: int | None = None
    right_whole: int | None = None
    operator: str = ""


def reduce_fraction(options: dict[str, Any]) -> FractionProblem:
    denominator_max = _denominator_max(options)
    include_improper = bool(options.get("includeImproperFractions", False))
    for _ in range(1000):
        reduced_denominator = random.randint(2, max(3, denominator_max // 2))
        reduced_numerator = random.randint(1, reduced_denominator - 1)
        if include_improper and random.choice([True, False]):
            reduced_numerator = random.randint(reduced_denominator + 1, denominator_max)
        if math.gcd(reduced_numerator, reduced_denominator) != 1:
            continue
        multiplier = random.randint(2, max(2, denominator_max // reduced_denominator))
        numerator = reduced_numerator * multiplier
        denominator = reduced_denominator * multiplier
        if denominator <= denominator_max:
            answer = _fraction_text(reduced_numerator, reduced_denominator)
            return FractionProblem(
                prompt=f"{_fraction_text(numerator, denominator)} =",
                answer=answer,
                left_numerator=numerator,
                left_denominator=denominator,
            )
    raise ValueError("Unable to generate a reducible fraction.")


def equivalent_fraction(options: dict[str, Any]) -> FractionProblem:
    denominator_max = _denominator_max(options)
    for _ in range(1000):
        numerator, denominator = _proper_fraction_terms(max(3, denominator_max // 2))
        multiplier = random.randint(2, max(2, denominator_max // denominator))
        equivalent_numerator = numerator * multiplier
        equivalent_denominator = denominator * multiplier
        if equivalent_denominator <= denominator_max:
            return FractionProblem(
                prompt=f"{_fraction_text(numerator, denominator)} =",
                answer=_fraction_text(equivalent_numerator, equivalent_denominator),
                left_numerator=numerator,
                left_denominator=denominator,
                right_numerator=equivalent_numerator,
                right_denominator=equivalent_denominator,
            )
    raise ValueError("Unable to generate an equivalent fraction.")


def compare_fraction(options: dict[str, Any]) -> FractionProblem:
    denominator_max = _denominator_max(options)
    for _ in range(1000):
        left_numerator, left_denominator = _proper_fraction_terms(denominator_max)
        right_numerator, right_denominator = _proper_fraction_terms(denominator_max)
        left_value = Fraction(left_numerator, left_denominator)
        right_value = Fraction(right_numerator, right_denominator)
        if left_value == right_value:
            continue
        answer = ">" if left_value > right_value else "<"
        return FractionProblem(
            prompt=f"{_fraction_text(left_numerator, left_denominator)} ____ {_fraction_text(right_numerator, right_denominator)}",
            answer=answer,
            left_numerator=left_numerator,
            left_denominator=left_denominator,
            right_numerator=right_numerator,
            right_denominator=right_denominator,
            operator="compare",
        )
    raise ValueError("Unable to generate comparable fractions.")


def add_fraction(options: dict[str, Any]) -> FractionProblem:
    denominator_max = _denominator_max(options)
    style = str(options.get("fractionAdditionStyle", "fraction_fraction"))
    if style == "mixed":
        style = random.choice(["fraction_fraction", "integer_fraction", "integer_mixed"])

    left_whole: int | None = None
    right_whole: int | None = None
    left_numerator: int | None
    left_denominator: int | None
    right_numerator: int | None
    right_denominator: int | None

    if style == "fraction_fraction":
        left_numerator, left_denominator = _proper_fraction_terms(denominator_max)
        right_numerator, right_denominator = _proper_fraction_terms(denominator_max)
        left_value = Fraction(left_numerator, left_denominator)
        right_value = Fraction(right_numerator, right_denominator)
    elif style == "integer_fraction":
        left_whole = random.randint(1, 9)
        left_numerator = None
        left_denominator = None
        right_numerator, right_denominator = _proper_fraction_terms(denominator_max)
        left_value = Fraction(left_whole, 1)
        right_value = Fraction(right_numerator, right_denominator)
    elif style == "integer_mixed":
        left_whole = random.randint(1, 9)
        left_numerator = None
        left_denominator = None
        right_whole = random.randint(1, 9)
        right_numerator, right_denominator = _proper_fraction_terms(denominator_max)
        left_value = Fraction(left_whole, 1)
        right_value = Fraction(right_whole, 1) + Fraction(right_numerator, right_denominator)
    else:
        raise ValueError("Unsupported fraction addition style.")

    prompt = f"{_term_text(left_whole, left_numerator, left_denominator)} + {_term_text(right_whole, right_numerator, right_denominator)} = ?"
    return FractionProblem(
        prompt=prompt,
        answer=_mixed_fraction_text(left_value + right_value),
        left_numerator=left_numerator,
        left_denominator=left_denominator,
        left_whole=left_whole,
        right_numerator=right_numerator,
        right_denominator=right_denominator,
        right_whole=right_whole,
        operator="add",
    )


def multiply_divide_fraction(options: dict[str, Any]) -> FractionProblem:
    denominator_max = _denominator_max(options)
    style = str(options.get("fractionMultiplicationDivisionStyle", "mixed"))
    if style == "mixed":
        style = random.choice(["multiply", "divide"])

    left_numerator, left_denominator = _proper_fraction_terms(denominator_max)
    right_numerator, right_denominator = _proper_fraction_terms(denominator_max)
    left_value = Fraction(left_numerator, left_denominator)
    right_value = Fraction(right_numerator, right_denominator)

    if style == "multiply":
        prompt_operator = "x"
        answer = left_value * right_value
    elif style == "divide":
        prompt_operator = "÷"
        answer = left_value / right_value
    else:
        raise ValueError("Unsupported fraction multiplication/division style.")

    prompt = f"{_fraction_text(left_numerator, left_denominator)} {prompt_operator} {_fraction_text(right_numerator, right_denominator)} = ?"
    return FractionProblem(
        prompt=prompt,
        answer=_mixed_fraction_text(answer),
        left_numerator=left_numerator,
        left_denominator=left_denominator,
        right_numerator=right_numerator,
        right_denominator=right_denominator,
        operator=style,
    )


def _denominator_max(options: dict[str, Any]) -> int:
    difficulty = str(options.get("fractionDifficulty", "easy"))
    if difficulty == "hard":
        return 24
    if difficulty == "medium":
        return 16
    return 12


def _fraction_text(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator}"


def _proper_fraction_terms(denominator_max: int) -> tuple[int, int]:
    for _ in range(1000):
        denominator = random.randint(2, denominator_max)
        numerator = random.randint(1, denominator - 1)
        if math.gcd(numerator, denominator) == 1:
            return numerator, denominator
    raise ValueError("Unable to generate a simplified proper fraction.")


def _term_text(whole: int | None, numerator: int | None, denominator: int | None) -> str:
    if numerator is None or denominator is None:
        return str(whole)
    fraction = _fraction_text(numerator, denominator)
    if whole is None:
        return fraction
    return f"{whole} {fraction}"


def _mixed_fraction_text(value: Fraction) -> str:
    whole = value.numerator // value.denominator
    remainder = value - whole
    if remainder == 0:
        return str(whole)
    fraction = _fraction_text(remainder.numerator, remainder.denominator)
    if whole == 0:
        return fraction
    return f"{whole} {fraction}"
