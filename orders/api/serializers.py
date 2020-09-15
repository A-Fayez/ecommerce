from django.contrib.auth.models import User, Group
from rest_framework import serializers
from orders.models import ShoppingCart, MenuItem, Category


class ShoppingCartSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: associate user
    class Meta:
        model = ShoppingCart
        fields = ["id", "items", "total"]


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ["id", "category", "name", "price"]


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
