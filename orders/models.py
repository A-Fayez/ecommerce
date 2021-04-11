from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    # A menu item must have at least a price
    def clean(self):
        super().clean()

        if not self.price:
            raise ValidationError(_("A menu Item must have a price"))

    def __str__(self):
        return f"Name: {self.name} - category: {self.category} - price: {self.price}"

    def __unicode__(self):
        return f"{self.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField()
    checked_out = models.BooleanField()

    def __str__(self):
        return f"user: {self.user} - date: {self.date_created} - \
                checked out: {self.checked_out}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"items: {self.product} - price: {self.price} \
                - quantity: {self.quantity}"
