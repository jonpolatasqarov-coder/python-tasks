class Item:
    def __init__(self, name):
        self.name = name

    def use(self, player):
        raise NotImplementedError


class HealthPotion(Item):
    def __init__(self, heal_amount):
        super().__init__("Health Potion")
        self.heal_amount = heal_amount

    def use(self, player):
        old_health = player.health

        player.health = min(
            player.max_health,
            player.health + self.heal_amount
        )

        healed = player.health - old_health

        print(
            f"{player.name} used Health Potion "
            f"and restored {healed} HP."
        )