# Generated by Django 3.2.5 on 2021-10-22 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_customeuser_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeuser',
            name='rating',
        ),
    ]
