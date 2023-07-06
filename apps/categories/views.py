from django.shortcuts import render

from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter

from .models import Service_category , Product_category, Sale_category
from .serializers import Service_categorySerializer, Product_categorySerializer, Sale_categorySerializer


# CATEGORY 1 ----------------------------------------------------------
class Service_categoryList(generics.ListAPIView):
    queryset = Service_category.objects.filter(parent__isnull=True). \
        select_related('parent'). \
        prefetch_related('children',
                         'children__children',
                         'children__children__children')
    serializer_class = Service_categorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class Service_categoryRetrieve(generics.RetrieveAPIView):
    queryset = Service_category.objects.filter()

    serializer_class = Service_categorySerializer
    
# 2 ----------------------------------------------------------------
    
class Product_categoryList(generics.ListAPIView):
    queryset = Product_category.objects.filter(parent__isnull=True). \
        select_related('parent'). \
        prefetch_related('children',
                         'children__children',
                         'children__children__children')
    serializer_class = Product_categorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class Product_categoryRetrieve(generics.RetrieveAPIView):
    queryset = Product_category.objects.filter()

    serializer_class = Product_categorySerializer
    
    
#3 ----------------------------------------------------------------

class Sale_categoryList(generics.ListAPIView):
    queryset = Sale_category.objects.filter(parent__isnull=True). \
        select_related('parent'). \
        prefetch_related('children',
                         'children__children',
                         'children__children__children')
    serializer_class = Sale_categorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class Sale_categoryRetrieve(generics.RetrieveAPIView):
    queryset = Sale_category.objects.filter()

    serializer_class = Sale_categorySerializer