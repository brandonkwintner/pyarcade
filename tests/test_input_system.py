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


if __name__ == "__main__":
    unittest.main()
