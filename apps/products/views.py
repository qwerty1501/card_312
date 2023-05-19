from django.shortcuts import render
from rest_framework import generics

from .models import Products
from .serializers import ProductsSerializer


class ProductCreateListView(generics.ListCreateAPIView):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()
    
    
class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()