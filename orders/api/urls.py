from django.urls import path
from orders.api.views import CategoriesAPIView, MenuItemAPIView, ItemsAPIView

urlpatterns = [
    path("categories/", CategoriesAPIView.as_view(), name="categories-api"),
    path("menu-items/", ItemsAPIView.as_view(), name="menu-items-api"),
    path("menu-items/<int:pk>", MenuItemAPIView.as_view(), name="menu-item-api"),
]
