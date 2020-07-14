from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "orders_category"

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

    # A menu item must have at least a price
    def clean(self):
        super().clean()

        if not self.small_price and not self.large_price and not self.price:
            raise ValidationError(_("A menu Item must have at least one price"))

    def __str__(self):

        if not self.price:
            return f"{self.name}, small: {self.small_price}, large: {self.large_price}"

        if not self.small_price and not self.large_price:
            return f"{self.name}, price: {self.price}"


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
