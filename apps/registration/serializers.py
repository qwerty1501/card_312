from rest_framework import serializers as s
from .models import Register

class Register(s.ModelSerializer):
    
    class Meta:
        model = Register
        fields = '__all__'