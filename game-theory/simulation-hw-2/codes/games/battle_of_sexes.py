
# Available actions
BOXING = "Boxing"
PING_PONG = "Ping Pong"

ACTIONS = [BOXING, PING_PONG]

# Payoff matrix: (Husband, Wife)
PAYOFFS = {
    (BOXING, BOXING): (3, 2),
    (BOXING, PING_PONG): (0, 0),
    (PING_PONG, BOXING): (0, 0),
    (PING_PONG, PING_PONG): (2, 3)
}
