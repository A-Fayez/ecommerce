from django.urls import path, include

from orders.api.views import (
    CategoryList,
    MenuItemDetail,
    MenuItemList,
    CategoryDetail,
    ShoppingCartAPIView,
)

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("categories/", CategoryList.as_view(), name="categories-api"),
    path("categories/<int:pk>", CategoryDetail.as_view(), name="category-api"),
    path("menu-items/", MenuItemList.as_view(), name="menu-items-api"),
    path("menu-items/<int:pk>", MenuItemDetail.as_view(), name="menu-item-api"),
    path("auth/", include("rest_auth.urls")),
    path("cart", ShoppingCartAPIView.as_view(), name="cart"),
    path("auth/token", obtain_auth_token, name="obtain-token"),
]
