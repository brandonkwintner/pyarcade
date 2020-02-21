from typing import Optional, List, Tuple
from pyarcade.eval_input import Evaluation
from pyarcade.abstract_game import AbstractGame
import random


class Mastermind(AbstractGame):
    """ A class representing a Mastermind game session

        Args:
            width: (int) The number of random digits to generate

            max_range: (int) The range that a single digit can vary

    """
    def __init__(self, width: Optional[int] = 4, max_range: Optional[int] = 9):
        AbstractGame.__init__(self)

        self.width = width
        self.max_range = max_range

        # generated sequence
        self.gen_sequence = self.generate_hidden_sequence()

    def generate_hidden_sequence(self) -> List[int]:
        """ Generates a hidden sequence for mastermind game.

        Returns:
            hidden_sequence: List[int] A sequence of integers to be guessed.

        """

        return \
            [random.randint(0, self.max_range) for _ in range(self.width)]

    def enter_user_turn(self, guess: List[int]) -> bool:
        """ Checks if guess matches the hidden sequence.

        Args:
            guess: User's list of int to guess

        Returns:
            result: (bool) True if correct, false otherwise.

        """

        super().enter_user_turn(guess)

        guesses_eval = self.check_guess(guess)

        if not guesses_eval:
            return False

        self.current_history.append(guesses_eval)

        if guess == self.gen_sequence:
            self.correct_guess()
            return True
        else:
            return False

    def check_guess(self, guess: List[int]) -> List[Tuple[int, Evaluation]]:
        """ Evaluates a guess to the current generated sequence.

        Args:
            guess: User's list of int to guess

        Returns:
            Evaluation list of tuples(int, evaluation).
            Empty list if invalid array given.

        """

        if len(guess) != len(self.gen_sequence):
            return []

        for num in guess:
            if not isinstance(num, int) or num < 0 or num > 9:
                return []

        guesses_eval = []

        for idx in range(len(guess)):
            guess_num = guess[idx]

            if guess_num == self.gen_sequence[idx]:
                guesses_eval.append((guess_num, Evaluation.CORRECT))
            elif guess_num in self.gen_sequence:
                guesses_eval.append((guess_num, Evaluation.SOMEWHERE))
            else:
                guesses_eval.append((guess_num, Evaluation.INCORRECT))

        return guesses_eval

    def correct_guess(self):
        """ Correct guess was issued, add current history to entire history
        Generate new sequence.

        """

        self.entire_history.append(self.current_history)
        self.clear_history()
        self.gen_sequence = self.generate_hidden_sequence()

    def reset_game(self):
        """ Reset single game. (input reset)
        """

        super().reset_game()

        self.clear_history()
        self.gen_sequence = self.generate_hidden_sequence()

    def clear_game(self):
        """ Clears entire game. (input clear)
        """

        super().clear_game()

        self.clear_all_history()
        self.gen_sequence = self.generate_hidden_sequence()

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

        super().get_last_turn()

        if len(self.current_history) < 1:
            return []

        # gets # of guess and converts to eval enum into a string value
        return [(guess[0], guess[1].value)
                for guess in self.current_history[-1]]

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets pattern for mastermind.

        Returns:
            Pattern for only numbers between 0-9 inclusive.

        """
        AbstractGame.get_regex_pattern()

        return r"^\s*[0-9]\s+[0-9]\s+[0-9]\s+[0-9]\s*$"

    @staticmethod
    def get_instructions() -> str:
        """ Instructions for game.

        Returns:
            Instructions for mastermind.

        """

        AbstractGame.get_instructions()

        return "Enter 4 digits between 0-9 (inclusive)."
