from django.test import TestCase
from orders.models import Category, MenuItem
from django.core.exceptions import ValidationError


class MenuItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):

        c = Category.objects.create(name="Pizza")
        p = Category.objects.create(name="Pasta")
        MenuItem.objects.create(
            name="test", small_price=5.0, large_price=10.0, category=c
        )
        MenuItem.objects.create(name="foo", price=15.0, category=p)

    def test_string_representation(self):
        a = MenuItem.objects.get(pk=1)
        b = MenuItem.objects.get(pk=2)

        self.assertEqual(str(a), "test, small: 5.00, large: 10.00")
        self.assertEqual(str(b), "foo, price: 15.00")

    def test_foreign_keys(self):
        a = MenuItem.objects.get(pk=1)
        b = MenuItem.objects.get(pk=2)

        self.assertIsInstance(a.category, Category)
        self.assertIsInstance(b.category, Category)
        self.assertEqual(str(a.category), "Pizza")
        self.assertEqual(str(b.category), "Pasta")

    def test_price_constraints(self):
        a = MenuItem.objects.create(
            name="test", category=Category.objects.create(name="Pizza")
        )
        with self.assertRaises(ValidationError):
            a.save()
