# Generated by Django 3.2.9 on 2023-08-28 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_basicuser_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Возраст'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='city',
            field=models.CharField(blank=True, max_length=223, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Мужской'), (2, 'Женский'), (3, 'Другое')], null=True, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='is_animals',
            field=models.BooleanField(default=False, verbose_name='Наличие животных'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='is_children',
            field=models.BooleanField(default=False, verbose_name='Наличие детей'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='profession',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Профессия'),
        ),
    ]
