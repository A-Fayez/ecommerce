from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.models import User


class EmailValidationError(ValidationError):
    def __init__(self, email, message, code="email"):
        self.email = email
        self.message = message
        self.code = code
        super().__init__(self.message, code=code)


class UsernameValidationError(ValidationError):
    def __init__(self, username, message, code="username"):
        self.username = username
        self.message = message
        self.code = code
        super().__init__(self.message, code=code)


class LoginError(Exception):
    def __init__(self, message=_("Either username or email is wrong")):
        self.message = message
        super().__init__(self.message)


def validate_email_address(email):
    """Use django's custom email validation as well as checking for its uniqueness
    """

    try:
        validate_email(email)
    except ValidationError as err:
        raise EmailValidationError(
            email, message=_("Invalid email format"), code="email",
        ) from err

    if User.objects.filter(email=email).exists():
        raise EmailValidationError(
            email, message=_("This email is already in use"), code="email",
        )


def validate_username(username):
    """Use django's custom username validation as well as checking for its uniqueness
    """

    if " " in username:
        raise UsernameValidationError(
            username,
            message=_("Invalid username: username mustn't have whitespaces in it"),
            code="username",
        )

    if User.objects.filter(username=username).exists():
        raise UsernameValidationError(
            username, message=_("This username already exists"), code="username",
        )


def validate_login_key(username):
    """This method is used to validate login username or email
    because I'm using a custom backend that authenticate with either
    username or email. it's just an extra validator
    used at the login view to lessen sql injection"""

    if " " in username.strip():
        raise LoginError(_("whitespaces in username"))
