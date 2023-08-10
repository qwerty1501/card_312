from django.shortcuts import render

from rest_framework import generics
from .models import Register
from .serializers import RegisterSerializer


class RegisterCreateListView(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()


class RegisterView(generics.DestroyAPIView):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()