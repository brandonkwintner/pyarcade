from django.db import models

from enum import Enum
from .user_model import UserModel


class Game(Enum):
    """ Enum representing each game.
    """

    MASTERMIND = "Mastermind"
    CONNECT4 = "Connect 4"
    BLACKJACK = "Blackjack"
    WAR = "War"
    GO_FISH = "Go Fish"
    HORSEMAN = "Horseman"

    @classmethod
    def value_of(cls, game_str: str) -> Enum:
        """
        Converts a string into a game enum.

        Args:
            game_str: string to convert

        Returns:
            Game enum
        """

        game_str = game_str.lower()

        if game_str in ("mastermind", "game.mastermind",):
            return cls.MASTERMIND
        elif game_str in ("connect4", "connect 4", "connect four",
                          "game.connect4",):
            return cls.CONNECT4
        elif game_str in ("blackjack", "game.blackjack",):
            return cls.BLACKJACK
        elif game_str in ("war", "game.war",):
            return cls.WAR
        elif game_str in ("go_fish", "go fish", "game.go_fish",):
            return cls.GO_FISH
        elif game_str in ("horseman", "game.horseman"):
            return cls.HORSEMAN
        else:
            return None


class GameModel(models.Model):
    """
    Game table in database.
    """

    player = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    game_played = models.CharField(max_length=20,
                                   choices=[(game.name, game.value) for game in
                                            Game])
    did_win = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    meta = models.TextField(blank=True)
