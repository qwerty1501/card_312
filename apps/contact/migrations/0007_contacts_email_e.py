# Generated by Django 3.2.9 on 2023-06-29 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_auto_20230629_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='email_e',
            field=models.EmailField(default=1, max_length=64, verbose_name='Почта2'),
            preserve_default=False,
        ),
    ]
