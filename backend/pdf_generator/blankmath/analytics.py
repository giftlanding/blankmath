import json
import os
import uuid
from typing import Any
from urllib import parse, request


MEASUREMENT_URL = "https://www.google-analytics.com/mp/collect"


def record_pdf_generated(generate_request: dict[str, Any]) -> None:
    measurement_id = os.environ.get("GA4_MEASUREMENT_ID")
    api_secret = os.environ.get("GA4_API_SECRET")
    if not measurement_id or not api_secret:
        return

    payload = build_measurement_payload(generate_request)
    endpoint = f"{MEASUREMENT_URL}?{parse.urlencode({
        'measurement_id': measurement_id,
        'api_secret': api_secret,
    })}"
    body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        endpoint,
        data=body,
        headers={"content-type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=2):
            pass
    except Exception as error:
        print(f"GA4 generate_pdf event failed: {error}")


def build_measurement_payload(generate_request: dict[str, Any]) -> dict[str, Any]:
    analytics = generate_request.get("analytics") or {}
    options = generate_request.get("options") or {}
    params: dict[str, str | int | float | bool] = {
        "worksheet_type": str(generate_request.get("worksheetType", "")),
        "engagement_time_msec": 1,
    }

    for source_key, ga_key in [
        ("layout", "layout"),
        ("problemCount", "problem_count"),
        ("sheetCount", "sheet_count"),
        ("digits", "digits"),
        ("base", "base"),
        ("direction", "direction"),
        ("difficulty", "difficulty"),
        ("includeAnswerKey", "include_answer_key"),
    ]:
        value = options.get(source_key)
        if isinstance(value, str | int | float | bool):
            params[ga_key] = value

    return {
        "client_id": analytics.get("gaClientId") or str(uuid.uuid4()),
        "events": [
            {
                "name": "generate_pdf",
                "params": params,
            }
        ],
    }
