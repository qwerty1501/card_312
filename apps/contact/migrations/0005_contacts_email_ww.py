# Generated by Django 3.2.9 on 2023-06-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_contacts_email_r'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='email_ww',
            field=models.EmailField(default=1, max_length=64, verbose_name='Почта 4'),
            preserve_default=False,
        ),
    ]
