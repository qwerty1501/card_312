from django.db import models


class ProductImage(models.Model):
    photo = models.ImageField(upload_to='media/service/product')

    class Meta:
        verbose_name = 'Фото для продукта'
        verbose_name_plural = 'Фотки для продукта'


class Characteristic(models.Model):
    category = models.ForeignKey('categories.Service_category', on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=223, verbose_name='Название')

    def __str__(self):
        return f'{self.category} --> {self.title}'

    class Meta:
        verbose_name = 'Характеристика для Услуги'
        verbose_name_plural = 'Характеристики для Услуги'


class AdditionalInformation(models.Model):
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    description = models.CharField(max_length=225)

    def __str__(self):
        return f"{self.characteristic} - {self.description}"

    class Meta:
        verbose_name = 'Доп. информация для характеристики '
        verbose_name_plural = 'Доп. информации для характеристики'


class Product(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Партнер')
    title = models.CharField(max_length=223, verbose_name='Название Товара/Услуги')
    category = models.ForeignKey('categories.Service_category', on_delete=models.CASCADE, verbose_name='Категория')
    images = models.ManyToManyField(ProductImage, verbose_name='Фото', blank=True, null=True)
    city = models.CharField(max_length=223, verbose_name='Город')
    description = models.TextField(verbose_name='Описание')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во')
    characteristic = models.ManyToManyField(AdditionalInformation, verbose_name='Доп. инфо')
    price = models.DecimalField(
        verbose_name='Цена',
        decimal_places=2,
        max_digits=12,
        default=0.00
    )
    type = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Товар'),
            (2, 'Услуга'),
        )
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'

    def __str__(self):
        return f"{self.title}"


class PromotionType(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип скидки или акции'
        verbose_name_plural = 'Тип скидки или акции:'


class Promotion(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Партнер')
    promotion_type = models.ForeignKey(PromotionType, on_delete=models.CASCADE, verbose_name='Выберите тип скидки или акции')
    title = models.CharField(max_length=223, verbose_name='Название скидки или акции')
    description = models.TextField(verbose_name='Условия и требования акции/скидки')
    limitation = models.PositiveIntegerField(verbose_name='Ограничения по количеству')
    start = models.DateField(verbose_name='Начало акции')
    end = models.DateField(verbose_name='Конец акции')
    old_price = models.DecimalField(
        verbose_name='Цена до скидки или акции',
        decimal_places=2,
        max_digits=12,
        default=0.00
    )
    new_price = models.DecimalField(
        verbose_name='Цена со скидкой',
        decimal_places=2,
        max_digits=12,
        default=0.00
    )
    percentage_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Количество процента'
    )
    cashback_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Количество кэшбека'
    )
    products = models.ManyToManyField(Product, verbose_name='Выберите товар/услугу для акций и скидки')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Акция/Скидка'
        verbose_name_plural = 'Акции/Скидки'
