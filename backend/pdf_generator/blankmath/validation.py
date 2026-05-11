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
SHEET_COUNT_MIN = 1
SHEET_COUNT_MAX = 50
RANGE_MIN = 0
RANGE_MAX = 10000
DIGIT_OPTIONS = {"1d", "2d", "3d", "l12", "l20"}
LAYOUT_OPTIONS = {"horizontal", "vertical"}

RANGE_WORKSHEET_TYPES = {
    "addition",
    "minus",
    "mixed_add_minus",
    "additionmn",
    "minusmn",
    "mixed_add_minus_mn",
}

DIGIT_WORKSHEET_TYPES = {
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

LAYOUT_WORKSHEET_TYPES = {
    "addition",
    "minus",
    "mixed_add_minus",
    "additionmn",
    "minusmn",
    "mixed_add_minus_mn",
    "multiplication",
    "division",
    "mixed_times_divide",
    "multiplicationmn",
    "division_mn",
    "mixed_times_divide_mn",
}

COMMON_OPTIONS = {"problemCount", "sheetCount", "includeAnswerKey"}
RANGE_OPTIONS = {"from", "to", "smallOperandLessThan10"}
DIGIT_OPTIONS_KEYS = {"digits"}
LAYOUT_OPTIONS_KEYS = {"layout"}


def parse_generate_request(payload: Any) -> GenerateRequest:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be an object.")

    worksheet_type = payload.get("worksheetType")
    if not isinstance(worksheet_type, str) or worksheet_type not in WORKSHEET_TYPES:
        raise ValidationError("Unknown worksheet type.")

    options = payload.get("options")
    if not isinstance(options, dict):
        raise ValidationError("Options must be an object.")

    normalized_options = normalize_options(worksheet_type, options)
    return {
        "worksheetType": worksheet_type,
        "options": normalized_options,
    }


def normalize_options(worksheet_type: str, options: dict[str, Any]) -> dict[str, str | int | float | bool]:
    normalized: dict[str, str | int | float | bool] = {}
    allowed_options = allowed_options_for(worksheet_type)

    for key, value in options.items():
        if not isinstance(key, str):
            raise ValidationError("Option names must be strings.")
        if key not in allowed_options:
            raise ValidationError(f"Unsupported option {key} for worksheet type {worksheet_type}.")
        if not isinstance(value, str | int | float | bool):
            raise ValidationError(f"Unsupported value for option {key}.")
        normalized[key] = value

    problem_count = int_option(normalized, "problemCount")
    if problem_count is not None and problem_count not in PROBLEM_COUNTS:
        raise ValidationError("Problem count must be 10, 20, 30, or 50.")

    sheet_count = int_option(normalized, "sheetCount")
    if sheet_count is not None and not SHEET_COUNT_MIN <= sheet_count <= SHEET_COUNT_MAX:
        raise ValidationError("Sheet count must be between 1 and 50.")

    from_value = int_option(normalized, "from")
    to_value = int_option(normalized, "to")
    if worksheet_type in RANGE_WORKSHEET_TYPES or from_value is not None or to_value is not None:
        if from_value is None or to_value is None:
            raise ValidationError("Both From and To are required for range worksheets.")
        if not RANGE_MIN <= from_value <= RANGE_MAX or not RANGE_MIN <= to_value <= RANGE_MAX:
            raise ValidationError("Range values must be between 0 and 10000.")
        if from_value >= to_value:
            raise ValidationError("From must be less than To.")

    digits = normalized.get("digits")
    if digits is not None and digits not in DIGIT_OPTIONS:
        raise ValidationError("Digits must be one of 1d, 2d, 3d, l12, or l20.")

    layout = normalized.get("layout")
    if layout is not None and layout not in LAYOUT_OPTIONS:
        raise ValidationError("Layout must be horizontal or vertical.")

    bool_option(normalized, "smallOperandLessThan10")
    bool_option(normalized, "includeAnswerKey")

    return normalized


def allowed_options_for(worksheet_type: str) -> set[str]:
    options = set(COMMON_OPTIONS)
    if worksheet_type in RANGE_WORKSHEET_TYPES:
        options.update(RANGE_OPTIONS)
    if worksheet_type in DIGIT_WORKSHEET_TYPES:
        options.update(DIGIT_OPTIONS_KEYS)
    if worksheet_type in LAYOUT_WORKSHEET_TYPES:
        options.update(LAYOUT_OPTIONS_KEYS)
    return options


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


def bool_option(options: dict[str, str | int | float | bool], key: str) -> bool | None:
    value = options.get(key)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValidationError(f"{key} must be true or false.")
    return value
