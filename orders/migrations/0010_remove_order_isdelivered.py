# Generated by Django 3.2.5 on 2021-08-10 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='isDelivered',
        ),
    ]
