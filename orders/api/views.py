from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status


from orders.models import Category, MenuItem
from .serializers import CategoriesSerializer, MenuItemSerializer


class ShoppingCartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass


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
            serialzier = CategoriesSerializer(queryset, many=True)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialzier.data)
