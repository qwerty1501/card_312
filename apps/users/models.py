import uuid
import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from apps.users.managers import CustomManager

from apps.products.models import Products

from .services import get_upload_path, validate_file_extension


class Rename:
    def __init__(self, path):
        self.path = path;
        
    def rename(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (uuid.uuid4(), ext)
        return os.path.join(self.path, filename)


class User(AbstractUser):
    
    class Meta:
        # db_table = 'users_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    def __str__(self):
        return self.uniqueId.__str__();
    
    username = None;

    uniqueId = models.UUIDField(unique=True, verbose_name="Уникальный id", blank=True, null=True);

    logo = models.FileField(verbose_name='Загрузить фото *(150x150)', upload_to=get_upload_path, validators=[validate_file_extension], null=True, blank=True)
    email = models.EmailField(verbose_name='Почта', max_length=500, default=None, unique=True, blank=True, null=True)
    name = models.CharField(verbose_name='Имя', max_length=32)
    surname = models.CharField(verbose_name='Фамилия', max_length=32, blank=True, null=True)
    phone_one = models.CharField(verbose_name="Номер телефона", max_length=32, blank=True, null=True)
    dob = models.CharField(verbose_name='Дата рождения', max_length=16, blank=True, null=True)
    card = models.CharField(verbose_name='Номер дисконтной карты', max_length=16)
    password = models.CharField(verbose_name='Пароль', max_length=500)
    # REST_Password
    resetPasswordUUID = models.UUIDField(verbose_name="Ссылка для восстановления пароля", blank=True, null=True);
    resetPasswordDate = models.BigIntegerField(verbose_name="Время восстановления пароля", blank=True, null=True);
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    
    objects = CustomManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.uniqueId = uuid.uuid4()
        super(User, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        
        quantity = models.PositiveIntegerField(default=0)
        user = models.ForeignKey(Products,on_delete=models.CASCADE)
    
    
class Basket(models.Model):
    
    class Meta:
        verbose_name = 'Kорзина'
        verbose_name_plural = 'Kорзина'
    
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f'Корзина{self.user.username} | Корзина {self.product.name}'
        
    


class Mycard(models.Model):
    class Meta:
        verbose_name = 'Моя карта'
        verbose_name_plural = 'Моя карта'

    name = models.CharField(verbose_name='№ карты',max_length=32)
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class Bankcard(models.Model):
        class Meta:
            verbose_name = 'Добавить банковскую карту '
            verbose_name_plural ='Добавить банковскую карту '
            
        user = models.ForeignKey("User",on_delete=models.CASCADE)    
        numcard = models.CharField(verbose_name='Номер карты', max_length=64)
        period = models.BooleanField(verbose_name='Срок действия карты', max_length=12)
        name_plural = models.CharField(verbose_name='Имя владельца', max_length=32)
        code = models.BooleanField(verbose_name='Код CVC/CVV', max_length=12)
        email = models.EmailField(verbose_name='Email', max_length=64, default=None, unique=True, blank=True, null=True)
        
        def __str__(self):
            return self.name_plural
        
class Subscr(models.Model):
        
        class Meta:
            verbose_name = 'Подписки'
            verbose_name_plural = 'Подписки'
            
            
        user = models.ForeignKey("User",on_delete=models.CASCADE)
        image = models.ImageField(verbose_name='Фотография', upload_to='apps/images/users')    
        name = models.CharField(verbose_name="Название", max_length=50)
        
        def __str__(self):
            return self.name
        
        
class Coment(models.Model):
        
        class Meta:
            verbose_name = 'Мои комментарии'
            verbose_name_plural = 'Мои комментарии'
            
        user = models.ForeignKey("User",on_delete=models.CASCADE)
        image = models.ImageField(verbose_name='Фотография', upload_to='apps/images/users')    
        name = models.CharField(verbose_name="Oписание", max_length=50)
        
        def __str__(self):
            return self.name
        
        
        
        
class Like(models.Model):
        
        class Meta:
            verbose_name = 'Лайки'
            verbose_name_plural = 'Лайки'
            
        post = models.ForeignKey("User", on_delete=models.CASCADE)
        image = models.ImageField(verbose_name='Фотография *(200x160)', upload_to='apps/images/users' , max_length=32, blank=True, null=True)    
        name = models.CharField(verbose_name="Лайки", max_length=32, blank=True, null=True)
        title = models.CharField(max_length=32, blank=True, null=True)
        likes = models.BooleanField(default=False)

        def __str__(self):
            return f'{self.likes}'
        
        
        
        
class Post(models.Model):
    '''данные о посте'''
    title = models.CharField('Заголовок записи', max_length=100)
    description = models.TextField('Текст записи')
    author = models.CharField('Имя автора', max_length=100)
    date = models.DateField('Дата публикации')
    img = models.ImageField("Изображение", upload_to='image/%Y')

    def __str__(self):
        return f'{self.title}, {self.author}'
    
    
    
            
class Likes(models.Model):
    '''лайки'''
    ip = models.CharField('IP-адрес', max_length=100)
    pos = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)


class Favorites(models.Model):
        
        class Meta:
            verbose_name = 'Избранное'
            verbose_name_plural = 'Избранное'
            
        user = models.ForeignKey("User",on_delete=models.CASCADE)
        like = models.ForeignKey("Post",on_delete=models.CASCADE)
        image = models.ImageField(verbose_name='Фотография *(400x167)', upload_to='apps/images/users')    
        name = models.CharField(verbose_name="Название", max_length=50)
        name_one = models.CharField(verbose_name="Oписание" , max_length=999)
        
        def __str__(self):
            return self.name
    
    
    
    
