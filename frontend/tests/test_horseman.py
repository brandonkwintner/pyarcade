from pyarcade.horseman import Horseman
import unittest


class HorsemanTestCase(unittest.TestCase):
    def test_game_construction(self):
        game = Horseman()

        self.assertEqual(6, game.num_guesses_left)
        self.assertFalse(game.game_over)

    def test_enter_user_turn(self):
        game = Horseman()

        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        result = game.enter_user_turn("h")
        correct_word = ['h', '_', '_', '_', '_']

        self.assertEqual(correct_word, game.current_word)
        self.assertFalse(result)

    def test_enter_user_turn_two_letters(self):
        game = Horseman()

        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        result = game.enter_user_turn("l")
        correct_word = ['_', '_', 'l', 'l', '_']

        self.assertEqual(correct_word, game.current_word)
        self.assertFalse(result)

    def test_get_last_turn(self):
        game = Horseman()

        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        game.enter_user_turn("l")

        self.assertEqual(("__ll_", False), game.get_last_turn())

        game.enter_user_turn("h")

        self.assertEqual(("h_ll_", False), game.get_last_turn())

    def test_player_winning(self):
        game = Horseman()

        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        result1 = game.enter_user_turn("l")
        self.assertFalse(result1)
        result2 = game.enter_user_turn("h")
        self.assertFalse(result2)
        result3 = game.enter_user_turn("e")
        self.assertFalse(result3)
        result4 = game.enter_user_turn("o")
        self.assertTrue(result4)
        self.assertEqual(game.word, game.current_word)

    def test_player_losing(self):
        game = Horseman()
        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        game.num_guesses_left = 1

        result = game.enter_user_turn("r")

        self.assertTrue(game.game_over)
        self.assertTrue(result)

    def test_clear_game(self):
        game = Horseman()
        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        game.num_guesses_left = 1

        result = game.enter_user_turn("r")

        self.assertTrue(game.game_over)
        self.assertTrue(result)

        game.clear_game()

        self.assertEqual(0, len(game.entire_history))
        self.assertEqual(0, len(game.entire_history))

    def test_reset_game(self):
        game = Horseman()
        game.word = ['h', 'e', 'l', 'l', 'o']
        game.current_word = ['_', '_', '_', '_', '_']
        game.num_guesses_left = 1

        result = game.enter_user_turn("r")
        initial_word = game.word

        self.assertTrue(game.game_over)
        self.assertTrue(result)

        game.reset_game()

        self.assertEqual(0, len(game.current_history))
        self.assertNotEqual(initial_word, game.word)
