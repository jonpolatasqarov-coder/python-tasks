import random
from character import Character


class Enemy(Character):
    def __init__(self, name, health, strength, defense):
        super().__init__(name, health, strength, defense)
        self.has_retreat = False

    def choose_action(self, player):
        if (
            not self.is_alive()
            or self.has_retreat
            or not player.is_alive()
        ):
            return None

        if self.health <= 10:
            return random.choice(["attack", "retreat"])

        return "attack"

    def take_action(self, player):
        if (
            not self.is_alive()
            or self.has_retreat
            or not player.is_alive()
        ):
            return None

        action = self.choose_action(player)

        if action == "attack":
            damage = self.attack(player)
            message = (
                f"{self.name} attacked {player.name} "
                f"for {damage} damage."
            )
            print(message)
            return message

        if action == "retreat":
            self.has_retreat = True
            message = f"{self.name} retreated from battle!"
            print(message)
            return message

        return None
