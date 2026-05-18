import sys
import unittest
import re
import math
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.generators import generate_problems
from blankmath.generators import _has_addition_carry, _has_subtraction_borrow, _has_borrow_across_zeros
from blankmath.worksheets.chicken_rabbit import ChickenRabbitProblem, VALID_SCENARIOS
from blankmath.worksheets.fractions import FractionProblem
from blankmath.worksheets.hundred_charts import HundredChartProblem
from blankmath.worksheets.number_lines import NumberLineProblem
from blankmath.worksheets.time import TimeProblem


class GeneratorTest(unittest.TestCase):
    def test_generates_requested_problem_count(self):
        problems = generate_problems("addition", {
            "problemCount": 10,
            "sheetCount": 2,
            "from": 0,
            "to": 20,
        })

        self.assertEqual(len(problems), 20)
        self.assertEqual(len({problem.prompt for problem in problems}), 20)

    def test_generates_addition_with_carrying(self):
        problems = generate_problems("addition", {
            "problemCount": 10,
            "sheetCount": 1,
            "from": 10,
            "to": 99,
            "additionRegrouping": "with_carrying",
        })

        for problem in problems:
            left, right = _binary_terms(problem.prompt, "+")
            self.assertTrue(_has_addition_carry(left, right))

    def test_generates_addition_without_carrying(self):
        problems = generate_problems("addition", {
            "problemCount": 10,
            "sheetCount": 1,
            "from": 10,
            "to": 99,
            "additionRegrouping": "without_carrying",
        })

        for problem in problems:
            left, right = _binary_terms(problem.prompt, "+")
            self.assertFalse(_has_addition_carry(left, right))

    def test_generates_subtraction_with_borrowing(self):
        problems = generate_problems("minus", {
            "problemCount": 10,
            "sheetCount": 1,
            "from": 0,
            "to": 99,
            "subtractionRegrouping": "with_borrowing",
        })

        for problem in problems:
            left, right = _binary_terms(problem.prompt, "-")
            self.assertTrue(_has_subtraction_borrow(left, right))

    def test_generates_subtraction_without_borrowing(self):
        problems = generate_problems("minus", {
            "problemCount": 10,
            "sheetCount": 1,
            "from": 0,
            "to": 99,
            "subtractionRegrouping": "without_borrowing",
        })

        for problem in problems:
            left, right = _binary_terms(problem.prompt, "-")
            self.assertFalse(_has_subtraction_borrow(left, right))

    def test_can_avoid_borrowing_across_zeros(self):
        problems = generate_problems("minus", {
            "problemCount": 10,
            "sheetCount": 1,
            "from": 0,
            "to": 999,
            "subtractionRegrouping": "with_borrowing",
            "borrowAcrossZeros": False,
        })

        for problem in problems:
            left, right = _binary_terms(problem.prompt, "-")
            self.assertFalse(_has_borrow_across_zeros(left, right))

    def test_generates_missing_number_answers(self):
        problems = generate_problems("multiplicationmn", {
            "problemCount": 10,
            "sheetCount": 1,
            "digits": "1d",
        })

        self.assertTrue(all("____" in problem.prompt for problem in problems))
        self.assertTrue(all(problem.answer for problem in problems))

    def test_generates_distributive_property_near_number_problems(self):
        problems = generate_problems("distributive_property_near_numbers", {
            "problemCount": 10,
            "sheetCount": 1,
            "base": "near_100",
            "direction": "subtraction",
            "difficulty": "multiples_of_10",
            "layout": "distributive_property",
        })

        self.assertEqual(len(problems), 10)
        for problem in problems:
            parsed = re.fullmatch(r"(\d+) x (\d+) = \1 x \((\d+) - (\d+)\)", problem.prompt)
            self.assertIsNotNone(parsed)
            factor, _target, base, offset = (int(value) for value in parsed.groups())
            self.assertEqual(base % 100, 0)
            self.assertEqual(problem.answer, str(factor * (base - offset)))

    def test_generates_breaking_parentheses_problems(self):
        problems = generate_problems("breaking_parentheses", {
            "problemCount": 20,
            "sheetCount": 1,
            "layout": "breaking_parentheses",
        })

        self.assertEqual(len(problems), 20)
        for problem in problems:
            self.assertEqual(problem.prompt.count("("), 1)
            self.assertEqual(problem.prompt.count(")"), 1)
            self.assertNotIn("(", problem.answer)
            self.assertNotIn(")", problem.answer)

            numbers = [int(value) for value in re.findall(r"\d+", problem.prompt)]
            parenthesized = re.search(r"\(([^)]+)\)", problem.prompt)
            self.assertIsNotNone(parenthesized)
            group_numbers = re.findall(r"\d+", parenthesized.group(1))

            self.assertGreaterEqual(len(numbers), 3)
            self.assertLessEqual(len(numbers), 7)
            self.assertTrue(all(1 <= value <= 50 for value in numbers))
            self.assertGreaterEqual(len(group_numbers), 2)
            self.assertLessEqual(len(group_numbers), 4)

    def test_generates_chicken_rabbit_word_problems(self):
        problems = generate_problems("chicken_rabbit", {
            "problemCount": 10,
            "numberSize": "small",
        })

        self.assertEqual(len(problems), 10)
        self.assertTrue(all(isinstance(problem, ChickenRabbitProblem) for problem in problems))
        self.assertTrue(all(problem.answer_a >= 1 and problem.answer_b >= 1 for problem in problems))
        self.assertTrue(all(problem.count_total <= 24 for problem in problems))
        self.assertTrue(all(problem.value_total > 0 for problem in problems))
        for problem in problems:
            self.assertEqual(problem.answer_a + problem.answer_b, problem.count_total)

    def test_chicken_rabbit_has_many_scenario_templates(self):
        self.assertGreaterEqual(len(VALID_SCENARIOS), 20)

    def test_generates_place_value_expanded_form(self):
        problems = generate_problems("place_value_expanded_form", {
            "problemCount": 10,
            "sheetCount": 1,
            "placeValueDigits": "4d",
            "zeroMode": "allow",
        })

        self.assertEqual(len(problems), 10)
        for problem in problems:
            self.assertTrue(problem.prompt.endswith("="))
            self.assertIn("+", problem.answer)
            self.assertRegex(problem.prompt, r"^\d,\d{3} =$")

    def test_generates_place_value_standard_form(self):
        problems = generate_problems("place_value_standard_form", {
            "problemCount": 10,
            "sheetCount": 1,
            "placeValueDigits": "3d",
            "zeroMode": "avoid",
        })

        self.assertEqual(len(problems), 10)
        for problem in problems:
            self.assertIn("+", problem.prompt)
            self.assertRegex(problem.answer, r"^\d{3}$")

    def test_generates_place_value_digit_value(self):
        problems = generate_problems("place_value_digit_value", {
            "problemCount": 10,
            "sheetCount": 1,
            "placeValueDigits": "5d",
            "zeroMode": "mixed",
        })

        self.assertEqual(len(problems), 10)
        for problem in problems:
            self.assertIn("what is the value of", problem.prompt)
            self.assertNotEqual(problem.answer, "0")

    def test_generates_reduce_fraction_problems(self):
        problems = generate_problems("fraction_reduce", {
            "problemCount": 10,
            "sheetCount": 1,
            "fractionDifficulty": "easy",
        })

        self.assertEqual(len(problems), 10)
        self.assertTrue(all(isinstance(problem, FractionProblem) for problem in problems))
        for problem in problems:
            numerator, denominator = _fraction_terms(problem.answer)
            self.assertEqual(math.gcd(numerator, denominator), 1)

    def test_generates_equivalent_fraction_problems(self):
        problems = generate_problems("fraction_equivalent", {
            "problemCount": 10,
            "sheetCount": 1,
            "fractionDifficulty": "medium",
        })

        self.assertEqual(len(problems), 10)
        for problem in problems:
            self.assertEqual(
                problem.left_numerator * problem.right_denominator,
                problem.right_numerator * problem.left_denominator,
            )

    def test_generates_compare_fraction_problems(self):
        problems = generate_problems("fraction_compare", {
            "problemCount": 10,
            "sheetCount": 1,
            "fractionDifficulty": "hard",
        })

        self.assertEqual(len(problems), 10)
        for problem in problems:
            left = problem.left_numerator * problem.right_denominator
            right = problem.right_numerator * problem.left_denominator
            self.assertEqual(problem.answer, ">" if left > right else "<")

    def test_generates_missing_number_line_problems(self):
        problems = generate_problems("number_line_missing", {
            "problemCount": 4,
            "sheetCount": 1,
            "numberLineSize": "small",
        })

        self.assertEqual(len(problems), 4)
        self.assertTrue(all(isinstance(problem, NumberLineProblem) for problem in problems))
        for problem in problems:
            self.assertEqual(len(problem.labels), 7)
            self.assertGreaterEqual(len(problem.missing_indexes), 2)
            self.assertEqual(len(problem.answer.split(", ")), len(problem.missing_indexes))

    def test_generates_read_clock_problems(self):
        problems = generate_problems("time_read_clock", {
            "problemCount": 4,
            "sheetCount": 1,
            "timeIncrement": "quarter_hour",
        })

        self.assertEqual(len(problems), 4)
        self.assertTrue(all(isinstance(problem, TimeProblem) for problem in problems))
        for problem in problems:
            self.assertEqual(problem.mode, "read")
            self.assertEqual(problem.minute % 15, 0)

    def test_generates_draw_clock_hands_problems(self):
        problems = generate_problems("time_draw_hands", {
            "problemCount": 4,
            "sheetCount": 1,
            "timeIncrement": "five_minutes",
        })

        self.assertEqual(len(problems), 4)
        self.assertTrue(all(problem.mode == "draw" for problem in problems))
        self.assertTrue(all(problem.minute % 5 == 0 for problem in problems))

    def test_generates_hundred_chart_problems(self):
        problems = generate_problems("hundred_chart_missing", {
            "problemCount": 1,
            "sheetCount": 1,
            "chartRange": "1_100",
            "blankPercent": 20,
            "skipMultiple": 5,
        })

        self.assertEqual(len(problems), 1)
        problem = problems[0]
        self.assertIsInstance(problem, HundredChartProblem)
        self.assertEqual(len(problem.values), 100)
        self.assertTrue(all(value % 5 == 0 for value in problem.missing_values))


def _binary_terms(prompt: str, operator: str) -> tuple[int, int]:
    left, rest = prompt.split(f" {operator} ")
    right = rest.split(" = ")[0]
    return int(left), int(right)


def _fraction_terms(value: str) -> tuple[int, int]:
    numerator, denominator = value.split("/")
    return int(numerator), int(denominator)


if __name__ == "__main__":
    unittest.main()
