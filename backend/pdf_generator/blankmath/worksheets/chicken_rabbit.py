import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Scenario:
    id: str
    item_a: str
    item_b: str
    unit_a: int
    unit_b: int
    unit_name: str
    count_name: str
    template: str


@dataclass(frozen=True)
class ChickenRabbitProblem:
    prompt: str
    answer: str
    scenario_id: str
    item_a: str
    item_b: str
    answer_a: int
    answer_b: int
    count_total: int
    value_total: int
    number_size: str


SCENARIOS = (
    Scenario(
        "chicken_rabbit",
        "chickens",
        "rabbits",
        2,
        4,
        "legs",
        "animals",
        "A farmer has {count_total} chickens and rabbits. They have {value_total} legs altogether. How many chickens and rabbits are there?",
    ),
    Scenario(
        "duck_goat",
        "ducks",
        "goats",
        2,
        4,
        "legs",
        "animals",
        "A small farm has {count_total} ducks and goats. The animals have {value_total} legs altogether. How many ducks and goats are there?",
    ),
    Scenario(
        "spider_dragonfly",
        "spiders",
        "dragonflies",
        8,
        6,
        "legs",
        "creatures",
        "In a garden there are {count_total} spiders and dragonflies. They have {value_total} legs altogether. How many spiders and dragonflies are there?",
    ),
    Scenario(
        "tricycle_bicycle",
        "tricycles",
        "bicycles",
        3,
        2,
        "wheels",
        "cycles",
        "A playground has {count_total} tricycles and bicycles. They have {value_total} wheels altogether. How many tricycles and bicycles are there?",
    ),
    Scenario(
        "cars_motorcycles",
        "cars",
        "motorcycles",
        4,
        2,
        "wheels",
        "vehicles",
        "A parking lot has {count_total} cars and motorcycles. They have {value_total} wheels altogether. How many cars and motorcycles are there?",
    ),
    Scenario(
        "five_two_bills",
        "$5 bills",
        "$2 bills",
        5,
        2,
        "dollars",
        "bills",
        "There are {count_total} bills. Some are $5 bills and some are $2 bills. Their total value is ${value_total}. How many of each bill are there?",
    ),
    Scenario(
        "ten_five_bills",
        "$10 bills",
        "$5 bills",
        10,
        5,
        "dollars",
        "bills",
        "A wallet has {count_total} bills. Some are $10 bills and some are $5 bills. The total value is ${value_total}. How many of each bill are there?",
    ),
    Scenario(
        "quarters_dimes",
        "quarters",
        "dimes",
        25,
        10,
        "cents",
        "coins",
        "A jar has {count_total} quarters and dimes. The coins are worth {value_total} cents altogether. How many quarters and dimes are there?",
    ),
    Scenario(
        "nickels_pennies",
        "nickels",
        "pennies",
        5,
        1,
        "cents",
        "coins",
        "A pocket has {count_total} nickels and pennies. The coins are worth {value_total} cents altogether. How many nickels and pennies are there?",
    ),
    Scenario(
        "adult_child_tickets",
        "adult tickets",
        "child tickets",
        12,
        7,
        "dollars",
        "tickets",
        "A museum sold {count_total} adult and child tickets. The total ticket money was ${value_total}. How many adult tickets and child tickets were sold?",
    ),
    Scenario(
        "movie_snack_tickets",
        "movie tickets",
        "snack coupons",
        9,
        4,
        "dollars",
        "items",
        "A class bought {count_total} movie tickets and snack coupons. They spent ${value_total}. How many movie tickets and snack coupons did they buy?",
    ),
    Scenario(
        "sunny_rainy_days",
        "sunny days",
        "rainy days",
        20,
        12,
        "bananas",
        "days",
        "A monkey eats 20 bananas on a sunny day and 12 bananas on a rainy day. In {count_total} days it ate {value_total} bananas. How many sunny and rainy days were there?",
    ),
    Scenario(
        "reading_math_pages",
        "reading days",
        "math days",
        15,
        9,
        "pages",
        "days",
        "Mia practiced for {count_total} days. On reading days she read 15 pages. On math days she read 9 pages. She read {value_total} pages in all. How many reading and math days were there?",
    ),
    Scenario(
        "correct_wrong_score",
        "correct answers",
        "wrong answers",
        5,
        -3,
        "points",
        "questions",
        "A contest has {count_total} answered questions. Each correct answer earns 5 points and each wrong answer loses 3 points. The score was {value_total}. How many correct and wrong answers were there?",
    ),
    Scenario(
        "easy_hard_questions",
        "easy questions",
        "hard questions",
        2,
        5,
        "points",
        "questions",
        "A quiz has {count_total} easy and hard questions. Easy questions are worth 2 points and hard questions are worth 5 points. The quiz is worth {value_total} points. How many easy and hard questions are there?",
    ),
    Scenario(
        "girls_boys_trees",
        "girls",
        "boys",
        4,
        2,
        "trees",
        "students",
        "A class has {count_total} girls and boys planting trees. Each girl plants 4 trees and each boy plants 2 trees. They plant {value_total} trees altogether. How many girls and boys are there?",
    ),
    Scenario(
        "large_small_boxes",
        "large boxes",
        "small boxes",
        8,
        3,
        "books",
        "boxes",
        "There are {count_total} large and small boxes. A large box holds 8 books and a small box holds 3 books. The boxes hold {value_total} books altogether. How many large and small boxes are there?",
    ),
    Scenario(
        "tables_chairs",
        "tables",
        "chairs",
        4,
        1,
        "legs",
        "furniture pieces",
        "A room has {count_total} tables and chairs. Together they have {value_total} legs. How many tables and chairs are there?",
    ),
    Scenario(
        "cranes_turtles",
        "cranes",
        "turtles",
        2,
        4,
        "legs",
        "animals",
        "A pond has {count_total} cranes and turtles. They have {value_total} legs altogether. How many cranes and turtles are there?",
    ),
    Scenario(
        "stamps",
        "10-cent stamps",
        "4-cent stamps",
        10,
        4,
        "cents",
        "stamps",
        "An envelope has {count_total} 10-cent and 4-cent stamps. The stamps are worth {value_total} cents altogether. How many of each stamp are there?",
    ),
    Scenario(
        "vans_cars",
        "vans",
        "cars",
        7,
        5,
        "seats",
        "vehicles",
        "A field trip uses {count_total} vans and cars. Each van has 7 seats and each car has 5 seats. There are {value_total} seats altogether. How many vans and cars are there?",
    ),
    Scenario(
        "pencil_boxes_singles",
        "pencil boxes",
        "single pencils",
        10,
        1,
        "pencils",
        "items",
        "A drawer has {count_total} pencil boxes and single pencils. Each box has 10 pencils. There are {value_total} pencils altogether. How many boxes and single pencils are there?",
    ),
)

