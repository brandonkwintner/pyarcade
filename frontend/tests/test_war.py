from pyarcade.war import War, Ranks
from pyarcade.cards import Suits

import unittest
import re


class WarTestCase(unittest.TestCase):

    def test_new_game(self):
        game = War()
        self.assertEqual(26, len(game.player_one_hand))
        self.assertEqual(26, len(game.player_two_hand))
        self.assertEqual(0, game.last_turn_winner)

    def test_reset_game(self):
        game = War()
        for i in range(0, 3):
            game.play_turn([])
        game.reset_game()
        self.assertEqual(26, len(game.player_one_hand))
        self.assertEqual(26, len(game.player_two_hand))
        self.assertEqual(0, game.last_turn_winner)
        self.assertEqual(0, len(game.current_history))

    def test_clear_game(self):
        game = War()
        for _ in range(0, 3):
            for _ in range(0, 3):
                game.play_turn([])
            game.reset_game()
        game.clear_game()
        self.assertEqual(26, len(game.player_one_hand))
        self.assertEqual(26, len(game.player_two_hand))
        self.assertEqual(0, game.last_turn_winner)
        self.assertEqual(0, len(game.entire_history))

    def test_play_turn_player_one_wins_turn(self):
        game = War()
        game.player_one_hand[0] = (Ranks.THREE, Suits.DIAMONDS)
        game.player_two_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertTrue(turn)
        self.assertEqual(27, len(game.player_one_hand))
        self.assertEqual(25, len(game.player_two_hand))
        self.assertEqual(1, game.last_turn_winner)

    def test_play_turn_player_two_wins_turn(self):
        game = War()
        game.player_one_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        game.player_two_hand[0] = (Ranks.THREE, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertTrue(turn)
        self.assertEqual(25, len(game.player_one_hand))
        self.assertEqual(27, len(game.player_two_hand))
        self.assertEqual(2, game.last_turn_winner)

    def test_play_turn_war_occurs(self):
        game = War()
        game.player_one_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        game.player_two_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        game.player_one_hand[4] = (Ranks.FIVE, Suits.DIAMONDS)
        game.player_two_hand[4] = (Ranks.FOUR, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertTrue(turn)
        self.assertEqual(31, len(game.player_one_hand))
        self.assertEqual(21, len(game.player_two_hand))
        self.assertEqual(1, game.last_turn_winner)

    def test_play_turn_player_one_wins_game(self):
        game = War()
        game.player_one_hand = [(Ranks.THREE, Suits.DIAMONDS)]
        game.player_two_hand = [(Ranks.TWO, Suits.DIAMONDS)]
        turn = game.play_turn([])
        self.assertFalse(turn)
        self.assertEqual(2, len(game.player_one_hand))
        self.assertEqual(0, len(game.player_two_hand))
        self.assertEqual(1, game.last_turn_winner)

    def test_play_turn_player_two_wins_game(self):
        game = War()
        game.player_one_hand = [(Ranks.TWO, Suits.DIAMONDS)]
        game.player_two_hand = [(Ranks.THREE, Suits.DIAMONDS)]
        turn = game.play_turn([])
        self.assertFalse(turn)
        self.assertEqual(0, len(game.player_one_hand))
        self.assertEqual(2, len(game.player_two_hand))
        self.assertEqual(2, game.last_turn_winner)

    def test_play_turn_player_one_wins_post_war(self):
        game = War()
        player_two_hand = [(Ranks.TWO, Suits.CLUBS), (Ranks.THREE, Suits.CLUBS),
                           (Ranks.FOUR, Suits.CLUBS), (Ranks.FIVE, Suits.CLUBS)]
        game.player_two_hand = player_two_hand
        game.player_one_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertFalse(turn)
        self.assertEqual(0, len(game.player_two_hand))
        self.assertEqual(1, game.last_turn_winner)

    def test_play_turn_player_two_wins_post_war(self):
        game = War()
        player_one_hand = [(Ranks.TWO, Suits.CLUBS), (Ranks.THREE, Suits.CLUBS),
                           (Ranks.FOUR, Suits.CLUBS), (Ranks.FIVE, Suits.CLUBS)]
        game.player_one_hand = player_one_hand
        game.player_two_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertFalse(turn)
        self.assertEqual(0, len(game.player_one_hand))
        self.assertEqual(2, game.last_turn_winner)

    def test_play_turn_player_one_wins_mid_war(self):
        game = War()
        player_two_hand = [(Ranks.TWO, Suits.CLUBS), (Ranks.THREE, Suits.CLUBS),
                           (Ranks.FOUR, Suits.CLUBS)]
        game.player_two_hand = player_two_hand
        game.player_one_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertFalse(turn)
        self.assertEqual(0, len(game.player_two_hand))
        self.assertEqual(1, game.last_turn_winner)

    def test_play_turn_player_two_wins_mid_war(self):
        game = War()
        player_one_hand = [(Ranks.TWO, Suits.CLUBS), (Ranks.THREE, Suits.CLUBS),
                           (Ranks.FOUR, Suits.CLUBS)]
        game.player_one_hand = player_one_hand
        game.player_two_hand[0] = (Ranks.TWO, Suits.DIAMONDS)
        turn = game.play_turn([])
        self.assertFalse(turn)
        self.assertEqual(0, len(game.player_one_hand))
        self.assertEqual(2, game.last_turn_winner)

    def test_update_current_history(self):
        game = War()
        game.play_turn([])
        self.assertEqual(1, len(game.current_history))

    def test_update_entire_history(self):
        game = War()
        game.play_turn([])
        game.update_entire_history()
        self.assertEqual(1, len(game.entire_history))

    def test_enter_user_turn_returns_true(self):
        game = War()
        turn = game.enter_user_turn("Flip Card")
        self.assertTrue(turn)

    def test_enter_user_turn_returns_false(self):
        game = War()
        game.player_one_hand = [(Ranks.TWO, Suits.DIAMONDS)]
        game.player_two_hand = [(Ranks.THREE, Suits.DIAMONDS)]
        turn = game.enter_user_turn("Flip Card")
        self.assertFalse(turn)
        self.assertEqual(1, len(game.entire_history))

    def test_get_last_turn(self):
        game = War()
        game.player_one_hand = [(Ranks.TWO, Suits.DIAMONDS),
                                (Ranks.THREE, Suits.DIAMONDS)]
        game.player_two_hand = [(Ranks.THREE, Suits.DIAMONDS),
                                (Ranks.FOUR, Suits.DIAMONDS)]
        results = game.get_last_turn()
        player_one_card = results[0]
        player_two_card = results[1]
        player_one_card_count = results[2]
        player_two_card_count = results[3]
        game_over = results[4]
        last_turn_winner = results[5]
        self.assertEqual("TWO", player_one_card)
        self.assertEqual("THREE", player_two_card)
        self.assertEqual(2, player_one_card_count)
        self.assertEqual(2, player_two_card_count)
        self.assertFalse(game_over)
        self.assertEqual(0, last_turn_winner) # Since no turn was played yet.

    def test_regex_pattern(self):
        pattern = War.get_regex_pattern()
        regex = re.compile(pattern)
        self.assertTrue(regex.match("flip card"))
        self.assertFalse(regex.match("Hello"))


if __name__ == "__main__":
    unittest.main()
