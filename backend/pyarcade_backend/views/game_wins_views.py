from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from distutils.util import strtobool
from ..models.game_model import GameModel
from ..models.game_model import Game
from ..utilities.tokens import Token
from ..utilities.data_validation import UserValidator


class GameWinsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        When args is empty - Returns number of wins across all games.
        When args contains an argument - Returns number of wins for that
        game.

        Ex) .../game_wins/?game=war DO NOT INCLUDE A " / " AFTER THE GAME!!

        Returns:
            JSON response.
        """

        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        queries = request.GET.dict()

        if len(queries) == 0:
            game = "All"
            total_games_won = len(GameModel.objects.filter(player=user,
                                                           did_win=True))
        elif len(queries) == 1:
            game = Game.value_of(queries['game'].lower())
            if game is None:
                return JsonResponse({
                    "message": "Invalid request."
                }, status=400)
            else:
                total_games_won = len(GameModel.objects
                                      .filter(player=user,
                                              did_win=True,
                                              game_played__iexact=game))
                game = game.value
        else:
            return JsonResponse({
                "message": "Invalid URL."
            }, status=400)

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "game": game,
            "wins": total_games_won,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    def post(self, request):
        """
        Add new game played to database.
        Args:
            request: contains a JSON object in the form: {
                                                            "game" : game,
                                                            "won" : bool
                                                         }
        Returns:
            JSON response.
        """
        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        queries = request.POST.dict()
        game = Game.value_of(queries['game'].lower())

        if game is None:
            return JsonResponse({
                "message": "Invalid request."
            }, status=400)

        # creating game and adding it to the database
        try:
            won = strtobool(queries["won"])

        except (KeyError, ValueError, Exception):
            return JsonResponse({
                "message": "Invalid request."
            }, status=400)

        new_game = GameModel(player=user, game_played=game, did_win=won)
        new_game.save()

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "access": token["access"],
            "refresh": token["refresh"],
        })
