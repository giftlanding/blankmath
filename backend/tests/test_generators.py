import sys
import unittest
import re
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.generators import generate_problems
from blankmath.panels.distributive_property import parse_distributive_property_problem


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
            parsed = parse_distributive_property_problem(problem.prompt)
            self.assertIsNotNone(parsed)
            self.assertEqual(parsed.operation, "-")
            self.assertEqual(parsed.base % 100, 0)
            self.assertEqual(problem.answer, str(parsed.answer))

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


if __name__ == "__main__":
    unittest.main()
