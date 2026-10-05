from spaced_repetition import SpacedRepetition


class User:
    def __init__(self, name):
        self.name = name

        self.cards_studied = 0
        self.correct_answers = 0
        self.wrong_answers = 0

        self.card_progress = {}

    def get_card_progress(self, card):
        if card.question not in self.card_progress:
            self.card_progress[card.question] = {
                "attempts": 0,
                "correct_answers": 0,
                "success_rate": 0,
                "repetition": SpacedRepetition()
            }

        return self.card_progress[card.question]

    def record_answer(self, card, is_correct):
        progress = self.get_card_progress(card)

        progress["attempts"] += 1

        if is_correct:
            progress["correct_answers"] += 1
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

        self.cards_studied += 1

        progress["success_rate"] = round(
            progress["correct_answers"]
            / progress["attempts"]
            * 100
        )

    def update_repetition(self, card, quality):
        progress = self.get_card_progress(card)

        progress["repetition"].update(quality)

    def get_accuracy(self):
        if self.cards_studied == 0:
            return 0

        return (
            self.correct_answers
            / self.cards_studied
            * 100
        )

    def show_statistics(self):
        print("\n===== USER STATISTICS =====")

        print(f"Name: {self.name}")

        print(
            f"Cards studied: "
            f"{self.cards_studied}"
        )

        print(
            f"Correct answers: "
            f"{self.correct_answers}"
        )

        print(
            f"Wrong answers: "
            f"{self.wrong_answers}"
        )

        print(
            f"Accuracy: "
            f"{self.get_accuracy():.2f}%"
        )