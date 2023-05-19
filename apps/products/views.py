from django.shortcuts import render
from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer


class ProductCreateListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    
class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()