# Generated by Django 3.1.7 on 2021-08-09 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210806_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Placed', 'Placed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], max_length=50, null=True),
        ),
    ]
