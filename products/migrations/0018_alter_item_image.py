# Generated by Django 3.2.5 on 2021-08-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_item_qty_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(blank=True, default='noImage.png', null=True, upload_to='items'),
        ),
    ]
