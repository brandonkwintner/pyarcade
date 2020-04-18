from django.http import JsonResponse

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

from rest_framework.views import APIView

from ..models.user_model import UserModel
from ..utilities.tokens import Token


# Create your views here.

class SignUpView(APIView):
    def get(self, request):
        return JsonResponse({
            "message": "success",
        })

    def post(self, request):
        try:
            username = request.validated["username"]
            password = request.validated["password"]
        except AttributeError:
            return JsonResponse({
                "message": "Did not meet requirements."
            }, status=400)

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

        token = Token.get_tokens_for_user(new_user)

        return JsonResponse({
            "access": token['access'],
            "refresh": token['refresh'],
        })


class LogInView(APIView):
    def post(self, request):
        try:
            username = request.validated["username"]
            password = request.validated["password"]
        except AttributeError:
            return JsonResponse({
                "message": "Did not meet requirements."
            }, status=400)

        try:
            user_found = UserModel.objects.get(username__iexact=username)

            if not check_password(password, user_found.password):
                raise UserModel.DoesNotExist

        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Did not match credentials."
            }, status=400)


        token = Token.get_tokens_for_user(user_found)

        return JsonResponse({
            "access": token['access'],
            "refresh": token["refresh"],
        })
