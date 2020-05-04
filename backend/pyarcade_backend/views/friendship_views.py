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

        Args:
            request: GET request with a userID

        Returns:
            JSON Object with a list of all friendships for requesting user.
            This will also show all pending requests, so user knows they have requests pending
        """
        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        # grab all friendships that this user has in the database
        friends_list = FriendshipModel.objects.filter(Q(user_one=user) | Q(user_two=user),
                                                      Q(friendship_status="friends") | Q(friendship_status="pending"))

        # this list will just contain the friends of the user as Strings
        filtered_friends_list = []
        for friendship in friends_list.values():
            friend_string = ""
            if friendship["status"] is "pending":
                friend_string += "(Pending) "

            if friendship["user_one"] is not user.username:
                filtered_friends_list.append(friend_string + friendship["user_one"])
            elif friendship["user_two"] is not user.username:
                filtered_friends_list.append(friend_string + friendship["user_two"])

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
                                                            "user1" : "user1 id"
                                                            "user2" : "user2 id",
                                                            "status" : str
                                                         }
            **status can only be one of three strings:
                "friends": this would be the equivalent of accepting a friend request
                "not friends": this would be the equivalent of un-friending someone
                "": this would be a new friend request

        Returns:
            JSON response of the Friendship created/updated.
        """
        queries = request.POST.dict()

        # Attempt to get all of the query params.
        try:
            user1 = queries['user1']  # this is the user requesting user
            user2 = queries['user2']  # this is the user who the requesting user wants to be friends with or un-friend
            status = queries['status']
        except (KeyError, ValueError, Exception):
            return JsonResponse({
                "message": "Invalid request."
            }, status=400)

        user1 = UserValidator.validate_user(user1)
        user2 = UserValidator.validate_user(user2)

        if user1 is None or user2 is None:
            return JsonResponse({
                "message": "Invalid credentials.",
            }, status=400)

        user_list = [].append(user1).append(user2).sort(key=lambda x: x.username)  # sort users by username

        # if the friendship already exists, update its status and save, else create it
        try:
            friendship = FriendshipModel.objects.get(user_one=user_list[0])

            # either the user is accepting or rejecting a friend request, or is un-friending
            if status is not "friends" or "not friends":
                friendship.status = status
            else:  # reach this point if the Friendship was already created but request did not specify how to update
                return JsonResponse({
                    "message": "Invalid request."
                }, status=400)
        except FriendshipModel.DoesNotExist:  # if friendship does not exists, this should be a friend request
            friendship = FriendshipModel(user_one=user_list[0], user_two=user_list[1], status="pending")

            if status is not "":  # you cannot make a new friend request with a status in it
                return JsonResponse({
                    "message": "Invalid request."
                }, status=400)

        friendship.save()

        token = Token.get_tokens_for_user(user1)

        return JsonResponse({
            "username": user1.username,
            "friendship": friendship,
            "access": token["access"],
            "refresh": token["refresh"],
        })
