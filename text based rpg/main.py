from game import Game
from save_system import SaveSystem


def show_menu():
    print("\n===== TEXT RPG =====")
    print("1. Show status")
    print("2. Attack")
    print("3. Defend")
    print("4. Use potion")
    print("5. Explore")
    print("6. Show world")
    print("7. Save game")
    print("8. Load game")
    print("9. Replay Log")
    print("0. Exit")


game = Game()


while True:
    show_menu()

    choice = input("Choose an option: ").strip()

    if choice == "1":
        game.show_status()

    elif choice == "2":
        game.run_turn("attack")

    elif choice == "3":
        game.run_turn("defend")

    elif choice == "4":
        game.run_turn("potion")

    elif choice == "5":
        game.run_turn("explore")

    elif choice == "6":
        game.show_world()

    elif choice == "7":
        SaveSystem.save_game(game)

    elif choice == "8":
        try:
            SaveSystem.load_game(game)
        except FileNotFoundError:
            print("Save file not found.")

    elif choice == "9":
        game.replay_log()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option!")