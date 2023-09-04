# Generated by Django 3.2.9 on 2023-08-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Ф.И.О')),
                ('phone', models.CharField(max_length=36, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=64, verbose_name='Почта')),
                ('email_two', models.EmailField(max_length=64, verbose_name='Почта2')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
                'db_table': '',
            },
        ),
    ]
