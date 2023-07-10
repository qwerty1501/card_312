# Generated by Django 3.2.9 on 2023-07-06 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230704_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=500, null=True, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=500, verbose_name='Пароль'),
        ),
    ]