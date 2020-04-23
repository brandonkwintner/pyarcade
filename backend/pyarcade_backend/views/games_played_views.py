from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.game_model import GameModel
from ..models.user_model import UserModel
from ..utilities.tokens import Token


class GamesPlayedView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        When args is empty - Returns number of games played across all games.
        When args contains an argument - Returns number of games played for that
        game.

        -- Need username in get request! --
        """

        # must be authenticated to access
        user_id = request.user.id
        GamesPlayedView.validate_user(user_id)
        user = UserModel.objects.get(id__iexact=user_id)

        # All games.
        games_played = len(GameModel.objects.filter(player__exact=user))
       
        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "games_played": games_played,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    @staticmethod
    def validate_user(user_id):
        """
        Args:
            user_id: username to be checked

        Returns:
            Nothing or a status 400 error.
        """
        try:
            UserModel.objects.get(id__iexact=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)

    @staticmethod
    def validate_game(game):
        """
        Args:
            game: game to be checked

        Returns:
            Nothing or a status 400 error.
        """
        # TODO - implement and call in get
        return
