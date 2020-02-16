from pyarcade.input_system import InputSystem
from pyarcade.eval_input import Evaluation
from pyarcade.game_option import Game
from pyarcade.mastermind import Mastermind
from pyarcade.connect4 import Connect4
from pyarcade.connect4_states import C4State
import unittest


class InputSystemTestCase(unittest.TestCase):
    def test_init_mastermind(self):
        in_sys = InputSystem()

        self.assertTrue(isinstance(in_sys.game, Mastermind))
        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game_num, 1)

    def test_init_c4(self):
        in_sys = InputSystem(Game.CONNECT4)

        self.assertTrue(isinstance(in_sys.game, Connect4))
        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game_num, 1)

    def test_make_guess_mastermind(self):
        in_sys = InputSystem()

        current_seq = in_sys.game.gen_sequence
        # purposely make an incorrect guess
        guess = [x+1 for x in current_seq]

        self.assertFalse(in_sys.make_guess_for_mastermind(guess))

        self.assertEqual(in_sys.game_num, 1)

        self.assertTrue(in_sys.make_guess_for_mastermind(current_seq))

        self.assertEqual(in_sys.round, 1)

    def test_make_guess_c4(self):
        in_sys = InputSystem(Game.CONNECT4)

        # TODO
        self.assertTrue(True)

    def test_reset_mastermind(self):
        in_sys = InputSystem()

        in_sys.round = 100
        old_sequence = in_sys.game.gen_sequence

        in_sys.reset()

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game_num, 1)
        self.assertIsNot(old_sequence, in_sys.game.gen_sequence)

    def test_reset_c4(self):
        in_sys = InputSystem(Game.CONNECT4)

        in_sys.round = 100
        in_sys.game.current_history = []

        in_sys.reset()

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game_num, 1)
        self.assertIsNot(Connect4.setup_board(), in_sys.game.current_history)

    def test_clear_mastermind(self):
        in_sys = InputSystem()

        in_sys.make_guess_for_mastermind([1, 2, 3, 4])

        self.assertEqual(len(in_sys.game.current_history), 1)

        in_sys.clear()

        self.assertEqual(len(in_sys.game.current_history), 0)
        self.assertEqual(len(in_sys.game.entire_history), 0)

    def test_clear_c4(self):
        in_sys = InputSystem(Game.CONNECT4)

        self.assertFalse(in_sys.make_guess_for_connect4([0]))

        in_sys.clear()

        self.assertEqual(in_sys.game.current_history, Connect4.setup_board())
        self.assertEqual(len(in_sys.game.entire_history), 0)

    def test_guess_take_input_mastermind(self):
        in_sys = InputSystem()

        custom_seq = [1, 2, 3, 4]
        in_sys.game.gen_sequence = custom_seq

        win, valid = in_sys.take_input("1 5 4 3")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 2)
        self.assertEqual(in_sys.game_num, 1)

        # correct sequence
        win, valid = in_sys.take_input("1 2 3 4")

        self.assertTrue(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game_num, 2)

    def test_guess_take_input_c4(self):
        in_sys = InputSystem(Game.CONNECT4)

#todo
        # self.assertEqual(f"Player {C4State.X.value}", in_sys.get_round_info())
        win, valid = in_sys.take_input("1")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 2)
        self.assertEqual(in_sys.game_num, 1)

        # correct sequence
        win, valid = in_sys.take_input("1 2 3 4")

        self.assertFalse(win)
        self.assertFalse(valid)

    def test_reset_take_input(self):
        in_sys = InputSystem()

        # invalid sequence assignment (since only >= 0 will be created).
        in_sys.game.gen_sequence = [-1, -1, -1, -1]
        old_seq = in_sys.game.gen_sequence

        win, valid = in_sys.take_input("reset")

        self.assertFalse(win)
        self.assertTrue(valid)

        self.assertEqual(in_sys.round, 1)
        self.assertNotEqual(in_sys.game.gen_sequence, old_seq)

    def test_get_last_guess(self):
        in_sys = InputSystem()

        self.assertEqual([], in_sys.get_last_guess())

        in_sys.game.gen_sequence = [1, 2, 3, 4]
        in_sys.make_guess_for_mastermind([1, 5, 4, 3])

        expected = [(1, Evaluation.CORRECT.value),
                    (5, Evaluation.INCORRECT.value),
                    (4, Evaluation.SOMEWHERE.value),
                    (3, Evaluation.SOMEWHERE.value)]

        self.assertEqual(expected, in_sys.get_last_guess())

    def test_clear_take_input(self):
        in_sys = InputSystem()

        in_sys.game.gen_sequence = [-1, -1, -1, -1]
        old_seq = in_sys.game.gen_sequence

        win, valid = in_sys.take_input("clear")

        self.assertFalse(win)
        self.assertTrue(valid)

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game_num, 1)
        self.assertEqual(in_sys.get_last_guess(), [])
        self.assertNotEqual(in_sys.game.gen_sequence, old_seq)

    def test_correct_take_input_many(self):
        in_sys = InputSystem()

        custom_seq = [1, 2, 3, 4]
        in_sys.game.gen_sequence = custom_seq

        win, valid = in_sys.take_input("1 5 4 3")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 2)
        self.assertEqual(in_sys.game_num, 1)

        expected_last_guess = [(1, Evaluation.CORRECT.value),
                               (5, Evaluation.INCORRECT.value),
                               (4, Evaluation.SOMEWHERE.value),
                               (3, Evaluation.SOMEWHERE.value)]

        self.assertEqual(expected_last_guess, in_sys.get_last_guess())

        win, valid = in_sys.take_input("clear")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.get_last_guess(), [])

        win, valid = in_sys.take_input("reset")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.get_last_guess(), [])

        in_sys.game.gen_sequence = custom_seq
        win, valid = in_sys.take_input("1 2 3 4")

        self.assertTrue(win)
        self.assertTrue(valid)

    def test_incorrect_take_input(self):
        in_sys = InputSystem()

        win, valid = in_sys.take_input("someBadInput")
        self.assertFalse(win)
        self.assertFalse(valid)

        win, valid = in_sys.take_input("1 -1 1 1")
        self.assertFalse(win)
        self.assertFalse(valid)

        win, valid = in_sys.take_input("1 1 1")
        self.assertFalse(win)
        self.assertFalse(valid)

        win, valid = in_sys.take_input("10 1 1 1")
        self.assertFalse(win)
        self.assertFalse(valid)

        win, valid = in_sys.take_input("1 1 clear 1")
        self.assertFalse(win)
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
