# Generated by Django 2.1.8 on 2019-08-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0006_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatting',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Date published'),
        ),
    ]