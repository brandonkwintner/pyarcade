from ..models.user_model import UserModel


class UserValidator:
    @staticmethod
    def validate_user(user_id: int) -> UserModel:
        """
        Args:
            user_id: username to be checked

        Returns:
            User model object or None
        """
        try:
            return UserModel.objects.get(id__iexact=user_id)
        except UserModel.DoesNotExist:
            return None
