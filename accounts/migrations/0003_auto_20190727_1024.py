# Generated by Django 2.1.8 on 2019-07-27 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='money',
            field=models.IntegerField(default=0),
        ),
    ]
