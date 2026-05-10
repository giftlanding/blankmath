import json
import os
import sys
import unittest
from pathlib import Path


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

    def test_accepts_known_worksheet_request_until_renderer_exists(self):
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
        self.assertEqual(result["statusCode"], 501)
        self.assertEqual(body["worksheetType"], "addition")


if __name__ == "__main__":
    unittest.main()
