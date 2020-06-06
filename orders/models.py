from django.db import models

# Create your models here.  
class Topping(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(blank=True)

    def __str__(self):
        print(f"{self.name}: {self.price}")


# add-ons on the subs
class Extra(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()

    def __str__(self):
        print(f"{self.name} small: {self.small_price}, large: {self.large_price}")


class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        print(f"{self.name}, small: {self.small_price}, large: {self.large_price}")


class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        print(f"{self.name}, small: {self.small_price}, large: {self.large_price}")


class Sub(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()
    extras = models.ManyToManyField(Sub)

    def __str__(self):
        print(f"{self.name} small: {self.small_price}, large: {self.large_price}")


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField()

    def __str__(self):
        print(f"{self.name}: {self.price}")


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField()

    def __str__(self):
        print(f"{self.name}: {self.price}")


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField()
    large_price = models.DecimalField()

     def __str__(self):
        print(f"{self.name} small: {self.small_price}, large: {self.large_price}")
