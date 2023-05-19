from rest_framework import serializers as s

from .models import Product


class ProductSerializer(s.ModelSerializer):

    class Meta:
        model = Product
        fields = ['partners', 'image', 'discounts', 'name', 'description', 'data', 'price', 'id']