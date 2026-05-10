import json
import os


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
        },
        "body": json.dumps(body),
    }


def handler(event, context):
    expected_token = os.environ.get("INTERNAL_API_TOKEN")
    headers = event.get("headers") or {}
    provided_token = headers.get("x-blankmath-internal-token") or headers.get("X-Blankmath-Internal-Token")

    if not expected_token or provided_token != expected_token:
        return response(403, {"error": "forbidden"})

    return response(
        501,
        {
            "error": "not_implemented",
            "message": "Blankmath PDF generation is not implemented yet.",
        },
    )
