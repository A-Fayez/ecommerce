from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("login", views.login, name="login"),
    path("logout", views.login, name="logout"),
    path("register", views.register, name="register"),
    path("menu", views.menu, name="menu"),
]
