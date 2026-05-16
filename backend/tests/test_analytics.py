import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))

from blankmath.analytics import build_measurement_payload, record_pdf_generated


class AnalyticsTest(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("GA4_MEASUREMENT_ID", None)
        os.environ.pop("GA4_API_SECRET", None)

    def test_builds_generate_pdf_payload(self):
        payload = build_measurement_payload({
            "worksheetType": "division",
            "analytics": {"gaClientId": "1234567890.9876543210"},
            "options": {
                "problemCount": 20,
                "sheetCount": 1,
                "digits": "2d",
                "layout": "long_division",
            },
        })

        self.assertEqual(payload["client_id"], "1234567890.9876543210")
        self.assertEqual(payload["events"][0]["name"], "generate_pdf")
        self.assertEqual(payload["events"][0]["params"]["worksheet_type"], "division")
        self.assertEqual(payload["events"][0]["params"]["layout"], "long_division")
        self.assertEqual(payload["events"][0]["params"]["problem_count"], 20)

    def test_skips_when_measurement_config_is_missing(self):
        with patch("blankmath.analytics.request.urlopen") as urlopen:
            record_pdf_generated({
                "worksheetType": "addition",
                "analytics": {},
                "options": {},
            })

        urlopen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
