from enum import Enum

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.game_model import GameModel
from ..models.game_model import Game
from ..models.user_model import UserModel
from ..utilities.tokens import Token


class GamesPlayedView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        When args is empty - Returns number of games played across all games.
        When args contains an argument - Returns number of games played for that
        game.

        Ex) .../games_played?game=war DO NOT INCLUDE A " / " AFTER THE GAME!!
        """
        user_id = request.user.id
        user = GamesPlayedView.validate_user(user_id)
        queries = request.GET.dict()

        if len(queries) == 0:
            game = "ALL"
            games_played = len(GameModel.objects.filter(player__exact=user))
        elif len(queries) == 1:
            game = GamesPlayedView.validate_game(queries['game'].lower())
            games_played = len(GameModel.objects.filter(player__exact=user,
                                                        game_played__exact=game)
                               )
            game = game.name
        else:
            return JsonResponse({
                "message": "Invalid URL."
            }, status=400)

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "game": str(game),
            "games_played": games_played,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    @staticmethod
    def validate_user(user_id) -> int:
        """
        Args:
            user_id: username to be checked

        Returns:
            Nothing or a status 400 error.
        """
        try:
            user = UserModel.objects.get(id__iexact=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)
        return user

    @staticmethod
    def validate_game(game: str) -> Enum:
        """
        Args:
            game: game to be checked

        Returns:
            Game Enum or a status 400 error.
        """
        if Game.value_of(game) == Game.INVALID_GAME:
            return JsonResponse({
                "message": "Invalid game."
            }, status=400)
        else:
            return Game.value_of(game)
