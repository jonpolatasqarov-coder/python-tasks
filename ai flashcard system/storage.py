import json
from datetime import datetime
from spaced_repetition import SpacedRepetition


class Storage:
    def __init__(
        self,
        filename="sessions.json",
        users_filename="users.json"
    ):
        self.filename = filename
        self.users_filename = users_filename

    # =========================
    # SESSION STORAGE
    # =========================

    def save_session(self, session):
        sessions = self.load_sessions()

        session_data = {
            "user": session.user.name,
            "deck": session.deck.name,
            "results": session.results,
            "start_time": session.start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        sessions.append(session_data)

        with open(
            self.filename,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                sessions,
                file,
                indent=4,
                ensure_ascii=False
            )

    def load_sessions(self):
        try:
            with open(
                self.filename,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except FileNotFoundError:
            return []

    # =========================
    # USER STORAGE
    # =========================

    def save_user(self, user):
        users = self.load_users()

        user_data = {
            "name": user.name,
            "cards_studied": user.cards_studied,
            "correct_answers": user.correct_answers,
            "wrong_answers": user.wrong_answers,
            "card_progress": {}
        }

        for question, progress in user.card_progress.items():

            repetition = progress["repetition"]

            user_data["card_progress"][question] = {
                "attempts": progress["attempts"],
                "correct_answers": progress["correct_answers"],
                "success_rate": progress["success_rate"],
                "repetition": {
                    "repetitions": repetition.repetitions,
                    "interval": repetition.interval,
                    "ease_factor": repetition.ease_factor,
                    "next_review": (
                        repetition.next_review.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )
                }
            }

        user_found = False

        for saved_user in users:

            if (
                saved_user["name"].lower()
                == user.name.lower()
            ):
                saved_user.update(user_data)
                user_found = True
                break

        if not user_found:
            users.append(user_data)

        with open(
            self.users_filename,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                users,
                file,
                indent=4,
                ensure_ascii=False
            )

    def load_users(self):
        try:
            with open(
                self.users_filename,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except FileNotFoundError:
            return []

    def load_user(self, user):
        users = self.load_users()

        for saved_user in users:

            if (
                saved_user["name"].lower()
                == user.name.lower()
            ):
                user.cards_studied = saved_user.get(
                    "cards_studied",
                    0
                )

                user.correct_answers = saved_user.get(
                    "correct_answers",
                    0
                )

                user.wrong_answers = saved_user.get(
                    "wrong_answers",
                    0
                )

                saved_progress = saved_user.get(
                    "card_progress",
                    {}
                )

                for question, data in saved_progress.items():

                    repetition_data = data.get(
                        "repetition",
                        {}
                    )

                    repetition = SpacedRepetition()

                    repetition.repetitions = (
                        repetition_data.get(
                            "repetitions",
                            0
                        )
                    )

                    repetition.interval = (
                        repetition_data.get(
                            "interval",
                            0
                        )
                    )

                    repetition.ease_factor = (
                        repetition_data.get(
                            "ease_factor",
                            2.5
                        )
                    )

                    next_review = repetition_data.get(
                        "next_review"
                    )

                    if next_review:
                        repetition.next_review = (
                            datetime.strptime(
                                next_review,
                                "%Y-%m-%d %H:%M:%S"
                            )
                        )

                    user.card_progress[question] = {
                        "attempts": data.get(
                            "attempts",
                            0
                        ),
                        "correct_answers": data.get(
                            "correct_answers",
                            0
                        ),
                        "success_rate": data.get(
                            "success_rate",
                            0
                        ),
                        "repetition": repetition
                    }

                return

    # =========================
    # SAVED SESSIONS
    # =========================

    def show_sessions(self):
        sessions = self.load_sessions()

        print("\n===== SAVED SESSIONS =====")

        if not sessions:
            print("No saved sessions.")
            return

        for index, session in enumerate(
            sessions,
            start=1
        ):
            print(
                f"{index}. "
                f"{session['user']} | "
                f"{session['deck']} | "
                f"{len(session['results'])} answers | "
                f"{session['start_time']}"
            )