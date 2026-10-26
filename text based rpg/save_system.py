
import json
import os
import re

from item import HealthPotion, AncientKey
from quest import Quest
from states import HealthyState, PoisonedState, DeadState


class SaveSystem:
    SAVE_DIR = "saves"

    @staticmethod
    def item_to_dict(item):
        data = {"name": item.name}

        if isinstance(item, HealthPotion):
            data["heal_amount"] = item.heal_amount

        return data

    @staticmethod
    def create_item(item_data):
        if not isinstance(item_data, dict):
            return None

        name = item_data.get("name")

        if name == "Health Potion":
            heal_amount = item_data.get("heal_amount", 30)

            if (
                isinstance(heal_amount, bool)
                or not isinstance(heal_amount, (int, float))
                or heal_amount < 0
            ):
                return None

            return HealthPotion(heal_amount)

        if name == "Ancient Key":
            return AncientKey()

        return None

    @staticmethod
    def safe_filename(name):
        name = re.sub(r'[<>:"/\\|?*]', "_", str(name)).strip()
        name = name.rstrip(". ")
        return name or "Player"

    @staticmethod
    def list_saves():
        os.makedirs(SaveSystem.SAVE_DIR, exist_ok=True)
        saves = []

        for filename in os.listdir(SaveSystem.SAVE_DIR):
            if not filename.endswith(".json"):
                continue

            path = os.path.join(SaveSystem.SAVE_DIR, filename)

            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                player = data.get("player")
                if not isinstance(player, dict):
                    continue

                name = player.get("name")
                if not isinstance(name, str) or not name.strip():
                    continue

                saves.append({
                    "name": name,
                    "filename": path,
                })

            except (
                OSError,
                json.JSONDecodeError,
                AttributeError,
                TypeError,
            ):
                continue

        saves.sort(key=lambda save: save["name"].lower())
        return saves

    @staticmethod
    def save_game(game):
        os.makedirs(SaveSystem.SAVE_DIR, exist_ok=True)

        player = game.player
        filename = SaveSystem.safe_filename(player.name) + ".json"
        path = os.path.join(SaveSystem.SAVE_DIR, filename)

        data = {
            "game_over": game.game_over,
            "player": {
                "name": player.name,
                "health": player.health,
                "max_health": player.max_health,
                "strength": player.strength,
                "defense": player.defense,
                "base_defense": player.base_defense,
                "state": type(player.state).__name__,
                "defend_count": player.defend_count,
                "actions_since_defend": player.actions_since_defend,
                "inventory": [
                    SaveSystem.item_to_dict(item)
                    for item in player.inventory
                ],
            },
            "enemy": {
                "name": game.enemy.name,
                "health": game.enemy.health,
                "max_health": game.enemy.max_health,
                "strength": game.enemy.strength,
                "defense": game.enemy.defense,
                "has_retreat": game.enemy.has_retreat,
            },
            "quests": [
                {
                    "quest_type": quest.quest_type,
                    "target": quest.target,
                    "completed": quest.completed,
                }
                for quest in game.quests
            ],
            "quest_index": game.quest_index,
            "world": {
                "name": game.world.name,
                "items": [
                    SaveSystem.item_to_dict(item)
                    for item in game.world.items
                ],
            },
        }

        temp_path = path + ".tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            os.replace(temp_path, path)
            print(f"Game saved for {player.name}.")

        except OSError as error:
            print(f"Could not save game: {error}")

            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass

    @staticmethod
    def load_game(game, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Save data must be a JSON object.")

            player_data = data.get("player")
            enemy_data = data.get("enemy")
            world_data = data.get("world", {})
            quests_data = data.get("quests", [])

            if not isinstance(player_data, dict):
                raise ValueError("Player data is missing.")

            if not isinstance(enemy_data, dict):
                raise ValueError("Enemy data is missing.")

            if not isinstance(world_data, dict):
                raise ValueError("World data is invalid.")

            if not isinstance(quests_data, list) or not quests_data:
                raise ValueError("Quest data is missing.")

            required_player = (
                "name", "health", "max_health", "strength", "defense"
            )
            required_enemy = (
                "name", "health", "max_health", "strength", "defense"
            )

            for key in required_player:
                if key not in player_data:
                    raise ValueError(f"Missing player field: {key}")

            for key in required_enemy:
                if key not in enemy_data:
                    raise ValueError(f"Missing enemy field: {key}")

            def valid_number(value):
                return (
                    isinstance(value, (int, float))
                    and not isinstance(value, bool)
                )

            for key in (
                "health", "max_health", "strength", "defense"
            ):
                if not valid_number(player_data[key]):
                    raise ValueError(f"Invalid player field: {key}")

            for key in (
                "health", "max_health", "strength", "defense"
            ):
                if not valid_number(enemy_data[key]):
                    raise ValueError(f"Invalid enemy field: {key}")

            for quest_data in quests_data:
                if (
                    not isinstance(quest_data, dict)
                    or "quest_type" not in quest_data
                    or "target" not in quest_data
                ):
                    raise ValueError("Invalid quest data.")

            inventory_data = player_data.get("inventory", [])
            world_items_data = world_data.get("items", [])

            if not isinstance(inventory_data, list):
                raise ValueError("Player inventory is invalid.")

            if not isinstance(world_items_data, list):
                raise ValueError("World items are invalid.")

            quest_index = data.get("quest_index", 0)

            if (
                isinstance(quest_index, bool)
                or not isinstance(quest_index, int)
            ):
                raise ValueError("Quest index is invalid.")

        except FileNotFoundError:
            print("Save file not found.")
            return False

        except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
            print(f"Could not load save: {error}")
            return False

        player = game.player

        player.name = player_data["name"]
        player.health = player_data["health"]
        player.max_health = player_data["max_health"]
        player.strength = player_data["strength"]
        player.base_defense = player_data.get(
            "base_defense", player_data["defense"]
        )
        player.defense = player_data["defense"]
        player.defend_count = player_data.get("defend_count", 0)
        player.actions_since_defend = player_data.get(
            "actions_since_defend", 0
        )

        state_classes = {
            "HealthyState": HealthyState,
            "PoisonedState": PoisonedState,
            "DeadState": DeadState,
        }

        state_name = player_data.get("state", "HealthyState")
        state_class = state_classes.get(state_name)

        if state_class is None:
            state_class = HealthyState

        player.state = state_class()

        player.inventory.clear()

        for item_data in inventory_data:
            item = SaveSystem.create_item(item_data)

            if item is not None:
                player.inventory.append(item)

        enemy = game.enemy

        enemy.name = enemy_data["name"]
        enemy.health = enemy_data["health"]
        enemy.max_health = enemy_data["max_health"]
        enemy.strength = enemy_data["strength"]
        enemy.defense = enemy_data["defense"]
        enemy.has_retreat = enemy_data.get("has_retreat", False)

        game.quests.clear()

        for quest_data in quests_data:
            quest = Quest(
                quest_data["quest_type"],
                quest_data["target"],
            )
            quest.completed = quest_data.get("completed", False)
            game.quests.append(quest)

        game.world.quests = game.quests
        game.quest_index = max(
            0,
            min(quest_index, len(game.quests) - 1),
        )
        game.quest = game.quests[game.quest_index]

        game.world.name = world_data.get("name", game.world.name)
        game.world.items.clear()

        for item_data in world_items_data:
            item = SaveSystem.create_item(item_data)

            if item is not None:
                game.world.items.append(item)

        game.game_over = data.get("game_over", False)

        # Restore state consistently with current HP.
        player.update_state()

        print(f"Game loaded for {player.name}.")
        return True

    @staticmethod
    def delete_save(filename):
        try:
            os.remove(filename)
            print("Completed save deleted.")
        except FileNotFoundError:
            pass
        except OSError as error:
            print(f"Could not delete save: {error}")
