from pyarcade.mastermind import Mastermind
from pyarcade.eval_input import Evaluation
import unittest


class MastermindTestCase(unittest.TestCase):
    @staticmethod
    def _mastermind_array_to_str(array):
        result = ""

        for element in array:
            result += str(element[0]) + " : " + element[1] + "\n"

        return result

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

        self.assertFalse(game.enter_user_turn(guess))

        self.assertEqual(len(game.current_history), 1)

        actual = game.current_history[0]
        expected = [(5, Evaluation.INCORRECT)] * 4

        self.assertEqual(actual, expected)

    def test_all_correct_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [5] * 4
        guess = game.gen_sequence

        self.assertTrue(game.enter_user_turn(guess))

        self.assertEqual(len(game.current_history), 1)

    def test_all_somewhere_guess(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [4, 3, 2, 1]
        guess = [1, 2, 3, 4]

        game.enter_user_turn(guess)

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

        game.enter_user_turn(guess)

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

        self.assertFalse(game.enter_user_turn(over_range))
        self.assertFalse(game.enter_user_turn(under_range))
        self.assertFalse(game.enter_user_turn(bad_type))
        self.assertFalse(game.enter_user_turn(bad_len))

    def test_correct_guess_entire_history(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [5] * 4
        guess = game.gen_sequence

        game.enter_user_turn(guess)

        self.assertEqual(len(game.current_history), 1)
        self.assertEqual(len(game.entire_history), 1)

    def test_multiple_guess_entire_history(self):
        game = Mastermind()

        # create known sequence
        game.gen_sequence = [5] * 4
        bad_guess = [1, 5, 3, 5]
        guess = game.gen_sequence

        game.enter_user_turn(bad_guess)
        game.enter_user_turn(guess)

        self.assertEqual(len(game.current_history), 2)
        self.assertEqual(len(game.entire_history), 1)

    def test_reset_game(self):
        game = Mastermind()

        current_seq = game.gen_sequence

        self.assertTrue(game.enter_user_turn(current_seq))

        self.assertEqual(len(game.current_history), 1)
        self.assertEqual(len(game.entire_history), 1)

        game.reset_game()

        self.assertNotEqual(current_seq, game.gen_sequence)
        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 1)

    def test_clear_game(self):
        game = Mastermind()

        current_seq = game.gen_sequence

        self.assertTrue(game.enter_user_turn(current_seq))

        self.assertEqual(len(game.current_history), 1)
        self.assertEqual(len(game.entire_history), 1)

        current_seq = game.gen_sequence
        game.clear_game()

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 0)
        self.assertNotEqual(current_seq, game.gen_sequence)

    def test_clear_history(self):
        game = Mastermind()

        game.gen_sequence = [1, 1, 1, 1]
        guess = [1, 2, 3, 4]

        game.enter_user_turn(guess)

        self.assertEqual(len(game.current_history), 1)

        game.clear_history()

        self.assertEqual(len(game.current_history), 0)

    def test_clear_all_history(self):
        game = Mastermind()

        game.gen_sequence = [1, 1, 1, 1]
        current_seq = game.gen_sequence
        guess = [1, 2, 3, 4]

        game.enter_user_turn(guess)

        self.assertEqual(len(game.current_history), 1)

        game.enter_user_turn(current_seq)

        self.assertEqual(len(game.entire_history), 1)
        self.assertEqual(len(game.current_history), 2)

        game.clear_all_history()

        self.assertEqual(len(game.current_history), 0)
        self.assertEqual(len(game.entire_history), 0)

    def test_get_last_turn(self):
        game = Mastermind()

        self.assertEqual("", game.get_last_turn())

        game.gen_sequence = [1, 2, 3, 4]
        game.enter_user_turn([1, 3, 2, 5])

        expected = [(1, Evaluation.CORRECT.value),
                    (3, Evaluation.SOMEWHERE.value),
                    (2, Evaluation.SOMEWHERE.value),
                    (5, Evaluation.INCORRECT.value)]

        expected_str = MastermindTestCase._mastermind_array_to_str(expected)
        self.assertEqual(expected_str, game.get_last_turn())


if __name__ == "__main__":
    unittest.main()
