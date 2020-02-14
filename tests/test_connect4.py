from pyarcade.connect4 import Connect4
from pyarcade.connect4_states import C4State
import unittest


class Connect4TestCase(unittest.TestCase):
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

        # self.assertEqual(C4State.O, game.get_turn())


if __name__ == "__main__":
    unittest.main()
