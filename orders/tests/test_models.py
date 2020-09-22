from django.test import TestCase
from orders.models import Category, ShoppingCart, CartItem
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class CartItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):

        c = Category.objects.create(name="Pizza")
        p = Category.objects.create(name="Pasta")
        CartItem.objects.create(name="test", price=10.0, category=c, quantity=2)
        CartItem.objects.create(name="foo", price=15.0, category=p, quantity=2)

    def test_string_representation(self):
        a = CartItem.objects.get(pk=1)
        b = CartItem.objects.get(pk=2)

        self.assertEqual(str(a), "test")
        self.assertEqual(str(b), "foo")

    def test_foreign_keys(self):
        a = CartItem.objects.get(pk=1)
        b = CartItem.objects.get(pk=2)

        self.assertIsInstance(a.category, Category)
        self.assertIsInstance(b.category, Category)
        self.assertEqual(str(a.category), "Pizza")
        self.assertEqual(str(b.category), "Pasta")

    def test_price_constraints(self):
        a = CartItem.objects.create(
            name="test", category=Category.objects.create(name="Pizza")
        )
        with self.assertRaises(ValidationError):
            a.clean()
            a.save()

    def test_total_price(self):
        a = CartItem.objects.get(pk=1)
        b = CartItem.objects.get(pk=2)
        self.assertEqual(a.total, 20.0)
        self.assertEqual(b.total, 30.0)


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="category")
        self.foo = CartItem.objects.create(
            category=self.c, name="foo", price="1.50", quantity=5
        )
        self.bar = CartItem.objects.create(
            category=self.c, name="bar", price="3.50", quantity=1
        )
        self.baz = CartItem.objects.create(
            category=self.c, name="baz", price="5.00", quantity=3
        )

        self.user = User.objects.create_user("john", "test@test.com", "password")
        self.cart = ShoppingCart.objects.create(user=User.objects.get(username="john"))

    def test_total_price(self):
        foo = CartItem.objects.get(name="foo")
        bar = CartItem.objects.get(name="bar")
        baz = CartItem.objects.get(name="baz")

        _cart = ShoppingCart.objects.get(user=User.objects.get(username="john"))
        _cart.items.add(foo, bar, baz)
        _cart.total = 26.00
        self.assertEqual(_cart.total, foo.total + bar.total + baz.total)
