import json

from item import HealthPotion


class SaveSystem:
    @staticmethod
    def save_game(game, filename="save.json"):
        data = {
            "player": {
                "name": game.player.name,
                "health": game.player.health,
                "max_health": game.player.max_health,
                "strength": game.player.strength,
                "defense": game.player.defense,
                "state": game.player.state.__class__.__name__,
                "inventory": [
                    {
                        "name": item.name,
                        "heal_amount": getattr(
                            item,
                            "heal_amount",
                            None
                        )
                    }
                    for item in game.player.inventory
                ]
            },
            "enemy": {
                "name": game.enemy.name,
                "health": game.enemy.health,
                "max_health": game.enemy.max_health,
                "strength": game.enemy.strength,
                "defense": game.enemy.defense
            },
            "quest": {
                "quest_type": game.quest.quest_type,
                "target": game.quest.target,
                "completed": game.quest.completed
            }
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4
            )

        print(f"Game saved to {filename}")

    @staticmethod
    def load_game(game, filename="save.json"):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        player_data = data["player"]

        game.player.name = player_data["name"]
        game.player.health = player_data["health"]
        game.player.max_health = player_data["max_health"]
        game.player.strength = player_data["strength"]
        game.player.defense = player_data["defense"]

        game.player.inventory.clear()

        for item_data in player_data["inventory"]:
            if item_data["name"] == "Health Potion":
                potion = HealthPotion(
                    item_data["heal_amount"]
                )

                game.player.inventory.append(potion)

        game.player.update_state()

        enemy_data = data["enemy"]

        game.enemy.name = enemy_data["name"]
        game.enemy.health = enemy_data["health"]
        game.enemy.max_health = enemy_data["max_health"]
        game.enemy.strength = enemy_data["strength"]
        game.enemy.defense = enemy_data["defense"]

        quest_data = data["quest"]

        game.quest.quest_type = quest_data["quest_type"]
        game.quest.target = quest_data["target"]
        game.quest.completed = quest_data["completed"]

        print(f"Game loaded from {filename}")