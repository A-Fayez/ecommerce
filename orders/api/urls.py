from django.urls import path
from orders.api.views import (
    CategoriesAPIView,
    MenuItemAPIView,
    ItemsAPIView,
    CategoryAPIView,
)

urlpatterns = [
    path("categories/", CategoriesAPIView.as_view(), name="categories-api"),
    path("categories/<int:pk>", CategoryAPIView.as_view(), name="category-api"),
    path("menu-items/", ItemsAPIView.as_view(), name="menu-items-api"),
    path("menu-items/<int:pk>", MenuItemAPIView.as_view(), name="menu-item-api"),
]
