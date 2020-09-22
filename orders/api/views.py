from rest_framework.views import APIView, Response
from rest_framework import status, generics
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


class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
