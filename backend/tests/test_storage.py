import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pdf_generator"))
sys.modules["boto3"] = MagicMock()

from blankmath.storage import upload_pdf


class StorageTest(unittest.TestCase):
    def setUp(self):
        os.environ["GENERATED_PDFS_BUCKET"] = "r.blankmath.com"
        os.environ["GENERATED_PDFS_PUBLIC_BASE_URL"] = "https://r.blankmath.com"

    def tearDown(self):
        os.environ.pop("GENERATED_PDFS_BUCKET", None)
        os.environ.pop("GENERATED_PDFS_PUBLIC_BASE_URL", None)

    def test_upload_returns_public_custom_domain_url(self):
        with patch("boto3.client") as boto3_client:
            url = upload_pdf(b"%PDF-test")

        s3_client = boto3_client.return_value
        s3_client.put_object.assert_called_once()
        s3_client.generate_presigned_url.assert_not_called()
        self.assertTrue(url.startswith("https://r.blankmath.com/generated/"))
        self.assertTrue(url.endswith(".pdf"))


if __name__ == "__main__":
    unittest.main()
