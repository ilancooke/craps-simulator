import random
import json
import sys

class CrapsGame:
    def __init__(self, config_file):
        self.balance = 0
        self.load_config(config_file)

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            self.initial_balance = config['initial_balance']
            self.base_bet = config['base_bet']
            self.max_rounds = config['max_rounds']
            self.strategy = config['strategy']
            self.balance = self.initial_balance
        except FileNotFoundError:
            print(f"Config file {config_file} not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file {config_file}.")
            sys.exit(1)
        except KeyError as e:
            print(f"Missing key in config file: {e}")
            sys.exit(1)

    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def play_round(self):
        bet = self.get_bet()
        if bet > self.balance:
            print("Insufficient funds. Game over.")
            return False

        self.balance -= bet
        come_out_roll = self.roll_dice()
        print(f"Come out roll: {come_out_roll}")

        if come_out_roll in (7, 11):
            print("Natural! You win!")
            self.balance += bet * 2
            return True
        elif come_out_roll in (2, 3, 12):
            print("Craps! You lose.")
            return True

        point = come_out_roll
        print(f"Point is set to {point}")

        while True:
            next_roll = self.roll_dice()
            print(f"You rolled: {next_roll}")
            if next_roll == point:
                print("You hit the point! You win!")
                self.balance += bet * 2
                return True
            elif next_roll == 7:
                print("You rolled a 7. You lose.")
                return True

    def get_bet(self):
        if self.strategy == 'constant':
            return self.base_bet
        elif self.strategy == 'martingale':
            return min(self.base_bet * (2 ** self.losses), self.balance)
        else:
            return self.base_bet  # Default to constant betting

    def play_game(self):
        for round in range(1, self.max_rounds + 1):
            print(f"\nRound {round}")
            print(f"Current balance: ${self.balance}")
            if not self.play_round():
                break
            if self.balance <= 0:
                print("You've run out of money. Game over.")
                break

        print(f"\nGame over. Final balance: ${self.balance}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python craps_game.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    game = CrapsGame(config_file)
    game.play_game()
