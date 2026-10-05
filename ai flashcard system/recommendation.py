class Recommendation:
    def __init__(self, user, deck):
        self.user = user
        self.deck = deck

    def get_recommendations(self):
        recommendations = []

        for card in self.deck.cards:

            progress = self.user.get_card_progress(
                card
            )

            attempts = progress["attempts"]

            if attempts == 0:
                recommendations.append({
                    "card": card,
                    "reason": "Not studied yet",
                    "score": 100
                })

                continue

            success_rate = progress["success_rate"]

            repetition = progress["repetition"]

            if repetition.is_due():

                recommendations.append({
                    "card": card,
                    "reason": "Due for review",
                    "score": 90
                })

            elif success_rate < 50:

                recommendations.append({
                    "card": card,
                    "reason": "Very low success rate",
                    "score": 80
                })

            elif success_rate < 70:

                recommendations.append({
                    "card": card,
                    "reason": "Low success rate",
                    "score": 70
                })

        return sorted(
            recommendations,
            key=lambda item: item["score"],
            reverse=True
        )

    def get_recommended_topics(self):
        topic_data = {}

        for card in self.deck.cards:

            progress = self.user.get_card_progress(
                card
            )

            if progress["attempts"] == 0:
                continue

            topic = card.topic

            if topic not in topic_data:
                topic_data[topic] = []

            topic_data[topic].append(
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
            key=lambda item: item[1]
        )

    def show_recommendations(self):
        print(
            "\n===== AI RECOMMENDATIONS ====="
        )

        recommendations = (
            self.get_recommendations()
        )

        if not recommendations:
            print(
                "No recommendations right now."
            )
            return

        for index, item in enumerate(
            recommendations[:3],
            start=1
        ):
            card = item["card"]

            progress = (
                self.user.get_card_progress(
                    card
                )
            )

            print(
                f"\n{index}. "
                f"{card.question}"
            )

            print(
                f"   Topic: "
                f"{card.topic}"
            )

            print(
                f"   Success rate: "
                f"{progress['success_rate']}%"
            )

            print(
                f"   Reason: "
                f"{item['reason']}"
            )

        topics = self.get_recommended_topics()

        if topics:
            print(
                "\n===== RECOMMENDED TOPIC ====="
            )

            topic, rate = topics[0]

            print(
                f"Topic: {topic}"
            )

            print(
                f"Average success: {rate}%"
            )