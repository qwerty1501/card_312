from rest_framework import serializers as s

from .models import Products


class ProductsSerializer(s.ModelSerializer):

    class Meta:
        model = Products
        fields = ['partners', 'image', 'discounts', 'name', 'description', 'data', 'price', 'id']