import hashlib
import os
from datetime import datetime, timezone

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
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=24 * 60 * 60,
    )


def _object_key(pdf: bytes) -> str:
    today = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    digest = hashlib.sha1(pdf).hexdigest()
    return f"generated/{today}/{digest}.pdf"
