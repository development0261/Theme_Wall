# Generated by Django 3.2.5 on 2021-08-06 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='serial_no',
            field=models.CharField(default='', max_length=200),
        ),
    ]
