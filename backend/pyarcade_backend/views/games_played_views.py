from enum import Enum

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.game_model import GameModel
from ..models.game_model import Game
from ..utilities.tokens import Token
from ..utilities.data_validation import UserValidator


class GamesPlayedView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        When args is empty - Returns number of games played across all games.
        When args contains an argument - Returns number of games played for that
        game.

        Ex) .../games_played?game=war DO NOT INCLUDE A " / " AFTER THE GAME!!

        Returns:
            JSON response.
        """
        user = UserValidator.validate_user(request.user.id)
        queries = request.GET.dict()

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)

        if len(queries) == 0:
            game = "All"
            games_played = len(GameModel.objects.filter(player__exact=user))
        elif len(queries) == 1:
            game = Game.value_of(queries['game'].lower())
            if game is None:
                return JsonResponse({
                    "message": "Invalid request."
                }, status=400)
            else:
                games_played = len(GameModel.objects.filter(player__exact=user,
                                                            game_played__exact=
                                                            game))
                game = game.value
        else:
            return JsonResponse({
                "message": "Invalid URL."
            }, status=400)

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "game": game,
            "games_played": games_played,
            "access": token["access"],
            "refresh": token["refresh"],
        })
