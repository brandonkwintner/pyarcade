from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.user_model import UserModel
from ..models.game_model import GameModel
from ..models.game_model import Game

from ..utilities.tokens import Token
from ..utilities.data_validation import UserValidator

import random

class ResetUserStatsView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        """
        Args:
            request: parameters for API call.

        Returns:
            JSON response.
        """
        # creates sample games
        user = UserModel.objects.get(id__iexact=request.user.id)
        games = [g for g in Game]

        for game in games:
            new_game = GameModel(player=user, game_played=game,
                                 did_win=random.randint(1,10) % 2 == 0)
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

        user = UserValidator.validate_user(request.user.id)

        if user is None:
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
                game = Game.value_of(body["game"].lower())

                if game is None:
                    raise Exception("invalid game")

                games = [game]

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

            An invalid game defaults to all.

        Returns:
            e.g.,
            {
                "game": "MASTERMIND"
                "board": [
                    {
                        "user": "user1",
                        "wins": 20,
                        "total": 40
                    },
                    {
                        "user": "user2",
                        "wins": 10,
                        "total": 20
                    },
                ],
                "access": "access token",
                "refresh: "refresh token",
            }

        """

        queries = request.GET.dict()
        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        try:
            game = Game.value_of(queries["game"].lower())

        except (KeyError, ValueError, Exception):
            game = None

        try:
            sort = queries["sort"].lower()

            if sort not in ["wins", "total",]:
                raise ValueError("invalid key value")

        except (KeyError, ValueError, Exception):
            sort = "wins"

        entries = GameModel.objects.values("player").filter(is_deleted=False)

        if game is not None:
            entries = entries.filter(game_played=game)
            game = game.value
        else:
            game = "All"

        entries = entries.annotate(
            wins=(Count("player", filter=Q(did_win=True))),
            total=(Count("player"))
        )

        if sort == "wins":
            entries = entries.order_by("-wins")
        elif sort == "total":
            entries = entries.order_by("-total")

        board = ScoreboardView.get_board_from_db_rows(entries)

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "game": game,
            "board": board,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    @staticmethod
    def get_board_from_db_rows(entries: [dict]) -> [dict]:
        """
        Given a array of dict's from the database return the board response.
        e.g., [{ "player": 1, "wins": 10, "total": 40 }]

        Args:
            entries: array of dict objects

        Returns:
            2d array
            e.g., [{ "user": "username", "wins": 10, "total": 40 }]

        """

        board = []

        for entry in entries:
            try:
                user = UserModel.objects.get(id__iexact=entry["player"])
                wins = entry["wins"]
                total = entry["total"]
            except UserModel.DoesNotExist:
                continue
            except (KeyError, Exception):
                return []

            board.append({
                "user": user.username,
                "wins": wins,
                "total": total,
            })

        return board
