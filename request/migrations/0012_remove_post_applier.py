# Generated by Django 2.1.8 on 2019-07-22 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0011_post_applier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='applier',
        ),
    ]