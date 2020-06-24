from django.test import TestCase
from orders.validators import (
    validate_login_key,
    validate_username,
    validate_email_address,
    LoginError,
    UsernameValidationError,
    EmailValidationError,
)
from django.contrib.auth.models import User


class LoginErrorTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "test user"

    def test_login_error(self):
        with self.assertRaises(LoginError):
            validate_login_key(username=self.username)


class EmailValidationErrorTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="john",
            last_name="doe",
            email="test@example.com",
            password="test",
            username="test",
        )
        cls.user.save()

    def test_duplicate_email(self):
        email = "test@example.com"
        with self.assertRaises(EmailValidationError):
            validate_email_address(email)

    def test_invalid_email_format(self):
        email = "wrong format"
        with self.assertRaises(EmailValidationError):
            validate_email_address(email)


class UsernameValidationErrorTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="john",
            last_name="doe",
            email="test@example.com",
            password="test",
            username="test",
        )
        cls.user.save()

    def test_duplicate_username(self):
        username = "test"
        with self.assertRaises(UsernameValidationError):
            validate_username(username)

    def test_invalid_username_format(self):
        username = "wrong format"
        with self.assertRaises(UsernameValidationError):
            validate_username(username)
