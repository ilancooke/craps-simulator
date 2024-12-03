import random
import json
import sys

class CrapsGame:
    def __init__(self, config_file):
        self.balance = 0
        self.dice_counts = {i: 0 for i in range(2, 13)}
        self.load_config(config_file)

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            self.initial_balance = config['initial_balance']
            self.base_bet = config['base_bet']
            self.max_rounds = config['max_rounds']
            self.strategy = config['strategy']
            self.bet_type = config.get('bet_type', 'pass_line')  # Default to pass line if not specified
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
        roll = random.randint(1, 6) + random.randint(1, 6)
        self.dice_counts[roll] += 1
        return roll

    def play_round(self):
        self.losses = 0
        bet = self.get_bet()
        if bet > self.balance:
            print("Insufficient funds. Game over.")
            return False

        self.balance -= bet
        come_out_roll = self.roll_dice()
        print(f"Come out roll: {come_out_roll}")

        if self.bet_type == 'pass_line':
            return self.play_pass_line(bet, come_out_roll)
        elif self.bet_type == 'dont_pass_bar':
            return self.play_dont_pass_bar(bet, come_out_roll)

    def play_pass_line(self, bet, come_out_roll):
        if come_out_roll in (7, 11):
            print("Natural! You win!")
            self.balance += bet * 2
            self.losses = 0
            return True
        elif come_out_roll in (2, 3, 12):
            print("Craps! You lose.")
            self.losses += 1
            return True

        return self.play_point_phase(bet, come_out_roll, win_on_point=True)

    def play_dont_pass_bar(self, bet, come_out_roll):
        if come_out_roll in (2, 3):
            print("Craps! You win!")
            self.balance += bet * 2
            self.losses = 0
            return True
        elif come_out_roll in (7, 11):
            print("Natural! You lose.")
            self.losses += 1
            return True
        elif come_out_roll == 12:
            print("Push on 12. Your bet is returned.")
            self.balance += bet
            return True

        return self.play_point_phase(bet, come_out_roll, win_on_point=False)

    def play_point_phase(self, bet, point, win_on_point):
        print(f"Point is set to {point}")
        while True:
            next_roll = self.roll_dice()
            print(f"You rolled: {next_roll}")
            if next_roll == point:
                if win_on_point:
                    print("You hit the point! You win!")
                    self.balance += bet * 2
                    self.losses = 0
                else:
                    print("Point is hit. You lose.")
                    self.losses += 1
                return True
            elif next_roll == 7:
                if win_on_point:
                    print("You rolled a 7. You lose.")
                    self.losses += 1
                else:
                    print("You rolled a 7. You win!")
                    self.balance += bet * 2
                    self.losses = 0
                return True

    def get_bet(self):
        if self.strategy == 'constant':
            return self.base_bet
        elif self.strategy == 'martingale':
            return min(self.base_bet * (2 ** self.losses), self.balance)
        else:
            return self.base_bet

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
        self.print_dice_statistics()

    def print_dice_statistics(self):
        total_rolls = sum(self.dice_counts.values())
        print("\nDice Roll Statistics:")
        print("Roll | Count | Frequency")
        print("--------------------------")
        for roll, count in sorted(self.dice_counts.items()):
            frequency = (count / total_rolls) * 100 if total_rolls > 0 else 0
            print(f"{roll:4d} | {count:5d} | {frequency:6.2f}%")
        print(f"\nTotal rolls: {total_rolls}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python craps_game.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    game = CrapsGame(config_file)
    game.play_game()
