from pyarcade.input_system import InputSystem
import unittest


class InputSystemTestCase(unittest.TestCase):
    def test_init(self):
        in_sys = InputSystem()

        self.assertEqual(in_sys.round, 1)
        self.assertEqual(in_sys.game, 1)
        self.assertIsNotNone(in_sys.mastermind)
