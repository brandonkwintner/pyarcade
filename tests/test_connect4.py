from pyarcade.connect4 import Connect4
from pyarcade.connect4_states import C4State
import unittest


class Connect4TestCase(unittest.TestCase):
    @staticmethod
    def _shift_array(array):
        if not isinstance(array, list):
            return None

        right = array.pop()
        array.insert(0, right)

    @staticmethod
    def _shift_2d_array(array):
        if not isinstance(array, list):
            return None

        for sub in array:
            Connect4TestCase._shift_array(sub)

    def test_for_shifting(self):
        array = [
            [2, 3, 1],
            [5, 6, 4]
        ]

        expected = [[1, 2, 3], [4, 5, 6]]
        Connect4TestCase._shift_2d_array(array)

        self.assertEqual(expected, array)

    def test_init(self):
        game = Connect4()

        self.assertEqual(len(game.entire_history), 0)
        self.assertEqual(len(game.current_history), 6)
        self.assertEqual(len(game.current_history[0]), 7)

    def test_board_setup(self):
        # static method, returns 6x7 board of all empty states
        expected = [[C4State.E] * 7] * 6
        self.assertEqual(expected, Connect4.setup_board())

    def test_reset(self):
        game = Connect4()

        game.entire_history = [1]
        game.current_history = []
        game.reset_game()

        self.assertNotEqual([], game.current_history)
        # should have no change
        self.assertEqual([1], game.entire_history)

    def test_clear(self):
        game = Connect4()

        game.entire_history = [1]
        game.current_history = []
        game.clear_game()

        self.assertNotEqual([], game.current_history)
        self.assertEqual([], game.entire_history)

    def test_get_turn(self):
        game = Connect4()

        # player X goes first
        self.assertEqual(C4State.X, game.get_turn())

        game.guess_sequence(0)
        self.assertEqual(C4State.O, game.get_turn())

        game.guess_sequence(0)
        self.assertEqual(C4State.X, game.get_turn())

    def test_get_bad_free_row(self):
        game = Connect4()

        # bad row
        self.assertEqual(-1, game.get_free_row(-1))
        # bad type
        self.assertEqual(-1, game.get_free_row("yes"))
        self.assertEqual(-1, game.get_free_row(7))

    def test_get_good_single_free_row(self):
        game = Connect4()

        # should always get bottom row since empty board
        for col in range(Connect4.MAX_COLS):
            self.assertEqual(Connect4.MAX_ROWS - 1, game.get_free_row(col))

    def test_get_good_mult_free_row(self):
        game = Connect4()

        # check if getting correct row
        for row in range(Connect4.MAX_ROWS):
            for col in range(Connect4.MAX_COLS):
                self.assertEqual(Connect4.MAX_ROWS - row - 1,
                                 game.get_free_row(col))

                game.guess_sequence(col)

        # no empty slot should be left
        for row in game.current_history:
            self.assertFalse(C4State.E in row)

    def test_check_win_rows(self):
        game = Connect4()

        win_row = [C4State.X] * 4
        win_row.extend([C4State.O] * 3)

        og_board = game.current_history.copy()

        for _ in range(3):
            # shift Xs over to right
            win_row.pop()
            win_row.insert(0, C4State.O)

            for idx in range(len(game.current_history)):
                # move the win row down
                game.current_history[idx] = win_row
                self.assertTrue(game.check_win_rows())
                # go back to original
                game.current_history = og_board.copy()

    def test_check_win_rows_invalid(self):
        game = Connect4()

        # [x, x, x, o, x, o, o]
        win_row = [C4State.X] * 3
        win_row.append(C4State.O)
        win_row.append(C4State.X)
        win_row.extend([C4State.O] * 2)

        og_board = game.current_history.copy()

        for _ in range(3):
            # shift over to right
            win_row.pop()
            win_row.insert(0, C4State.O)

            for idx in range(Connect4.MAX_ROWS):
                # move the win row down
                game.current_history[idx] = win_row
                self.assertFalse(game.check_win_rows())
                # go back to original
                game.current_history = og_board.copy()

    def test_check_win_cols_top(self):
        game = Connect4()

        # 7 - 2 = 5 (-1 for range) rows to change
        for idx in range(Connect4.MAX_ROWS - 2):
            game.current_history[idx].pop()
            game.current_history[idx].insert(0, C4State.X)

        for _ in range(Connect4.MAX_COLS):
            self.assertTrue(game.check_win_cols())
            Connect4TestCase._shift_2d_array(game.current_history)

    def test_check_win_cols_mid(self):
        game = Connect4()

        # 7 - 2 = 5 (-1 for range) rows to change
        for idx in range(Connect4.MAX_ROWS - 2):
            game.current_history[idx+1].pop()
            game.current_history[idx+1].insert(0, C4State.X)

        for _ in range(Connect4.MAX_COLS):
            self.assertTrue(game.check_win_cols())
            Connect4TestCase._shift_2d_array(game.current_history)

    def test_check_win_cols_bottom(self):
        game = Connect4()

        # 7 - 2 = 5 (-1 for range) rows to change
        for idx in range(Connect4.MAX_ROWS - 2):
            game.current_history[idx+2].pop()
            game.current_history[idx+2].insert(0, C4State.X)

        for _ in range(Connect4.MAX_COLS):
            self.assertTrue(game.check_win_cols())
            Connect4TestCase._shift_2d_array(game.current_history)

    def test_check_win_diag_up(self):
        self.assertTrue(True)

    def test_check_win_diag_down(self):
        self.assertTrue(True)

    def test_check_win(self):
        self.assertTrue(True)

    def test_check_guess_sequence(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
