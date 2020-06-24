from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.contrib.auth import authenticate


@override_settings(
    AUTHENTICATION_BACKENDS=("orders.backends.EmailOrUsernameAuthBackend",)
)
class EmailOrUsernameAuthBackendTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("test", "test@example.com", "test")

    def test_auth_with_username(self):
        self.assertEqual(authenticate(username="test", password="test"), self.user)
        self.assertIsNone(authenticate(username="wrong", password="test"))
        self.assertIsNone(authenticate(username="test", password="wrong"))
        self.assertIsInstance(authenticate(username="test", password="test"), User)

    def test_auth_with_email(self):
        self.assertEqual(
            authenticate(username="test@example.com", password="test"), self.user
        )
        self.assertIsInstance(
            authenticate(username="test@example.com", password="test"), User
        )
