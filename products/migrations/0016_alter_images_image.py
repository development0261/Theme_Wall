# Generated by Django 3.2.5 on 2021-08-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210819_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.FileField(blank=True, default='noImage.png', null=True, upload_to='items'),
        ),
    ]
