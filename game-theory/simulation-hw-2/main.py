
from core.two_player_game import (
    Player,
    TwoPlayerGame,
    get_strategies
)

from check_nash_equilibrium import print_nash_equilibria

# Import games
from games import (
    baz_kabootar,
    two_prisoners,
    coordination_game,
    advertising_game
)


# Available games
GAMES = {
    "1": ("Prisoner's Dilemma", two_prisoners),
    "2": ("Hawk-Dove Game", baz_kabootar),
    "3": ("Coordination Game", coordination_game),
    "4": ("Advertising Game", advertising_game)
}


def choose_strategy(player_name, actions):
    strategies = get_strategies(actions)

    print(f"\n--- {player_name} Strategies ---")

    for key, (name, _) in strategies.items():
        print(f"{key} - {name}")

    while True:
        choice = input(f"{player_name} strategy: ")

        if choice in strategies:
            return strategies[choice][1]

        print("Invalid strategy! Try again.")


def run_game(game_name, game_module):

    actions = game_module.ACTIONS
    payoffs = game_module.PAYOFFS

    print(f"\n===== {game_name} =====")

    # Show Nash Equilibrium
    print_nash_equilibria(payoffs, actions)

    # Choose player strategies
    player1_strategy = choose_strategy("Player 1", actions)
    player2_strategy = choose_strategy("Player 2", actions)

    # Number of rounds
    rounds = int(input("\nGame rounds: "))

    if rounds <= 0:
        rounds = 1

    # Create players
    player1 = Player("Player 1", player1_strategy)
    player2 = Player("Player 2", player2_strategy)

    # Create game
    game = TwoPlayerGame(
        player1=player1,
        player2=player2,
        actions=actions,
        payoffs=payoffs,
        game_name=game_name
    )

    # Run simulation
    game.play(rounds)


if __name__ == "__main__":

    print("=" * 50)
    print("       GAME THEORY SIMULATOR")
    print("       Core 2 Player Simulation")
    print("=" * 50)

    while True:

        print("\nSelect a game:")

        for key, (name, _) in GAMES.items():
            print(f"{key} - {name}")

        print("0 - Exit")

        try:
            choice = input("\nGame choice: ")

            if choice == "0":
                print("Exiting simulation...")
                break

            if choice not in GAMES:
                print("Invalid game choice!")
                continue

            game_name, game_module = GAMES[choice]

            run_game(game_name, game_module)

        except ValueError:
            print("Invalid numeric input!")

        except KeyboardInterrupt:
            print("\n\nSimulation interrupted.")
            break
