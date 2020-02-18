from abc import abstractmethod, ABCMeta


class AbstractGame(metaclass=ABCMeta):
    def __init__(self):
        # histories
        self.entire_history = []
        self.current_history = []

    @abstractmethod
    def enter_user_turn(self, guess) -> bool:
        """ Checks if guess is correct in some way according
        to the current game.

        Args:
            guess: User's to the game.

        Returns:
            result (bool): True if correct, false otherwise.

        """
        pass

    @abstractmethod
    def reset_game(self):
        """ Reset single game. (input reset)
        """
        pass

    @abstractmethod
    def clear_game(self):
        """ Clears entire game. (input clear)
        """
        pass

    @abstractmethod
    def get_last_turn(self):
        """ Gets the last turn/state of game.

        Returns:
            Meaningful state of the current game.
        """
        pass
