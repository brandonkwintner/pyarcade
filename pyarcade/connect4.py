from pyarcade.connect4_states import C4State
from typing import List


class Connect4:
    """ A class representing a Connect4 game session
    """

    MAX_ROWS = 6
    MAX_COLS = 7

    def __init__(self):
        # all previous games
        self.entire_history = []
        # current 6x7 board
        self.current_history = Connect4.setup_board()
        self.turn = 0

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
                C4State.X if turn even
                C4State.O if turn odd

        """

        return C4State.X if self.turn % 2 == 0 else C4State.O

    def guess_sequence(self, col: int) -> bool:
        """ Inputs a player's move.

            Args:
                col - column to drop "piece" in

            Returns:
                True if winning move was made False otherwise.

        """

        row = self.get_free_row(col)

        if row == -1:
            return False

        current_turn = self.get_turn()

        self.current_history[row][col] = current_turn
        self.turn += 1

        if self.check_win():
            self.entire_history.append((self.current_history, current_turn))
            return True
        else:
            return False

    def get_free_row(self, col: int) -> int:
        """ Gets a free row given a column.

            Returns:
                index of free row or -1 if row is full or invalid input.
        """

        # parameter checking
        if not isinstance(col, int):
            return -1
        elif col < 0 or col >= Connect4.MAX_COLS:
            return -1

        # start at bottom, going up given a column
        for row in reversed(range(Connect4.MAX_ROWS)):
            # found empty [row][col]
            if self.current_history[row][col] == C4State.E:
                return row

        return -1

    def check_win(self) -> bool:
        """ Checks if a player has won on the current board.

            Returns:
                True if game has been won.
        """
        return self.check_win_rows() or self.check_win_cols() \
            or self.check_win_diag_up() or self.check_win_diag_down()

    def check_win_cols(self) -> bool:
        """ Checks if a player has won vertically.

            Returns:
                True if game has been won False otherwise.

        """

        lookahead_limit = Connect4.MAX_ROWS - 3

        for col in range(Connect4.MAX_COLS):
            for row in range(lookahead_limit):
                if self.current_history[row][col] != C4State.E and \
                        self.current_history[row][col] == \
                        self.current_history[row+1][col] == \
                        self.current_history[row+2][col] == \
                        self.current_history[row+3][col]:
                    return True

        return False

    def check_win_rows(self) -> bool:
        """ Checks if a player has won horizontally.

            Returns:
                True if game has been won False otherwise.

        """
        # e.g., 7 - 3 = 4, limit to 4 iterations
        lookahead_limit = Connect4.MAX_COLS - 3

        for row in self.current_history:
            for idx in range(lookahead_limit):
                if row[idx] != C4State.E and \
                        row[idx] == row[idx+1] == row[idx+2] == row[idx+3]:
                    return True

        return False

    def check_win_diag_up(self):
        """ Checks if a player has won diagonally.
            (y = x).

            Returns:
                True if game has been won False otherwise.

        """

        for row in reversed(range(Connect4.MAX_ROWS)):
            for col in range(Connect4.MAX_COLS):
                # disregard starting point with x < 3 or y > 3
                # since they are not able to get 4 in a row
                if row < 3 or col > 3:
                    break

                if self.current_history[row][col] != C4State.E and \
                        self.current_history[row][col] == \
                        self.current_history[row - 1][col + 1] == \
                        self.current_history[row - 2][col + 2] == \
                        self.current_history[row - 3][col + 3]:
                    return True

        return False

    def check_win_diag_down(self):
        """ Checks if a player has won diagonally.
            (y = -x).

            Returns:
                True if game has been won False otherwise.

        """

        for row in range(Connect4.MAX_ROWS):
            for col in range(Connect4.MAX_COLS):
                if row > 2 or col > 3:
                    break

                if self.current_history[row][col] != C4State.E and \
                        self.current_history[row][col] == \
                        self.current_history[row + 1][col + 1] == \
                        self.current_history[row + 2][col + 2] == \
                        self.current_history[row + 3][col + 3]:
                    return True

        return False
