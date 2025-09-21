from rest_framework import serializers
from .models import Users, Cart, Cartitems, Products  # import Products

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["productid", "name", "price", "imagepath"]  # add more fields if needed


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source="productid", read_only=True)  # nest product

    class Meta:
        model = Cartitems
        fields = ["cartitemid", "quantity", "product"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cartitems_set", many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["cartid", "userid_id", "createdat", "items"]
