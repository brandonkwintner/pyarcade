from enum import Enum


class Options(Enum):
    MAIN_MENU_OPTIONS = ['', 'Play Games', 'Options', 'Exit']

    GAME_OPTIONS = ['', 'Play Mastermind', 'Play Connect Four',
                    'Play Blackjack', 'Play War', 'Play Go Fish',
                    'Play Horseman', 'Back']

    GAME_STARTUP = ['', 'New Game', 'Back']
    GAME_STARTUP_DIFFICULT = ['', 'Easy Mode', 'Normal Mode', 'Hard Mode',
                              'Back']

    MASTERMIND_OPTIONS = ['', 'Take Guess', 'Reset', 'Clear', 'Back']
    MASTERMIND_NEW_GAME = ['You Win!', 'New Game', 'Clear', 'Back']

    CONNECT_FOUR_OPTIONS = ['', 'Enter Column', 'Reset', 'Clear', 'Back']
    CONNECT_FOUR_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    BLACKJACK_OPTIONS = ['', 'Hit', 'Stand', 'Reset', 'Clear', 'Back']
    BLACKJACK_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    WAR_OPTIONS = ['', 'Flip Card', 'Reset', 'Clear', 'Back']
    WAR_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    GO_FISH_OPTIONS = ['', 'Take Guess', 'Reset', 'Clear', 'Back']
    GO_FISH_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    HORSEMAN_OPTIONS = ['', 'Take Guess', 'Reset', 'Clear', 'Back']
    HORSEMAN_NEW_GAME = ['', 'New Game', 'Clear', 'Back']

    FEATURE_OPTIONS = ['', 'Login', 'Signup', 'About', 'Back']
    FEATURE_LOGOUT_OPTIONS = ['', 'Logout', 'About', 'Back']
