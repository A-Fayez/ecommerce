from django.urls import path
from orders.api.views import CategoryDetail, ProductList, ProductDetails, CategoryList

urlpatterns = [
    path("categories/<int:pk>", CategoryDetail.as_view(), name="category-endpoint"),
    path("categories", CategoryList.as_view(), name="categories-endpoint"),
    path("products", ProductList.as_view(), name="products-endpoint"),
    path("products/<int:pk>", ProductDetails.as_view(), name="product-endpoint"),
]
