from django.db import models


class EventImage(models.Model):
    image = models.ImageField(upload_to='media/event', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото для Мероприятия'
        verbose_name_plural = 'Фотоки для Мероприятия'


class Event(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Партнер')
    title = models.CharField(max_length=225, verbose_name='Заголовок')
    location = models.CharField(max_length=500, verbose_name='Место')
    date = models.DateTimeField(verbose_name='Дата и время')
    description = models.TextField(verbose_name='Описание')
    start_price = models.DecimalField(
        verbose_name='Стоимость от',
        decimal_places=2,
        max_digits=12,
        default=0.00
    )
    end_price = models.DecimalField(
        verbose_name='Стоимость до',
        decimal_places=2,
        max_digits=12,
        default=0.00
    )
    photo = models.ManyToManyField(EventImage, verbose_name='Фото')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'





