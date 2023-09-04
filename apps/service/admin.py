from django.contrib import admin
from apps.service.models import ProductImage, Characteristic, AdditionalInformation, Product, PromotionType, Promotion


class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'type', 'created_date')
    list_filter = ('category', 'type', 'created_date')
    search_fields = ('user', 'title')
    list_display_links = list_display


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'promotion_type', 'created_date')
    list_display_links = list_display
    list_filter = ('promotion_type', 'start', 'end', 'created_date')
    search_fields = ('user', 'title')


admin.site.register(ProductImage)
admin.site.register(Characteristic)
admin.site.register(AdditionalInformation)
admin.site.register(Product, ProductAdmin)
admin.site.register(PromotionType)
admin.site.register(Promotion, PromotionAdmin)
