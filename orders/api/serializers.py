from orders.models import Product, Category, Cart, CartItem
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["name", "price"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "products"]


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source="product.name")
    price = serializers.ReadOnlyField(source="product.price")

    class Meta:
        model = CartItem
        fields = ["product", "price", "quantity"]


class CartSerialzer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["user", "date_created", "checked_out", "items"]
