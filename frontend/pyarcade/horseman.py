from pyarcade.abstract_game import AbstractGame
from pyarcade.difficulties import Difficulty
from typing import Optional


class Horseman(AbstractGame):
    def __init__(self, difficulty: Optional[Difficulty] = Difficulty.NORMAL):
        if difficulty == Difficulty.EASY:
            self.word_length = 4
        elif difficulty == Difficulty.NORMAL:
            self.word_length = 6
        else:
            self.word_length = 8

        self.num_guesses = 0
        self.difficulty = difficulty
        self.word = self.pick_word()

    @staticmethod
    def pick_word():
        return ""

    def enter_user_turn(self, guess) -> bool:
        """ Checks if guess is correct in some way according
        to the current game.

        Args:
            guess: User's to the game.

        Returns:
            result (bool): True if correct, false otherwise.

        """
        super().enter_user_turn(guess)



    def reset_game(self):
        """ Reset single game. (input reset)
        """
        super.reset_game()

        self.current_history = []
        self.word = self.pick_word()

    def clear_game(self):
        """ Clears entire game. (input clear)
        """
        super.clear_game()

        self.current_history = []
        self.entire_history = []
        self.word = self.pick_word()

    def get_last_turn(self):
        """ Gets the last turn/state of game.

        Returns:
            Meaningful state of the current game.
        """
        pass

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets validator for game.

        Returns:
            Regex string.
        """
        AbstractGame.get_regex_pattern()

        return r"^[a-zA-Zz]$"
