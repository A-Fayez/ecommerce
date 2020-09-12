from django.urls import path
from orders.api.views import CategoryAPIView, MenuItemAPIView

urlpatterns = [
    path("categories/", CategoryAPIView.as_view(), name="categories-api"),
    path("menu-items/<int:pk>", MenuItemAPIView.as_view(), name="categories-api"),
]
