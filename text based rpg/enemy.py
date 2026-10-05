from character import Character


class Enemy(Character):
    def __init__(self, name, health, strength, defense):
        super().__init__(
            name,
            health,
            strength,
            defense
        )

    def choose_action(self, player):
        if self.health <= self.max_health * 0.3:
            return "retreat"

        return "attack"

    def take_action(self, player):
        action = self.choose_action(player)

        if action == "attack":
            damage = self.attack(player)

            print(
                f"{self.name} attacked "
                f"{player.name} for {damage} damage."
            )

            return (
                f"{self.name} attacked "
                f"{player.name} for {damage} damage."
            )

        elif action == "retreat":
            print(f"{self.name} retreated!")

            return f"{self.name} retreated!"

        return None