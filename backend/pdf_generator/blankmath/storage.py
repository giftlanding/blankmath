import hashlib
import os
from datetime import datetime, timezone
from urllib.parse import quote

import boto3


def upload_pdf(pdf: bytes) -> str:
    bucket = os.environ["GENERATED_PDFS_BUCKET"]
    key = _object_key(pdf)
    client = boto3.client("s3")
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=pdf,
        ContentType="application/pdf",
        ServerSideEncryption="AES256",
    )
    public_base_url = os.environ.get("GENERATED_PDFS_PUBLIC_BASE_URL")
    if not public_base_url:
        public_base_url = f"https://{bucket}.s3.amazonaws.com"
    return f"{public_base_url.rstrip('/')}/{quote(key)}"


def _object_key(pdf: bytes) -> str:
    today = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    digest = hashlib.sha1(pdf).hexdigest()
    return f"generated/{today}/{digest}.pdf"
