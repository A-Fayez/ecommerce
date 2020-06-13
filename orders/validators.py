from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.models import User


def validate_email_address(email):
    """Use django's custom email validation as well as checking for its uniqueness
    """

    validate_email(email)
    if User.objects.filter(email=email).exists():
        raise ValidationError(
            _("This email is already in use"), code="email",
        )


def validate_username(username):
    """Use django's custom username validation as well as checking for its uniqueness
    """

    if User.objects.filter(username=username).exists():
        raise ValidationError(
            _("This username is already in use"), code="username",
        )
