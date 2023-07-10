from django.contrib import admin

from .models import Service_category, Product_category, Sale_category


admin.site.register(Service_category)
admin.site.register(Product_category)
admin.site.register(Sale_category)

