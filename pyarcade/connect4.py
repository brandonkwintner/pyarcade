from pyarcade.connect4_states import C4State
from typing import List


class Connect4:
    MAX_ROWS = 6
    MAX_COLS = 7
    """ A class representing a Connect4 game session
    """
    def __init__(self):
        # all previous games
        self.entire_history = []
        # current 6x7 board
        self.current_history = Connect4.setup_board()

    @staticmethod
    def setup_board() -> List[List[C4State]]:
        """ Sets up a blank connect 4 game.

            Returns:
                MAX_ROWS x MAX_COLS 2d array of empty states.
        """
        board = []

        for _ in range(Connect4.MAX_ROWS):
            # array of size 7 filled with empty states
            row_array = [C4State.E] * Connect4.MAX_COLS

            board.append(row_array)

        return board

    def reset_game(self):
        """ Reset single game. (input reset)
        """

        self.current_history = Connect4.setup_board()

    def clear_game(self):
        """ Clears entire game. (input clear)
        """

        self.entire_history = []
        self.current_history = Connect4.setup_board()

    def get_turn(self) -> C4State:
        """ Determines the turn of the 2 players.

            Returns:
                C4State.X if even
                C4State.O if odd

        """

        return C4State.X if len(self.current_history) % 2 == 0 else C4State.O

    def guess_sequence(self, row: int, col: int) -> bool:
        """ Inputs a player's move.

            Args:
                col - x position, indexed at 0.
                row - y position, indexed at 0.

            Returns:
                True if winning move was made.

        """

        if not isinstance(row, int) or not isinstance(col, int):
            return False
        elif row < 0 or col < 0:
            return False
        elif row >= Connect4.MAX_ROWS or col >= Connect4.MAX_COLS:
            return False

        self.current_history[row][col] = self.get_turn()
