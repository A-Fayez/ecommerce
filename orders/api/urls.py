from django.urls import path, include

from orders.api.views import (
    CategoriesAPIView,
    MenuItemAPIView,
    ItemsAPIView,
    CategoryAPIView,
    ShoppingCartAPIView,
)

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("categories/", CategoriesAPIView.as_view(), name="categories-api"),
    path("categories/<int:pk>", CategoryAPIView.as_view(), name="category-api"),
    path("menu-items/", ItemsAPIView.as_view(), name="menu-items-api"),
    path("menu-items/<int:pk>", MenuItemAPIView.as_view(), name="menu-item-api"),
    path("auth/", include("rest_auth.urls")),
    path("cart", ShoppingCartAPIView.as_view(), name="cart"),
    path("auth/token", obtain_auth_token, name="obtain-token"),
]
