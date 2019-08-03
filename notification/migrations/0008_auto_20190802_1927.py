# Generated by Django 2.1.8 on 2019-08-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0007_notification_notifi_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('like', 'Like'), ('comment', 'Comment'), ('mission_apply', 'Mission_apply'), ('mission_accept', 'Mission_accept'), ('mission_reject', 'Mission_reject'), ('mision_submit', 'Mission_submit'), ('mission_complete', 'Mission_complete'), ('chat', 'Chat'), ('report', 'Report')], max_length=20),
        ),
    ]
