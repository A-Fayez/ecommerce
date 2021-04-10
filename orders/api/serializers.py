from orders.models import Product, Category
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Product
        fields = ["name", "price", "category"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'products']
