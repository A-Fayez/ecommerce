from orders.models import Product, Category, Cart, CartItem
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "products"]


class CartItemSerializer(WritableNestedModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price", "total"]


class CartSerialzer(WritableNestedModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "date_created", "checked_out", "items"]
