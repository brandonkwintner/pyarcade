from typing import List, Tuple
from pyarcade.cards import Ranks, Suits
from pyarcade.abstract_game import AbstractGame
from pyarcade.blackjack_players import BlackJackWinner
import random


class Blackjack(AbstractGame):
    MAX_WINNING_LIMIT = 21
    NPC_STOP_LIMIT = 17

    def __init__(self):
        AbstractGame.__init__(self)

        self.deck_of_cards = Blackjack.generate_new_deck()
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []

    @staticmethod
    def generate_new_deck() -> [(Ranks, Suits)]:
        deck = []

        for rank in Ranks:
            if rank == Ranks.One:
                continue
            for suit in Suits:
                deck.append((rank, suit))

        return deck

    def shuffle_deck(self) -> List[Tuple[Ranks, Suits]]:
        for idx in range((len(self.deck_of_cards) - 1), -1, -1):
            card = self.deck_of_cards[idx]
            random_position = random.randint(0, idx)
            self.deck_of_cards[idx] = self.deck_of_cards[random_position]
            self.deck_of_cards[random_position] = card

        return self.deck_of_cards

    def start_game(self):
        for _ in range(2):
            self.player_hand.append(self.hit())
            self.dealer_hand.append(self.hit())

        self.current_history.append(self.player_hand)

    def player_draw(self) -> bool:
        if self.evaluate_hand(self.player_hand) < self.MAX_WINNING_LIMIT:
            self.player_hand.append(self.hit())
            self.current_history.append(self.player_hand)
            return True

        return False

    def npc_draw(self, npc_hand: [(Ranks, Suits)]):
        hand_value = self.evaluate_hand(npc_hand)

        while hand_value < self.NPC_STOP_LIMIT:
            npc_hand.append(self.hit())
            hand_value = self.evaluate_hand(npc_hand)

    def hit(self) -> (Ranks, Suits):
        if len(self.deck_of_cards) == 0:
            self.deck_of_cards = self.generate_new_deck()
            self.shuffle_deck()

        card = self.deck_of_cards.pop(0)

        return card

    def evaluate_hand(self, card_hand: List[Ranks]) -> int:
        hand_total = self.MAX_WINNING_LIMIT + 1

        while hand_total > self.MAX_WINNING_LIMIT:
            hand_total = 0

            for card in card_hand:
                hand_total += int(card[0].value)

            if hand_total > self.MAX_WINNING_LIMIT and \
                    not Blackjack.change_ace_to_one(card_hand):
                return hand_total

        return hand_total

    @staticmethod
    def change_ace_to_one(card_hand: [Ranks]) -> bool:
        for idx in range(len(card_hand)):
            if card_hand[idx][0] == Ranks.Ace:
                card_hand[idx] = (Ranks.One, card_hand[idx][1])
                return True

        return False

    def stand(self) -> BlackJackWinner:
        self.npc_draw(self.dealer_hand)
        winner = self.calculate_winner()
        self.entire_history.append((winner, [self.player_hand, self.dealer_hand]))
        self.reset_game()

        return winner

    def calculate_winner(self) -> BlackJackWinner:
        player_value = self.evaluate_hand(self.player_hand)
        dealer_value = self.evaluate_hand(self.dealer_hand)

        if player_value > self.MAX_WINNING_LIMIT:
            return BlackJackWinner.DEALER

        if dealer_value > self.MAX_WINNING_LIMIT:
            return BlackJackWinner.PLAYER

        if player_value > dealer_value:
            return BlackJackWinner.PLAYER
        else:
            return BlackJackWinner.DEALER

    def reset_game(self):
        super().reset_game()

        self.player_hand = []
        self.dealer_hand = []
        self.deck_of_cards = self.generate_new_deck()
        self.shuffle_deck()
        self.current_history = []
        self.start_game()

    def clear_game(self):
        super().clear_game()

        self.reset_game()
        self.entire_history = []

    def get_last_turn(self) -> str:
        super().get_last_turn()

        return "".join(self.player_hand)

    def enter_user_turn(self, cmd: str) -> bool:
        """ Enter's a user's input to the blackjack game.

        Args:
            cmd: either "stand" or "hit".

        Returns:
            True if player stands (end of game). False otherwise.

        """
        super().enter_user_turn(cmd)

        if cmd == "hit":
            self.player_draw()
            return False
        elif cmd == "stand":
            self.stand()
            return True
        else:
            return False

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets pattern for blackjack.

        Returns:
            Pa

        """
        AbstractGame.get_regex_pattern()

        return r"^\s*(hit)\s*$|^\s*(stand)\s*$"

    @staticmethod
    def get_instructions() -> str:
        """ Instructions for game.

        Returns:
            Instructions for blackjack.

        """

        AbstractGame.get_instructions()

        return "Instructions for blackjack"
