# Generated by Django 2.1.8 on 2019-08-09 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='o_post',
        ),
        migrations.DeleteModel(
            name='Opinion',
        ),
    ]