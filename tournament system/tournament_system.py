import random
import csv
import json
import os

class Person:
    def __init__(self, name):
        self.name = name


class GoodForm:
    def on_win(self):
        return GoodForm()

    def on_draw(self):
        return NormalForm()

    def on_loss(self):
        return BadForm()


class NormalForm:
    def on_win(self):
        return GoodForm()

    def on_draw(self):
        return NormalForm()

    def on_loss(self):
        return BadForm()


class BadForm:
    def on_win(self):
        return GoodForm()

    def on_draw(self):
        return NormalForm()

    def on_loss(self):
        return BadForm()


class Player(Person):
    def __init__(self, name):
        Person.__init__(self, name)
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.goal_difference = 0
        self.matches_played = 0
        self.clean_sheets = 0
        self.form = NormalForm()
        
    def add_win(self):
        self.wins += 1
        self.points += 3
        self.matches_played += 1
        self.form = self.form.on_win()

    def add_draw(self):
        self.draws += 1
        self.points += 1
        self.matches_played += 1
        self.form = self.form.on_draw()

    def add_loss(self):
        self.losses += 1
        self.matches_played += 1
        self.form = self.form.on_loss()

class Referee(Person):
    def __init__(self, name):
        Person.__init__(self, name)
        self.games_officiated = 0

    def officiate(self, match):
        match.play()
        self.games_officiated += 1

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0
        self.score2 = 0
        self.winner = None
        self.played = False

    def calculate_goals(self, player, opponent):
        goals = 0

        for _ in range(5):
            probability = 0.30

            if isinstance(player.form, GoodForm):
                probability += 0.05
            elif isinstance(player.form, BadForm):
                probability -= 0.05

            if isinstance(opponent.form, GoodForm):
                probability -= 0.05
            elif isinstance(opponent.form, BadForm):
                probability += 0.05

            probability = max(0.05, min(0.95, probability))

            if random.random() < probability:
                goals += 1

        return goals

    def play(self):
        if self.played:
            raise ValueError("Match has already been played.")
        
        self.score1 = self.calculate_goals(
            self.player1, self.player2
        )
        self.score2 = self.calculate_goals(
            self.player2, self.player1
        )

        self.player1.goals_scored += self.score1
        self.player1.goals_conceded += self.score2

        self.player2.goals_scored += self.score2
        self.player2.goals_conceded += self.score1

        self.player1.goal_difference = (
            self.player1.goals_scored - self.player1.goals_conceded
        )

        self.player2.goal_difference = (
            self.player2.goals_scored - self.player2.goals_conceded
        )

        if self.score1 > self.score2:
            self.winner = self.player1
            self.player1.add_win()
            self.player2.add_loss()

        elif self.score2 > self.score1:
            self.winner = self.player2
            self.player2.add_win()
            self.player1.add_loss()

        else:
            self.winner = None
            self.player1.add_draw()
            self.player2.add_draw()

        if self.score1 == 0:
            self.player2.clean_sheets += 1

        if self.score2 == 0:
            self.player1.clean_sheets += 1

        self.played = True

    def get_result(self):
        return {
            "Player 1": self.player1.name,
            "Player 2": self.player2.name,
            "Score 1": self.score1,
            "Score 2": self.score2,
            "Winner": self.winner.name if self.winner else "Draw"
        }

