from django.urls import path
from orders.api.views import (CategoryDetail, ProductList,
                              ProductDetails, CategoryList, CartList, CartDetail)

urlpatterns = [
    path("categories/<uuid:pk>", CategoryDetail.as_view(), name="category-endpoint"),
    path("categories", CategoryList.as_view(), name="categories-endpoint"),
    path("products", ProductList.as_view(), name="products-endpoint"),
    path("products/<uuid:pk>", ProductDetails.as_view(), name="product-endpoint"),
    path("carts", CartList.as_view(), name="carts-endpoint"),
    path("carts/<uuid:pk>", CartDetail.as_view(), name="cart-endpoint"),
]
