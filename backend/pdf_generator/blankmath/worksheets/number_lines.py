import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NumberLineProblem:
    prompt: str
    answer: str
    start: int
    step: int
    labels: tuple[int | None, ...]
    missing_indexes: tuple[int, ...]


def missing_labels(options: dict[str, Any]) -> NumberLineProblem:
    size = str(options.get("numberLineSize", "small"))
    if size == "large":
        step = random.choice([5, 10, 20, 25])
        start = random.randrange(0, 501, step)
    else:
        step = random.choice([1, 2, 5])
        start = random.randrange(0, 51, step)

    tick_count = 7
    values = [start + index * step for index in range(tick_count)]
    missing_count = random.choice([2, 3])
    middle_indexes = list(range(1, tick_count - 1))
    missing_indexes = tuple(sorted(random.sample(middle_indexes, missing_count)))
    labels: list[int | None] = []
    answers = []

    for index, value in enumerate(values):
        if index in missing_indexes:
            labels.append(None)
            answers.append(str(value))
        else:
            labels.append(value)

    prompt = f"Number line from {values[0]} to {values[-1]} by {step}."
    return NumberLineProblem(
        prompt=prompt,
        answer=", ".join(answers),
        start=start,
        step=step,
        labels=tuple(labels),
        missing_indexes=missing_indexes,
    )
