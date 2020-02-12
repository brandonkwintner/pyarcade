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


if __name__ == "__main__":
    unittest.main()
