# Generated by Django 2.1.8 on 2019-07-25 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_profile_post_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='post_fk',
        ),
    ]
