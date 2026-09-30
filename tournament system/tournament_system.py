import random
import csv
import json


class Person:
    def __init__(self, name):
        self.name = name


class GoodForm:
    def on_win(self):
        return GoodForm()

    def on_draw(self):
        return GoodForm()

    def on_loss(self):
        return NormalForm()


class NormalForm:
    def on_win(self):
        return GoodForm()

    def on_draw(self):
        return NormalForm()

    def on_loss(self):
        return BadForm()


class BadForm:
    def on_win(self):
        return NormalForm()

    def on_draw(self):
        return BadForm()

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
        self.form = GoodForm()
        
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

    def play(self):
        if self.played:
            raise ValueError("Match has already been played.")
        
        self.score1 = random.randint(0, 5)
        self.score2 = random.randint(0, 5)

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
        self.played = False


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
        winners = []

        for match in self.matches:
            referee.officiate(match)
            self.all_matches.append(match)

            if match.score1 == match.score2:
                self.strategy.resolve_draw(match)

            winners.append(match.winner)

        if hasattr(self.strategy, "bye_player"):
            if self.strategy.bye_player is not None:
                winners.append(self.strategy.bye_player)

        while len(winners) > 1:

            self.matches = self.strategy.create_next_round(winners)

            winners = []

            for match in self.matches:
                referee.officiate(match)
                self.all_matches.append(match)

                if match.score1 == match.score2:
                    self.strategy.resolve_draw(match)

                winners.append(match.winner)

            if self.strategy.bye_player is not None:
                winners.append(self.strategy.bye_player)
        self.played = True
        return winners[0]

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
        top_scorer = max(
            self.players,
            key=lambda player: player.goals_scored
        )

        best_player = max(
            self.players,
            key=lambda player: player.points
        )

        most_clean_sheets = max(
            self.players,
            key=lambda player: player.clean_sheets
        )

        return {
            "Top Scorer": top_scorer,
            "Best Player": best_player,
            "Most Clean Sheets": most_clean_sheets
        }

    def save_matches_to_csv(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Player 1",
                    "Player 2", 
                    "Score 1",
                    "Score 2", 
                    "Winner"
                ]
            )

            writer.writeheader()

            for match in self.all_matches:
                writer.writerow(match.get_result())

    def save_standings_to_json(self, filename):
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

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        

        
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

        for i in range(0, len(winners) - 1, 2):
            match = Match(winners[i], winners[i + 1])
            matches.append(match)

        if len(winners) % 2 != 0:
            self.bye_player = winners[-1]
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
            print("Error: Maximum 16 players allowed.")
            return

        name = name.strip()

        if not name:
            print("Player name cannot be empty.")
            return

        if not name.isalpha():
            print("Player name must contain letters only.")
            return

        name = name.capitalize()

        for player in self.tournament.players:
            if player.name.lower() == name.lower():
                print("Error: Player already exists.")
                return

        
        player = Player(name)

        try:
            self.tournament.add_player(player)
            print(f"{name} tournamentga qo'shildi.")
        except ValueError as error:
            print("Error:", error)

        
        

    def choose_strategy(self):
        if self.tournament.matches:
            print("Error: Tournament has already been started.")
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
        if self.tournament.strategy is None:
            print("Error: Choose tournament type first.")
            return
        
        try:
            self.tournament.start()
            print("Tournament started.")
            print("Matches scheduled:", len(self.tournament.matches))
        except ValueError as error:
            print("Error:", error)
        

    def play_tournament(self):
        if not self.tournament.matches:
            print("Error: Tournament has not been started.")
            return 

        try:
            if isinstance(self.tournament.strategy, KnockoutStrategy):
                champion = self.tournament.play_knockout(self.referee)
                print("Champion:", champion.name)
            else:
                self.tournament.play_matches(self.referee)
                print("Tournament matches played")

        except ValueError as error:
            print("Error:", error)

    def stop_tournament(self):
        if not self.tournament.players:
            print("Error: No tournament to stop.")
            return
        
        self.running = False
        print("Tournament stopped")

    def show_standings(self):
        standings = self.tournament.get_standings()

        if not standings:
            print("Error: No players in tournament.")
            return

        print("\n===== STANDINGS =====")

        for player in standings:
            form_name = type(player.form).__name__.replace("Form", "")

            print(
                player.name,
                "| Points:", player.points,
                "| Matches", player.matches_played,
                "| Wins:", player.wins,
                "| Draws:", player.draws,
                "| Losses:", player.losses,
                "| Goals:", player.goals_scored,
                "| Clean Sheets:", player.clean_sheets,
                "| GD:", player.goal_difference,
                "| Form:", form_name
            )

    def show_awards(self):
        try:
            awards = self.tournament.generate_awards()

            print("\n===== AWARDS =====")

            print("Top Scorer:", awards["Top Scorer"].name)
            print("Best Player:", awards["Best Player"].name)
            print("Most Clean Sheets:", awards["Most Clean Sheets"].name)
        except ValueError as error:
            print("Error:", error)


    def run(self):
        while self.running:
            print(f"Players:{len(self.tournament.players)}/16")
            print("1. Add player")
            print("2. Choose tournament type")
            print("3. Start tournament")
            print("4. Play tournament")
            print("5. Show standings")
            print("6. Show awards")
            print("7. Save matches to CSV")
            print("8. Save standings to JSON")
            print("9. Stop tournament")
            print("10. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                name = input("Enter player name: ")
                self.add_player(name)

            elif choice == "2":
                self.choose_strategy()

            elif choice == "3":
                self.start_tournament()

            elif choice == "4":
                self.play_tournament()

            elif choice == "5":
                self.show_standings()

            elif choice == "6":
                self.show_awards()

            elif choice == "7":
                if not self.tournament.all_matches:
                    print("Error: No matches have been played.")
                else:
                    self.tournament.save_matches_to_csv("matches.csv")
                    print("Matches saved to matches.csv")

            elif choice == "8":
                if not self.tournament.players:
                    print("Error: No players in tournament.")
                else:
                    self.tournament.save_standings_to_json("standings.json")
                    print("Standings saved to standings.json")

            elif choice == "9":
                self.stop_tournament()

            elif choice == "10":
                self.running = False
                print("Goodbye.")

            else:
                print("Invalid option.")

if __name__ == "__main__":
    tournament = Tournament("My Tournament", None)
    referee = Referee("Referee")
    admin = Admin(tournament, referee)
    admin.run()

