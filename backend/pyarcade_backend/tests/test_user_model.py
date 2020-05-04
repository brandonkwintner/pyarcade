from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models.user_model import UserModel

# Create your tests here.

# run tests by: python manage.py test pyarcade_backend


class UserModelTestCase(TestCase):
    """
    Tests for User creation.
    """
    def test_create_simple_user(self):
        user = UserModel(username="bob", password="test")

        # should go to else
        try:
            user.full_clean()
        except ValidationError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_create_bad_username(self):
        user = UserModel(username="!x", password="test")

        try:
            user.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_create_bad_password(self):
        user = UserModel(username="bob", password="bad")

        try:
            user.full_clean()
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
