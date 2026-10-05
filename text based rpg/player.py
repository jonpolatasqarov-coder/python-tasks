from character import Character
from states import HealthyState, PoisonedState, DeadState


class Player(Character):
    def __init__(self, name, health, strength, defense):
        super().__init__(
            name,
            health,
            strength,
            defense
        )

        self.base_defense = defense
        self.inventory = []
        self.state = HealthyState()

    def update_state(self):
        if self.health <= 0:
            self.health = 0
            self.state = DeadState()

        elif self.health <= self.max_health * 0.3:
            self.state = PoisonedState()

        else:
            self.state = HealthyState()

    def perform_action(self):
        self.update_state()
        self.state.handle_action(self)
        self.update_state()

    def defend(self):
        if isinstance(self.state, DeadState):
            print(f"{self.name} is dead and cannot defend.")
            return

        self.defense = self.base_defense + 5

        print(f"{self.name} is defending!")

    def reset_defense(self):
        self.defense = self.base_defense

    def use_item(self, item):
        if isinstance(self.state, DeadState):
            print(f"{self.name} is dead and cannot use items.")
            return

        if item in self.inventory:
            item.use(self)
            self.inventory.remove(item)
            self.update_state()
        else:
            print("Item is not in inventory.")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{item.name} added to inventory.")