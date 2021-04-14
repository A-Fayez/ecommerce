from orders.models import Product, Category, Cart, CartItem
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "products"]


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(source="product.id")
    product_name = serializers.CharField(
        max_length=64, source="product.name")
    product_price = serializers.DecimalField(
        max_digits=5, decimal_places=2, source="product.price")

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product_name",
                  "product_price", "quantity", "total"]


class CartSerialzer(WritableNestedModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "date_created", "checked_out", "items", "total"]

    def create(self, validated_data):
        checked_out = validated_data.get("checked_out")
        user = validated_data.get("user")
        cart = Cart.objects.create(user=user, checked_out=checked_out)

        for cart_item in validated_data.get("items"):
            try:
                product_id = cart_item.get("product").get("id")
                quantity = cart_item.get("quantity", 1)
                product = self._get_associated_product(product_id)
                product_price = product.price
                cart_item_instance = CartItem.objects.create(
                    price=product_price, cart=cart, product=product, quantity=quantity)
                cart.items.add(cart_item_instance)
            except KeyError:
                raise serializers.ValidationError(
                    "Bad Request: \
                     Product does not exist or it's not being served at the moment")

        return cart

    def _get_associated_product(self, pk):
        try:
            print(pk)
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            print("in associated product method")
            raise serializers.ValidationError(
                "Bad Request: \
                 Product does not exist or it's not being served at the moment")
