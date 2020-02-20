from enum import Enum


class C4State(Enum):
    """ Represents the state of each slot on the board

        "E" - Empty slot

        "X" - Player X occupies slot

        "O" - Player O occupies slot

    """

    E = "-"
    X = "X"
    O = "O"


