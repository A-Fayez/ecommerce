from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from orders.models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer

from django.contrib.auth.models import User


class ShoppingCartAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            queryset = User.objects.all()
            serialzier = UserSerializer(queryset)

            if not serialzier.data:
                return Response({"details": "This user has no active carts yet"})

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialzier.data)


class ItemsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = MenuItem.objects.all()
            serialzier = MenuItemSerializer(queryset, many=True)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialzier.data)


class MenuItemAPIView(APIView):
    def get(self, request, pk):
        try:
            queryset = MenuItem.objects.get(pk=pk)
            serializer = MenuItemSerializer(queryset)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)


class CategoriesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = Category.objects.all()
            serialzier = CategorySerializer(queryset, many=True)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialzier.data)


class CategoryAPIView(APIView):
    def get(self, request, pk):
        try:
            queryset = Category.objects.get(pk=pk)
            serializer = CategorySerializer(queryset)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)
