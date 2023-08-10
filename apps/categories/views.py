from django.shortcuts import render

from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter

from .models import Service_category
from .serializers import Service_categorySerializer


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
  