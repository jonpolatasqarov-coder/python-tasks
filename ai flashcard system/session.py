from datetime import datetime


class Session:
    def __init__(self, user, deck):
        self.user = user
        self.deck = deck
        self.results = []
        self.start_time = datetime.now()

    def answer_card(self, card, user_answer):
        is_correct = card.check_answer(user_answer)

        self.user.record_answer(
            card,
            is_correct
        )

        self.results.append({
            "question": card.question,
            "correct": is_correct
        })

        self.log_answer(
            card,
            is_correct
        )

        return is_correct

    def log_answer(self, card, is_correct):
        result = (
            "correct"
            if is_correct
            else "wrong"
        )

        with open(
            "session.log",
            "a",
            encoding="utf-8"
        ) as file:

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            file.write(
                f"[{timestamp}] "
                f"{self.user.name} | "
                f"{card.question} | "
                f"{result}\n"
            )

    def show_results(self):
        print("\n===== SESSION RESULTS =====")

        for result in self.results:
            status = (
                "Correct"
                if result["correct"]
                else "Wrong"
            )

            print(
                f"{result['question']} - {status}"
            )

        print(
            f"\nCards answered: "
            f"{len(self.results)}"
        )

    def finish(self):
        self.show_results()

        print(
            f"\nSession finished for "
            f"{self.user.name}."
        )