from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.models import User


def validate_email_address(email):
    """Use django's custom email validation as well as checking for its uniqueness"""
    validate_email(email)
    user = User.objects.get(email=email)
    if user is not None:
        raise ValidationError(
            _("This email is already in use"), code="duplicate",
        )
