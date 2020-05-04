from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.friendship_model import FriendshipModel
from django.db.models import Q
from ..utilities.data_validation import UserValidator
from ..utilities.tokens import Token


class FriendshipView(APIView):
    permission_classes = [IsAuthenticated, ]
    """
    Get / Post status for a friendship between two users.
    """

    def get(self, request):
        """
            Returns:
                JSON Object with a list of all friendships for requesting user.
        """
        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        # grab all friendships that this user has in the database
        friends_list = FriendshipModel.objects.filter(Q(user_one=user) | Q(user_two=user),
                                                      Q(friendship_status="friends"))

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "Friends": friends_list,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    def post(self, request):
        pass
