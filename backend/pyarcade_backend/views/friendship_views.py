from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.friendship_model import FriendshipModel
from ..models.user_model import UserModel
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

        Args:
            request: GET request with a userID

        Returns:
            JSON Object with a list of all friendships for requesting user.
            This will also show all pending requests,
            so user knows they have requests pending
        """
        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        # grab all friendships that this user has in the database
        friends_list = FriendshipModel.objects.filter(
            Q(user_one=user.username) | Q(user_two=user.username),
            Q(friendship_status="friends") | Q(friendship_status="pending"))

        # this list will just contain the friends of the user as Strings
        filtered_friends_list = []
        for friendship in friends_list.values():
            friend_string = ""
            if friendship["friendship_status"] == "pending":
                friend_string += "(Pending) "

            if friendship["user_one"] != user.username:
                filtered_friends_list.append(
                    friend_string + friendship["user_one"])
            elif friendship["user_two"] != user.username:
                filtered_friends_list.append(
                    friend_string + friendship["user_two"])

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "friends": filtered_friends_list,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    def post(self, request):
        """
        Adds or updates a friendship in the database
        Args:
            request: contains a JSON object in the form: {
                                                            "user2": username
                                                         }
        **status can only be one of three strings:
            "friends": equivalent of accepting a friend request
            not friends": this would be the equivalent of un-friending someone
            "": this would be a new friend request

        Returns:
            JSON response of the Friendship created/updated.
        """
        queries = request.POST.dict()

        # Attempt to get all of the query params.
        try:
            user2_username = queries["user2"]
        except (KeyError, ValueError, Exception):
            return JsonResponse({
                "message": "Invalid request."
            }, status=400)

        # validate requesting user
        user1 = UserValidator.validate_user(request.user.id)
        if user1 is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        # validate requested user
        try:
            user2 = UserModel.objects.get(username=user2_username)
        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Invalid request.",
            }, status=400)

        if user1.username == user2.username:
            return JsonResponse({
                "message": "Invalid request. You cannot friend yourself",
            }, status=400)

        try:
            FriendshipModel.objects.get(user_one=user1.username,
                                        user_two=user2.username)
            return JsonResponse({
                "message": "Already exists.",
            }, status=400)
        except FriendshipModel.MultipleObjectsReturned:
            return JsonResponse({
                "message": "Already exists.",
            }, status=400)
        except FriendshipModel.DoesNotExist:
            pass

        # the friendship already exists,
        # then a user must be accepting the request
        try:
            friendship = FriendshipModel.objects.get(user_two=user1.username,
                                                     user_one=user2.username)
            friendship.friendship_status = "friends"
        except FriendshipModel.MultipleObjectsReturned:
            return JsonResponse({
                "message": "Already exists.",
            }, status=400)
        except FriendshipModel.DoesNotExist:
            # if friendship does not exists, this should be a friend request
            friendship = FriendshipModel(user_one=user1.username,
                                         user_two=user2.username,
                                         friendship_status="pending")

        friendship.save()

        token = Token.get_tokens_for_user(user1)

        return JsonResponse({
            "username": user1.username,
            "requested_user": user2.username,
            "access": token["access"],
            "refresh": token["refresh"],
        })
