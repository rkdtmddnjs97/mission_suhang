# Generated by Django 2.1.8 on 2019-07-22 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_applymission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='applyMission',
        ),
    ]