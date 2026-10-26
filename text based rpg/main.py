
from game import Game
from save_system import SaveSystem
import os

def show_main_menu():
    print("\n===== TEXT RPG =====")
    print("1. New Game")
    print("2. Load Game")
    print("0. Exit")

def show_game_menu():
    print("\n===== TEXT RPG =====")
    print("1. Start Battle")
    print("2. Explore")
    print("3. Show Status")
    print("4. Show World")
    print("5. Save Game")
    print("0. Main Menu")

def show_battle_menu():
    print("\n===== BATTLE =====")
    print("1. Attack")
    print("2. Defend")
    print("3. Use Potion")
    print("0. Back")

def play_battle(game):
    if not game.enemy.is_alive():
        print("Goblin has been defeated.")
        return

    if game.enemy.has_retreat:
        print("Goblin has returned for another battle!")

        game.enemy.has_retreat = False
        game.enemy.health += 20
        game.enemy.max_health += 20
        game.enemy.strength += 5

        print(f"Goblin's HP increased to {game.enemy.health}!")
        print(f"Goblin's strength increased to {game.enemy.strength}!")

    while game.player.is_alive() and game.enemy.is_alive():
        if game.enemy.has_retreat or game.game_over:
            break

        print("\n===== BATTLE =====")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Potion")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            game.run_turn("attack")
        elif choice == "2":
            game.run_turn("defend")
        elif choice == "3":
            game.run_turn("potion")
        elif choice == "0":
            break
        else:
            print("Invalid option!")

    if game.enemy.has_retreat:
        print("Goblin escaped. You can start another battle later.")


def play_game(game):
    while not game.game_over:
        show_game_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if game.enemy.is_alive():
                play_battle(game)
            else:
                print("The enemy has been defeated.")

        elif choice == "2":
            game.player_explore()

        elif choice == "3":
            game.show_status()

        elif choice == "4":
            game.show_world()

        elif choice == "5":
            SaveSystem.save_game(game)

        elif choice == "0":
            return

        else:
            print("Invalid option!")

    print("\n===== GAME FINISHED =====")

    if game.game_over:
        SaveSystem.delete_save(
            os.path.join(
                SaveSystem.SAVE_DIR,
                SaveSystem.safe_filename(game.player.name) + ".json"
            )
        )

def new_game():
    name = input("Enter your character name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    game = Game()
    game.player.name = name
    play_game(game)

def load_game():
    saves = SaveSystem.list_saves()

    if not saves:
        print("There is no data to load.")
        return

    print("\n===== SAVED GAMES =====")
    for index, save in enumerate(saves, start=1):
        print(f"{index}. {save['name']}")
    print("0. Back")

    choice = input("Choose a save: ").strip()

    if choice == "0":
        return

    if not choice.isdigit():
        print("Invalid option.")
        return

    index = int(choice)

    if index < 1 or index > len(saves):
        print("Invalid option.")
        return

    game = Game()

    try:
        loaded = SaveSystem.load_game(game, saves[index - 1]["filename"])
        if loaded:
            game.check_end_game()
            if not game.game_over:
                play_game(game)
    except (ValueError, KeyError, TypeError) as error:
        print(f"Could not load save: {error}")


def main():
    while True:
        show_main_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_game()
        elif choice == "2":
            load_game()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()
