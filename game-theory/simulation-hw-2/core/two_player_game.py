
import random


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.score = 0
        self.history = []

    def choose_action(self, opponent_history, actions):
        return self.strategy(opponent_history, actions)

    def reset(self):
        self.score = 0
        self.history.clear()


class TwoPlayerGame:
    def __init__(
        self,
        player1,
        player2,
        actions,
        payoffs,
        game_name="Two Player Game"
    ):
        self.player1 = player1
        self.player2 = player2
        self.actions = actions
        self.payoffs = payoffs
        self.game_name = game_name
        self.round_number = 0

        self._validate_game()

    def _validate_game(self):
        if not self.actions:
            raise ValueError("Actions cannot be empty.")

        if len(set(self.actions)) != len(self.actions):
            raise ValueError("Actions must be unique.")

        expected = {
            (action1, action2)
            for action1 in self.actions
            for action2 in self.actions
        }

        if set(self.payoffs.keys()) != expected:
            raise ValueError(
                "Payoff matrix must contain all action combinations."
            )

    def play_round(self):
        action1 = self.player1.choose_action(
            self.player2.history,
            self.actions
        )

        action2 = self.player2.choose_action(
            self.player1.history,
            self.actions
        )

        if action1 not in self.actions or action2 not in self.actions:
            raise ValueError("Strategy returned an invalid action.")

        payoff1, payoff2 = self.payoffs[(action1, action2)]

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
        if rounds <= 0:
            raise ValueError("Rounds must be greater than zero.")

        print(f"\n===== {self.game_name} =====")

        for _ in range(rounds):
            self.play_round()

        self.show_results()

    def show_results(self):
        print("\n--- Final Results ---")
        print(f"{self.player1.name}: {self.player1.score}")
        print(f"{self.player2.name}: {self.player2.score}")

    def reset(self):
        self.player1.reset()
        self.player2.reset()
        self.round_number = 0


# ==================================================
# COMMON STRATEGIES
# ==================================================

def always_action(action):
    def strategy(opponent_history, actions):
        if action not in actions:
            raise ValueError("Invalid action for this game.")
        return action

    return strategy


def random_strategy(opponent_history, actions):
    return random.choice(actions)


def tit_for_tat(opponent_history, actions):
    if not opponent_history:
        return actions[0]

    return opponent_history[-1]


def get_strategies(actions):
    strategies = {}

    for index, action in enumerate(actions, 1):
        strategies[str(index)] = (
            f"Always {action}",
            always_action(action)
        )

    next_index = len(actions) + 1

    strategies[str(next_index)] = (
        "Random Strategy",
        random_strategy
    )

    strategies[str(next_index + 1)] = (
        "Tit for Tat",
        tit_for_tat
    )

    return strategies
