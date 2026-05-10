from typing import Any, TypedDict


class GenerateRequest(TypedDict):
    worksheetType: str
    options: dict[str, str | int | float | bool]


class ValidationError(ValueError):
    pass


WORKSHEET_TYPES = {
    "addition",
    "minus",
    "mixed_add_minus",
    "additionmn",
    "minusmn",
    "mixed_add_minus_mn",
    "add_three_numbers",
    "add_minus_three_numbers",
    "add_three_numbers_mn",
    "multiplication",
    "division",
    "mixed_times_divide",
    "multiplicationmn",
    "division_mn",
    "mixed_times_divide_mn",
    "greater_than_less_than",
}

PROBLEM_COUNTS = {10, 20, 30, 50}


def parse_generate_request(payload: Any) -> GenerateRequest:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be an object.")

    worksheet_type = payload.get("worksheetType")
    if not isinstance(worksheet_type, str) or worksheet_type not in WORKSHEET_TYPES:
        raise ValidationError("Unknown worksheet type.")

    options = payload.get("options")
    if not isinstance(options, dict):
        raise ValidationError("Options must be an object.")

    normalized_options = normalize_options(options)
    return {
        "worksheetType": worksheet_type,
        "options": normalized_options,
    }


def normalize_options(options: dict[str, Any]) -> dict[str, str | int | float | bool]:
    normalized: dict[str, str | int | float | bool] = {}

    for key, value in options.items():
        if not isinstance(key, str):
            raise ValidationError("Option names must be strings.")
        if not isinstance(value, str | int | float | bool):
            raise ValidationError(f"Unsupported value for option {key}.")
        normalized[key] = value

    problem_count = int_option(normalized, "problemCount")
    if problem_count is not None and problem_count not in PROBLEM_COUNTS:
        raise ValidationError("Problem count must be 10, 20, 30, or 50.")

    sheet_count = int_option(normalized, "sheetCount")
    if sheet_count is not None and not 1 <= sheet_count <= 50:
        raise ValidationError("Sheet count must be between 1 and 50.")

    from_value = int_option(normalized, "from")
    to_value = int_option(normalized, "to")
    if from_value is not None or to_value is not None:
        if from_value is None or to_value is None:
            raise ValidationError("Both From and To are required for range worksheets.")
        if not 0 <= from_value <= 10000 or not 0 <= to_value <= 10000:
            raise ValidationError("Range values must be between 0 and 10000.")
        if from_value >= to_value:
            raise ValidationError("From must be less than To.")

    return normalized


def int_option(options: dict[str, str | int | float | bool], key: str) -> int | None:
    value = options.get(key)
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValidationError(f"{key} must be a number.")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValidationError(f"{key} must be a number.") from error
    if str(parsed) != str(value):
        raise ValidationError(f"{key} must be an integer.")
    return parsed
