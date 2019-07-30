# Generated by Django 2.1.8 on 2019-07-30 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_auto_20190730_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('like', 'Like'), ('comment', 'Comment'), ('mission_apply', 'Mission_apply'), ('mission_accept', 'Mission_accept'), ('mission_reject', 'Mission_reject'), ('mission_complete', 'Mission_complete'), ('chat', 'Chat')], max_length=20),
        ),
    ]