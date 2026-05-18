import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


@dataclass(frozen=True)
class FractionProblem:
    prompt: str
    answer: str
    left_numerator: int
    left_denominator: int
    right_numerator: int | None = None
    right_denominator: int | None = None
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
        denominator = random.randint(2, max(3, denominator_max // 2))
        numerator = random.randint(1, denominator - 1)
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
        left_denominator = random.randint(2, denominator_max)
        right_denominator = random.randint(2, denominator_max)
        left_numerator = random.randint(1, left_denominator - 1)
        right_numerator = random.randint(1, right_denominator - 1)
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


def _denominator_max(options: dict[str, Any]) -> int:
    difficulty = str(options.get("fractionDifficulty", "easy"))
    if difficulty == "hard":
        return 24
    if difficulty == "medium":
        return 16
    return 12


def _fraction_text(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator}"
