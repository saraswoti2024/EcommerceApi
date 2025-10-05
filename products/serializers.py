from .models import Product,CartItem,WishlistItem
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["id", "product"]