from pyarcade.go_fish import GoFish
from pyarcade.cards import Ranks, Suits

import unittest
import copy


class GoFishTestCase(unittest.TestCase):
    def test_game_construction(self):
        game = GoFish()
        self.assertEqual(5, len(game.player_one_hand))
        self.assertEqual(5, len(game.computer_hand))
        self.assertEqual(42, len(game.deck_of_cards))
        self.assertFalse(game.has_won)

    def test_shuffle(self):
        game = GoFish()

        for _ in range(10):
            deck = copy.deepcopy(game.shuffle_deck())
            deck_2 = copy.deepcopy(game.shuffle_deck())
            self.assertNotEqual(deck, deck_2)

    def test_enter_user_turn_valid(self):
        game = GoFish()

        game.enter_user_turn("Jack")
        self.assertEqual(6, len(game.player_one_hand))

    def test_enter_user_turn_invalid(self):
        game = GoFish()

        result = game.enter_user_turn("Joker")
        self.assertFalse(result)
        self.assertEqual(5, len(game.player_one_hand))

    def test_check_for_winner(self):
        hand_1 = [(Ranks.ACE, Suits.DIAMONDS), (Ranks.ACE, Suits.CLUBS),
                  (Ranks.ACE, Suits.HEARTS), (Ranks.ACE, Suits.SPADES)]
        hand_2 = [(Ranks.ACE, Suits.DIAMONDS), (Ranks.ACE, Suits.CLUBS),
                  (Ranks.ACE, Suits.HEARTS), (Ranks.KING, Suits.SPADES)]

        self.assertTrue(GoFish.check_for_winner(hand_1))
        self.assertFalse(GoFish.check_for_winner(hand_2))

    def test_reset_game(self):
        game = GoFish()

        for i in range(5):
            game.current_history.append("Winner")

        game.reset_game()

        self.assertEqual(5, len(game.player_one_hand))
        self.assertEqual(5, len(game.computer_hand))
        self.assertEqual(0, len(game.current_history))

    def test_clear_game(self):
        game = GoFish()

        for i in range(5):
            game.current_history.append("Winner")
            game.entire_history.append("Winner")

        game.clear_game()

        self.assertEqual(5, len(game.player_one_hand))
        self.assertEqual(5, len(game.computer_hand))
        self.assertEqual(0, len(game.current_history))
        self.assertEqual(0, len(game.entire_history))

    def test_getting_a_winner(self):
        game = GoFish()

        game.player_one_hand = [(Ranks.ACE, Suits.SPADES), (Ranks.ACE, Suits.HEARTS), (Ranks.ACE, Suits.CLUBS),
                                (Ranks.EIGHT, Suits.CLUBS), (Ranks.NINE, Suits.DIAMONDS)]
        game.computer_hand = [(Ranks.FIVE, Suits.SPADES), (Ranks.FOUR, Suits.HEARTS), (Ranks.FOUR, Suits.CLUBS),
                              (Ranks.SEVEN, Suits.DIAMONDS), (Ranks.ACE, Suits.DIAMONDS)]

        result = game.enter_user_turn("Ace")

        self.assertTrue(result)
        self.assertEqual(6, len(game.player_one_hand))
        self.assertEqual(4, len(game.computer_hand))

    def test_getting_a_winner2(self):
        game = GoFish()

        game.player_one_hand = [(Ranks.ACE, Suits.SPADES), (Ranks.ACE, Suits.HEARTS), (Ranks.THREE, Suits.CLUBS),
                                (Ranks.EIGHT, Suits.CLUBS), (Ranks.NINE, Suits.DIAMONDS)]
        game.computer_hand = [(Ranks.FIVE, Suits.SPADES), (Ranks.FOUR, Suits.HEARTS), (Ranks.FOUR, Suits.CLUBS),
                              (Ranks.ACE, Suits.CLUBS), (Ranks.ACE, Suits.DIAMONDS)]

        result = game.enter_user_turn("Ace")

        self.assertTrue(result)
        self.assertEqual(7, len(game.player_one_hand))
        self.assertEqual(3, len(game.computer_hand))
