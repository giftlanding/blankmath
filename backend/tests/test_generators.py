import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.generators import generate_problems


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


if __name__ == "__main__":
    unittest.main()
