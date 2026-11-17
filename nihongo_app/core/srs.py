"""SM-2 spaced-repetition scheduling."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class ReviewResult:
    item_id: str
    ease: float
    interval: int
    repetitions: int
    due: str
    lapses: int
    last_review: str


def initial_result(item_id: str) -> ReviewResult:
    return ReviewResult(item_id, 2.5, 0, 0, date.today().isoformat(), 0, "")


def schedule(result: ReviewResult, quality: int) -> ReviewResult:
    """quality: 0=Again, 3=Hard, 4=Good, 5=Easy."""
    today = date.today()
    reps = result.repetitions
    ease = result.ease
    lapses = result.lapses

    if quality < 3:
        reps = 0
        lapses += 1
        interval = 1
        ease = max(1.3, ease - 0.2)
    else:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = max(1, round(result.interval * ease))
        if quality == 3:
            interval = max(1, int(interval * 0.8))
            ease = max(1.3, ease - 0.15)
        elif quality == 5:
            ease = min(3.2, ease + 0.15)
            interval = max(1, int(interval * 1.15))
        reps += 1

    return ReviewResult(
        item_id=result.item_id,
        ease=round(ease, 2),
        interval=interval,
        repetitions=reps,
        due=(today + timedelta(days=interval)).isoformat(),
        lapses=lapses,
        last_review=today.isoformat(),
    )
