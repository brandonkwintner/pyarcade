from django.test import TestCase

from ..models.user_model import UserModel
from ..models.game_model import GameModel
from ..models.game_model import Game

# Create your tests here.

# run tests by: python manage.py test pyarcade_backend


class GameModelTestCase(TestCase):
    """
    Tests for User Model / Game Model interaction.
    """
    # test case method
    def setUp(self):
        UserModel.objects.create(username="user", password="test")
        UserModel.objects.create(username="other_user", password="test")

    def test_make_game_enum(self):
        self.assertEqual(Game.GO_FISH, Game.value_of("go fish"))
        self.assertEqual(Game.CONNECT4, Game.value_of("connect4"))
        self.assertEqual(Game.BLACKJACK, Game.value_of("blackjack"))
        self.assertEqual(Game.MASTERMIND, Game.value_of("mastermind"))

    def test_make_player_entry(self):
        user = UserModel.objects.get(username__iexact="user")

        entry = GameModel(player=user, game_played=Game.MASTERMIND,
                          meta="test_make_player_entry")
        entry.save()

        game = GameModel.objects.get(meta="test_make_player_entry")

        self.assertEqual(game.player.id, user.id)

    def test_make_bad_player_entry(self):
        try:
            entry = GameModel(player="bad entry", game_played=Game.MASTERMIND)
            entry.save()
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_multiple_game_entries(self):
        user = UserModel.objects.get(username__iexact="user")

        for i in range(5):
            entry = GameModel(player=user, game_played=Game.MASTERMIND,
                              meta="test_multiple_game_entries")
            entry.save()

        games = GameModel.objects.filter(meta="test_multiple_game_entries")

        self.assertEqual(len(games), 5)

    def test_no_game_entries(self):
        user = UserModel.objects.get(username__iexact="user")
        other_user = UserModel.objects.get(username__iexact="other_user")

        GameModel(player=user, game_played=Game.MASTERMIND,
                  meta="test_no_game_entries")

        games = GameModel.objects.filter(player=other_user)

        self.assertEqual(len(games), 0)
