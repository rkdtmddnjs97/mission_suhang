# Generated by Django 2.1.8 on 2019-07-29 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notifi_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]