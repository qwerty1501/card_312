
from django.shortcuts import render
from rest_framework import generics

from apps.contact.models import Contacts
from apps.contact.serializers import ContactSerializer


class ContantsCreateListView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contacts.objects.all()


class ContantsDeteleView(generics.DestroyAPIView):
    serializer_class = Contacts
    queryset = Contacts.objects.all()