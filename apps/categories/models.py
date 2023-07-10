from django.db import models

from .services import get_upload_path, validate_file_extension
# from apps.categories import Service_category , Product_category, Sale_category
from apps.categories.choices import Size

class Service_category(models.Model):
    
    
    class Meta:
        db_table = 'service_category'
        verbose_name = 'Категория Услуг'
        verbose_name_plural = 'Категории Услуг'
        
    
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    size = models.CharField(verbose_name="Размер", max_length=100, default=None, choices=Size, blank=True, null=True)
    name = models.CharField(verbose_name="Название категории для", max_length=255)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    icon = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension], null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
    
    
    
class Product_category(models.Model):
    
    
    class Meta:
        db_table = 'product_category'
        verbose_name = 'Категория Товар'
        verbose_name_plural = 'Категории Товар'
        
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    name = models.CharField(verbose_name="Название категории для", max_length=255)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    icon = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension], null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
    
    
    
class Sale_category(models.Model):
        
        
    class Meta:
        
        db_table = 'sale_category'
        verbose_name = 'Категория Акции'
        verbose_name_plural = 'Категории Акции'
        
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    name = models.CharField(verbose_name="Название категории для", max_length=255)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    icon = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension], null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'
    
    
    
    