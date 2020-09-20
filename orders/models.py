from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False, null=False, default=0.0
    )
    quantity = models.IntegerField(default=1)

    @property
    def total(self):
        return float(self.price) * self.quantity

    # A menu item must have at least a price
    def clean(self):
        super().clean()
        if not self.quantity:
            raise ValidationError(_("A menu Item must have at least a quantity of one"))

        if not self.price:
            raise ValidationError(_("A menu Item must have at least one price"))

    def __str__(self):
        return self.name


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    exclude = ["quantity"]


class Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, default=0.0
    )

    def __str__(self):
        return self.name


class OrderedItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    extras = models.ManyToManyField(Extra, blank=True, related_name="extras")

    def __str__(self):
        return f"{self.item} with {(list(self.extras) or '')}"


# The table will contain info about all orders made by users
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(MenuItem, related_name="ordered_items")
    total = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)

    @property
    def _total_from_items(self):
        _total = 0
        for item in self.items:
            _total = _total + item.total
        return _total

    def clean(self):
        super().clean()

        if self._total_from_items != self.total:
            raise ValidationError(_("Error: total price of items isn't consistent"))

        if not self.items:
            raise ValidationError(_("A shopping cart must have at least one item"))

    def __str__(self):
        return f"Order made by: {self.user} and contains {self.items}"
