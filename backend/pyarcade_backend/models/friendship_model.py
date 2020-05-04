from django.db import models

from enum import Enum
from .user_model import UserModel


class Friendship(Enum):
    """
        Enum representing the status of each friendship.
    """

    FRIENDS = "friends"
    PENDING = "pending"
    NOT_FRIENDS = "not friends"


class FriendshipModel(models.Model):
    """
        Friendship table in the database.
        Note: The users in each entry are in alphabetical order base on username.
    """

    user_one = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    user_two = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    friendship_status = models.CharField(choices=[(friendship.name, friendship.value) for friendship in Friendship])
