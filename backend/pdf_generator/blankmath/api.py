import json
import os
from typing import Any

from blankmath.analytics import record_pdf_generated
from blankmath.validation import ValidationError, parse_generate_request


def handle_event(event: dict[str, Any]) -> dict[str, Any]:
    expected_token = os.environ.get("INTERNAL_API_TOKEN")
    headers = event.get("headers") or {}
    provided_token = headers.get("x-blankmath-internal-token") or headers.get("X-Blankmath-Internal-Token")

    if not expected_token or provided_token != expected_token:
        return response(403, {"error": "forbidden"})

    try:
        body = json.loads(event.get("body") or "{}")
        request = parse_generate_request(body)
    except json.JSONDecodeError:
        return response(400, {"error": "invalid_json"})
    except ValidationError as error:
        return response(400, {"error": "invalid_request", "message": str(error)})
    except Exception:
        return response(400, {"error": "invalid_request", "message": "Request could not be parsed."})

    try:
        url = generate_worksheet_pdf(request)
    except Exception as error:
        return response(500, {"error": "generation_failed", "message": str(error)})

    record_pdf_generated(request)
    return response(201, {"url": url})


def response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
        },
        "body": json.dumps(body),
    }


def generate_worksheet_pdf(request: dict[str, Any]) -> str:
    from blankmath.service import generate_worksheet_pdf as generate

    return generate(request)