class Tournament:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.players = []
        self.matches = []
        self.all_matches = []
        self.rounds = []
        self.played = False
        self.champion = None
        self.data_saved = False

    def add_player(self, player):

        if self.matches:
            raise ValueError("Cannot add players after tournament has started.")
        
        self.players.append(player)

    def start(self):
        if len(self.players) < 2:
            raise ValueError("Tournament requires at least 2 players.")

        if self.strategy is None:
            raise ValueError("Choose tournament type first.")

        if self.matches:
            raise ValueError("Tournament has already been started.")
        
        self.matches = self.strategy.create_matches(self.players)

    def play_matches(self, referee):
        if self.played:
            raise ValueError("Tournament has already been played.")

        if not self.matches:
            raise ValueError("Tournament has not been started.")
        
        self.all_matches = []

        for match in self.matches:
            referee.officiate(match)
            self.all_matches.append(match)

        self.played = True


    def play_knockout(self, referee):
        if self.played:
            raise ValueError("Tournament has already been played.")

        if not self.matches:
            raise ValueError("Tournament has not been started.")

        if not self.players:
            raise ValueError("Tournament has no players.")

        self.all_matches = []
        self.rounds = []
        winners = []

        # Birinchi raund
        current_round = self.matches.copy()
        self.rounds.append(current_round.copy())

        print("DEBUG: First round matches:", len(current_round))
        print("DEBUG: Registered players:", len(self.players))

        for match in current_round:
            referee.officiate(match)
            self.all_matches.append(match)

            if match.score1 == match.score2:
                self.strategy.resolve_draw(match)

            winners.append(match.winner)

        if hasattr(self.strategy, "bye_player"):
            if self.strategy.bye_player is not None:
                winners.append(self.strategy.bye_player)

        # Keyingi raundlar
        while len(winners) > 1:
            self.matches = self.strategy.create_next_round(winners)
            current_round = self.matches.copy()

            print("DEBUG: Next round matches:", len(current_round))
            print("DEBUG: Winners entering next round:", len(winners))

            self.rounds.append(current_round.copy())
            winners = []

            for match in current_round:
                referee.officiate(match)
                self.all_matches.append(match)

                if match.score1 == match.score2:
                    self.strategy.resolve_draw(match)

                winners.append(match.winner)

            if self.strategy.bye_player is not None:
                winners.append(self.strategy.bye_player)

        self.champion = winners[0]
        self.played = True
        return self.champion


    def get_standings(self):
        return sorted(
            self.players,
            key=lambda player: (
                player.points,
                player.goal_difference,
                player.goals_scored
            ),
            reverse=True
        )

    def generate_awards(self):
        if not self.players:
            raise ValueError("No players in tournament.")

        top_goals = max(player.goals_scored for player in self.players)
        top_scorers = [
            player for player in self.players
            if player.goals_scored == top_goals
        ]

        most_clean_sheets_count = max(
            player.clean_sheets for player in self.players
        )
        clean_sheet_winners = [
            player for player in self.players
            if player.clean_sheets == most_clean_sheets_count
        ]

        standings = sorted(
            self.players,
            key=lambda player: (
                player.points,
                player.goal_difference,
                player.goals_scored
            ),
            reverse=True
        )

        return {
            "Champion": self.champion,
            "Top Scorer": top_scorers,
            "Best Player": standings[0],
            "Most Clean Sheets": clean_sheet_winners
        }

    def save_matches_to_csv(self, filename):
        file_is_empty = (
            not os.path.exists(filename)
            or os.path.getsize(filename) == 0
        )

        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Tournament",
                    "Player 1",
                    "Player 2",
                    "Score 1",
                    "Score 2",
                    "Winner"
                ]
            )

            if file_is_empty:
                writer.writeheader()

            for match in self.all_matches:
                result = match.get_result()
                result["Tournament"] = self.name

                writer.writerow(result)

    
    def save_knockout_standings_to_json(self, filename):
        standings = self.get_standings()
        data = []

        for position, player in enumerate(standings, start=1):
            data.append({
                "position": position,
                "name": player.name,
                "matches_played": player.matches_played,
                "wins": player.wins,
                "losses": player.losses,
                "goals_scored": player.goals_scored,
                "goals_conceded": player.goals_conceded,
                "goal_difference": player.goal_difference,
                "clean_sheet": player.clean_sheets
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


    def save_round_robin_standings_to_json(self, filename):
        standings = self.get_standings()
        data = []

        for player in standings:
            data.append({
                "name": player.name,
                "points": player.points,
                "matches_played": player.matches_played,
                "wins": player.wins,
                "draws": player.draws,
                "losses": player.losses,
                "goals_scored": player.goals_scored,
                "goals_conceded": player.goals_conceded,
                "clean_sheets": player.clean_sheets,
                "goal_difference": player.goal_difference
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

class RoundRobinStrategy:
    def create_matches(self, players):
        matches = []

        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                match = Match(players[i], players[j])
                matches.append(match)

        return matches


class KnockoutStrategy:
    def create_matches(self, players):
        matches = []

        for i in range(0, len(players) - 1, 2):
            match = Match(players[i], players[i + 1])
            matches.append(match)

        if len(players) % 2 != 0:
            self.bye_player = players[-1]
        else:
            self.bye_player = None

        return matches

    def resolve_draw(self, match):
        if match.score1 != match.score2:
            return

        was_zero_zero = (
            match.score1 == 0
            and match.score2 == 0
        )

        goal = random.randint(1, 2)

        if goal == 1:
            match.score1 += 1
            winner = match.player1
            loser = match.player2
        else:
            match.score2 += 1
            winner = match.player2
            loser = match.player1

        winner.goals_scored += 1
        loser.goals_conceded += 1

        if was_zero_zero:
            loser.clean_sheets -= 1

        winner.goal_difference = (
            winner.goals_scored - winner.goals_conceded
        )

        loser.goal_difference = (
            loser.goals_scored - loser.goals_conceded
        )

        match.winner = winner

        winner.draws -= 1
        loser.draws -= 1

        winner.points += 2
        loser.points -= 1

        winner.wins += 1
        loser.losses += 1

        winner.form = winner.form.on_win()
        loser.form = loser.form.on_loss()
            
    def create_next_round(self, winners):
        matches = []
        round_players = list(winners)

        previous_bye = self.bye_player

        if (
            len(round_players) % 2 != 0
            and previous_bye is not None
            and round_players[-1] is previous_bye
        ):
            round_players = (
                [previous_bye] + round_players[:-1]
            )

        for i in range(0, len(round_players) - 1, 2):
            match = Match(
                round_players[i],
                round_players[i + 1]
            )
            matches.append(match)

        if len(round_players) % 2 != 0:
            self.bye_player = round_players[-1]
        else:
            self.bye_player = None

        return matches

class Admin:
    def __init__(self, tournament, referee):
        self.tournament = tournament
        self.referee = referee
        self.running = True

    def add_player(self, name):
        if len(self.tournament.players) >= 16:
            print("Maximum 16 players allowed.")
            return

        name = name.strip()

        if not name:
            print("Player name cannot be empty.")
            return


        if not all(char.isalnum() or char in " -'‘’" for char in name):
            print(
                "Player name can contain letters, numbers, spaces, "
                "hyphens, and apostrophes only."
            )
            return

        for player in self.tournament.players:
            if player.name.lower() == name.lower():
                print("Player already exists.")
                return

        player = Player(name)

        try:
            self.tournament.add_player(player)
            print(f"{name} has been added to the tournament.")
        except ValueError as error:
            print("Error:", error)

    def choose_strategy(self):
        if self.tournament.matches:
            print("Tournament has already been started.")
            return
        
        print("\n===== Tournament TYPE =====")
        print("1. Round Robin")
        print("2. Knockout")

        choice = input("Choose tournament type: ")
        if choice == "1":
            self.tournament.strategy = RoundRobinStrategy()
            print("Tournament type: Round Robin")

        elif choice == "2":
            self.tournament.strategy = KnockoutStrategy()
            print("Tournament type: Knockout")

        else:
            print("Invalid tournament type.")

    def start_tournament(self):
        if self.tournament.matches:
            print("Tournament has already been started.")
            return

        if len(self.tournament.players) < 2:
            print("At least 2 players are required.")
            return

        print("\nChoose tournament type:")
        print("1. Round Robin")
        print("2. Knockout")

        choice = input("Choose tournament type: ").strip()

        if choice == "1":
            self.tournament.strategy = RoundRobinStrategy()

        elif choice == "2":
            self.tournament.strategy = KnockoutStrategy()

        else:
            print("Invalid tournament type.")
            return

        tournament_name = input("Enter tournament name: ").strip()

        while not tournament_name:
            print("Tournament name cannot be empty.")
            tournament_name = input("Enter tournament name: ").strip()

        self.tournament.name = tournament_name

        try:
            self.tournament.start()
            print(f"Tournament '{self.tournament.name}' started.")

        except ValueError as error:
            print(error)


    def play_tournament(self):
        if not self.tournament.matches:
            print("Tournament has not been started.")
            return

        try:
            if isinstance(self.tournament.strategy, KnockoutStrategy):
                champion = self.tournament.play_knockout(self.referee)
                print("Champion:", champion.name)
            else:
                self.tournament.play_matches(self.referee)
                print("Tournament matches played")

            self.save_tournament_data()

        except ValueError as error:
            print("Error:", error)


    
    def save_tournament_data(self):
        if not self.tournament.played:
            return False

        if self.tournament.data_saved:
            return True

        try:
            if isinstance(self.tournament.strategy, RoundRobinStrategy):
                self.tournament.save_matches_to_csv(
                    "round_robin_matches.csv"
                )
                self.tournament.save_round_robin_standings_to_json(
                    "standings.json"
                )

            elif isinstance(self.tournament.strategy, KnockoutStrategy):
                self.tournament.save_matches_to_csv(
                    "knockout_matches.csv"
                )
                self.tournament.save_knockout_standings_to_json(
                    "knockout_standings.json"
                )

            self.tournament.data_saved = True
            print("All tournament data saved successfully.")
            return True

        except (OSError, ValueError) as error:
            print("Could not save tournament data:", error)
            return False


    def stop_tournament(self, create_new=True):
        if not self.tournament.players:
            print("No tournament to stop.")
            return

        if not self.tournament.played:
            print("Tournament has not been played.")
            return

        if not self.save_tournament_data():
            print("Tournament was not stopped because saving failed.")
            return

        print("Tournament stopped.")
        print("All data saved successfully.")

        if create_new:
            self.tournament = Tournament("", None)



    def show_standings(self):
        strategy_name = type(self.tournament.strategy).__name__

        # Knockout turniri
        if strategy_name == "KnockoutStrategy":
            rounds = getattr(self.tournament, "rounds", [])

            if not rounds:
                print("\nNo knockout results available yet.")
                return

            print("\n" + "=" * 60)
            print("                 KNOCKOUT RESULTS")
            print("=" * 60)

            for round_index, matches in enumerate(rounds):

                print(f"\n--- Round {round_index + 1} ---")
                
                if not matches:
                    print("No matches.")
                    continue

                for match in matches:
                    player1 = match.player1
                    player2 = match.player2

                    print(
                        f"{player1.name} "
                        f"{match.score1} - {match.score2} "
                        f"{player2.name}"
                    )

                    if match.winner:
                        print(f"  Winner: {match.winner.name}")

            if self.tournament.played:
                champion = self.tournament.players

                # Final raunddagi o'yin g'olibi chempion bo'ladi.
                if rounds and rounds[-1]:
                    final_match = rounds[-1][-1]
                    if final_match.winner:
                        print("\n" + "=" * 60)
                        print(f"CHAMPION: {final_match.winner.name}")
                        print("=" * 60)

            return

        # Round Robin turniri: eski standings jadvali
        standings = self.tournament.get_standings()

        if not standings:
            print("\nNo standings available yet.")
            return

        print("\n" + "=" * 112)
        print(
            f"{'':>3} {'PLAYER':<16} {'PTS':>4} {'MP':>4} "
            f"{'W':>4} {'D':>4} {'L':>4} {'GF':>4} "
            f"{'CS':>4} {'GD':>5} {'FORM':<10}"
        )
        print("=" * 112)

        for position, player in enumerate(standings, start=1):
            print(
                f"{position:>3} "
                f"{player.name:<16} "
                f"{player.points:>4} "
                f"{player.matches_played:>4} "
                f"{player.wins:>4} "
                f"{player.draws:>4} "
                f"{player.losses:>4} "
                f"{player.goals_scored:>4} "
                f"{player.clean_sheets:>4} "
                f"{player.goal_difference:>5} "
                f"{type(player.form).__name__.replace('Form', ''):<10}"
            )

        print("=" * 112)
        print("PTS: Points | MP: Matches Played | W: Wins | D: Draws | L: Losses")
        print("GF: Goals For | CS: Clean Sheets | GD: Goal Difference")

    def show_awards(self):
        if not self.tournament.played:
            print("Awards are not available yet. Play the tournament first.")
            return

        try:
            awards = self.tournament.generate_awards()

            print("\n===== AWARDS =====")
            champion = awards["Champion"]

            if champion is not None:
                print(f"Champion: {champion.name}")

            print("Top Scorer:")
            for player in awards["Top Scorer"]:
                print(f"  - {player.name} ({player.goals_scored} goals)")

            best_player = awards["Best Player"]
            print(f"Best Player: {best_player.name} ({best_player.points} points)")

            print("Most Clean Sheets:")
            for player in awards["Most Clean Sheets"]:
                print(f"  - {player.name} ({player.clean_sheets} matches)")

        except ValueError as error:
            print("Error:", error)

    def run(self):
        while self.running:
            print("\n")
            print("=" * 44)
            print("          TOURNAMENT MANAGER")
            print("=" * 44)
            print(f"  Players registered: {len(self.tournament.players)}/16")
            print("-" * 44)
            print("  1. Add player")
            print("  2. Start tournament")
            print("  3. Play tournament")
            print("  4. Show standings")
            print("  5. Show awards")
            print("  6. Stop tournament")
            print("  7. Exit")
            print("=" * 44)

            choice = input("  Choose an option (1-7): ").strip()

            if choice == "1":
                while len(self.tournament.players) < 16:
                    print(
                        f"\n  Players registered: "
                        f"{len(self.tournament.players)}/16"
                    )

                    name = input(
                        "  Enter player name ('0' to return): "
                    ).strip()

                    if name == "0":
                        break

                    old_count = len(self.tournament.players)
                    self.add_player(name)

                    if len(self.tournament.players) > old_count:
                        print(
                            f"  Progress: "
                            f"{len(self.tournament.players)}/16 players"
                        )

                if len(self.tournament.players) == 16:
                    print("\n  Maximum number of players reached.")

            elif choice == "2":
                self.start_tournament()

            elif choice == "3":
                self.play_tournament()

            elif choice == "4":
                self.show_standings()

            elif choice == "5":
                self.show_awards()

            elif choice == "6":
                self.stop_tournament()

            elif choice == "7":
                if self.tournament.played:
                    self.stop_tournament(create_new=False)

                self.running = False
                print("\n Tournament Manager closed. Goodbye!")

            else:
                print(
                    "\n  Invalid option. Please enter a number from 1 to 7."
                )

if __name__ == "__main__":
    tournament = Tournament("My Tournament", None)
    referee = Referee("Referee")
    admin = Admin(tournament, referee)
    admin.run()
