
import random

# Available actions
C = "Cooperate"
D = "Defect"

ACTIONS = [C, D]

# Payoff matrix: (Player 1, Player 2)
PAYOFFS = {
    (C, C): (3, 3),
    (C, D): (0, 5),
    (D, C): (5, 0),
    (D, D): (1, 1)
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


class PrisonersDilemma:
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

def always_cooperate(opponent_history):
    return C


def always_defect(opponent_history):
    return D


def random_strategy(opponent_history):
    return random.choice([C, D])


def tit_for_tat(opponent_history):
    if not opponent_history:
        return C
    return opponent_history[-1]

CHOOSE_STRATEGY_MESSAGE = "choose strategy {1-4}: always_cooperate(1), always_defect(2), random_strategy(3), tit_for_tat(4)"

CHOOSE_STRATEGY_MATRIX = {
    '1': always_cooperate,
    '2': always_defect,
    '3': random_strategy,
    '4': tit_for_tat
}

if __name__ == "__main__":

    print("=" * 50)
    print("       PRISONER'S DILEMMA | GAME SIMULATION")
    print("       Game Theory - 2 Player Simulation")
    print("=" * 50)

    while True:
        try:
            input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\n[!] Simulation interrupted by user.")
            print("[*] Shutting down gracefully...")
            break
            
        print(CHOOSE_STRATEGY_MESSAGE)
        player_1_strategy = CHOOSE_STRATEGY_MATRIX[input("player 1 strategy: ")]
        player_2_strategy = CHOOSE_STRATEGY_MATRIX[input("player 2 strategy: ")]
        print()
        
        game_rounds = int(input("game rounds (default=1): "))
        if game_rounds <= 0:
            game_rounds = 1

        # Create players
        player1 = Player("Player 1", player_1_strategy)
        player2 = Player("Player 2", player_2_strategy)

        # Create and run the game
        game = PrisonersDilemma(player1, player2)
        game.play(rounds=game_rounds)