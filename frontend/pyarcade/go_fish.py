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
        self.winner = 0
        self.has_won = False
        self.isFish = False

    @staticmethod
    def generate_new_deck() -> [(Ranks, Suits)]:
        """ Generates the deck of cards that will be used for the game.

            Returns:
                 List of Card objects.

        """
        deck = []

        for rank in Ranks:
            if rank == Ranks.ONE:
                continue
            for suit in Suits:
                deck.append((rank, suit))

        return deck

    def shuffle_deck(self) -> List[Tuple[Ranks, Suits]]:
        """ Shuffles the game's deck of cards.

        Returns:
            List of Card tuples.
        """
        for idx in range((len(self.deck_of_cards) - 1), -1, -1):
            card = self.deck_of_cards[idx]
            random_position = random.randint(0, idx)
            self.deck_of_cards[idx] = self.deck_of_cards[random_position]
            self.deck_of_cards[random_position] = card

        return self.deck_of_cards

    def deal_out_cards(self):
        """ Deals out 5 cards to each player.
        """
        for i in range(5):
            self.player_one_hand.append(self.deck_of_cards.pop())
            self.computer_hand.append(self.deck_of_cards.pop())

    def enter_user_turn(self, guess) -> bool:
        """ Checks if computer has this card.

        Args:
            guess: User's card they guessed

        Returns:
            result: (bool) True if player has 4 of a kind (end of game),
            false otherwise.

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
                self.isFish = False

        for card in has:
            self.player_one_hand.append(card)
            self.computer_hand.remove(card)

        if not found:
            self.go_fish(self.player_one_hand)
            self.player_two_guesses()
            self.isFish = True

        player_one_wins = self.check_for_winner(self.player_one_hand)
        computer_wins = self.check_for_winner(self.computer_hand)

        if player_one_wins:
            self.has_won = True
            self.current_history.append(("Player Wins", self._hand_to_str(
                self.player_one_hand)))
            self.entire_history.append(("Player Wins", self._hand_to_str(
                self.player_one_hand)))
            self.winner = 1
            return True

        elif computer_wins:
            self.has_won = True
            self.current_history.append(("Computer Wins", self._hand_to_str(
                self.computer_hand)))
            self.entire_history.append(("Computer Wins", self._hand_to_str(
                self.player_one_hand)))
            self.winner = 2
            return True

        else:
            if found:
                self.player_two_guesses()
            return False

    @staticmethod
    def parse_user_guess(input_str: str) -> int:
        """ Parses the user's input string.

        Args:
            input_str: User's guess.

        Returns:
            Integer value associated with the user's guess (-1 if invalid).
        """
        guess_rank = input_str.lower()

        if guess_rank == "two":
            guess_rank = 2
        elif guess_rank == "three":
            guess_rank = 3
        elif guess_rank == "four":
            guess_rank = 4
        elif guess_rank == "five":
            guess_rank = 5
        elif guess_rank == "six":
            guess_rank = 6
        elif guess_rank == "seven":
            guess_rank = 7
        elif guess_rank == "eight":
            guess_rank = 8
        elif guess_rank == "nine":
            guess_rank = 9
        elif guess_rank == "ten":
            guess_rank = 10
        elif guess_rank == "jack":
            guess_rank = 10.1
        elif guess_rank == "queen":
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
        """ Computer guesses a card.
        """
        rand_index = random.randint(0, len(self.computer_hand) - 1)
        (rank_picked, suit_picked) = self.computer_hand[rand_index]
        found = False
        has = []

        for card in self.player_one_hand:
            if rank_picked == card[0]:
                has.append(card)
                found = True

        for card in has:
            self.computer_hand.append(card)
            self.player_one_hand.remove(card)

        if not found:
            self.go_fish(self.computer_hand)

    def go_fish(self, player_hand):
        """

        Args:
            player_hand: Adds a Card to the player's hand.
        """
        player_hand.append(self.deck_of_cards.pop())

    @staticmethod
    def check_for_winner(player_hand: list) -> bool:
        """ Checks the 'player_hand' list for four of a kind.

        Args:
            player_hand: Player's hand of cards.

        Returns:
            True if list has four of a kind, False otherwise.
        """
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
        """ Reset single game. (input reset)
        """
        super().reset_game()

        self.player_one_hand = []
        self.computer_hand = []
        self.deck_of_cards = self.generate_new_deck()
        self.shuffle_deck()
        self.current_history = []
        self.deal_out_cards()
        self.winner = 0
        self.isFish = False

    def clear_game(self):
        """ Clears entire game. (input clear)
        """
        super().clear_game()

        self.reset_game()
        self.entire_history = []

    def get_last_turn(self) -> Tuple[str, bool, int]:
        """ Returns the current state of the game.

        Returns:
            Tuple containing the player's cards, is they guessed a correct
            card or not, and if there is a winner.
        """
        super().get_last_turn()

        player_cards = self._hand_to_str(self.player_one_hand)

        return player_cards, self.isFish, self.winner

    @staticmethod
    def _hand_to_str(hand):
        """ Converts a player's list of cards to a string.

        Args:
            hand: List of cards.

        Returns:
            String of all of the player's cards.
        """
        hand_str = ""
        for card in hand:
            hand_str += card[0].name + ", "

        return hand_str[:-2]

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets pattern for mastermind.

            Returns:
                Pattern for only numbers between 0-9 inclusive.

        """
        AbstractGame.get_regex_pattern()

        return r"^[2-9]{1}$|^10$|^ace$|^two$|^three$" \
               r"|^four$|^five$|^six$|^seven$|^eight$" \
               r"|^nine$|^ten$|^jack$|^queen$|^king$"
