from rest_framework_simplejwt.tokens import RefreshToken

class Token:
    """Utility class to manually generate/authenticate a JWT for a user.
    """
    @staticmethod
    def get_tokens_for_user(user) -> dict:
        """

        Args:
            user: A user model object.

        Returns:
            Dictionary containing the access and refresh tokens.

        """

        refresh = RefreshToken.for_user(user)

        return {
            "access": f"Bearer {str(refresh.access_token)}",
            "refresh": f"Bearer {str(refresh)}",
        }
