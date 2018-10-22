from django.contrib.auth.backends import ModelBackend
from .models import UserProfile


class EmailModelBackend(ModelBackend):
    """
    This is a ModelBackend that allows authentication with an email address.

    """

    def authenticate(self, username=None, password=None):
        try:

            user = UserProfile.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return UserProfile.objects.get(pk=username)
        except UserProfile.DoesNotExist:
            return None

        return None
