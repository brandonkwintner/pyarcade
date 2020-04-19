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

    def enter_user_turn(self, guess) -> bool:
        """ Checks if guess is correct in some way according
        to the current game.

        Args:
            guess: User's to the game.

        Returns:
            result (bool): True if correct, false otherwise.

        """
        pass

    def reset_game(self):
        """ Reset single game. (input reset)
        """
        pass

    def clear_game(self):
        """ Clears entire game. (input clear)
        """
        pass

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
        pass
