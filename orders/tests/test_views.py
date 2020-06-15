from django.test import TestCase, Client
from django.urls import reverse

# from orders.models import Category


class HomepageTestCase(TestCase):

    def test_response(self):
        c = Client()
        response = c.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)


class MenuTestCase(TestCase):
    fixtures = ["orders_testdata.json"]

    def test_index(self):
        c = Client()
        response = c.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Regular Pizza" in str(response.content))
