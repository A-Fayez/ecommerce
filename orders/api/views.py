from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status


from orders.models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class ShoppingCartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class MenuItemAPIView(APIView):
    def get(self, request, pk):
        try:
            queryset = MenuItem.objects.get(pk=pk)
            serializer = MenuItemSerializer(queryset)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = Category.objects.all()
            serialzier = CategorySerializer(queryset, many=True)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialzier.data)
