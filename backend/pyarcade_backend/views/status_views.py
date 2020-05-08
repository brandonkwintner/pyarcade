from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..utilities.tokens import Token
from ..utilities.data_validation import UserValidator


class StatusView(APIView):
    permission_classes = [IsAuthenticated, ]
    """
    Get / Post status for a user.
    """

    def get(self, request):
        """
        Returns:
             JSON Object with user status, or empty string if no status exists.
        """

        user = UserValidator.validate_user(request.user.id)

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)

        status = user.status_message

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "status": status,
            "access": token["access"],
            "refresh": token["refresh"],
        })

    def post(self, request):
        """
        Args:
            request: Contains new status for user.

        Returns:
            JSON Object with new user status
        """
        user = UserValidator.validate_user(request.user.id)
        queries = request.POST.dict()

        if user is None:
            return JsonResponse({
                "message": "Invalid credentials."
            }, status=400)

        # Attempt to get new status.
        try:
            status = queries['status']
        except (KeyError, ValueError, Exception):
            return JsonResponse({
                "message": "Invalid request."
            }, status=400)

        # Checks if status message is too long.
        if len(status) > 30:
            status = status[:30]

        user.status_message = status
        user.save()

        token = Token.get_tokens_for_user(user)

        return JsonResponse({
            "username": user.username,
            "status": status,
            "access": token["access"],
            "refresh": token["refresh"],
        })
