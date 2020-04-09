from enum import Enum


class Options(Enum):
    MAIN_MENU_OPTIONS = ['', 'Play Mastermind', 'Play Connect Four',
                         'Play Blackjack', 'Exit']

    MASTERMIND_OPTIONS = ['', 'Take Guess', 'Reset', 'Clear', 'Back']
    MASTERMIND_NEW_GAME = ['You Win!', 'New Game', 'Clear', 'Back']

    CONNECT_FOUR_OPTIONS = ['', 'Enter Column', 'Reset', 'Clear', 'Back']
    CONNECT_FOUR_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    BLACKJACK_OPTIONS = ['', 'Hit', 'Stand', 'Reset', 'Clear', 'Back']
    BLACKJACK_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    WAR_OPTIONS = ['', 'Flip Card', 'Reset', 'Clear', 'Back']
    WAR_NEW_GAME = ['', 'New Game', 'Clear', 'Back']
