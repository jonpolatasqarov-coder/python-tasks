from card import Card
from deck import Deck
from user import User
from session import Session
from statistics import Statistics
from storage import Storage
from recommendation import Recommendation

def create_deck():
    deck = Deck("Python OOP")

    deck.add_card(
        Card(
            "What is a class?",
            "blueprint",
            "easy",
            "OOP"
        )
    )

    deck.add_card(
        Card(
            "What is inheritance?",
            "code reuse",
            "medium",
            "Inheritance"
        )
    )

    deck.add_card(
        Card(
            "What is polymorphism?",
            "many forms",
            "hard",
            "Polymorphism"
        )
    )

    deck.add_card(
        Card(
            "What is encapsulation?",
            "data hiding",
            "medium",
            "Encapsulation"
        )
    )

    return deck


def study_session(user, deck, storage):
    session = Session(
        user,
        deck
    )

    due_cards = deck.get_due_cards(user)

    print("\n===== STUDY SESSION =====")
    print(f"Deck: {deck.name}")

    if not due_cards:
        print(
            "No cards are due for review."
        )
        return

    print(
        f"Cards for review: "
        f"{len(due_cards)}"
    )

    print("Type 'exit' to stop.\n")

    for card in due_cards:

        print(
            f"Question: "
            f"{card.question}"
        )

        user_answer = input(
            "Your answer: "
        )

        if user_answer.lower() == "exit":
            break

        is_correct = session.answer_card(
            card,
            user_answer
        )

        if is_correct:
            print("Correct! ✓")

            user.update_repetition(
                card,
                5
            )

        else:
            print(
                f"Wrong! "
                f"Correct answer: "
                f"{card.answer}"
            )

            user.update_repetition(
                card,
                1
            )

        progress = user.get_card_progress(
            card
        )

        repetition = progress[
            "repetition"
        ]

        print(
            f"Repetitions: "
            f"{repetition.repetitions}"
        )

        print(
            f"Interval: "
            f"{repetition.interval} day(s)"
        )

        print(
            f"Next review: "
            f"{repetition.next_review.strftime(
                '%Y-%m-%d %H:%M:%S'
            )}"
        )

        print(
            f"Success rate: "
            f"{progress['success_rate']}%"
        )

        print()

    session.finish()

    storage.save_session(session)
    storage.save_user(user)

    print("\nSession saved.")


def main():
    print(
        "===== AI FLASHCARD SYSTEM ====="
    )

    user_name = input(
        "Enter your name: "
    )

    user = User(user_name)

    storage = Storage()

    storage.load_user(user)

    deck = create_deck()

    while True:

        print("1. Show cards")
        print("2. Start study session")
        print("3. Show statistics")
        print("4. Show saved sessions")
        print("5. AI recommendations")
        print("0. Exit")

        choice = input(
            "Choose an option: "
        )

        if choice == "1":
            deck.show_cards()

        elif choice == "2":
            study_session(
                user,
                deck,
                storage
            )

        elif choice == "3":
            statistics = Statistics(
                user,
                deck
            )

            statistics.show_statistics()

        elif choice == "4":
            storage.show_sessions()

        elif choice == "5":
            recommendation = Recommendation(
                user,
                deck
            )

            recommendation.show_recommendations()

        elif choice == "0":
            storage.save_user(user)

            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()