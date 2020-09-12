from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .validators import (
    validate_login_key,
    LoginError,
    UsernameValidationError,
    EmailValidationError,
)
from .models import (
    Category,
    MenuItem,
)
from .validators import validate_email_address, validate_username


# Create your views here.
def index(request):
    return render(request, "pizza/homepage.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            validate_login_key(username)  # Throws a LoginError

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse("menu"))
            else:
                return render(request, "pizza/login.html", {"invalid": True})

        except LoginError as e:
            print(e)
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
                username=username,
                password=password,
                email=email,
            )
            user.save()
            authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("menu"))

        except UsernameValidationError as e:
            print(e)
            context = {
                f"{e.code}_validity_class": "is-invalid",
                f"{e.code}_feedback_class": "invalid-feedback",
                f"{e.code}_feedback_message": e.message,
            }
            return render(request, "pizza/register.html", context)

        except EmailValidationError as e:
            print(e)
            context = {
                f"{e.code}_validity_class": "is-invalid",
                f"{e.code}_feedback_class": "invalid-feedback",
                f"{e.code}_feedback_message": e.message,
            }

            return render(request, "pizza/register.html", context)

    return render(request, "pizza/register.html")


# cache menu daily
# @cache_page(24 * 60 * 60)
def menu(request):
    # print(request.COOKIES["sessionid"])

    menu_dict = {}
    items = MenuItem.objects.all()
    categories = Category.objects.all()

    for category in categories:
        menu_dict.update(
            {
                category.name: items.filter(
                    category_id=Category.objects.get(name=category.name).pk
                )
            }
        )

    context = {
        "menu": menu_dict,
    }
    return render(request, "pizza/menu.html", context)


def cart(request):
    return render(request, "pizza/shopping_cart.html")
