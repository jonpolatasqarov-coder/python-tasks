class Statistics:
    def __init__(self, user, deck):
        self.user = user
        self.deck = deck

    def get_accuracy(self):
        return self.user.get_accuracy()

    def get_hardest_cards(self):
        studied_cards = []

        for card in self.deck.cards:

            progress = self.user.get_card_progress(
                card
            )

            if progress["attempts"] > 0:
                studied_cards.append(
                    (card, progress)
                )

        return sorted(
            studied_cards,
            key=lambda item: item[1]["success_rate"]
        )

    def get_top_learned_topics(self):
        topic_data = {}

        for card in self.deck.cards:

            progress = self.user.get_card_progress(
                card
            )

            if progress["attempts"] == 0:
                continue

            if card.topic not in topic_data:
                topic_data[card.topic] = []

            topic_data[card.topic].append(
                progress["success_rate"]
            )

        topic_scores = []

        for topic, rates in topic_data.items():

            average_rate = (
                sum(rates)
                / len(rates)
            )

            topic_scores.append(
                (
                    topic,
                    round(average_rate, 2)
                )
            )

        return sorted(
            topic_scores,
            key=lambda item: item[1],
            reverse=True
        )

    def show_statistics(self):
        print("\n===== LEARNING STATISTICS =====")

        print(
            f"User: {self.user.name}"
        )

        print(
            f"Cards studied: "
            f"{self.user.cards_studied}"
        )

        print(
            f"Correct answers: "
            f"{self.user.correct_answers}"
        )

        print(
            f"Wrong answers: "
            f"{self.user.wrong_answers}"
        )

        print(
            f"Accuracy: "
            f"{self.get_accuracy():.2f}%"
        )

        print("\n===== HARDEST CARDS =====")

        hardest_cards = self.get_hardest_cards()

        if not hardest_cards:
            print("No studied cards yet.")

        else:
            for index, (card, progress) in enumerate(
                hardest_cards[:3],
                start=1
            ):
                print(
                    f"{index}. "
                    f"{card.question} "
                    f"[{card.topic}] "
                    f"({progress['success_rate']}%)"
                )

        print("\n===== TOP LEARNED TOPICS =====")

        topics = self.get_top_learned_topics()

        if not topics:
            print("No learned topics yet.")

        else:
            for index, (topic, rate) in enumerate(
                topics[:3],
                start=1
            ):
                print(
                    f"{index}. "
                    f"{topic}: "
                    f"{rate}% average success"
                )