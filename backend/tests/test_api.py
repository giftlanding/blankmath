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

    def test_rejects_invalid_regrouping_options(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "addition",
                "options": {
                    "problemCount": 20,
                    "sheetCount": 1,
                    "from": 0,
                    "to": 100,
                    "additionRegrouping": "always",
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

    def test_accepts_distributive_property_request(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "distributive_property_near_numbers",
                    "options": {
                        "problemCount": 10,
                        "sheetCount": 1,
                        "base": "near_100",
                        "direction": "subtraction",
                        "difficulty": "multiples_of_10",
                        "layout": "distributive_property",
                    },
                }),
            })

        self.assertEqual(result["statusCode"], 201)

    def test_accepts_breaking_parentheses_request(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "breaking_parentheses",
                    "options": {
                        "problemCount": 10,
                        "sheetCount": 1,
                        "layout": "breaking_parentheses",
                    },
                }),
            })

        self.assertEqual(result["statusCode"], 201)

    def test_accepts_chicken_rabbit_request(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "chicken_rabbit",
                    "options": {
                        "problemCount": 6,
                        "numberSize": "small",
                    },
                }),
            })

        self.assertEqual(result["statusCode"], 201)

    def test_rejects_invalid_chicken_rabbit_number_size(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "chicken_rabbit",
                "options": {
                    "problemCount": 6,
                    "numberSize": "medium",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_rejects_sheet_count_for_chicken_rabbit(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "chicken_rabbit",
                "options": {
                    "problemCount": 6,
                    "sheetCount": 2,
                    "numberSize": "small",
                    "layout": "chicken_rabbit",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_accepts_place_value_request(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "place_value_expanded_form",
                    "options": {
                        "problemCount": 10,
                        "sheetCount": 1,
                        "placeValueDigits": "4d",
                        "zeroMode": "mixed",
                        "includeAnswerKey": True,
                    },
                }),
            })

        self.assertEqual(result["statusCode"], 201)

    def test_accepts_fraction_request(self):
        with patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "fraction_reduce",
                    "options": {
                        "problemCount": 10,
                        "sheetCount": 1,
                        "fractionDifficulty": "easy",
                        "includeImproperFractions": False,
                        "includeAnswerKey": True,
                    },
                }),
            })

        self.assertEqual(result["statusCode"], 201)

    def test_rejects_invalid_fraction_options(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "fraction_compare",
                "options": {
                    "problemCount": 10,
                    "sheetCount": 1,
                    "fractionDifficulty": "extreme",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_rejects_invalid_place_value_options(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "place_value_digit_value",
                "options": {
                    "problemCount": 10,
                    "sheetCount": 1,
                    "placeValueDigits": "6d",
                    "zeroMode": "mixed",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_rejects_large_distributive_property_problem_count(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "distributive_property_near_numbers",
                "options": {
                    "problemCount": 30,
                    "sheetCount": 1,
                    "base": "near_100",
                    "direction": "subtraction",
                    "difficulty": "multiples_of_10",
                    "layout": "distributive_property",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

    def test_rejects_large_distributive_property_sheet_count(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "distributive_property_near_numbers",
                "options": {
                    "problemCount": 20,
                    "sheetCount": 11,
                    "base": "near_100",
                    "direction": "subtraction",
                    "difficulty": "multiples_of_10",
                    "layout": "distributive_property",
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)

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
        with (
            patch("blankmath.api.generate_worksheet_pdf", return_value="https://example.com/worksheet.pdf"),
            patch("blankmath.api.record_pdf_generated") as record_pdf_generated,
        ):
            result = handle_event({
                "headers": {"x-blankmath-internal-token": "test-token"},
                "body": json.dumps({
                    "worksheetType": "addition",
                    "analytics": {"gaClientId": "1234567890.9876543210"},
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
        record_pdf_generated.assert_called_once_with({
            "worksheetType": "addition",
            "analytics": {"gaClientId": "1234567890.9876543210"},
            "options": {
                "problemCount": 20,
                "sheetCount": 1,
                "from": 0,
                "to": 20,
            },
        })

    def test_rejects_unknown_analytics_fields(self):
        result = handle_event({
            "headers": {"x-blankmath-internal-token": "test-token"},
            "body": json.dumps({
                "worksheetType": "addition",
                "analytics": {"unknown": "value"},
                "options": {
                    "problemCount": 20,
                    "sheetCount": 1,
                    "from": 0,
                    "to": 20,
                },
            }),
        })

        self.assertEqual(result["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
