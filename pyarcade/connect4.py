from pyarcade.connect4_states import C4State


class Connect4:
    """ A class representing a Connect4 game session
    """
    def __init__(self):
        # all previous games
        self.entire_history = []
        # current 6x7 board
        self.current_history = Connect4.setup_board()

    @staticmethod
    def setup_board():
        """ Sets up a blank connect 4 game.

            Returns:
                6x7 Array of empty states
        """
        board = []

        for row in range(6):
            # array of size 7 filled with empty states
            row_array = [C4State.E] * 7

            board.append(row_array)

        return board
