from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models.game_model import GameModel
from ..models.game_model import Game

# Create your tests here.

# run tests by: python manage.py test pyarcade_backend


class UserModelTestCase(TestCase):
    def test_make_game_enum(self):
        self.assertEqual(Game.GO_FISH, Game.value_of("go fish"))
        self.assertEqual(Game.CONNECT4, Game.value_of("connect4"))
        self.assertEqual(Game.BLACKJACK, Game.value_of("blackjack"))
        self.assertEqual(Game.MASTERMIND, Game.value_of("mastermind"))

    # def test_make_player_entry(self):
