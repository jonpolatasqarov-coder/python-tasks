class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def get_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards[index]

        return None

    def get_card_count(self):
        return len(self.cards)

    def get_due_cards(self, user):
        due_cards = []

        for card in self.cards:

            progress = user.get_card_progress(card)

            if progress["attempts"] == 0:
                due_cards.append(card)

            elif progress["repetition"].is_due():
                due_cards.append(card)

        return due_cards

    def show_cards(self):
        print(f"\n===== {self.name} =====")

        if not self.cards:
            print("Deck is empty.")
            return

        for index, card in enumerate(
            self.cards,
            start=1
        ):
            print(
                f"{index}. "
                f"{card.question} "
                f"[{card.difficulty}]"
            )