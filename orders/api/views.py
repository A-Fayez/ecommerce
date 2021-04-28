from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from orders.models import Category, Product, Cart, Payment
from django.contrib.auth.models import User
from .serializers import (CategorySerializer, ProductSerializer,
                          CartSerialzer, UserSerializer,)
from rest_framework.response import Response


import stripe
import os
import math

stripe.api_key = os.environ.get("STRIPE_API_KEY")


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class PaymentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        cart_id = request.data.get("cart_id")
        amount = request.data.get("amount")

        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"message": "cart does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        stripe.PaymentIntent.create(
            amount=math.ceil(cart.total),
            currency='gbp',
            payment_method_types=['card'],
            receipt_email=self.request.user.email,
        )

        Payment.objects.create(cart=cart, amount=amount)

        return Response({
            "message":
            "You've successfuly completed payment"},
            status=status.HTTP_201_CREATED)


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
