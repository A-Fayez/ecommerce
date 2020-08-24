from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameAuthBackend(BaseBackend):
    """ A custom backend to authenticate user either using an email or username
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
