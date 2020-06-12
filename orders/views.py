from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.views.decorators.cache import cache_page

# Create your views here.
def index(request):
    return render(request, "pizza/homepage.html")


def login(request):
    return render(request, "pizza/login.html")


def register(request):
    return render(request, "pizza/register.html")


# cache menu daily
@cache_page(24 * 60 * 60)
def menu(request):
    # utilize caching of querysets
    regulars = MenuItem.objects.filter(
        category_id=Category.objects.get(name="Regular Pizza").pk
    )
    sicilians = MenuItem.objects.filter(
        category_id=Category.objects.get(name="Sicilian Pizza").pk
    )
    toppings = Topping.objects.all()
    subs = MenuItem.objects.filter(category_id=Category.objects.get(name="Subs").pk)
    pastas = MenuItem.objects.filter(category_id=Category.objects.get(name="Pasta").pk)
    salads = MenuItem.objects.filter(category_id=Category.objects.get(name="Salads").pk)
    platters = MenuItem.objects.filter(
        category_id=Category.objects.get(name="Dinner Platters").pk
    )

    context = {
        "regulars": regulars,
        "sicilians": sicilians,
        "toppings": toppings,
        "subs": subs,
        "pastas": pastas,
        "salads": salads,
        "platters": platters,
    }
    return render(request, "pizza/menu.html", context)
