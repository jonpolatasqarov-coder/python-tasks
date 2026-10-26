
class World:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.enemies = []
        self.items = []
        self.quests = []

    def add_player(self, player):
        self.players.append(player)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_item(self, item):
        self.items.append(item)

    def add_quest(self, quest):
        self.quests.append(quest)

    def find_item(self, player):
        if not self.items:
            print("There are no items left to find.")
            return None

        item = self.items[0]
        self.items.remove(item)
        player.add_item(item)

        print(f"You found: {item.name}!")

        return item

    def show_world(self):
        print(f"\n=== {self.name} ===")

        print("\nPlayers:")
        for player in self.players:
            print(f"- {player.name}")

        print("\nEnemies:")
        for enemy in self.enemies:
            print(f"- {enemy.name}")

        print("\nItems:")
        if self.items:
            for item in self.items:
                print(f"- {item.name}")
        else:
            print("- No items remaining")

        print("\nQuests:")
        for quest in self.quests:
            print(f"- {quest}")
