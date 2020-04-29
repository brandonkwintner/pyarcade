from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.game_model import GameModel
from ..models.game_model import Game
from ..models.user_model import UserModel
from ..utilities.tokens import Token


class GameWinsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        When args is empty - Returns number of wins across all games.
        When args contains an argument - Returns number of wins for that
        game.

        Ex) .../game_wins?game=war DO NOT INCLUDE A " / " AFTER THE GAME!!
        """
        user_id = request.user.id
        user = GameWinsView.validate_user(user_id)

        queries = request.GET.dict()

        if len(queries) == 0:
            game = "All Games"
            total_games_won = len(GameModel.objects.filter(player__exact=user, did_win__exact=True))
        elif len(queries) == 1:
            game = Game.value_of(queries['game'].lower())
            if game is None:
                return JsonResponse({
                    "message": "Invalid request."
                }, status=400)
            else:
                total_games_won = len(GameModel.objects.filter(player__exact=user, did_win__exact=True,
                                                               game_played__exact=game))
        else:
            return JsonResponse({
                "message": "Invalid URL."
            }, status=400)

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "game": str(game),
            "Wins": total_games_won,
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
        """
        user_id = request.user.id
        user = GameWinsView.validate_user(user_id)

        queries = request.POST.dict()
        game = Game.value_of(queries['game'].lower())

        if game is None:
            return JsonResponse({
                "message": "Invalid request."
            }, status=400)

        # creating game and adding it to the database
        new_game = GameModel(player=user, game_played=game, did_win=True)
        new_game.save()

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "game": str(game),
            "access": token["access"],
            "refresh": token["refresh"],
        })

    @staticmethod
    def validate_user(user_id) -> UserModel:
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
