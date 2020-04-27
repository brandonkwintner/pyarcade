from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.user_model import UserModel
from ..models.game_model import GameModel
from ..models.game_model import Game

from ..utilities.tokens import Token


class ResetUserStatsView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        # creates sample games
        user = UserModel.objects.get(id__iexact=request.user.id)
        games = [g for g in Game]

        for game in games:
            new_game = GameModel(player=user, game_played="master")
            new_game.save()

        return JsonResponse({"msg": "ok"})

    def post(self, request):
        """
        Resets game stats for a user.

        Args:
            request:
            game - "all" or a specific game depicted in Game enum.

            example request - body: { "game": "mastermind", }

        Returns:
            {
                "access": "access token",
                "refresh": "refresh token",
            }
        """

        try:
            user = UserModel.objects.get(id__iexact=request.user.id)
        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        try:
            body = request.POST.dict()
            game_str = body["game"].lower()

            if game_str == "all":
                # Game is an enum which is iterable
                games = [g.name for g in Game]
            else:
                games = [Game.value_of(body["game"].lower())]

        except (KeyError, Exception):
            return JsonResponse({
                "message": "Invalid request.",
            }, status=400)

        for game in games:
            try:
                query = GameModel.objects.filter(player=user.id,
                                                 game_played=game)

                query.update(is_deleted=True)
            except GameModel.DoesNotExist:
                continue

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "access": token["access"],
            "refresh": token["refresh"],
        })


class ScoreboardView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        """
        Retrieves a scoreboard from the database for all users.

        Args:
            request:
            game - specific game depicted in Game enum or default "all"
            sort - username, wins, plays (if no sort is given, default wins)
            example request - .../?game=mastermind&sort=win

        Returns:
            columns are: username, wins, amount played
            {
                "board": [
                    ["user1", 20, 40],
                    ["user2", 10, 20],
                ],
                "access": "access token",
                "refresh: "refresh token",
            }

        """

        user_id = request.user.id
        queries = request.GET.dict()

        try:
           user = UserModel.objects.get(id__iexact=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)

        try:
            games = Game.value_of(queries["game"].lower())

            if games is None:
                raise KeyError("invalid key value")
            else:
                games = [games]
        except (KeyError, ValueError, Exception):
            games = [g.name for g in Game]

        try:
            sort = queries["sort"].lower()

            if sort not in ["username", "wins", "plays"]:
                raise KeyError("invalid key value")

        except (KeyError, ValueError, Exception):
            sort = "wins"

        board = []



        # create and save game object
        # game = GameModel(player=user, game_played=Game.MASTERMIND)
        # game.save()

        # retrieves all games by a user id
        # games = GameModel.objects.filter(player=user_id)

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "board": board,
            "access": token["access"],
            "refresh": token["refresh"],
        })
