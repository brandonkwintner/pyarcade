from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.user_model import UserModel
from ..utilities.tokens import Token


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        # must be authenticated to access
        user_id = request.user.id

        try:
           user = UserModel.objects.get(id__iexact=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)


        msg = f"hello, {user.username}"

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "message": msg,
            "access": token["access"],
            "refresh": token["refresh"],
        })
