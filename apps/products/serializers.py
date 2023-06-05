from rest_framework import serializers as s

from .models import Products, Playbill, Afishaslider,Discountslider
from apps.partners.serializers import PartnersSerializer

class ProductsSerializer(s.ModelSerializer):

    class Meta:
        model = Products
        fields = ['partners', 'image', 'discounts', 'name', 'description', 'data', 'price', 'id']
        
class PlaybillSerializer(s.ModelSerializer):

    class Meta:
        model = Playbill
        fields = ['image', 'title', 'description', 'price', 'id']
    
    
class AfishasliderSerializer(s.ModelSerializer): 
    
    class Meta:
        model = Afishaslider
        fields = 'photo','description'
    
class DiscountsliderSerializer(s.ModelSerializer):
    class Meta:
        model = Discountslider
        fields = 'image','description','title'
    
    
