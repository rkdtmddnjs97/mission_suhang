# Generated by Django 2.1.8 on 2019-07-20 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0007_opinion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='edit',
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='o_edit',
        ),
    ]