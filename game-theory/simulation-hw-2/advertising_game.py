
# Available actions
A = "Advertise"
N = "Not Advertise"

ACTIONS = [A, N]

# Payoff matrix: (Company X, Company Y)
PAYOFFS = {
    (A, A): (5, 5),
    (A, N): (15, 2),
    (N, A): (2, 15),
    (N, N): (10, 10)
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


class AdvertisingGame:
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

def always_advertise(opponent_history):
    return A


def never_advertise(opponent_history):
    return N


def random_strategy(opponent_history):
    import random
    return random.choice(ACTIONS)


def tit_for_tat(opponent_history):
    if not opponent_history:
        return A

    return opponent_history[-1]


STRATEGIES = {
    '1': always_advertise,
    '2': never_advertise,
    '3': random_strategy,
    '4': tit_for_tat
}


STRATEGY_MESSAGE = (
    "Choose strategy {1-4}:\n"
    "1 - Always Advertise\n"
    "2 - Never Advertise\n"
    "3 - Random Strategy\n"
    "4 - Tit for Tat"
)


if __name__ == "__main__":

    print("=" * 50)
    print("       ADVERTISING GAME")
    print("       Game Theory - 2 Player Simulation")
    print("=" * 50)

    while True:
        try:
            input("\nPress Enter to continue...")

            print(STRATEGY_MESSAGE)

            player1_strategy = STRATEGIES[
                input("Company X strategy: ")
            ]

            player2_strategy = STRATEGIES[
                input("Company Y strategy: ")
            ]

            game_rounds = int(
                input("Game rounds (default=1): ")
            )

            if game_rounds <= 0:
                game_rounds = 1

            player1 = Player("Company X", player1_strategy)
            player2 = Player("Company Y", player2_strategy)

            game = AdvertisingGame(player1, player2)
            game.play(rounds=game_rounds)

        except KeyboardInterrupt:
            print("\n\n[!] Simulation interrupted by user.")
            print("[*] Shutting down gracefully...")
            break

        except (ValueError, KeyError):
            print("Invalid input! Please try again.")
