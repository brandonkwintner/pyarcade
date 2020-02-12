from pyarcade.mastermind import Mastermind
from pyarcade.eval_input import Evaluation
import unittest


class MastermindTestCase(unittest.TestCase):
    def test_generate_random_sequence(self):
        game = Mastermind()
        self.assertEqual(len(game.generate_hidden_sequence()), 4)

    def test_regular_init(self):
        game = Mastermind()

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 0)

    def test_all_incorrect_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [1, 2, 3, 4]
        guess = [5, 5, 5, 5]

        self.assertFalse(game.guess_sequence(guess))

        self.assertEqual(len(game.current_history), 1)

        actual = game.current_history[0]
        expected = [(5, Evaluation.INCORRECT)] * 4

        self.assertEqual(actual, expected)

    def test_all_correct_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [5] * 4
        guess = game.gen_sequence

        self.assertTrue(game.guess_sequence(guess))

        self.assertEqual(len(game.current_history), 0)

        actual = game.entire_history[0][0]
        expected = [(5, Evaluation.CORRECT)] * 4

        self.assertEqual(actual, expected)

    def test_all_somewhere_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [4, 3, 2, 1]
        guess = [1, 2, 3, 4]

        game.guess_sequence(guess)

        self.assertEqual(len(game.current_history), 1)

        actual = game.current_history[0]
        expected = []

        for num in guess:
            expected.append((num, Evaluation.SOMEWHERE))

        self.assertEqual(actual, expected)

    def test_mixed_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [1, 2, 3, 4]
        guess = [1, 5, 4, 3]

        game.guess_sequence(guess)

        self.assertEqual(len(game.current_history), 1)

        actual = game.current_history[0]
        expected = [(1, Evaluation.CORRECT),
                    (5, Evaluation.INCORRECT),
                    (4, Evaluation.SOMEWHERE),
                    (3, Evaluation.SOMEWHERE)]

        self.assertEqual(actual, expected)

    def test_invalid_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [1, 2, 3, 4]
        over_range = [1, 5, 4, 10]
        under_range = [-1, -1, -1, -1]
        bad_type = [1, 5, 4, "1"]
        bad_len = []

        self.assertFalse(game.guess_sequence(over_range))
        self.assertFalse(game.guess_sequence(under_range))
        self.assertFalse(game.guess_sequence(bad_type))
        self.assertFalse(game.guess_sequence(bad_len))

    def test_correct_guess_entire_history(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [5] * 4
        guess = game.gen_sequence

        game.guess_sequence(guess)

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 1)

        actual = game.entire_history[0][0]
        expected = [(5, Evaluation.CORRECT)] * 4

        self.assertEqual(actual, expected)

    def test_multiple_guess_entire_history(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [5] * 4
        bad_guess = [1, 5, 3, 5]
        guess = game.gen_sequence

        game.guess_sequence(bad_guess)
        game.guess_sequence(guess)

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 1)

    def test_reset_game(self):
        game = Mastermind()

        game.generate_hidden_sequence()
        current_seq = game.gen_sequence

        self.assertTrue(game.guess_sequence(current_seq))

        self.assertNotEqual(current_seq, game.gen_sequence)
        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 1)

        game.reset_game()

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 1)

    def test_clear_game(self):
        game = Mastermind()

        game.generate_hidden_sequence()
        current_seq = game.gen_sequence

        self.assertTrue(game.guess_sequence(current_seq))

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 1)

        current_seq = game.gen_sequence
        game.clear_game()

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 0)
        self.assertNotEqual(current_seq, game.gen_sequence)

    def test_clear_history(self):
        game = Mastermind()

        game.generate_hidden_sequence()
        guess = [1, 2, 3, 4]

        game.guess_sequence(guess)

        self.assertEqual(len(game.current_history), 1)

        game.clear_history()

        self.assertEqual(len(game.current_history), 0)

    def test_clear_all_history(self):
        game = Mastermind()

        game.generate_hidden_sequence()
        current_seq = game.gen_sequence
        guess = [1, 2, 3, 4]

        game.guess_sequence(guess)

        self.assertEqual(len(game.current_history), 1)

        game.guess_sequence(current_seq)

        self.assertEqual(len(game.entire_history), 1)

        game.clear_all_history()

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 0)


if __name__ == "__main__":
    unittest.main()
