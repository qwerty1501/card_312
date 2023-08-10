# Generated by Django 3.2.9 on 2023-08-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='apps/discount/images/', verbose_name='ФОТОГРАФИЯ *(387x167)')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Все скидки ',
                'verbose_name_plural': 'Все скидки ',
            },
        ),
    ]
