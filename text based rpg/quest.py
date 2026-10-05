import random


class Quest:
    def __init__(self, quest_type, target):
        self.quest_type = quest_type
        self.target = target
        self.completed = False

    def complete(self):
        if not self.completed:
            self.completed = True

            print(
                f"Quest completed: "
                f"{self.quest_type} - {self.target}"
            )

    def __str__(self):
        status = "Completed" if self.completed else "Active"

        return (
            f"{self.quest_type}: "
            f"{self.target} [{status}]"
        )


def generate_random_quest():
    quests = [
        Quest("top item", "Health Potion"),
        Quest("kill monster", "Goblin"),
        Quest("explore zone", "Dark Forest")
    ]

    return random.choice(quests)