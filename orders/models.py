from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# add-ons on the subs
class Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.price}"


class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    large_price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name}, small: {self.small_price}, large: {self.large_price}"


class OrderedItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings")
    extras = models.ManyToManyField(Topping, blank=True, related_name="extras")

    def __str__(self):
        return (
            f"{self.item} with {(list(self.toppings) or '') (list(self.extras) or '')}"
        )


# The table will contain info about all orders made by users
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, related_name="ordered_items")

    def __str__(self):
        return f"Order made by: {self.user} and contains {list(self.items)}"
