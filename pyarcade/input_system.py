from typing import Tuple, List
from pyarcade.mastermind import Mastermind


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
        else:
            valid_cmd = False

        return win, valid_cmd

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
