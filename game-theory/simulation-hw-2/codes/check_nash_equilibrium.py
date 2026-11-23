
def _find_nash_equilibria(payoffs, actions):
    nash_equilibria = []

    for action1 in actions:
        for action2 in actions:

            payoff1, payoff2 = payoffs[(action1, action2)]

            # Check if Player 1 can improve by changing action
            player1_best = all(
                payoff1 >= payoffs[(other_action, action2)][0]
                for other_action in actions
            )

            # Check if Player 2 can improve by changing action
            player2_best = all(
                payoff2 >= payoffs[(action1, other_action)][1]
                for other_action in actions
            )

            if player1_best and player2_best:
                nash_equilibria.append(
                    (action1, action2, payoff1, payoff2)
                )

    return nash_equilibria


def print_nash_equilibria(payoffs, actions):
    equilibria = _find_nash_equilibria(payoffs, actions)

    print("\n--- Nash Equilibrium ---")

    if not equilibria:
        print("No pure strategy Nash equilibrium found.")
    else:
        for i, equilibrium in enumerate(equilibria, 1):
            action1, action2, payoff1, payoff2 = equilibrium

            print(f"Equilibrium {i}:")
            print(f"Player 1: {action1}")
            print(f"Player 2: {action2}")
            print(f"Payoffs: ({payoff1}, {payoff2})")


if __name__ == "__main__":
    from baz_kabootar import PAYOFFS as BAZ_KABOOTAR_PAYOFFS
    from baz_kabootar import ACTIONS as BAZ_KABOOTAR_ACTIONS

    from two_prisoners import PAYOFFS as TWO_PRISONERS_PAYOFFS
    from two_prisoners import ACTIONS as TWO_PRISONERS_ACTIONS

    print_nash_equilibria(BAZ_KABOOTAR_PAYOFFS, BAZ_KABOOTAR_ACTIONS)
    print_nash_equilibria(TWO_PRISONERS_PAYOFFS, TWO_PRISONERS_ACTIONS)
