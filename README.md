# Go Fish Simulator

A command-line simulator for the card game "Go Fish" with support for different player strategies and customizable game rules.

## Features

- Modular design with separate components for cards, players, and game logic
- Multiple AI player strategies:
  - Random: Makes completely random choices
  - Smart: Prioritizes ranks it already has multiple cards of
  - Memory: Remembers which cards other players have asked for
- Human player support for interactive gameplay
- Customizable game parameters (number of players, initial cards, etc.)
- Simulation mode for running multiple games and gathering statistics

## Project Structure

```
src/
├── gofish/
│   ├── __init__.py
│   ├── cards.py     # Card, Deck, and Hand classes
│   ├── player.py    # Player interface and strategy implementations
│   └── game.py      # Core game logic
└── main.py          # Command-line interface
```

## Requirements

- Python 3.6 or higher

## Usage

Run a single game with 4 random AI players:

```bash
python src/main.py
```

Include a human player:

```bash
python src/main.py --human
```

Customize the number of players and initial cards:

```bash
python src/main.py --players 3 --initial-cards 5
```

Run a simulation of multiple games:

```bash
python src/main.py --games 100 --quiet
```

Mix different player types:

```bash
python src/main.py --player-types random,smart,memory
```

Set a random seed for reproducible results:

```bash
python src/main.py --seed 42
```

## Command-Line Options

- `--players N`: Number of players (default: 4)
- `--human`: Include a human player
- `--initial-cards N`: Number of cards to deal initially (default: 7)
- `--quiet`: Run in quiet mode (no verbose output)
- `--games N`: Number of games to simulate (default: 1)
- `--player-types TYPES`: Comma-separated list of player types: random, smart, memory (default: random)
- `--seed N`: Random seed for reproducible results

## Extending the Simulator

### Adding New Player Strategies

To create a new player strategy, subclass the `Player` abstract base class in `player.py` and implement the required methods:

```python
from gofish.player import Player

class MyCustomPlayer(Player):
    def choose_rank_to_ask_for(self):
        # Your strategy for choosing a rank
        pass
        
    def choose_player_to_ask(self, player_names):
        # Your strategy for choosing a player
        pass
```

### Modifying Game Rules

The core game logic is centralized in the `GoFishGame` class in `game.py`. You can modify this class to implement different rule variations.

## License

This project is licensed under the terms of the MIT license.
