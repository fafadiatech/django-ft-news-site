from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailModelBackend(ModelBackend):
    """
    This is a ModelBackend that allows authentication with an email address.

    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None
