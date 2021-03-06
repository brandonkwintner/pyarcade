from typing import List, Tuple
from pyarcade.cards import Ranks, Suits
from pyarcade.abstract_game import AbstractGame
from pyarcade.blackjack_players import BlackJackWinner
import random
import math


class Blackjack(AbstractGame):

    MAX_WINNING_LIMIT = 21
    NPC_STOP_LIMIT = 17

    def __init__(self):
        AbstractGame.__init__(self)
        self.deck_of_cards = Blackjack.generate_new_deck()
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.start_game()
        self.hasWon = False

    @staticmethod
    def generate_new_deck() -> [(Ranks, Suits)]:
        """
        Generate new deck.

        Returns:
            New deck.
        """
        deck = []

        for rank in Ranks:
            if rank == Ranks.ONE:
                continue
            for suit in Suits:
                deck.append((rank, suit))

        return deck

    def shuffle_deck(self) -> List[Tuple[Ranks, Suits]]:
        """
        Shuffles deck.

        Returns:
            Shuffled deck.
        """
        for idx in range((len(self.deck_of_cards) - 1), -1, -1):
            card = self.deck_of_cards[idx]
            random_position = random.randint(0, idx)
            self.deck_of_cards[idx] = self.deck_of_cards[random_position]
            self.deck_of_cards[random_position] = card

        return self.deck_of_cards

    def start_game(self):
        """
        Starts new game.
        """
        for _ in range(2):
            self.player_hand.append(self.hit())
            self.dealer_hand.append(self.hit())

        self.current_history.append(self.player_hand)

    def player_draw(self) -> bool:
        """
        Player draws a card.

        Returns:
            True if the player can hit, False otherwise.
        """
        if self.evaluate_hand(self.player_hand) < self.MAX_WINNING_LIMIT:
            self.player_hand.append(self.hit())
            self.evaluate_hand(self.player_hand)
            self.current_history.append(self.player_hand)
            return True

        return False

    def npc_draw(self, npc_hand: [(Ranks, Suits)]):
        """
        Computer draws card.

        Args:
            npc_hand: Computer's hand.
        """
        hand_value = self.evaluate_hand(npc_hand)

        while hand_value < self.NPC_STOP_LIMIT:
            npc_hand.append(self.hit())
            hand_value = self.evaluate_hand(npc_hand)

    def hit(self) -> (Ranks, Suits):
        """
        Player decides to hit.

        Returns:
            First card of the deck.
        """
        if len(self.deck_of_cards) == 0:
            self.deck_of_cards = self.generate_new_deck()
            self.shuffle_deck()

        card = self.deck_of_cards.pop(0)

        return card

    def evaluate_hand(self, card_hand: List[Tuple[Ranks, Suits]]) -> int:
        """
        Determines value of hand.

        Args:
            card_hand: Hand to be evaluated.

        Returns:
            Hand total.
        """
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
        """
        Changes Ace high value to low value.

        Args:
            card_hand: Hand to be altered.

        Returns:
            True if an Ace was changed to low value, False otherwise.
        """
        for idx in range(len(card_hand)):
            if card_hand[idx][0] == Ranks.ACE:
                card_hand[idx] = (Ranks.ONE, card_hand[idx][1])
                return True

        return False

    def stand(self) -> BlackJackWinner:
        """
        Player stands.

        Returns:
            Winner of the game.
        """
        self.npc_draw(self.dealer_hand)
        winner = self.calculate_winner()
        self.entire_history.append(
            (winner, [self.player_hand, self.dealer_hand]))

        return winner

    def calculate_winner(self) -> BlackJackWinner:
        """
        Determine who won the game.

        Returns:
            Winner of the game.
        """
        player_value = self.evaluate_hand(self.player_hand)
        dealer_value = self.evaluate_hand(self.dealer_hand)

        if player_value > self.MAX_WINNING_LIMIT:
            return BlackJackWinner.DEALER

        if dealer_value > self.MAX_WINNING_LIMIT:
            self.hasWon = True
            return BlackJackWinner.PLAYER

        if player_value > dealer_value:
            self.hasWon = True
            return BlackJackWinner.PLAYER
        else:
            return BlackJackWinner.DEALER

    def reset_game(self):
        """
        Reset game
        """
        super().reset_game()

        self.player_hand = []
        self.dealer_hand = []
        self.deck_of_cards = self.generate_new_deck()
        self.shuffle_deck()
        self.current_history = []
        self.start_game()
        self.hasWon = False

    def clear_game(self):
        """
        Clear game history.
        """
        super().clear_game()

        self.reset_game()
        self.entire_history = []

    def get_last_turn(self) -> Tuple[Tuple[str, str], bool]:
        """
        Get information about the last turn played.

        Returns:
            Information about the last turn played.
        """
        super().get_last_turn()

        player_cards = Blackjack._hand_to_str(self.player_hand)
        dealer_cards = Blackjack._hand_to_str(self.dealer_hand)

        cards = (player_cards, dealer_cards)

        return cards, self.hasWon

    @staticmethod
    def _hand_to_str(hand):
        """
        Converts hand to a string.

        Args:
            hand: Hand of cards.

        Returns:
            String representation of hand.
        """
        hand_str = ""
        total = 0
        for card in hand:
            if card[0].name == Ranks.ONE.name:
                hand_str += "ACE, "
                total += 1
            else:
                hand_str += card[0].name + ", "
                total += card[0].value

        hand_str = hand_str[:-2]
        hand_str += ": " + str(math.floor(total))
        return hand_str

    def enter_user_turn(self, cmd: str) -> bool:
        """ Enter's a user's input to the blackjack game.

        Args:
            cmd: either "stand" or "hit".

        Returns:
            True if player cannot draw or stands (end round). False otherwise.

        """
        super().enter_user_turn(cmd)

        if cmd == "hit":
            return not self.player_draw()
        elif cmd == "stand":
            self.stand()
            return True
        else:
            return False

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets pattern for blackjack.

        Returns:
            Pattern match for game.

        """
        AbstractGame.get_regex_pattern()

        return r"^\s*(hit)\s*$|^\s*(stand)\s*$"
