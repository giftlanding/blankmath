import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TimeProblem:
    prompt: str
    answer: str
    hour: int
    minute: int
    mode: str


TIME_INCREMENTS = {
    "hour": 60,
    "half_hour": 30,
    "quarter_hour": 15,
    "five_minutes": 5,
    "one_minute": 1,
}


def read_clock(options: dict[str, Any]) -> TimeProblem:
    hour, minute = _time(options)
    answer = _time_text(hour, minute)
    return TimeProblem(
        prompt=f"What time is shown? {answer}",
        answer=answer,
        hour=hour,
        minute=minute,
        mode="read",
    )


def draw_clock_hands(options: dict[str, Any]) -> TimeProblem:
    hour, minute = _time(options)
    answer = _time_text(hour, minute)
    return TimeProblem(
        prompt=f"Draw hands for {answer}.",
        answer=answer,
        hour=hour,
        minute=minute,
        mode="draw",
    )


def _time(options: dict[str, Any]) -> tuple[int, int]:
    increment = TIME_INCREMENTS[str(options.get("timeIncrement", "five_minutes"))]
    hour = random.randint(1, 12)
    minute = random.randrange(0, 60, increment)
    return hour, minute


def _time_text(hour: int, minute: int) -> str:
    return f"{hour}:{minute:02d}"
