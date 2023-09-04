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
    name = models.CharField(verbose_name="Название категории", max_length=255)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    icon = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension], null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
