from django.test import TestCase
from django.core.exceptions import ValidationError

import os

from .models import UserModel

# Create your tests here.

# run tests by: python manage.py test pyarcade_backend


class UserModelTestCase(TestCase):
    def test_create_simple_user(self):
        user = UserModel(username="bob", password="test")

        user.clean()
        # assert true since user is valid
        self.assertTrue(True)

    def test_create_bad_username(self):
        user = UserModel(username="x", password="test")

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
