from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import uuid


class Category(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          editable=False, primary_key=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          editable=False, primary_key=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["name", "category"], name="unique product name per category")]

    def clean(self):
        super().clean()

        if not self.price:
            raise ValidationError(_("A menu Item must have a price"))

    def __str__(self):
        return f"Name: {self.name} - category: {self.category} - price: {self.price}"

    def __unicode__(self):
        return f"{self.name}"


class Cart(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"user: {self.user} - date: {self.date_created} - \
                checked out: {self.checked_out}"

    @property
    def total(self):
        if not self.items:
            return 0.00

        return sum(item.total for item in self.items.all())

    # TODO: add total property


class CartItem(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField(blank=False, null=False, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"items: {self.product} - price: {self.price} \
                - quantity: {self.quantity}"
