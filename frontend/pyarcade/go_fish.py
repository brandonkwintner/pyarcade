import random
from typing import List, Tuple

from pyarcade.abstract_game import AbstractGame
from pyarcade.cards import Ranks, Suits


class GoFish(AbstractGame):
    def __init__(self):
        AbstractGame.__init__(self)
        self.deck_of_cards = GoFish.generate_new_deck()
        self.shuffle_deck()
        self.player_one_hand = []
        self.computer_hand = []
        self.deal_out_cards()
        self.has_won = False

    @staticmethod
    def generate_new_deck() -> [(Ranks, Suits)]:
        deck = []

        for rank in Ranks:
            if rank == Ranks.ONE:
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

    def deal_out_cards(self):
        for i in range(5):
            self.player_one_hand.append(self.deck_of_cards.pop())
            self.computer_hand.append(self.deck_of_cards.pop())

    def enter_user_turn(self, guess) -> bool:
        """ Checks if computer has this card.

        Args:
            guess: User's card they guessed

        Returns:
            result: (bool) True if player has 4 of a kind (end of game), false otherwise.

        """
        guessed_rank = GoFish.parse_user_guess(guess)
        if guessed_rank == -1:
            return False

        found = False
        has = []

        for card in self.computer_hand:
            if guessed_rank == card[0].value:
                has.append(card)
                found = True

        for card in has:
            self.player_one_hand.append((card[0], card[1]))
            self.computer_hand.remove((card[0], card[1]))

        if not found:
            self.go_fish(self.player_one_hand)
            self.player_two_guesses()

        player_one_wins = self.check_for_winner(self.player_one_hand)
        computer_wins = self.check_for_winner(self.computer_hand)

        if player_one_wins:
            self.has_won = True
            self.current_history.append(("Player Wins", self._hand_to_str(self.player_one_hand)))
            self.entire_history.append(("Player Wins", self._hand_to_str(self.player_one_hand)))
            return True
        elif computer_wins:
            self.has_won = True
            self.current_history.append(("Computer Wins", self._hand_to_str(self.computer_hand)))
            self.entire_history.append(("Player Wins", self._hand_to_str(self.player_one_hand)))
        else:
            return False

    @staticmethod
    def parse_user_guess(input_str: str):
        guess_rank = input_str.lower()

        if guess_rank == "jack":
            guess_rank = 10.1
        elif guess_rank.lower() == "queen":
            guess_rank = 10.2
        elif guess_rank == "king":
            guess_rank = 10.3
        elif guess_rank == "ace":
            guess_rank = 11
        else:
            try:
                guess_rank = int(guess_rank)
            except ValueError:
                return -1

        return guess_rank

    def player_two_guesses(self):
        rand_index = random.randint(0, len(self.computer_hand) - 1)
        (rank_picked, suit_picked) = self.computer_hand[rand_index]
        found = False
        has = []

        for card in self.player_one_hand:
            if rank_picked == card[0]:
                has.append(card)
                found = True

        for card in has:
            self.computer_hand.append((card[0], card[1]))
            self.player_one_hand.remove((card[0], card[1]))

        if not found:
            self.go_fish(self.computer_hand)

    def go_fish(self, player_hand):
        player_hand.append(self.deck_of_cards.pop())

    @staticmethod
    def check_for_winner(player_hand: list) -> bool:
        amount = {}
        for card in player_hand:
            if card[0] not in amount.keys():
                amount[card[0]] = 1
            else:
                amount[card[0]] += 1
        for curr_amount in amount.keys():
            if amount[curr_amount] == 4:
                return True

        return False

    def reset_game(self):
        super().reset_game()

        self.player_one_hand = []
        self.computer_hand = []
        self.deck_of_cards = self.generate_new_deck()
        self.shuffle_deck()
        self.current_history = []
        self.deal_out_cards()

    def clear_game(self):
        super().clear_game()

        self.reset_game()
        self.entire_history = []

    def get_last_turn(self) -> Tuple[str, bool]:
        super().get_last_turn()

        player_cards = self._hand_to_str(self.player_one_hand)
        # computer_str = self._hand_to_str(self.computer_hand)

        return player_cards, self.has_won

    @staticmethod
    def _hand_to_str(hand):
        hand_str = ""
        for card in hand:
            if card[0].name == Ranks.ONE.name:
                hand_str += "ACE, "
            else:
                hand_str += card[0].name + ", "
        return hand_str[:-2]

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets pattern for mastermind.

                Returns:
                    Pattern for only numbers between 0-9 inclusive.

        """
        AbstractGame.get_regex_pattern()

        return r"^[2-10|Jack|jack|queen|Queen|king|King]$"
