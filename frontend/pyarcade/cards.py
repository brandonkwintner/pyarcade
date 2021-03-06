from enum import Enum


class Ranks(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10.1
    QUEEN = 10.2
    KING = 10.3
    ACE = 11


class Suits(Enum):
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    HEARTS = "Hearts"
    SPADES = "Spades"
