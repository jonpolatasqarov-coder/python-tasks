
from datetime import datetime

from player import Player
from enemy import Enemy
from item import HealthPotion, AncientKey
from quest import Quest
from world import World


class Game:
    def __init__(self):
        self.game_over = False

        self.world = World("Dark Forest")
        self.player = Player("Hero", 100, 20, 10)
        self.enemy = Enemy("Goblin", 60, 20, 5)
        self.potion = HealthPotion(30)

        # Defend cooldown
        self.player.defend_count = 0
        self.player.actions_since_defend = 0

        self.quests = [
            Quest("kill monster", "Goblin"),
            Quest("find item", "Ancient Key"),
            Quest("explore zone", "Dark Forest"),
        ]

        self.quest_index = 0
        self.quest = self.quests[self.quest_index]

        self.world.add_player(self.player)
        self.world.add_enemy(self.enemy)

        for quest in self.quests:
            self.world.add_quest(quest)

        self.player.add_item(self.potion)

        # Items available in the world
        self.world.add_item(HealthPotion(30))
        self.world.add_item(AncientKey())

    def log_action(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("log.txt", "a", encoding="utf-8") as file:
            file.write(
                f"[{timestamp}] [Player: {self.player.name}] "
                f"{message}\n"
            )

    def complete_current_quest(self):
        if not self.quest.completed:
            self.quest.complete()
            self.log_action(f"Quest completed: {self.quest}")

        if self.quest_index < len(self.quests) - 1:
            self.quest_index += 1
            self.quest = self.quests[self.quest_index]

            message = f"New quest: {self.quest}"
            print(message)
            self.log_action(message)
        else:
            self.check_end_game()

    def check_quest(self, action, item=None):
        if self.quest.completed:
            return

        if self.quest.quest_type == "find item":
            if action == "item" and item is not None:
                if item.name == self.quest.target:
                    self.complete_current_quest()

        elif self.quest.quest_type == "explore zone":
            if action == "explore":
                self.complete_current_quest()

    def show_status(self):
        print("\n=== PLAYER STATUS ===")
        print(f"Name: {self.player.name}")
        print(
            f"Health: {self.player.health}/{self.player.max_health}"
        )
        print(f"Strength: {self.player.strength}")
        print(f"Defense: {self.player.defense}")
        print(f"State: {self.player.state.__class__.__name__}")

        print("\nInventory:")

        if self.player.inventory:
            for item in self.player.inventory:
                print(f"- {item.name}")
        else:
            print("- Empty")

        print("\n=== ENEMY STATUS ===")
        print(f"Name: {self.enemy.name}")
        print(
            f"Health: {self.enemy.health}/{self.enemy.max_health}"
        )
        print(f"Strength: {self.enemy.strength}")
        print(f"Alive: {self.enemy.is_alive()}")
        print(f"Retreated: {self.enemy.has_retreat}")

        print("\n=== CURRENT QUEST ===")
        print(self.quest)

        if self.player.defend_count:
            print(
                "Defend cooldown: "
                f"{self.player.actions_since_defend}/3 actions"
            )
        else:
            print("Defend: Ready")

    def player_attack(self):
        if not self.player.is_alive():
            print("You are dead.")
            return False

        if self.enemy.has_retreat:
            print("Goblin has escaped. Start another battle to fight again.")
            return False

        if not self.enemy.is_alive():
            print("Goblin is already defeated!")
            print("Complete the remaining quests to achieve victory.")
            return False

        damage = self.player.attack(self.enemy)

        message = (
            f"{self.player.name} attacked {self.enemy.name} "
            f"for {damage} damage."
        )
        print(message)
        self.log_action(message)

        if not self.enemy.is_alive():
            message = f"{self.enemy.name} was defeated!"
            print(message)
            self.log_action(message)

            if (
                self.quest.quest_type == "kill monster"
                and self.quest.target == self.enemy.name
            ):
                self.complete_current_quest()

        return True

    def player_defend(self):
        if not self.player.is_alive():
            print("You are dead.")
            return False

        if not self.enemy.is_alive():
            print("The enemy has been defeated.")
            return False

        self.player.defend()
        self.log_action(f"{self.player.name} defended.")
        return True

    def player_use_potion(self):
        if not self.player.is_alive():
            print("You are dead.")
            return False

        if not self.player.inventory:
            print("You have no items.")
            return False

        item = self.player.inventory[0]

        if item.name == "Health Potion":
            if self.player.health >= self.player.max_health:
                print("Health is already full.")
                return False

        old_health = self.player.health
        self.player.use_item(item)

        if self.player.health == old_health:
            return False

        message = (
            f"{self.player.name} used {item.name}. "
            f"Health: {old_health} -> {self.player.health}"
        )

        print(message)
        self.log_action(message)
        return True

    def player_explore(self):
        if not self.player.is_alive():
            print("You are dead.")
            return False

        if self.quest.quest_type == "explore zone":
            message = f"You explored {self.world.name}."
            print(message)
            self.log_action(message)
            self.complete_current_quest()
            return True

        if self.quest.quest_type == "find item":
            target_item = next(
                (
                    item
                    for item in self.world.items
                    if item.name == self.quest.target
                ),
                None,
            )

            if target_item is None:
                print(
                    f"{self.quest.target} cannot be found "
                    "in this world."
                )
                return False

            self.world.items.remove(target_item)
            self.player.add_item(target_item)

            print(f"You found: {target_item.name}!")
            self.log_action(f"You found {target_item.name}.")
            self.check_quest("item", target_item)

            return True

        print("There is no exploration quest active.")
        return False

    def enemy_turn(self):
        if (
            not self.enemy.is_alive()
            or self.enemy.has_retreat
            or not self.player.is_alive()
        ):
            return

        message = self.enemy.take_action(self.player)

        if message:
            self.log_action(message)

        self.player.update_state()

        if not self.player.is_alive():
            self.check_end_game()

    def run_turn(self, action):
        if self.game_over:
            print("The game is over. Start a new game to continue.")
            return

        actions = {
            "attack": self.player_attack,
            "defend": self.player_defend,
            "potion": self.player_use_potion,
        }

        if action not in actions:
            print("Unknown battle action.")
            return

        if not self.player.is_alive():
            print("You are dead.")
            self.check_end_game()
            return

        if self.enemy.has_retreat:
            print("Goblin has escaped. Start another battle first.")
            return

        if not self.enemy.is_alive():
            print(
                "The enemy has been defeated. "
                "Complete the remaining quests!"
            )
            return

        # Defend cooldown
        if (
            action == "defend"
            and self.player.defend_count >= 1
            and self.player.actions_since_defend < 3
        ):
            remaining = 3 - self.player.actions_since_defend

            print(
                "You can't defend again yet! "
                f"{remaining} successful action(s) remaining."
            )
            self.log_action("Defend failed: cooldown active.")

            if self.enemy.is_alive() and self.player.is_alive():
                self.enemy_turn()

            self.check_end_game()
            return

        self.player.reset_defense()

        action_successful = actions[action]()

        if not action_successful:
            self.check_end_game()
            return

        # Apply the current player state effect after a successful action.
        if not self.player.perform_action():
            self.check_end_game()
            return

        if action == "defend":
            self.player.defend_count = 1
            self.player.actions_since_defend = 0

        elif self.player.defend_count >= 1:
            self.player.actions_since_defend += 1

            if self.player.actions_since_defend >= 3:
                self.player.defend_count = 0
                self.player.actions_since_defend = 0
                self.log_action("Defend cooldown finished.")

        if self.enemy.is_alive() and self.player.is_alive():
            self.enemy_turn()

        self.player.reset_defense()
        self.check_end_game()

    def check_end_game(self):
        if self.game_over:
            return

        if not self.player.is_alive():
            self.player.health = 0
            print("\n=== GAME OVER ===")
            print("You have been defeated!")
            self.game_over = True

        elif all(quest.completed for quest in self.quests):
            print("\n=== VICTORY ===")
            print("You completed all quests!")
            self.game_over = True

    def show_world(self):
        print(f"\n===== WORLD: {self.world.name} =====")

        print("\nPlayers:")
        for player in self.world.players:
            print(f"- {player.name}")

        print("\nEnemies:")
        for enemy in self.world.enemies:
            print(f"- {enemy.name} (HP: {enemy.health})")

        print("\nItems:")
        if self.world.items:
            for item in self.world.items:
                print(f"- {item.name}")
        else:
            print("No items remaining.")

        print("\nQuests:")
        for quest in self.quests:
            status = "Completed" if quest.completed else "Active"
            print(
                f"- {quest.quest_type}: "
                f"{quest.target} [{status}]"
            )
