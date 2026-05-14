import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.api import handle_event


class ApiTest(unittest.TestCase):
    def setUp(self):
        os.environ["INTERNAL_API_TOKEN"] = "test-token"

    def test_rejects_missing_internal_token(self):
        result = handle_event({"headers": {}, "body": "{}"})

        self.assertEqual(result["statusCode"], 403)

    def test_validates_request_shape(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({"worksheetType": "addition", "options": {"problemCount": 25}}),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_requires_range_options_for_range_worksheets(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "addition",
                "options": {
                    "problemCount": 20,
                    "sheetCount": 1,
                },
            }),
        })

        body = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(body["error"], "invalid_request")

    def test_rejects_unknown_options(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "multiplication",
                "options": {
                    "problemCount": 20,
                    "sheetCount": 1,
                    "digits": "1d",
                    "layout": "vertical",
                    "from": 0,
                    "to": 20,
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_rejects_invalid_choice_options(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "multiplication",
                "options": {
                    "problemCount": 20,
                    "sheetCount": 1,
                    "digits": "4d",
                    "layout": "diagonal",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_accepts_long_division_layout_for_division(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "division",
                    "options": {
                        "problemCount": 10,
                        "sheetCount": 1,
                        "digits": "2d",
                        "layout": "long_division",
                    },
                }),
            })

        self.assertEqual(result["statusCode"], 201)

    def test_rejects_long_division_layout_for_non_division(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "multiplication",
                "options": {
                    "problemCount": 10,
                    "sheetCount": 1,
                    "digits": "2d",
                    "layout": "long_division",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_rejects_non_boolean_flags(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "addition",
                "options": {
                    "problemCount": 20,
                    "sheetCount": 1,
                    "from": 0,
                    "to": 20,
                    "smallOperandLessThan10": "true",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_accepts_known_worksheet_request(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "addition",
                    "options": {
                        "problemCount": 20,
                        "sheetCount": 1,
                        "from": 0,
                        "to": 20,
                    },
                }),
            })

        body = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 201)
        self.assertEqual(body["url"], "https://example.com/worksheet.pdf")


if __name__ == "__main__":
    unittest.main()
