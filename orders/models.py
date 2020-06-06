from django.db import models

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(blank=True)


# add-ons on the subs
class Extra(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()


class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
    toppings = models.ManyToManyField(Topping)


class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
    toppings = models.ManyToManyField(Topping)


class Sub(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
    extras = models.ManyToManyField(Sub)


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField()


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField()


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
