from django.contrib.auth.models import User
from rest_framework import serializers
from orders.models import ShoppingCart, MenuItem, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = ShoppingCart
        fields = ["id", "items", "total", "user"]


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price", "category"]


class CategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "menu_items"]
