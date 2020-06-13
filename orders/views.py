from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from .models import (
    Category,
    MenuItem,
    Topping,
)
from django.views.decorators.cache import cache_page
from django.db import IntegrityError
from .validators import validate_email_address, validate_username


# Create your views here.
def index(request):
    return render(request, "pizza/homepage.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user=user)
            return render(request, "pizza/menu.html")  # TODO: render necessary view
        else:
            return render(request, "pizza/login.html", {"invalid": True})

    return render(request, "pizza/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def register(request):

    if request.method == "POST":
        try:
            email = request.POST["email"]
            validate_email_address(email)

            username = request.POST["username"]
            validate_username(username)

            first = request.POST["firstname"]
            last = request.POST["lastname"]
            password = request.POST["password"]

            user = User.objects.create_user(
                first_name=first,
                last_name=last,
                email=email,
                password=password,
                username=username,
            )
            user.save()
            # TODO: redirect to menu
            return HttpResponse("User created succefully")

        except IntegrityError as e:
            print(e)
            context = {
                "username_validity_class": "is-invalid",
                "username_feedback_class": "invalid-feedback",
                "username_feedback_message": "This username already exists",
            }
            return render(request, "pizza/register.html", context)

        except ValidationError as e:

            context = {
                f"{e.code}_validity_class": "is-invalid",
                f"{e.code}_feedback_class": "invalid-feedback",
                f"{e.code}_feedback_message": e.message,
            }

            return render(request, "pizza/register.html", context)

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
