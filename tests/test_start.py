from pyarcade.start import run_pyarcade
import unittest


class StartTestCase(unittest.TestCase):
    def test_run_pyarcade(self):
        # Pass for now
        self.assertIsNone(run_pyarcade())


if __name__ == "__main__":
    unittest.main()
