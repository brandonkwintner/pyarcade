from typing import Tuple, List
from pyarcade.mastermind import Mastermind
import re


class InputSystem:
    """ Represents input system for validation and game usage.
        And executes commands on user input.

    """
    def __init__(self):
        self.mastermind = Mastermind()
        self.mastermind.generate_hidden_sequence()
        self.round = 1
        self.game = 1

    def take_input(self, cmd: str) -> Tuple[bool, bool]:
        """ Takes in a user's input and interacts with mastermind
        accordingly.

        Args:
            cmd (string): user's command.

        Returns:
            A 2-tuple boolean representing (win, valid_cmd).

            win (bool): True iff correct sequence was guessed.
            valid_cmd (bool): True iff a valid cmd was inputted.

        """

        valid_cmd = True
        win = False

        if cmd == "reset":
            self.reset()
        elif cmd == "clear":
            self.clear()
        # matches only input with 4 numbers separated by whitespace
        elif re.match(r"^\s*[0-9]\s+[0-9]\s+[0-9]\s+[0-9]\s*$", cmd):
            # turns the string guess into an int list
            guess = [int(num) for num in cmd.split()]
            correct_guess = self.make_guess(guess)

            if correct_guess:
                self.round = 1
                self.game += 1
            else:
                self.round += 1

            win = correct_guess
        else:
            valid_cmd = False

        return win, valid_cmd

    def make_guess(self, guess: List[int]) -> bool:
        """ Checks if guess matches the hidden sequence.

        Args:
            guess (List[int]): user's guess list
        Returns:
            result (bool): True if correct, false otherwise.

        """

        return self.mastermind.guess_sequence(guess)

    def reset(self):
        """ Resets the mastermind game to starting state.
        """

        self.round = 1
        self.mastermind.reset_game()

    def clear(self):
        """ Clear the mastermind game history.
        """

        self.round = 1
        self.game = 1
        self.mastermind.clear_game()
