from datetime import datetime, timedelta


class SpacedRepetition:
    def __init__(self):
        self.repetitions = 0
        self.interval = 0
        self.ease_factor = 2.5
        self.next_review = datetime.now()

    def update(self, quality):
        if quality < 3:
            self.repetitions = 0
            self.interval = 1

        else:
            self.repetitions += 1

            if self.repetitions == 1:
                self.interval = 1

            elif self.repetitions == 2:
                self.interval = 6

            else:
                self.interval = round(
                    self.interval
                    * self.ease_factor
                )

            self.ease_factor += (
                0.1
                - (5 - quality)
                * (
                    0.08
                    + (5 - quality) * 0.02
                )
            )

            if self.ease_factor < 1.3:
                self.ease_factor = 1.3

        self.next_review = (
            datetime.now()
            + timedelta(
                days=self.interval
            )
        )

    def is_due(self):
        return datetime.now() >= self.next_review

    def get_status(self):
        return {
            "repetitions": self.repetitions,
            "interval": self.interval,
            "ease_factor": round(
                self.ease_factor,
                2
            ),
            "next_review": (
                self.next_review.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        }