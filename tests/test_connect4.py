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

    @staticmethod
    def _2d_to_str(array):
        result = ""

        for row in array:
            for element in row:
                result += element + " "
            result += "\n"

        return result

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

        game.enter_user_turn(0)
        self.assertEqual(C4State.O, game.get_turn())

        game.enter_user_turn(0)
        self.assertEqual(C4State.X, game.get_turn())

    def test_get_bad_free_row(self):
        game = Connect4()

        # bad row
        self.assertEqual(-1, game.get_free_row(-1))
        # bad type
        self.assertEqual(-1, game.get_free_row("yes"))
        self.assertEqual(-1, game.get_free_row(Connect4.MAX_COLS))

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
                free_row = game.get_free_row(col)

                self.assertEqual(Connect4.MAX_ROWS - row - 1,
                                 free_row)

                game.current_history[free_row][col] = C4State.X

        # no empty slot should be left
        for row in game.current_history:
            self.assertFalse(C4State.E in row)

        for col in range(Connect4.MAX_COLS):
            self.assertEqual(-1, game.get_free_row(col))

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

    def test_check_win_cols_invalid(self):
        game = Connect4()

        for idx in range(Connect4.MAX_ROWS - 3):
            game.current_history[idx+1].pop()
            game.current_history[idx+1].insert(0, C4State.X)

        # skip one row so looks like transpose([x, x, x, -, x])
        game.current_history[5][0] = C4State.X

        for _ in range(Connect4.MAX_COLS):
            self.assertFalse(game.check_win_cols())
            Connect4TestCase._shift_2d_array(game.current_history)

    def test_check_win_diag_down(self):
        game = Connect4()

        # from the top downwards
        for row in range(2):
            for idx in range(4):
                game.current_history[idx+row][idx+row] = C4State.X

            # shift right
            for _ in range(3):
                self.assertTrue(game.check_win_diag_down())
                Connect4TestCase._shift_2d_array(game.current_history)

            game.reset_game()

    def test_check_win_diag_down_invalid(self):
        game = Connect4()

        for row in range(2):
            for idx in range(3):
                game.current_history[idx+row][idx+row] = C4State.X

            game.current_history[4+row][4+row] = C4State.X

            # shift right
            for _ in range(3):
                self.assertFalse(game.check_win_diag_down())
                Connect4TestCase._shift_2d_array(game.current_history)

            game.reset_game()

    def test_check_win_diag_up(self):
        game = Connect4()

        for idx in range(2):
            col = 0
            for row in reversed(range(4)):
                game.current_history[row+idx][col+idx] = C4State.X
                col += 1

            for _ in range(3):
                self.assertTrue(game.check_win_diag_up())
                Connect4TestCase._shift_2d_array(game.current_history)

            game.reset_game()

    def test_check_win_diag_up_invalid(self):
        game = Connect4()

        for idx in range(2):
            col = 0
            for row in reversed(range(3)):
                game.current_history[row+idx][col+idx] = C4State.X
                col += 1

            game.current_history[4+idx][col+1] = C4State.X

            for _ in range(3):
                self.assertFalse(game.check_win_diag_up())
                Connect4TestCase._shift_2d_array(game.current_history)

            game.reset_game()

    def test_check_win(self):
        self.assertTrue(True)

    def test_check_guess_sequence_basic_moves(self):
        game = Connect4()

        self.assertFalse(game.enter_user_turn(0))
        self.assertEqual(game.current_history[Connect4.MAX_ROWS-1][0],
                         C4State.X)

        self.assertFalse(game.enter_user_turn(0))
        self.assertEqual(game.current_history[Connect4.MAX_ROWS-2][0],
                         C4State.O)

        self.assertFalse(game.enter_user_turn(1))
        self.assertEqual(game.current_history[Connect4.MAX_ROWS-1][1],
                         C4State.X)

        self.assertFalse(game.enter_user_turn(Connect4.MAX_COLS - 1))
        self.assertEqual(game.current_history[Connect4.MAX_ROWS-1]
                         [Connect4.MAX_COLS-1],
                         C4State.O)

    def test_check_guess_sequence_invalid_input(self):
        game = Connect4()

        self.assertFalse(game.enter_user_turn(-1))
        self.assertFalse(game.enter_user_turn("yes"))
        self.assertFalse(game.enter_user_turn(Connect4.MAX_COLS))

    def test_get_wins(self):
        game = Connect4()

        self.assertEqual({}, game.get_wins())

        game.entire_history = [
            ([[]], C4State.X),
            ([[]], C4State.X),
            ([[]], C4State.X),
            ([[]], C4State.X),
        ]

        wins = game.get_wins()

        self.assertEqual(4, wins[C4State.X.value])
        self.assertEqual(0, wins[C4State.O.value])

    def test_get_last_turn(self):
        game = Connect4()

        expected = []
        for row in Connect4.setup_board():
            expected.append([element.value for element in row])

        expected_str = Connect4TestCase._2d_to_str(expected)
        self.assertEqual(expected_str, game.get_last_turn())

        game.enter_user_turn(0)
        expected[Connect4.MAX_ROWS-1][0] = C4State.X.value
        expected_str = Connect4TestCase._2d_to_str(expected)

        self.assertEqual(expected_str, game.get_last_turn())

    def test_interactions(self):
        game = Connect4()

        self.assertFalse(game.enter_user_turn(2))

        self.assertEqual(game.get_turn(), C4State.O)
        self.assertFalse(game.enter_user_turn(3))
        self.assertFalse(game.enter_user_turn(3))
        self.assertFalse(game.enter_user_turn(3))
        self.assertFalse(game.enter_user_turn(3))

        self.assertEqual(game.get_turn(), C4State.O)
        self.assertFalse(game.enter_user_turn(5))
        self.assertFalse(game.enter_user_turn(4))
        self.assertFalse(game.enter_user_turn(5))
        self.assertFalse(game.enter_user_turn(4))
        self.assertFalse(game.enter_user_turn(5))
        self.assertFalse(game.enter_user_turn(4))

        self.assertEqual(game.get_turn(), C4State.O)
        self.assertFalse(game.enter_user_turn(4))
        self.assertTrue(game.enter_user_turn(5))

        expected = [
            [C4State.E] * Connect4.MAX_COLS,
            [C4State.E] * Connect4.MAX_COLS,

            [C4State.E, C4State.E, C4State.E, C4State.X,
             C4State.O, C4State.X, C4State.E],

            [C4State.E, C4State.E, C4State.E, C4State.O,
             C4State.X, C4State.O, C4State.E],

            [C4State.E, C4State.E, C4State.E, C4State.X,
             C4State.X, C4State.O, C4State.E],

            [C4State.E, C4State.E, C4State.X, C4State.O,
             C4State.X, C4State.O, C4State.E]
        ]

        self.assertEqual(1, len(game.entire_history))
        self.assertEqual(expected, game.entire_history[0][0])
        self.assertEqual(C4State.X, game.entire_history[0][1])
        self.assertEqual({C4State.X.value: 1, C4State.O.value: 0},
                         game.get_wins())


if __name__ == "__main__":
    unittest.main()