VALID_SCENARIOS = tuple(scenario for scenario in SCENARIOS if scenario.unit_a != scenario.unit_b)


def generate_chicken_rabbit_problem(options: dict[str, Any]) -> ChickenRabbitProblem:
    number_size = str(options.get("numberSize", "small"))
    scenario = random.choice(VALID_SCENARIOS)
    for _ in range(50):
        answer_a, answer_b = _answers(number_size)
        count_total = answer_a + answer_b
        value_total = scenario.unit_a * answer_a + scenario.unit_b * answer_b
        if value_total > 0:
            break
    else:
        raise ValueError("Unable to generate a positive total for chicken-rabbit problem.")
    prompt = scenario.template.format(count_total=count_total, value_total=value_total)
    answer = f"{scenario.item_a}: {answer_a}; {scenario.item_b}: {answer_b}"
    return ChickenRabbitProblem(
        prompt=prompt,
        answer=answer,
        scenario_id=scenario.id,
        item_a=scenario.item_a,
        item_b=scenario.item_b,
        answer_a=answer_a,
        answer_b=answer_b,
        count_total=count_total,
        value_total=value_total,
        number_size=number_size,
    )


def _answers(number_size: str) -> tuple[int, int]:
    if number_size == "big":
        left = random.randint(8, 120)
        right = random.randint(8, 120)
    else:
        left = random.randint(1, 12)
        right = random.randint(1, 12)
    return left, right
