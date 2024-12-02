# Craps Dice Game Simulator

This Python program simulates the popular casino dice game of Craps. It allows users to experiment with different betting strategies and initial conditions without risking real money.

## Features

- Simulates a realistic Craps dice game
- Configurable initial balance, base bet, and maximum number of rounds
- Supports multiple betting strategies (currently 'constant' and 'martingale')
- Loads game parameters from a JSON configuration file
- Provides detailed output for each round and final results

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository or download the `craps_game.py` file.
2. Ensure you have Python 3.6 or higher installed on your system.

## Usage

1. Create a JSON configuration file (e.g., `craps_config.json`) with the following structure:

```json
{
    "initial_balance": 1000,
    "base_bet": 10,
    "max_rounds": 100,
    "strategy": "constant"
}
```

2. Run the program from the command line, providing the path to your configuration file:

```
python craps_game.py craps_config.json
```

## Configuration Options

- initial_balance: The starting balance for the player (in dollars)
- base_bet: The base betting amount (in dollars)
- max_rounds: The maximum number of rounds to play
- strategy: The betting strategy to use (currently supports "constant" or "martingale")

## Betting Strategies

1. Constant: Always bet the base bet amount.
2. Martingale: Double the bet after each loss, reset to base bet after a win.

## Sample Output

```
Round 1
Current balance: $1000
Come out roll: 8
Point is set to 8
You rolled: 7
You rolled a 7. You lose.

Round 2
Current balance: $990
Come out roll: 7
Natural! You win!

...

Game over. Final balance: $1050
```

## Extending the Program

To add new betting strategies:

1. Implement the new strategy in the get_bet method of the CrapsGame class.
2. Update the configuration file to include the new strategy name.
