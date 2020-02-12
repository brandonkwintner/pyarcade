from pyarcade.input_system import InputSystem
from pyarcade.eval_input import Evaluation
import unittest


class InputSystemTestCase(unittest.TestCase):
    def test_init(self):
        in_sys = InputSystem()

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game, 1)
        self.assertIsNotNone(in_sys.mastermind)

    def test_make_guess(self):
        in_sys = InputSystem()

        current_seq = in_sys.mastermind.gen_sequence
        # purposely make an incorrect guess
        guess = [x+1 for x in current_seq]

        self.assertFalse(in_sys.make_guess(guess))

        self.assertEqual(in_sys.game, 1)

        self.assertTrue(in_sys.make_guess(current_seq))

        self.assertEqual(in_sys.round, 1)

    def test_reset(self):
        in_sys = InputSystem()

        in_sys.round = 100
        old_sequence = in_sys.mastermind.gen_sequence

        in_sys.reset()

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game, 1)
        self.assertIsNot(old_sequence, in_sys.mastermind.gen_sequence)

    def test_clear(self):
        in_sys = InputSystem()

        in_sys.make_guess([1, 2, 3, 4])

        self.assertEqual(len(in_sys.mastermind.current_history), 1)

        in_sys.clear()

        self.assertEqual(len(in_sys.mastermind.current_history), 0)
        self.assertEqual(len(in_sys.mastermind.entire_history), 0)

    def test_guess_take_input(self):
        in_sys = InputSystem()

        custom_seq = [1, 2, 3, 4]
        in_sys.mastermind.gen_sequence = custom_seq

        win, valid = in_sys.take_input("1 5 4 3")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 2)
        self.assertEqual(in_sys.game, 1)

        # correct sequence
        win, valid = in_sys.take_input("1 2 3 4")

        self.assertTrue(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game, 2)

    def test_reset_take_input(self):
        in_sys = InputSystem()

        # invalid sequence assignment (since only >= 0 will be created).
        in_sys.mastermind.gen_sequence = [-1, -1, -1, -1]
        old_seq = in_sys.mastermind.gen_sequence

        win, valid = in_sys.take_input("reset")

        self.assertFalse(win)
        self.assertTrue(valid)

        self.assertEqual(in_sys.round, 1)
        self.assertNotEqual(in_sys.mastermind.gen_sequence, old_seq)

    def test_get_last_guess(self):
        in_sys = InputSystem()

        self.assertEqual([], in_sys.get_last_guess())

        in_sys.mastermind.gen_sequence = [1, 2, 3, 4]
        in_sys.make_guess([1, 5, 4, 3])

        expected = [(1, Evaluation.CORRECT.value),
                    (5, Evaluation.INCORRECT.value),
                    (4, Evaluation.SOMEWHERE.value),
                    (3, Evaluation.SOMEWHERE.value)]

        self.assertEqual(expected, in_sys.get_last_guess())

    def test_clear_take_input(self):
        in_sys = InputSystem()

        in_sys.mastermind.gen_sequence = [-1, -1, -1, -1]
        old_seq = in_sys.mastermind.gen_sequence

        win, valid = in_sys.take_input("clear")

        self.assertFalse(win)
        self.assertTrue(valid)

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game, 1)
        self.assertEqual(in_sys.get_last_guess(), [])
        self.assertNotEqual(in_sys.mastermind.gen_sequence, old_seq)

    def test_correct_take_input_many(self):
        in_sys = InputSystem()

        custom_seq = [1, 2, 3, 4]
        in_sys.mastermind.gen_sequence = custom_seq

        win, valid = in_sys.take_input("1 5 4 3")

        self.assertFalse(win)
        self.assertTrue(valid)
        self.assertEqual(in_sys.round, 2)
        self.assertEqual(in_sys.game, 1)

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

        in_sys.mastermind.gen_sequence = custom_seq
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
