# Generated by Django 3.2.9 on 2023-08-10 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale_category',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Product_category',
        ),
        migrations.DeleteModel(
            name='Sale_category',
        ),
    ]
