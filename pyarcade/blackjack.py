from typing import Optional, List
from pyarcade.cards import Ranks, Suits
import random


class Blackjack:
    MAX_WINNING_LIMIT = 21
    NPC_STOP_LIMIT = 17

    def __init__(self):
        self.deck_of_cards = self.generate_new_deck()
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.history = []
        self.complete_history = []

    def generate_new_deck(self) -> [(Ranks, Suits)]:
        deck = []

        for rank in Ranks:
            if rank == Ranks.One:
                continue
            for suit in Suits:
                deck.append((rank, suit))

        return deck

    def shuffle_deck(self) -> [(Ranks, Suits)]:
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

        self.history.append(self.player_hand)

    def player_draw(self) -> bool:
        if self.evaluate_hand(self.player_hand) <= self.MAX_WINNING_LIMIT:
            self.player_hand.append(self.hit())
            self.history.append(self.player_hand)
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

    def evaluate_hand(self, card_hand: [Ranks]) -> int:
        hand_total = self.MAX_WINNING_LIMIT + 1

        while hand_total > self.MAX_WINNING_LIMIT:
            hand_total = 0

            for card in card_hand:
                hand_total += int(card[0].value)

            if hand_total > self.MAX_WINNING_LIMIT and not self.change_ace_to_one(card_hand):
                return hand_total

        return hand_total

    def change_ace_to_one(self, card_hand: [Ranks]) -> bool:
        for idx in range(len(card_hand)):
            if card_hand[idx][0] == Ranks.Ace:
                card_hand[idx] = (Ranks.One, card_hand[idx][1])
                return True

        return False

    def stand(self) -> str:
        self.npc_draw(self.dealer_hand)
        winner = self.calculate_winner()
        self.complete_history.append((winner, [self.player_hand, self.dealer_hand]))
        self.new_game()

        return winner

    def calculate_winner(self) -> str:
        player_value = self.evaluate_hand(self.player_hand)
        dealer_value = self.evaluate_hand(self.dealer_hand)

        if player_value > self.MAX_WINNING_LIMIT:
            return "Dealer Win"

        if dealer_value > self.MAX_WINNING_LIMIT:
            return "Player Win"

        if player_value > dealer_value:
            return "Player Win"
        else:
            return "Dealer Win"

    def new_game(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck_of_cards = self.generate_new_deck()
        self.shuffle_deck()
        self.history = []
        self.start_game()

    def clear_all(self):
        self.new_game()
        self.complete_history = []
