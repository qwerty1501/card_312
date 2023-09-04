import uuid
import os

from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.users.managers import CustomManager
from .services import get_upload_path, validate_file_extension
from .choices import Day


class Rename:
    def __init__(self, path):
        self.path = path
        
    def rename(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (uuid.uuid4(), ext)
        return os.path.join(self.path, filename)


class User(AbstractUser):
    
    class Meta:
        # db_table = 'users_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Все пользователи'

    def __str__(self):
        return self.name
    
    username = None

    uniqueId = models.UUIDField(unique=True, verbose_name="Уникальный id", blank=True, null=True)

    logo = models.FileField(verbose_name='Загрузить фото *(150x150)', upload_to=get_upload_path, validators=[validate_file_extension], null=True, blank=True)
    email = models.EmailField(verbose_name='Почта', max_length=500, default=None, unique=True)
    name = models.CharField(verbose_name='Имя', max_length=32)
    balance = models.DecimalField(
        verbose_name='Баланс',
        decimal_places=2,
        max_digits=12,
        default=0.00,
        blank=True,
        null=True
    )
    password = models.CharField(verbose_name='Пароль', max_length=500)
    user_type = models.PositiveSmallIntegerField(choices=(
        (1, 'Обычный пользователь'),
        (2, 'Партнер')),
        default=1,
        verbose_name='Тип пользователя')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    # REST_Password
    resetPasswordUUID = models.UUIDField(verbose_name="Ссылка для восстановления пароля", blank=True, null=True)
    resetPasswordDate = models.BigIntegerField(verbose_name="Время восстановления пароля", blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    
    objects = CustomManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.set_password(self.password)

        if not self.id:
            self.uniqueId = uuid.uuid4()
        super(User, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class BasicUser(User):
    class Meta:
        # db_table = 'users_user'
        verbose_name = 'Обычный пользователь'
        verbose_name_plural = 'Обычные пользователи'

    def __str__(self):
        return f"{self.name} {self.last_name}"

    phone_number = models.CharField(verbose_name="Номер телефона", max_length=32, blank=True, null=True)
    dob = models.CharField(verbose_name='Дата рождения', max_length=16, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Мужской'),
            (2, 'Женский'),
            (3, 'Другое'),
        ),
        verbose_name='Пол',
        blank=True,
        null=True
    )
    profession = models.CharField(max_length=500, verbose_name='Профессия', blank=True, null=True)
    city = models.CharField(max_length=223, verbose_name='Город', blank=True, null=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', blank=True, null=True)
    is_animals = models.BooleanField(verbose_name='Наличие животных', default=False)
    is_children = models.BooleanField(verbose_name='Наличие детей', default=False)


class Partners(User):
    class Meta:
        db_table = 'partners'
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёр'

    image = models.FileField(verbose_name='Загрузить фон *(305x210)', upload_to=get_upload_path,
                             validators=[validate_file_extension], null=True, blank=True)
    address = models.CharField(verbose_name='Адрес компании', max_length=64)
    org = models.CharField(verbose_name='Организационная правовая форма', max_length=64)
    inn = models.CharField(verbose_name='ИНН', max_length=16)
    activity_type = models.CharField(verbose_name='Тип деятельности', max_length=64)
    description = models.TextField(verbose_name='Описание компании')

    # Телефонный номер и социальные сети
    phone_one = models.CharField(verbose_name="Номера телефонов", max_length=32)
    phone_two = models.CharField(verbose_name="", max_length=32, blank=True, null=True)
    phone_three = models.CharField(verbose_name="", max_length=32, blank=True, null=True)
    phone_four = models.CharField(verbose_name="", max_length=32, blank=True, null=True)

    ##########################################
    whatsapp = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    day = models.CharField(
        verbose_name="Режим работы",
        max_length=16,
        default=None,
        choices=Day,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user_type == 1:
            self.user_type = 2
        return super().save(*args, **kwargs)


class Basket(models.Model):
    
    class Meta:
        verbose_name = 'Kорзина'
        verbose_name_plural = 'Kорзина'
    
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f'Корзина{self.user.username} | Корзина {self.product.name}'


class Mycard(models.Model):
    class Meta:
        verbose_name = 'Моя карта'
        verbose_name_plural = 'Моя карта'

    name = models.CharField(verbose_name='№ карты', max_length=32)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    
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


# лайки
class Likes(models.Model):
    ip = models.CharField('IP-адрес', max_length=100)
    pos = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)


class Favorites(models.Model):
        
        class Meta:
            verbose_name = 'Избранное'
            verbose_name_plural = 'Избранное'
            
        user = models.ForeignKey("User", on_delete=models.CASCADE)
        like = models.ForeignKey("Post", on_delete=models.CASCADE)
        image = models.ImageField(verbose_name='Фотография *(400x167)', upload_to='apps/images/users')    
        name = models.CharField(verbose_name="Название", max_length=50)
        name_one = models.CharField(verbose_name="Oписание", max_length=999)
        
        def __str__(self):
            return self.name

    
    
    
