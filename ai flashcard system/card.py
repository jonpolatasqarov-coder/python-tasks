class Card:
    def __init__(
        self,
        question,
        answer,
        difficulty="medium",
        topic="General"
    ):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.topic = topic

    def check_answer(self, user_answer):
        return (
            user_answer.strip().lower()
            == self.answer.strip().lower()
        )

    def __str__(self):
        return (
            f"Question: {self.question} | "
            f"Topic: {self.topic} | "
            f"Difficulty: {self.difficulty}"
        )