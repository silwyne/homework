
# Available actions
CINEMA = "Cinema"
CAFE = "Cafe"

ACTIONS = [CINEMA, CAFE]

# Payoff matrix: (Ali, Behrooz)
PAYOFFS = {
    (CINEMA, CINEMA): (3, 2),
    (CINEMA, CAFE): (0, 0),
    (CAFE, CINEMA): (0, 0),
    (CAFE, CAFE): (2, 3)
}


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.score = 0
        self.history = []

    def choose_action(self, opponent_history):
        return self.strategy(opponent_history)

    def reset(self):
        self.score = 0
        self.history = []


class BattleOfSexes:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.round_number = 0

    def play_round(self):
        action1 = self.player1.choose_action(
            self.player2.history
        )

        action2 = self.player2.choose_action(
            self.player1.history
        )

        payoff1, payoff2 = PAYOFFS[(action1, action2)]

        self.player1.score += payoff1
        self.player2.score += payoff2

        self.player1.history.append(action1)
        self.player2.history.append(action2)

        self.round_number += 1

        print(f"\nRound {self.round_number}")
        print(f"{self.player1.name}: {action1}")
        print(f"{self.player2.name}: {action2}")
        print(f"Payoffs: ({payoff1}, {payoff2})")

    def play(self, rounds=1):
        for _ in range(rounds):
            self.play_round()

        print("\n--- Final Results ---")
        print(f"{self.player1.name}: {self.player1.score}")
        print(f"{self.player2.name}: {self.player2.score}")


# Strategies

def always_cinema(opponent_history):
    return CINEMA


def always_cafe(opponent_history):
    return CAFE


def random_strategy(opponent_history):
    import random
    return random.choice(ACTIONS)


def tit_for_tat(opponent_history):
    if not opponent_history:
        return CINEMA

    return opponent_history[-1]


STRATEGIES = {
    '1': always_cinema,
    '2': always_cafe,
    '3': random_strategy,
    '4': tit_for_tat
}


STRATEGY_MESSAGE = (
    "Choose strategy {1-4}:\n"
    "1 - Always Cinema\n"
    "2 - Always Cafe\n"
    "3 - Random Strategy\n"
    "4 - Tit for Tat"
)


if __name__ == "__main__":

    print("=" * 50)
    print("       BATTLE OF THE SEXES")
    print("       Game Theory - 2 Player Simulation")
    print("=" * 50)

    while True:
        try:
            input("\nPress Enter to continue...")

            print(STRATEGY_MESSAGE)

            player1_strategy = STRATEGIES[
                input("Ali strategy: ")
            ]

            player2_strategy = STRATEGIES[
                input("Behrooz strategy: ")
            ]

            game_rounds = int(
                input("Game rounds (default=1): ")
            )

            if game_rounds <= 0:
                game_rounds = 1

            player1 = Player("Ali", player1_strategy)
            player2 = Player("Behrooz", player2_strategy)

            game = BattleOfSexes(player1, player2)
            game.play(rounds=game_rounds)

        except KeyboardInterrupt:
            print("\n\n[!] Simulation interrupted by user.")
            print("[*] Shutting down gracefully...")
            break

        except (ValueError, KeyError):
            print("Invalid input! Please try again.")
