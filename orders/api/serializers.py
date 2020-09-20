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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ["id", "category", "name", "price"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
