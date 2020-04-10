from enum import Enum


class BlackJackWinner(Enum):
    """ Represents the winner of a blackjack round

        "PLAYER" - player.

        "DEALER" - dealer.

    """

    PLAYER = "Player"
    DEALER = "Dealer"
