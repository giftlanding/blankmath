from typing import Any, TypedDict

from blankmath.worksheet_registry import WORKSHEETS, worksheet_definition


class GenerateRequest(TypedDict):
    worksheetType: str
    options: dict[str, str | int | float | bool]
    analytics: dict[str, str]


class ValidationError(ValueError):
    pass


WORKSHEET_TYPES = set(WORKSHEETS)

PROBLEM_COUNTS = {10, 20, 30, 50}
PROPERTY_PROBLEM_COUNTS = {10, 20}
BREAKING_PARENTHESES_PROBLEM_COUNTS = {10, 15, 20}
SHEET_COUNT_MIN = 1
SHEET_COUNT_MAX = 50
PROPERTY_SHEET_COUNT_MAX = 10
BREAKING_PARENTHESES_SHEET_COUNT_MAX = 10
RANGE_MIN = 0
RANGE_MAX = 10000
DIGIT_OPTIONS = {"1d", "2d", "3d", "l12", "l20"}
LAYOUT_OPTIONS = {"horizontal", "vertical", "equation", "long_division", "distributive_property", "breaking_parentheses", "chicken_rabbit", "place_value"}
DIVISION_LAYOUT_OPTIONS = {"horizontal", "equation", "long_division"}
DISTRIBUTIVE_BASE_OPTIONS = {"near_10", "near_100", "mixed"}
DISTRIBUTIVE_DIRECTION_OPTIONS = {"addition", "subtraction", "mixed"}
DISTRIBUTIVE_DIFFICULTY_OPTIONS = {"one_digit", "two_digit", "multiples_of_10", "mixed"}
NUMBER_SIZE_OPTIONS = {"small", "big"}
PLACE_VALUE_DIGIT_OPTIONS = {"2d", "3d", "4d", "5d"}
ZERO_MODE_OPTIONS = {"avoid", "allow", "mixed"}

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

DISTRIBUTIVE_PROPERTY_WORKSHEET_TYPES = {
    "distributive_property_near_numbers",
}

BREAKING_PARENTHESES_WORKSHEET_TYPES = {
    "breaking_parentheses",
}

PLACE_VALUE_WORKSHEET_TYPES = {
    "place_value_expanded_form",
    "place_value_standard_form",
    "place_value_digit_value",
}

COMMON_OPTIONS = {"problemCount", "sheetCount", "includeAnswerKey"}
RANGE_OPTIONS = {"from", "to", "smallOperandLessThan10"}
DIGIT_OPTIONS_KEYS = {"digits"}
LAYOUT_OPTIONS_KEYS = {"layout"}
DISTRIBUTIVE_PROPERTY_OPTIONS = {"base", "direction", "difficulty"}
CHICKEN_RABBIT_OPTIONS = {"numberSize"}
PLACE_VALUE_OPTIONS = {"placeValueDigits", "zeroMode"}


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
    analytics = normalize_analytics(payload.get("analytics"))
    return {
        "worksheetType": worksheet_type,
        "options": normalized_options,
        "analytics": analytics,
    }


