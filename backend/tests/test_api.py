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
