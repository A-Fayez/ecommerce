from rest_framework import generics, permissions
from rest_framework.views import APIView
from orders.models import Category, Product, Cart
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import (CategorySerializer, ProductSerializer,
                          CartSerialzer, UserSerializer)


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetails(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerialzer


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    queryset = Cart.objects.all()
    serializer_class = CartSerialzer


class UserDetail(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
