# Generated by Django 3.2.5 on 2021-10-22 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20211022_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerreview',
            name='stars',
            field=models.IntegerField(verbose_name='thumbs'),
        ),
    ]