def normalize_analytics(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValidationError("Analytics must be an object.")

    normalized: dict[str, str] = {}
    for key in value:
        if key != "gaClientId":
            raise ValidationError(f"Unsupported analytics field {key}.")

    ga_client_id = value.get("gaClientId")
    if ga_client_id is None:
        return normalized
    if not isinstance(ga_client_id, str):
        raise ValidationError("GA client id must be a string.")

    stripped = ga_client_id.strip()
    if not stripped:
        return normalized
    if len(stripped) > 128:
        raise ValidationError("GA client id is too long.")

    normalized["gaClientId"] = stripped
    return normalized


def normalize_options(worksheet_type: str, options: dict[str, Any]) -> dict[str, str | int | float | bool]:
    normalized: dict[str, str | int | float | bool] = {}
    definition = worksheet_definition(worksheet_type)
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
    allowed_problem_counts = set(definition.allowed_problem_counts)
    if problem_count is not None and problem_count not in allowed_problem_counts:
        if worksheet_type in DISTRIBUTIVE_PROPERTY_WORKSHEET_TYPES:
            raise ValidationError("Problem count must be 10 or 20.")
        if worksheet_type in BREAKING_PARENTHESES_WORKSHEET_TYPES:
            raise ValidationError("Problem count must be 10, 15, or 20.")
        if worksheet_type == "chicken_rabbit":
            raise ValidationError("Problem count must be 4, 6, 8, or 10.")
        if worksheet_type in PLACE_VALUE_WORKSHEET_TYPES:
            raise ValidationError("Problem count must be 10 or 20.")
        raise ValidationError("Problem count must be 10, 20, 30, or 50.")

    sheet_count = int_option(normalized, "sheetCount")
    if sheet_count is not None and not SHEET_COUNT_MIN <= sheet_count <= SHEET_COUNT_MAX:
        raise ValidationError("Sheet count must be between 1 and 50.")
    if (
        worksheet_type in DISTRIBUTIVE_PROPERTY_WORKSHEET_TYPES
        and sheet_count is not None
        and sheet_count > PROPERTY_SHEET_COUNT_MAX
    ):
        raise ValidationError("Sheet count must be between 1 and 10 for distributive property worksheets.")
    if (
        worksheet_type in BREAKING_PARENTHESES_WORKSHEET_TYPES
        and sheet_count is not None
        and sheet_count > definition.max_sheet_count
    ):
        raise ValidationError("Sheet count must be between 1 and 10 for breaking parentheses worksheets.")
    if worksheet_type == "chicken_rabbit" and sheet_count is not None and sheet_count > definition.max_sheet_count:
        raise ValidationError("Sheet count must be between 1 and 10 for chicken-rabbit worksheets.")
    if worksheet_type in PLACE_VALUE_WORKSHEET_TYPES and sheet_count is not None and sheet_count > definition.max_sheet_count:
        raise ValidationError("Sheet count must be between 1 and 10 for place-value worksheets.")

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
        raise ValidationError("Layout must be horizontal, vertical, equation, long_division, distributive_property, or breaking_parentheses.")
    if worksheet_type == "division" and layout is not None and layout not in DIVISION_LAYOUT_OPTIONS:
        raise ValidationError("Division layout must be equation or long division.")
    if worksheet_type != "division" and layout == "long_division":
        raise ValidationError("Long division layout is only supported for division worksheets.")
    if worksheet_type != "distributive_property_near_numbers" and layout == "distributive_property":
        raise ValidationError("Distributive property layout is only supported for distributive property worksheets.")
    if worksheet_type != "breaking_parentheses" and layout == "breaking_parentheses":
        raise ValidationError("Breaking parentheses layout is only supported for breaking parentheses worksheets.")
    if worksheet_type != "chicken_rabbit" and layout == "chicken_rabbit":
        raise ValidationError("Chicken-rabbit layout is only supported for chicken-rabbit worksheets.")
    if worksheet_type not in PLACE_VALUE_WORKSHEET_TYPES and layout == "place_value":
        raise ValidationError("Place-value layout is only supported for place-value worksheets.")

    base = normalized.get("base")
    if base is not None and base not in DISTRIBUTIVE_BASE_OPTIONS:
        raise ValidationError("Base must be near_10, near_100, or mixed.")

    direction = normalized.get("direction")
    if direction is not None and direction not in DISTRIBUTIVE_DIRECTION_OPTIONS:
        raise ValidationError("Direction must be addition, subtraction, or mixed.")

    difficulty = normalized.get("difficulty")
    if difficulty is not None and difficulty not in DISTRIBUTIVE_DIFFICULTY_OPTIONS:
        raise ValidationError("Difficulty must be one_digit, two_digit, multiples_of_10, or mixed.")

    number_size = normalized.get("numberSize")
    if number_size is not None and number_size not in NUMBER_SIZE_OPTIONS:
        raise ValidationError("Number size must be small or big.")

    place_value_digits = normalized.get("placeValueDigits")
    if place_value_digits is not None and place_value_digits not in PLACE_VALUE_DIGIT_OPTIONS:
        raise ValidationError("Place-value digits must be 2d, 3d, 4d, or 5d.")

    zero_mode = normalized.get("zeroMode")
    if zero_mode is not None and zero_mode not in ZERO_MODE_OPTIONS:
        raise ValidationError("Zero mode must be avoid, allow, or mixed.")

    bool_option(normalized, "smallOperandLessThan10")
    bool_option(normalized, "includeAnswerKey")

    return normalized


def allowed_options_for(worksheet_type: str) -> set[str]:
    definition = worksheet_definition(worksheet_type)
    profile = definition.option_profile
    options = set(COMMON_OPTIONS)
    if not definition.allow_answer_key:
        options.remove("includeAnswerKey")
    if profile == "chicken_rabbit":
        options.remove("sheetCount")
    if profile == "range_layout":
        options.update(RANGE_OPTIONS)
        options.update(LAYOUT_OPTIONS_KEYS)
    if profile in {"digits", "digits_layout", "division"}:
        options.update(DIGIT_OPTIONS_KEYS)
    if profile in {"digits_layout", "division"}:
        options.update(LAYOUT_OPTIONS_KEYS)
    if profile == "distributive_property":
        options.update(LAYOUT_OPTIONS_KEYS)
        options.update(DISTRIBUTIVE_PROPERTY_OPTIONS)
    if profile == "breaking_parentheses":
        options.update(LAYOUT_OPTIONS_KEYS)
    if profile == "chicken_rabbit":
        options.update(LAYOUT_OPTIONS_KEYS)
        options.update(CHICKEN_RABBIT_OPTIONS)
    if profile == "place_value":
        options.update(PLACE_VALUE_OPTIONS)
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
