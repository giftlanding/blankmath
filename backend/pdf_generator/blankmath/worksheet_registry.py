from dataclasses import dataclass


@dataclass(frozen=True)
class WorksheetDefinition:
    title: str
    default_layout: str = "horizontal"
    option_profile: str = "standard"
    allowed_problem_counts: tuple[int, ...] = (10, 20, 30, 50)
    max_sheet_count: int = 50
    allow_answer_key: bool = True


WORKSHEETS: dict[str, WorksheetDefinition] = {
    "addition": WorksheetDefinition("Addition", option_profile="range_layout"),
    "minus": WorksheetDefinition("Subtraction", option_profile="range_layout"),
    "mixed_add_minus": WorksheetDefinition("Mixed Addition and Subtraction", option_profile="range_layout"),
    "additionmn": WorksheetDefinition("Addition Missing Number", option_profile="range_layout"),
    "minusmn": WorksheetDefinition("Subtraction Missing Number", option_profile="range_layout"),
    "mixed_add_minus_mn": WorksheetDefinition("Mixed Addition and Subtraction Missing Number", option_profile="range_layout"),
    "add_three_numbers": WorksheetDefinition("Add Three Numbers", option_profile="digits"),
    "add_minus_three_numbers": WorksheetDefinition("Add and Subtract Three Numbers", option_profile="digits"),
    "add_three_numbers_mn": WorksheetDefinition("Add Three Numbers Missing Number", option_profile="digits"),
    "multiplication": WorksheetDefinition("Multiplication", option_profile="digits_layout"),
    "division": WorksheetDefinition("Division", option_profile="division"),
    "mixed_times_divide": WorksheetDefinition("Mixed Multiplication and Division", option_profile="digits_layout"),
    "multiplicationmn": WorksheetDefinition("Multiplication Missing Number", option_profile="digits_layout"),
    "division_mn": WorksheetDefinition("Division Missing Number", option_profile="digits_layout"),
    "mixed_times_divide_mn": WorksheetDefinition("Mixed Multiplication and Division Missing Number", option_profile="digits_layout"),
    "greater_than_less_than": WorksheetDefinition("Greater Than or Less Than", option_profile="digits"),
    "distributive_property_near_numbers": WorksheetDefinition(
        "Distributive Property",
        default_layout="distributive_property",
        option_profile="distributive_property",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "breaking_parentheses": WorksheetDefinition(
        "Breaking Parentheses Practice",
        default_layout="breaking_parentheses",
        option_profile="breaking_parentheses",
        allowed_problem_counts=(10, 15, 20),
        max_sheet_count=10,
        allow_answer_key=False,
    ),
    "chicken_rabbit": WorksheetDefinition(
        "Chicken-Rabbit Word Problems",
        default_layout="chicken_rabbit",
        option_profile="chicken_rabbit",
        allowed_problem_counts=(4, 6, 8, 10),
        max_sheet_count=10,
    ),
    "place_value_expanded_form": WorksheetDefinition(
        "Expanded Form",
        default_layout="place_value",
        option_profile="place_value",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "place_value_standard_form": WorksheetDefinition(
        "Standard Form",
        default_layout="place_value",
        option_profile="place_value",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "place_value_digit_value": WorksheetDefinition(
        "Digit Value",
        default_layout="place_value",
        option_profile="place_value",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "fraction_reduce": WorksheetDefinition(
        "Reduce Fractions",
        default_layout="fraction",
        option_profile="fraction",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "fraction_equivalent": WorksheetDefinition(
        "Equivalent Fractions",
        default_layout="fraction",
        option_profile="fraction",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "fraction_compare": WorksheetDefinition(
        "Compare Fractions",
        default_layout="fraction",
        option_profile="fraction",
        allowed_problem_counts=(10, 20),
        max_sheet_count=10,
    ),
    "number_line_missing": WorksheetDefinition(
        "Missing Number Lines",
        default_layout="number_line",
        option_profile="number_line",
        allowed_problem_counts=(4, 6, 8),
        max_sheet_count=10,
    ),
    "time_read_clock": WorksheetDefinition(
        "Read Analog Clocks",
        default_layout="clock",
        option_profile="time",
        allowed_problem_counts=(4, 6, 8),
        max_sheet_count=10,
    ),
    "time_draw_hands": WorksheetDefinition(
        "Draw Clock Hands",
        default_layout="clock",
        option_profile="time",
        allowed_problem_counts=(4, 6, 8),
        max_sheet_count=10,
    ),
}


def worksheet_definition(worksheet_type: str) -> WorksheetDefinition:
    return WORKSHEETS[worksheet_type]
