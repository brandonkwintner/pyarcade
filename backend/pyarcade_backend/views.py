from django.views import View
from django.http import JsonResponse

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

import json
from .models import UserModel


# Create your views here.

class SignUpView(View):
    def post(self, request):
        # username = request.validated['username']
        # password = request.validated['password'],

        found = True

        try:
            UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            found = False

        if found:
            return JsonResponse({
                "message": "Username taken."
            }, status=400)

        new_user = UserModel(username=username, password=password)

        try:
            new_user.full_clean()
        except ValidationError:
            return JsonResponse({
                "message": "Did not meet requirements."
            }, status=400)

        # hash password before storing
        new_user.password = make_password(new_user.password)
        new_user.save()

        # TODO return an actual auth token
        token = username

        return JsonResponse({
            "message": "Success.",
            "token": token
        })

