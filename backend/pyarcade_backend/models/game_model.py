from django.db import models

from enum import Enum
from .user_model import UserModel


class Game(Enum):
    """ Enum representing each game.
    """

    MASTERMIND = "mastermind"
    CONNECT4 = "connect4"
    BLACKJACK = "blackJack"
    WAR = "war"
    GO_FISH = "go_fish"
    HORSEMAN = "horseman"

    @classmethod
    def value_of(cls, game_str: str) -> Enum:
        """
        Converts a string into a game enum
        Args:
            game_str: string to convert

        Returns:
            Game enum
        """

        if game_str in ("mastermind", "Game.MASTERMIND",):
            return cls.MASTERMIND
        elif game_str in ("connect4", "connect 4", "connect four",
                          "Game.CONNECT4",):
            return cls.CONNECT4
        elif game_str in ("blackjack", "Game.BLACKJACK",):
            return cls.BLACKJACK
        elif game_str in ("war", "Game.WAR",):
            return cls.WAR
        elif game_str in ("go_fish", "go fish", "Game.GO_FISH",):
            return cls.GO_FISH
        elif game_str in ("horseman", "Game.HORSEMAN"):
            return cls.HORSEMAN


class GameModel(models.Model):
    """
    Game table in database.
    """

    player = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    game_played = models.CharField(max_length=20,
                        choices=[(game.name, game.value) for game in Game])
    did_win = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    meta = models.TextField(blank=True)
