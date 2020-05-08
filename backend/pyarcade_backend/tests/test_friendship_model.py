from django.test import TestCase

from ..models.friendship_model import FriendshipModel
from ..models.friendship_model import Friendship
from ..models.user_model import UserModel

# Create your tests here.

# run tests by: python manage.py test pyarcade_backend


class GameModelTestCase(TestCase):
    """
    Tests for Friendship Model.
    """
    # test case method
    def setUp(self):
        UserModel.objects.create(username="a_user", password="test")
        UserModel.objects.create(username="friends_with_user", password="test")
        UserModel.objects.create(username="no_friends", password="test")

    def test_make_friends_pending(self):
        user = UserModel.objects.get(username="a_user")
        friend = UserModel.objects.get(username="friends_with_user")

        friendship = FriendshipModel(user_one=user.username,
                                     user_two=friend.username,
                                     friendship_status=\
                                         Friendship.PENDING.value)
        friendship.save()

        find = FriendshipModel.objects.get(friendship_status=
                                           Friendship.PENDING.value)

        self.assertEqual(find.user_one, user.username)
        self.assertEqual(find.user_two, friend.username)

    def test_make_friends_accept(self):
        user = UserModel.objects.get(username="a_user")
        friend = UserModel.objects.get(username="friends_with_user")


        friendship = FriendshipModel(user_one=user.username,
                                     user_two=friend.username,
                                     friendship_status= \
                                         Friendship.PENDING.value)
        friendship.save()

        try:
            find = FriendshipModel.objects.get(user_one=user.username,
                                                     user_two=friend.username)
            self.assertEqual(find.user_one, user.username)
            self.assertEqual(find.user_two, friend.username)
        except FriendshipModel.DoesNotExist:
            self.assertTrue(False)

    def test_not_friends(self):
        user = UserModel.objects.get(username="a_user")
        no_friends = UserModel.objects.get(username="no_friends")

        try:
            FriendshipModel.objects.get(user_one=user.username,
                                               user_two=no_friends.username)
            self.assertTrue(False)
        except FriendshipModel.DoesNotExist:
            self.assertTrue(True)

