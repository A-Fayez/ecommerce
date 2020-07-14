from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Category, MenuItem, Topping
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


class MenuViewTestCase(TestCase):
    fixtures = ["orders_testdata.json"]
    categories = Category.objects.values_list("name", flat=True)
    c = Client()
    response = c.get(reverse("menu"))

    regulars = MenuItem.objects.values_list("name", flat=True).filter(
        category_id=Category.objects.get(name="Regular Pizza").pk
    )
    sicilians = MenuItem.objects.values_list("name", flat=True).filter(
        category_id=Category.objects.get(name="Sicilian Pizza").pk
    )
    toppings = Topping.objects.values_list("name", flat=True)
    subs = MenuItem.objects.values_list("name", flat=True).filter(
        category_id=Category.objects.get(name="Subs").pk
    )
    pastas = MenuItem.objects.values_list("name", flat=True).filter(
        category_id=Category.objects.get(name="Pasta").pk
    )
    salads = MenuItem.objects.values_list("name", flat=True).filter(
        category_id=Category.objects.get(name="Salads").pk
    )
    platters = MenuItem.objects.values_list("name", flat=True).filter(
        category_id=Category.objects.get(name="Dinner Platters").pk
    )

    # testing all categories of the pinochio's menu
    def test_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "pizza/menu.html")
        self.assertEqual(self.response["content-type"], "text/html; charset=utf-8")
        self.assertTrue(self.response.content.endswith(b"</html>"))

    def test_pinochio_menu_categories(self):
        self.assertTrue(
            all(
                bytes(category, encoding="utf-8") in self.response.content
                for category in self.categories
            )
        )

    def test_regular_pizzas(self):

        self.assertTrue(
            all(
                bytes(regular_pizza, encoding="utf-8") in self.response.content
                for regular_pizza in self.regulars
            )
        )

    def test_sicilian_pizzas(self):
        self.assertTrue(
            all(
                bytes(sicilian_pizza, encoding="utf-8") in self.response.content
                for sicilian_pizza in self.sicilians
            )
        )

    def test_pastas(self):
        self.assertTrue(
            all(
                bytes(pasta, encoding="utf-8") in self.response.content
                for pasta in self.pastas
            )
        )

    def test_salads(self):
        self.assertTrue(
            all(
                bytes(salad, encoding="utf-8") in self.response.content
                for salad in self.salads
            )
        )

    def test_platters(self):
        self.assertTrue(
            all(
                bytes(platter, encoding="utf-8") in self.response.content
                for platter in self.platters
            )
        )


@override_settings(
    AUTHENTICATION_BACKENDS=("orders.backends.EmailOrUsernameAuthBackend",)
)
class RegisterViewTestCase(TestCase):

    fixtures = ["orders_testdata.json"]
    c = Client()
    # a holder object to avoid duplicating code
    # only change the keys that are tested
    user_data = {
        "firstname": "John Doe",
        "lastname": "Doe",
        "email": "valid_email@domain.com",
        "username": "john_doe123",
        "password": "strongpw123",
    }

    def test_response(self):
        response = self.c.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "pizza/register.html")
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        self.assertTrue(response.content.endswith(b"</html>"))

    def test_valid_registeration(self):
        """first we test posting the data to return redirect
        then we test the content of the redirected response that will contain the
        greeting message asserting a successful registration
        """

        self.user_data["username"] = "john_doe123"
        self.user_data["email"] = "valid_email@domain.com"

        posting_data_response = self.c.post(
            reverse("register"), self.user_data, follow=False
        )
        redirect_response = self.c.post(
            reverse("register"), self.user_data, follow=True,
        )

        # redirecting to menu view and welcome the new user
        self.assertEqual(posting_data_response.status_code, 302)
        self.assertIn(b"john_doe123", redirect_response.content)

    def test_invalid_username(self):
        # wrong username field (i.e. contains whitespaces)
        self.user_data["username"] = "john doe123"
        self.user_data["email"] = "valid_email@domain.com"

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
        self.user_data["username"] = "nnn"
        self.user_data["email"] = "valid_email@domain.com"

        response = self.c.post(reverse("register"), self.user_data, follow=True,)

        self.assertEqual(
            response.context["username_feedback_message"],
            "This username already exists",
        )

    def test_invalid_email(self):
        # duplicate email
        self.user_data["username"] = "john_doe123"
        self.user_data["email"] = "test@test.com"  # duplicate in fixtures

        response = self.c.post(reverse("register"), self.user_data, follow=True,)

        self.assertEqual(
            response.context["email_feedback_message"], "This email is already in use",
        )

        # invalid email format
        self.user_data["username"] = "john_doe123"
        self.user_data["email"] = "Wrong email"

        response = self.c.post(reverse("register"), self.user_data, follow=True,)

        self.assertEqual(
            response.context["email_feedback_message"], "Invalid email format",
        )


@override_settings(DEBUG=True)
class LoginViewTestCase(TestCase):
    fixtures = ["orders_testdata.json"]
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
