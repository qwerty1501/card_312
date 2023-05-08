from django.db import models

from apps.categories.models import Category
from apps.partners.models import Partners


class Products(models.Model):
    partners = models.ForeignKey(Partners, verbose_name=Партнёр, on_delete=models.CASCADE)
    discounts = models.CharField(verbose_name="Скидки", max_length=16, blank=True, null=True)
    