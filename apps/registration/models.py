from django.db import models

class Register(models.Model):
    
    class Meta:
        db_table = 'Регистрация'
        verbose_name = 'Регистрация пользователя'
        verbose_name_plural = 'Регистрация пользователя'

    email = models.EmailField(verbose_name=" Введите адрес электронной почты", max_length=32)
    number = models.CharField(verbose_name="Телефон", max_length=16)
    num_card = models.CharField(verbose_name="Номер карты", max_length=36)
    surname = models.CharField(verbose_name="Фамилия", max_length=16)
    name = models.CharField(verbose_name="Имя", max_length=16)
    
    password = models.CharField(verbose_name="Придумайте пароль", max_length=36)
    password_rep = models.CharField(verbose_name="Повторите пароль", max_length=36)

    def __str__(self):
        return self.email