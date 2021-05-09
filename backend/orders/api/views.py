from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from orders.models import Category, Product, Cart, Payment
from django.contrib.auth.models import User
from .serializers import (CategorySerializer, ProductSerializer,
                          CartSerialzer,)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


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
    throttle_scope = "payment"

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

        cart.checked_out = True
        Payment.objects.create(cart=cart, amount=amount)

        return Response({
            "message":
            "You've successfuly completed payment"},
            status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    throttle_scope = "register"

    def post(self, request, *args, **kwargs):
        if not request.data["username"] \
                or not request.data["password"] \
                or not request.data["first_name"] \
                or not request.data["last_name"]:

            return Response({"message": "Missing required fields for registration"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=request.data["username"], password=request.data["password"],
                                   first_name=request.data["first_name"], last_name=request.data["last_name"])

        token = RefreshToken.for_user(user)
        return Response({"refresh": str(token), "access": str(token.access_token)})


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
