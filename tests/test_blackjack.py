from pyarcade.blackjack import Blackjack
from pyarcade.cards import Ranks, Suits

import unittest
import copy


class BlackJackTestCase(unittest.TestCase):
    def test_create_deck(self):
        game = Blackjack()
        self.assertEqual(52, len(game.deck_of_cards))

    def test_shuffle(self):
        game = Blackjack()

        for _ in range(10):
            deck = copy.deepcopy(game.shuffle_deck())
            deck_2 = copy.deepcopy(game.shuffle_deck())
            self.assertNotEqual(deck, deck_2)

    def test_reshuffle_deck(self):
        game = Blackjack()
        game.deck_of_cards = [(Ranks.Ace, Suits.Diamonds)]
        self.assertEqual(1, len(game.deck_of_cards))
        game.hit()
        self.assertEqual(0, len(game.deck_of_cards))
        game.hit()
        self.assertEqual(51, len(game.deck_of_cards))

    def test_draw_card(self):
        game = Blackjack()

        for _ in range(10):
            card = game.deck_of_cards[0]
            self.assertEqual(card, game.hit())

    def test_player_draw(self):
        game = Blackjack()
        self.assertEqual(0, len(game.player_hand))
        game.player_draw()
        self.assertEqual(1, len(game.player_hand))
        game.player_draw()
        self.assertEqual(2, len(game.player_hand))

    def test_player_draw_limits(self):
        game = Blackjack()
        card_1 = (Ranks.Nine, Suits.Diamonds)
        card_2 = (Ranks.Queen, Suits.Diamonds)
        card_3 = (Ranks.Two, Suits.Diamonds)

        game.player_hand = [card_1, card_2, card_3]
        self.assertTrue(game.player_draw())
        self.assertFalse(game.player_draw())

    def test_dealer_draw(self):
        game = Blackjack()

        for _ in range(10):
            game.dealer_hand = []
            self.assertEqual(0, len(game.dealer_hand))
            game.npc_draw(game.dealer_hand)
            dealer_value = game.evaluate_hand(game.dealer_hand)
            self.assertGreaterEqual(dealer_value, game.NPC_STOP_LIMIT)

    def test_calculate_hand(self):
        game = Blackjack()
        card_1 = (Ranks.Ace, Suits.Clubs)
        card_2 = (Ranks.Five, Suits.Clubs)
        card_3 = (Ranks.Ten, Suits.Diamonds)

        player = [card_1, card_2]
        self.assertEqual(16, game.evaluate_hand(player))
        player = [card_1, card_3]
        self.assertEqual(21, game.evaluate_hand(player))
        player = [card_3, card_2]
        self.assertEqual(15, game.evaluate_hand(player))
        player = [card_3, card_3, card_3]
        self.assertEqual(30, game.evaluate_hand(player))

    def test_changing_ace_to_one(self):
        game = Blackjack()
        card_1 = (Ranks.Five, Suits.Clubs)
        card_2 = (Ranks.Ace, Suits.Clubs)
        card_2_change = (Ranks.One, Suits.Clubs)
        card_3 = (Ranks.Ten, Suits.Diamonds)

        player = [card_1, card_2, card_3]
        player_change = [card_1, card_2_change, card_3]

        game.change_ace_to_one(player)

        self.assertEqual(player_change, player)

    def test_evaluate_change(self):
        game = Blackjack()
        card_1 = (Ranks.Five, Suits.Clubs)
        card_2 = (Ranks.Ace, Suits.Clubs)
        card_2_change = (Ranks.One, Suits.Clubs)
        card_3 = (Ranks.Ten, Suits.Diamonds)

        player = [card_1, card_2, card_3]
        player_change = [card_1, card_2_change, card_3]

        game.evaluate_hand(player)
        self.assertEqual(player_change, player)

    def test_winner(self):
        game = Blackjack()
        card_lose_1 = (Ranks.Five, Suits.Clubs)
        card_lose_2 = (Ranks.Ace, Suits.Clubs)
        card_win_1 = (Ranks.Ten, Suits.Diamonds)
        card_win_2 = (Ranks.Jack, Suits.Clubs)
        card_bust = (Ranks.Ten, Suits.Diamonds)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_1, card_win_2]
        winner = game.calculate_winner()
        self.assertEqual("Dealer Win", winner)

        game.player_hand = [card_win_1, card_win_2]
        game.dealer_hand = [card_lose_1, card_lose_2]
        winner = game.calculate_winner()
        self.assertEqual("Player Win", winner)

        game.player_hand = [card_win_1, card_win_2, card_bust]
        game.dealer_hand = [card_lose_1, card_lose_2]
        winner = game.calculate_winner()
        self.assertEqual("Dealer Win", winner)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_1, card_win_2, card_bust]
        winner = game.calculate_winner()
        self.assertEqual("Player Win", winner)

    def test_history(self):
        game = Blackjack()
        game.start_game()
        card_1 = (Ranks.One, Suits.Clubs)
        self.assertEqual(len(game.history), 1)

        game.player_hand = [card_1, card_1]
        game.player_draw()
        self.assertEqual(len(game.history), 2)

        game.player_hand = [card_1, card_1, card_1]
        game.player_draw()
        self.assertEqual(len(game.history), 3)

    def test_complete_history(self):
        game = Blackjack()

        card_lose_1 = (Ranks.Nine, Suits.Clubs)
        card_lose_2 = (Ranks.Ten, Suits.Clubs)
        card_win_3 = (Ranks.Ten, Suits.Diamonds)
        card_win_4 = (Ranks.Jack, Suits.Clubs)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_3, card_win_4]
        game.stand()
        self.assertEqual(len(game.complete_history), 1)
        self.assertEqual(game.complete_history[0][0], "Dealer Win")

        game.player_hand = [card_win_3, card_win_4]
        game.dealer_hand = [card_lose_1, card_lose_2]
        game.stand()
        self.assertEqual(len(game.complete_history), 2)
        self.assertEqual(game.complete_history[1][0], "Player Win")

        game.clear_all()
        self.assertEqual(len(game.complete_history), 0)
