# Generated by Django 3.1.3 on 2021-11-11 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_customeuser_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeuser',
            name='social_status',
            field=models.IntegerField(default=0),
        ),
    ]
