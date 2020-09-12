from django.urls import path
from orders.api.views import CategoryAPIView

urlpatterns = [
    path("categories/", CategoryAPIView.as_view(), name="categories-api"),
]
