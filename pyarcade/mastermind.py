from typing import Optional, List, Tuple
from pyarcade.eval_input import Evaluation
from pyarcade.abstract_game import AbstractGame
import random


class Mastermind(AbstractGame):
    """ A class representing a Mastermind game session

        Args:
            width (int): The number of random digits to generate

            max_range (int): The range that a single digit can vary

    """
    def __init__(self, width: Optional[int] = 4, max_range: Optional[int] = 9):
        AbstractGame.__init__(self)

        self.width = width
        self.max_range = max_range

        # generated sequence
        self.gen_sequence = []
        self.generate_hidden_sequence()

    def generate_hidden_sequence(self) -> List[int]:
        """ Generates a hidden sequence for mastermind game.

        Returns:
            hidden_sequence List[int]: A sequence of integers to be guessed.

        """

        self.gen_sequence = \
            [random.randint(0, self.max_range) for _ in range(self.width)]

        return self.gen_sequence

    def enter_user_turn(self, guess: List[int]) -> bool:
        """ Checks if guess matches the hidden sequence.

        Returns:
            result (bool): True if correct, false otherwise.

        """

        if len(guess) != len(self.gen_sequence):
            return False

        for num in guess:
            if not isinstance(num, int) or num < 0 or num > 9:
                return False

        history = []

        for idx in range(len(guess)):
            guess_num = guess[idx]

            # check exact location
            # check somewhere inside
            # not in
            if guess_num == self.gen_sequence[idx]:
                history.append((guess_num, Evaluation.CORRECT))
            elif guess_num in self.gen_sequence:
                history.append((guess_num, Evaluation.SOMEWHERE))
            else:
                history.append((guess_num, Evaluation.INCORRECT))

        self.current_history.append(history)

        if guess == self.gen_sequence:
            self.correct_guess()
            return True
        else:
            return False

    def correct_guess(self):
        """ Correct guess was issued, add current history to entire histor
        Generate new sequence.

        """

        self.entire_history.append(self.current_history)
        self.clear_history()
        self.generate_hidden_sequence()

    def reset_game(self):
        """ Reset single game. (input reset)
        """

        self.clear_history()
        self.generate_hidden_sequence()

    def clear_game(self):
        """ Clears entire game. (input clear)
        """

        self.clear_all_history()
        self.generate_hidden_sequence()

    def clear_all_history(self):
        """ Clears history of entire game.
        """

        self.current_history = []
        self.entire_history = []

    def clear_history(self):
        """ Clears history of current session.
        """

        self.current_history = []

    def get_last_turn(self) -> List[Tuple[int, str]]:
        """ Retrieves the player's last guess.

               Returns:
                   List[Tuple[int, str]]: The evaluation list of last guess.

       """

        if len(self.current_history) < 1:
            return []

        # gets # of guess and converts to eval enum into a string value
        return [(guess[0], guess[1].value)
                for guess in self.current_history[-1]]
