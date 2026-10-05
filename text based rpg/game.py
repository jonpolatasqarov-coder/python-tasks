from datetime import datetime

from player import Player
from enemy import Enemy
from item import HealthPotion
from quest import generate_random_quest
from world import World


class Game:
    def __init__(self):
        self.world = World("Dark Forest")

        self.player = Player(
            "Hero",
            100,
            20,
            10
        )

        self.enemy = Enemy(
            "Goblin",
            60,
            15,
            5
        )

        self.potion = HealthPotion(30)

        self.quest = generate_random_quest()

        self.world.add_player(self.player)
        self.world.add_enemy(self.enemy)
        self.world.add_item(self.potion)
        self.world.add_quest(self.quest)

        self.player.add_item(self.potion)

        self.check_quest("item")

    def log_action(self, message):
        with open("log.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            file.write(
                f"[{timestamp}] {message}\n"
            )

    def check_quest(self, action):
        if self.quest.completed:
            return

        if self.quest.quest_type == "top item":
            for item in self.player.inventory:
                if item.name == self.quest.target:
                    self.quest.complete()

                    self.log_action(
                        f"Quest completed: {self.quest}"
                    )
                    return

        elif self.quest.quest_type == "explore zone":
            if action == "explore":
                self.quest.complete()

                self.log_action(
                    f"Quest completed: {self.quest}"
                )

    def show_status(self):
        print("\n===== PLAYER STATUS =====")
        print(f"Name: {self.player.name}")
        print(
            f"Health: "
            f"{self.player.health}/{self.player.max_health}"
        )
        print(f"Strength: {self.player.strength}")
        print(f"Defense: {self.player.defense}")
        print(
            f"State: "
            f"{self.player.state.__class__.__name__}"
        )

        print("\n===== ENEMY STATUS =====")
        print(f"Name: {self.enemy.name}")
        print(
            f"Health: "
            f"{self.enemy.health}/{self.enemy.max_health}"
        )

        print("\n===== QUEST =====")
        print(self.quest)

    def player_attack(self):
        if not self.player.is_alive():
            print("You are dead.")
            return

        if not self.enemy.is_alive():
            print("Enemy is already defeated.")
            return

        damage = self.player.attack(self.enemy)

        message = (
            f"{self.player.name} attacked "
            f"{self.enemy.name} for {damage} damage."
        )

        print(message)
        self.log_action(message)

        if not self.enemy.is_alive():
            print(f"{self.enemy.name} was defeated!")

            self.log_action(
                f"{self.enemy.name} was defeated."
            )

            if (
                self.quest.quest_type == "kill monster"
                and self.quest.target == self.enemy.name
            ):
                self.quest.complete()

                self.log_action(
                    f"Quest completed: {self.quest}"
                )

    def player_defend(self):
        if not self.player.is_alive():
            print("You are dead.")
            return

        self.player.defend()

        self.log_action(
            f"{self.player.name} defended."
        )

    def player_use_potion(self):
        if not self.player.is_alive():
            print("You are dead.")
            return False

        if not self.player.inventory:
            print("Inventory is empty.")
            return False

        item = self.player.inventory[0]

        if (
            item.name == "Health Potion"
            and self.player.health >= self.player.max_health
        ):
            print("Health is already full.")
            return False

        self.player.use_item(item)

        self.log_action(
            f"{self.player.name} used {item.name}."
        )

        self.check_quest("item")

        return True

    def player_explore(self):
        if not self.player.is_alive():
            print("You are dead.")
            return

        if self.quest.quest_type != "explore zone":
            print("There is no exploration quest active.")
            return

        zone = self.quest.target

        print(
            f"{self.player.name} explored "
            f"{zone}."
        )

        message = (
            f"{self.player.name} explored "
            f"{zone}."
        )

        self.log_action(message)
        self.check_quest("explore")

    def enemy_turn(self):
        if self.enemy.is_alive() and self.player.is_alive():
            message = self.enemy.take_action(
                self.player
            )

            if message:
                self.log_action(message)

            self.player.update_state()

    def run_turn(self, action):
        self.player.reset_defense()

        action_successful = True

        if action == "attack":
            self.player_attack()

        elif action == "defend":
            self.player_defend()

        elif action == "potion":
            action_successful = self.player_use_potion()

        elif action == "explore":
            self.player_explore()

        else:
            print("Unknown action.")
            return

        if (
            action_successful
            and action != "explore"
            and self.enemy.is_alive()
            and self.player.is_alive()
        ):
            self.enemy_turn()

    def show_world(self):
        self.world.show_world()

    def replay_log(self):
        try:
            with open("log.txt", "r", encoding="utf-8") as file:
                logs = file.readlines()

            if not logs:
                print("Log is empty.")
                return

            print("\n===== ACTION REPLAY =====")

            for log in logs:
                print(log.strip())

        except FileNotFoundError:
            print("Log file not found.")