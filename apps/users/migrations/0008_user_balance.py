# Generated by Django 3.2.9 on 2023-08-30 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230828_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Баланс'),
        ),
    ]
