# Generated by Django 3.2.5 on 2021-08-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_extra_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_size',
            name='size',
            field=models.CharField(blank=True, choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large'), ('No_Size', 'No_Size')], max_length=20, null=True),
        ),
    ]
