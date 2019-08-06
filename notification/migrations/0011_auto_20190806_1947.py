# Generated by Django 2.1.8 on 2019-08-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0010_notification_notifi_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('like', 'Like'), ('comment', 'Comment'), ('mission_apply', 'Mission_apply'), ('mission_accept', 'Mission_accept'), ('mission_reject', 'Mission_reject'), ('mision_submit', 'Mission_submit'), ('mission_complete', 'Mission_complete'), ('chat', 'Chat'), ('report', 'Report'), ('scrap', 'Scrap')], max_length=20),
        ),
    ]