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
