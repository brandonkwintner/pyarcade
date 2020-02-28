from pyarcade.blackjack import Blackjack
from pyarcade.cards import Ranks, Suits
from pyarcade.blackjack_players import BlackJackWinner

import unittest
import copy


class BlackJackTestCase(unittest.TestCase):
    @staticmethod
    def _hand_to_str(hand):
        hand_str = ""
        for card in hand:
            if card[0].name == Ranks.ONE.name:
                hand_str += "ACE, "
            else:
                hand_str += card[0].name + ", "
        return hand_str[:-2]

    def test_create_deck(self):
        game = Blackjack()
        self.assertEqual(52, len(game.generate_new_deck()))
        self.assertEqual(48, len(game.deck_of_cards))

    def test_shuffle(self):
        game = Blackjack()

        for _ in range(10):
            deck = copy.deepcopy(game.shuffle_deck())
            deck_2 = copy.deepcopy(game.shuffle_deck())
            self.assertNotEqual(deck, deck_2)

    def test_reshuffle_deck(self):
        game = Blackjack()
        game.deck_of_cards = [(Ranks.ACE, Suits.DIAMONDS)]
        self.assertEqual(1, len(game.deck_of_cards))
        game.hit()
        self.assertEqual(0, len(game.deck_of_cards))
        game.hit()
        self.assertEqual(51, len(game.deck_of_cards))

    def test_enter_input_valid(self):
        game = Blackjack()
        game.player_hand = []

        self.assertFalse(game.enter_user_turn("hit"))
        self.assertEqual(len(game.player_hand), 1)
        self.assertTrue(game.enter_user_turn("stand"))

    def test_enter_input_invalid(self):
        game = Blackjack()
        game.player_hand = []

        self.assertFalse(game.enter_user_turn("hi t"))
        self.assertEqual(len(game.player_hand), 0)
        self.assertFalse(game.enter_user_turn("123"))
        self.assertFalse(game.enter_user_turn("fail"))

    def test_draw_card(self):
        game = Blackjack()

        for _ in range(10):
            card = game.deck_of_cards[0]
            self.assertEqual(card, game.hit())

    def test_player_draw(self):
        game = Blackjack()
        game.player_hand = []
        self.assertEqual(0, len(game.player_hand))
        game.player_draw()
        self.assertEqual(1, len(game.player_hand))
        game.player_draw()
        self.assertEqual(2, len(game.player_hand))

    def test_player_draw_limits(self):
        game = Blackjack()
        card_1 = (Ranks.NINE, Suits.DIAMONDS)
        card_2 = (Ranks.QUEEN, Suits.DIAMONDS)
        card_3 = (Ranks.TWO, Suits.DIAMONDS)

        game.player_hand = [card_1, card_2, card_3]
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
        card_1 = (Ranks.ACE, Suits.CLUBS)
        card_2 = (Ranks.FIVE, Suits.CLUBS)
        card_3 = (Ranks.TEN, Suits.DIAMONDS)

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
        card_1 = (Ranks.FIVE, Suits.CLUBS)
        card_2 = (Ranks.ACE, Suits.CLUBS)
        card_2_change = (Ranks.ONE, Suits.CLUBS)
        card_3 = (Ranks.TEN, Suits.DIAMONDS)

        player = [card_1, card_2, card_3]
        player_change = [card_1, card_2_change, card_3]

        game.change_ace_to_one(player)

        self.assertEqual(player_change, player)

    def test_evaluate_change(self):
        game = Blackjack()
        card_1 = (Ranks.FIVE, Suits.CLUBS)
        card_2 = (Ranks.ACE, Suits.CLUBS)
        card_2_change = (Ranks.ONE, Suits.CLUBS)
        card_3 = (Ranks.TEN, Suits.DIAMONDS)

        player = [card_1, card_2, card_3]
        player_change = [card_1, card_2_change, card_3]

        game.evaluate_hand(player)
        self.assertEqual(player_change, player)

    def test_winner(self):
        game = Blackjack()
        card_lose_1 = (Ranks.FIVE, Suits.CLUBS)
        card_lose_2 = (Ranks.ACE, Suits.CLUBS)
        card_win_1 = (Ranks.TEN, Suits.DIAMONDS)
        card_win_2 = (Ranks.JACK, Suits.CLUBS)
        card_bust = (Ranks.TEN, Suits.DIAMONDS)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_1, card_win_2]
        winner = game.calculate_winner()
        self.assertEqual(BlackJackWinner.DEALER, winner)

        game.player_hand = [card_win_1, card_win_2]
        game.dealer_hand = [card_lose_1, card_lose_2]
        winner = game.calculate_winner()
        self.assertEqual(BlackJackWinner.PLAYER, winner)

        game.player_hand = [card_win_1, card_win_2, card_bust]
        game.dealer_hand = [card_lose_1, card_lose_2]
        winner = game.calculate_winner()
        self.assertEqual(BlackJackWinner.DEALER, winner)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_1, card_win_2, card_bust]
        winner = game.calculate_winner()
        self.assertEqual(BlackJackWinner.PLAYER, winner)

    def test_history(self):
        game = Blackjack()

        card_1 = (Ranks.ONE, Suits.CLUBS)
        self.assertEqual(len(game.current_history), 1)

        game.player_hand = [card_1, card_1]
        game.player_draw()
        self.assertEqual(len(game.current_history), 2)

        game.player_hand = [card_1, card_1, card_1]
        game.player_draw()
        self.assertEqual(len(game.current_history), 3)

    def test_complete_history(self):
        game = Blackjack()

        card_lose_1 = (Ranks.NINE, Suits.CLUBS)
        card_lose_2 = (Ranks.TEN, Suits.CLUBS)
        card_win_3 = (Ranks.TEN, Suits.DIAMONDS)
        card_win_4 = (Ranks.JACK, Suits.CLUBS)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_3, card_win_4]
        game.stand()
        self.assertEqual(len(game.entire_history), 1)
        self.assertEqual(game.entire_history[0][0], BlackJackWinner.DEALER)

        game.player_hand = [card_win_3, card_win_4]
        game.dealer_hand = [card_lose_1, card_lose_2]
        game.stand()
        self.assertEqual(len(game.entire_history), 2)
        self.assertEqual(game.entire_history[1][0], BlackJackWinner.PLAYER)

        game.clear_game()
        self.assertEqual(len(game.entire_history), 0)

    def test_get_last_turn_lose(self):
        game = Blackjack()

        card_lose_1 = (Ranks.NINE, Suits.CLUBS)
        card_lose_2 = (Ranks.TEN, Suits.CLUBS)
        card_win_3 = (Ranks.TEN, Suits.DIAMONDS)
        card_win_4 = (Ranks.JACK, Suits.CLUBS)

        game.player_hand = [card_lose_1, card_lose_2]
        game.dealer_hand = [card_win_3, card_win_4]

        game.stand()
        player_str = BlackJackTestCase._hand_to_str(game.player_hand)
        dealer_str = BlackJackTestCase._hand_to_str(game.dealer_hand)

        self.assertEqual(game.get_last_turn()[0], (player_str, dealer_str))
        self.assertFalse(game.get_last_turn()[1])

    def test_get_last_turn_win(self):
        game = Blackjack()

        card_lose_1 = (Ranks.NINE, Suits.CLUBS)
        card_lose_2 = (Ranks.TEN, Suits.CLUBS)

        card_win_1 = (Ranks.TEN, Suits.CLUBS)
        card_win_2 = (Ranks.JACK, Suits.CLUBS)
        card_win_3 = (Ranks.ACE, Suits.DIAMONDS)

        game.player_hand = [card_win_1, card_win_2, card_win_3]
        game.dealer_hand = [card_lose_1, card_lose_2]
        game.stand()

        player_str = BlackJackTestCase._hand_to_str(game.player_hand)
        dealer_str = BlackJackTestCase._hand_to_str(game.dealer_hand)

        self.assertEqual(game.get_last_turn()[0], (player_str, dealer_str))
        self.assertTrue(game.get_last_turn()[1])
