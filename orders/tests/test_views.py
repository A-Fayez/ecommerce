from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import User


class HomepageViewTestCase(TestCase):
    def test_response(self):
        c = Client()
        response = c.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pizza/homepage.html")
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        self.assertTrue(response.content.endswith(b"</html>"))


@override_settings(
    AUTHENTICATION_BACKENDS=("orders.backends.EmailOrUsernameAuthBackend",)
)
class RegisterViewTestCase(TestCase):
    c = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "firstname": "John Doe",
            "lastname": "Doe",
            "email": "valid_email@domain.com",
            "username": "john_doe123",
            "password": "strongpw123",
        }

    def setUp(self):
        User.objects.create_user("duplicate", "duplicate@domain.com", "dup")

    # a holder object to avoid duplicating code
    # only change the keys that are tested

    def test_response(self):
        response = self.c.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "pizza/register.html")
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        self.assertTrue(response.content.endswith(b"</html>"))

    def test_valid_registration(self):
        """first we test posting the data to return redirect
        then we test the content of the redirected response that will contain the
        greeting message asserting a successful registration
        """

        self.__class__.user_data["username"] = "john_doe123"
        self.__class__.user_data["email"] = "valid_email@domain.com"

        posting_data_response = self.c.post(
            reverse("register"), self.__class__.user_data, follow=False
        )
        redirect_response = self.c.post(
            reverse("register"), self.__class__.user_data, follow=True,
        )

        # redirecting to menu view and welcome the new user
        self.assertEqual(posting_data_response.status_code, 302)
        self.assertIn(b"john_doe123", redirect_response.content)

    def test_invalid_username(self):
        # wrong username field (i.e. contains whitespaces)
        self.__class__.user_data["username"] = "john doe123"
        self.__class__.user_data["email"] = "valid_email@domain.com"

        response = self.c.post(reverse("register"), self.user_data, follow=True,)

        self.assertEqual(response.context["username_validity_class"], "is-invalid")
        self.assertEqual(
            response.context["username_feedback_class"], "invalid-feedback"
        )
        self.assertEqual(
            response.context["username_feedback_message"],
            "Invalid username: username mustn't have whitespaces in it",
        )

        # duplicate username
        self.__class__.user_data["username"] = "duplicate"
        self.__class__.user_data["email"] = "dup@domain.com"

        response = self.c.post(
            reverse("register"), self.__class__.user_data, follow=True,
        )

        self.assertEqual(
            response.context["username_feedback_message"],
            "This username already exists",
        )

    def test_invalid_email(self):
        # duplicate email
        self.__class__.user_data["username"] = "john_doe123"
        self.__class__.user_data[
            "email"
        ] = "duplicate@domain.com"  # duplicate in fixtures

        response = self.c.post(
            reverse("register"), self.__class__.user_data, follow=True,
        )

        self.assertEqual(
            response.context["email_feedback_message"], "This email is already in use",
        )

        # invalid email format
        self.__class__.user_data["username"] = "john_doe123"
        self.__class__.user_data["email"] = "Wrong email"

        response = self.c.post(reverse("register"), self.user_data, follow=True,)

        self.assertEqual(
            response.context["email_feedback_message"], "Invalid email format",
        )


@override_settings(DEBUG=True)
class LoginViewTestCase(TestCase):
    c = Client()

    def setUp(self):
        user = User.objects.create_user(
            first_name="john",
            last_name="doe",
            email="john@gmail.com",
            password="john123",
            username="johnd",
        )
        user.save()

    def test_response(self):
        response = self.c.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pizza/login.html")

        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        self.assertTrue(response.content.endswith(b"</html>"))

    def test_valid_login(self):

        # test login with email
        login_with_email_response = self.c.post(
            reverse("login"), {"username": "john@gmail.com", "password": "john123"},
        )
        self.assertEqual(login_with_email_response.status_code, 302)
        self.c.logout()

        # test login with username
        login_with_username_response = self.c.post(
            reverse("login"), {"username": "johnd", "password": "john123"},
        )
        self.assertEqual(login_with_username_response.status_code, 302)
        self.c.logout()

        # test follow up redirection after successful login
        response = self.c.post(
            reverse("login"), {"username": "johnd", "password": "john123"}, follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        response = self.c.post(
            reverse("login"), {"username": "johnd", "password": "wrongpw"},
        )
        self.assertIn(b"Either your email or password is incorrect.", response.content)
