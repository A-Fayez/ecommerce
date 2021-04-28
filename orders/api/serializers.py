from orders.models import Product, Category, Cart, CartItem, Payment
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"],
                                   first_name=validated_data["first_name"],
                                   last_name=validated_data["last_name"])

        user.set_password(validated_data["password"])
        user.save()

        return user

    def validate(self, data):
        if not data["username"] \
                or not data["password"] \
                or not data["first_name"] \
                or not data["last_name"]:
            raise serializers.ValidationError("Missing required fields")
        return data


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


class CartSerialzer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "date_created", "checked_out", "items", "total"]

    def create(self, validated_data):
        try:
            checked_out = validated_data.get("checked_out")
        except KeyError:
            raise serializers.ValidationError("Missing checked_out field")

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
                    "Product does not exist or it's not being served at the moment")

        return cart

    def update(self, instance, validated_data):
        checked_out = validated_data.get("checked_out")
        instance.checked_out = checked_out

        # TODO: implement this in a more efficient way
        # Either implement a diffing algorithm or use event sourcing
        CartItem.objects.filter(cart=instance).delete()
        for cart_item in validated_data.get("items"):
            try:
                product_id = cart_item.get("product").get("id")
                quantity = cart_item.get("quantity", 1)
                product = self._get_associated_product(product_id)
                product_price = product.price
                cart_item_instance = CartItem.objects.create(
                    price=product_price, cart=instance, product=product,
                    quantity=quantity)
                instance.items.add(cart_item_instance)
            except KeyError:
                raise serializers.ValidationError(
                    "Product does not exist or it's not being served at the moment")

        instance.save()
        return instance

    def _get_associated_product(self, pk):
        try:
            print(pk)
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            print("in associated product method")
            raise serializers.ValidationError(
                "Product does not exist or it's not being served at the moment")
