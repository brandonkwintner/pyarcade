from enum import Enum


class Difficulty(Enum):
    """
    Represents the game difficulty.

    EASY - Easy game mode.

    NORMAL - Default game mode.

    HARD - Hard game mode.
    """
    EASY = "Easy"
    NORMAL = "Normal"
    HARD = "Hard"
