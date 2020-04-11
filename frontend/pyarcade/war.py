import random
from enum import Enum
from pyarcade.cards import Suits
from pyarcade.abstract_game import AbstractGame


class Ranks(Enum):
    """
    Enumerated Type for card ranks of War.
    """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class War(AbstractGame):

    def __init__(self):
        """
        Sets up player one and two's initial hands.
        """
        AbstractGame.__init__(self)
        self.player_one_hand = []
        self.player_two_hand = []
        self.last_turn_winner = 0  # Since there is no last turn winner.
        self.new_game()

    def play_turn(self, pile: [(Ranks, Suits)]) -> bool:
        """
        Args:
            pile: Cards to be given to winner of turn.

        Returns:
            True if the game is to be continued, False if there is a winner.
        """
        # Check if there is a winner. Need check here also in case where after
        # 3 cards flipped for war results in a player having 0 cards left.
        if len(self.player_one_hand) == 0:
            self.last_turn_winner = 2
            self.update_current_history()
            return False
        elif len(self.player_two_hand) == 0:
            self.last_turn_winner = 1
            self.update_current_history()
            return False

        player_one_card = War.flip(self.player_one_hand)
        player_two_card = War.flip(self.player_two_hand)
        pile.extend([player_one_card, player_two_card])
        evaluation = War.compare_to(player_one_card, player_two_card)

        # Turn evaluation.
        if evaluation != 0:
            if evaluation > 0:
                self.last_turn_winner = 1
                self.player_one_hand.extend(pile)
                self.update_current_history()
            elif evaluation < 0:
                self.last_turn_winner = 2
                self.player_two_hand.extend(pile)
                self.update_current_history()

            # Check if there is a winner.
            if len(self.player_one_hand) == 0:
                return False
            elif len(self.player_two_hand) == 0:
                return False
            else:
                return True
        else:
            return self.war(pile)

    def war(self, pile: [(Ranks, Suits)]) -> bool:
        """
        Case where turn results in a war. Each player adds 3 additional cards
        to the pile before playing a new turn.
        Args:
            pile: Cards to be given to winner of turn.

        Returns:
            Recursive call to play_turn with an updated pile.
        """
        if len(self.player_one_hand) < 3:
            self.last_turn_winner = 2
            self.player_one_hand = []
            return False
        if len(self.player_two_hand) < 3:
            self.last_turn_winner = 1
            self.player_two_hand = []
            return False

        for count in range(0, 3):
            # Check if there is a winner.
            if len(self.player_one_hand) == 0:
                self.last_turn_winner = 2
                return False
            elif len(self.player_two_hand) == 0:
                self.last_turn_winner = 1
                return False
            else:
                player_one_card = War.flip(self.player_one_hand)
                player_two_card = War.flip(self.player_two_hand)
                pile.extend([player_one_card, player_two_card])

        return self.play_turn(pile)

    def enter_user_turn(self, cmd: str) -> bool:
        """
        Args:
            cmd: "Flip Card"
        Returns:
            Outcome of turn. (False if there is a winner)
        """
        turn_outcome = self.play_turn([])

        if turn_outcome:
            return True
        else:
            self.update_entire_history()
            return False

    def get_last_turn(self) -> (str, str, int, int, bool, int):
        """
        Returns:
            A Tuple containing String representations of both player's hands and
            the player who won the last turn.
        """

        if len(self.player_one_hand) == 0 or len(self.player_two_hand) == 0:
            return "", "", len(self.player_one_hand), \
                   len(self.player_two_hand), True, self.last_turn_winner

        player_one_str = War.to_str([self.player_one_hand[0]])
        player_two_str = War.to_str([self.player_two_hand[0]])

        return player_one_str, player_two_str, len(self.player_one_hand),\
            len(self.player_two_hand), False, self.last_turn_winner

    def reset_game(self):
        self.new_game()
        self.current_history = []

    def clear_game(self):
        self.reset_game()
        self.entire_history = []

    def new_game(self):
        """
        Deals new hands to players.
        """
        deck = War.generate_new_deck()
        shuffled = War.shuffle_deck(deck)
        self.player_one_hand, self.player_two_hand = War.deal_hands(shuffled)
        self.last_turn_winner = 0  # Since there is no last turn winner.

    @staticmethod
    def generate_new_deck() -> [(Ranks, Suits)]:
        """
        Returns:
            New deck of cards.
        """
        deck = []
        for rank in Ranks:
            for suit in Suits:
                deck.append((rank, suit))
        return deck

    @staticmethod
    def shuffle_deck(deck: [(Ranks, Suits)]) -> [(Ranks, Suits)]:
        """
        Args:
            deck: List of cards to be shuffled.

        Returns:
            Shuffled deck.
        """
        for idx in range((len(deck) - 1), -1, -1):
            card = deck[idx]
            random_position = random.randint(0, idx)
            deck[idx] = deck[random_position]
            deck[random_position] = card

        return deck

    @staticmethod
    def deal_hands(deck: [(Ranks, Suits)]) \
            -> ([(Ranks, Suits)], [(Ranks, Suits)]):
        """
        Args:
            deck: Deck which cards will be dealt.

        Returns:
            Two lists of 26 cards.
        """
        return deck[:26], deck[26:]

    @staticmethod
    def to_str(deck: [(Ranks, Suits)]) -> str:
        """
        Args:
            deck: List of cards.

        Returns:
            String containing all ranks in hand.
        """
        hand = ""
        for card in deck:
            hand += card[0].name + ", "
        return hand[:-2]

    @staticmethod
    def flip(deck: [(Ranks, Suits)]):
        """
        Args:
            deck: Deck of cards.

        Returns:
            Top card of the deck.
        """
        return deck.pop(0)

    @staticmethod
    def compare_to(card_one: (Ranks, Suits), card_two: (Ranks, Suits)) -> int:
        """
        Args:
            card_one: Player one card.
            card_two: Player two card.

        Returns:
            Positive number if player one wins turn, negative if player two wins
            turn, zero if there is a war.
        """
        if card_one[0].value > card_two[0].value:
            return 1
        elif card_one[0].value < card_two[0].value:
            return -1
        else:
            return 0

    @staticmethod
    def get_regex_pattern() -> str:
        """
        Gets regex pattern for War.
        Returns:
            Pattern match for game.
        """
        return r"^\s*(flip card)\s*$"

    def update_current_history(self):
        """
        Adds each player's hand and previous turn winner to current history.
        """
        player_one = War.to_str(self.player_one_hand)
        player_two = War.to_str(self.player_two_hand)
        last_turn_winner = self.last_turn_winner
        self.current_history.append((player_one, player_two, last_turn_winner))

    def update_entire_history(self):
        """
        Adds winner of game, and current history, to entire history.
        """
        winner = self.last_turn_winner
        self.entire_history.append((winner, self.current_history))
