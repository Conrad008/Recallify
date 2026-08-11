from dataclasses import dataclass
from datetime import date, timedelta

@dataclass
class ReviewResult:
    easiness_factor: float
    repetitions: int
    interval: int
    next_review_date: date

class SpacedRepetitionScheduler:

    MIN_EASINESS_FACTOR = 1.3
    DEFAULT_EASINESS_FACTOR = 2.5
 
    @staticmethod
    def calculate_next_review(
        quality_rating: int,
        easiness_factor: float,
        repetitions: int,
        interval: int,
        today: date = None,
    ) -> ReviewResult:
        if not (0 <= quality_rating <= 5):
            raise ValueError("quality_rating must be between 0 and 5")
 
        today = today or date.today()
 
        if quality_rating < 3:
            new_repetitions = 0
            new_interval = 1
        else:
            if repetitions == 0:
                new_interval = 1
            elif repetitions == 1:
                new_interval = 6
            else:
                new_interval = round(interval * easiness_factor)
            new_repetitions = repetitions + 1

        new_ef = easiness_factor + (
            0.1 - (5 - quality_rating) * (0.08 + (5 - quality_rating) * 0.02)
        )
        new_ef = max(SpacedRepetitionScheduler.MIN_EASINESS_FACTOR, new_ef)
 
        next_review_date = today + timedelta(days=new_interval)
 
        return ReviewResult(
            easiness_factor=round(new_ef, 2),
            repetitions=new_repetitions,
            interval=new_interval,
            next_review_date=next_review_date,
        )
 