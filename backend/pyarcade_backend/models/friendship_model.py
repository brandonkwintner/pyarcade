from django.db import models

from enum import Enum


class Friendship(Enum):
    """
        Enum representing the status of each friendship.
    """

    FRIENDS = "friends"
    PENDING = "pending"


class FriendshipModel(models.Model):
    """
        Friendship table in the database.
        Note: The users in each entry are in alphabetical order base on username.
    """

    user_one = models.CharField(max_length=30)
    user_two = models.CharField(max_length=30)
    friendship_status = models.CharField(choices=[(friendship.name,
                                                   friendship.value) for\
                                                  friendship in Friendship],
                                         max_length=8)
