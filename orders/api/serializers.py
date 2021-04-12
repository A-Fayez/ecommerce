from orders.models import Product, Category, Cart, CartItem
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["name", "price"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "products"]


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(source="product.id")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=5, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product_price", "quantity", "total"]


class CartSerialzer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "date_created", "checked_out", "items"]

    def create(self, validated_data):
        cart_items = validated_data.pop("items")
        cart = Cart.objects.create(**validated_data)
        for item in cart_items:
            product_instance = Product.objects.get(id=item.get("product").get("id"))
            c = CartItem(price=item.get("product").get("price"), cart=cart,
                         product=product_instance, quantity=item.get("quantity"))
            c.save()

        return cart

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items")
        cart_items = []
        for item in items_data:
            product_instance = Product.objects.get(id=item.get("product").get("id"))
            c = CartItem(price=item.get("product").get("price"), cart=instance,
                         product=product_instance, quantity=item.get("quantity"))
            cart_items.append(c)

        instance.items.set(cart_items)

        instance.checked_out = validated_data.get("checked_out") == "true"
        instance.save()
        return instance

        # {
        #     "user": 2,
        #     "date_created": "2021-04-12",
        #     "checked_out": false,
        #     "items": [
        #         {
        #             "product_id": "624fb1ab-d468-43e5-9a66-12aa20a7905b",
        #             "product_price": 20.99,
        #             "quantity": 1,
        #             "total": 20.99
        #         },            {
        #             "product_id": "a9f2575c-2100-4fe5-b17a-e7fe203b59d9",
        #             "product_price": 5.99,
        #             "quantity": 1,
        #             "total": 5.99
        #         }
        #     ]
        # }
