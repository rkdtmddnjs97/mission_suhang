# Generated by Django 2.1.8 on 2019-07-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_auto_20190718_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='con',
        ),
    ]