class HealthyState:
    def handle_action(self, player):
        print(f"{player.name} is healthy and can act normally.")


class PoisonedState:
    def handle_action(self, player):
        player.health -= 5

        if player.health < 0:
            player.health = 0

        print(
            f"{player.name} is poisoned and lost 5 HP."
        )


class DeadState:
    def handle_action(self, player):
        print(f"{player.name} is dead and cannot act.")