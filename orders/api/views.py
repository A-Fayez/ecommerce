from rest_framework.views import APIView
from rest_framework.views import Response

from orders.models import ShoppingCart, Category
from .serializers import CategorySerializer


class ShoppingCartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serialzier = CategorySerializer(queryset, many=True)
        return Response(serialzier.data)
