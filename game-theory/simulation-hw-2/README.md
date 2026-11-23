# Game Theory Simulator

A Python-based simulator for two-player strategic games.

## Features
- Simulate two-player games for multiple rounds.
- Support different player strategies.
- Calculate pure strategy Nash equilibria.
- Easily add new games using only `ACTIONS` and `PAYOFFS`.

## Project Structure
```text
simulation-hw-2/
├── core/
├── games/
├── check_nash_equilibrium.py
└── main.py
```

## Run
```bash
python main.py
```

## Add a New Game
Create a Python file inside `games/` and define:

```python
ACTIONS = [...]
PAYOFFS = {
    # (player1_action, player2_action): (player1_payoff, player2_payoff)
}
```

Then register the game in `main.py`.

## Requirements
- Python 3.8+
- No external dependencies
