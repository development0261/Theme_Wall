# Generated by Django 3.2.5 on 2021-07-29 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210729_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeuser',
            name='contact_no',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
