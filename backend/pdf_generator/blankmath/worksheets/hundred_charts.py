import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HundredChartProblem:
    prompt: str
    answer: str
    start: int
    values: tuple[int | None, ...]
    missing_values: tuple[int, ...]


def missing_numbers(options: dict[str, Any]) -> HundredChartProblem:
    start = _chart_start(options)
    blank_percent = int(options.get("blankPercent", 20))
    skip_multiple = int(options.get("skipMultiple", 0))
    values = list(range(start, start + 100))

    candidates = values if skip_multiple == 0 else [value for value in values if value % skip_multiple == 0]
    blank_count = max(1, round(len(values) * blank_percent / 100))
    blank_count = min(blank_count, len(candidates))
    missing_values = tuple(sorted(random.sample(candidates, blank_count)))
    missing_set = set(missing_values)
    visible_values = tuple(None if value in missing_set else value for value in values)

    return HundredChartProblem(
        prompt=f"Fill in the missing numbers from {start} to {start + 99}.",
        answer=", ".join(str(value) for value in missing_values),
        start=start,
        values=visible_values,
        missing_values=missing_values,
    )


def _chart_start(options: dict[str, Any]) -> int:
    range_option = str(options.get("chartRange", "1_100"))
    return {
        "1_100": 1,
        "0_99": 0,
        "101_200": 101,
        "201_300": 201,
    }[range_option]
