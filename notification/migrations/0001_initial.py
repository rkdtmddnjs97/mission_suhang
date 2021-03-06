# Generated by Django 2.1.8 on 2019-08-09 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notifi_comment', models.TextField(blank=True, null=True)),
                ('notifi_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('notification_type', models.CharField(choices=[('like', 'Like'), ('comment', 'Comment'), ('mission_apply', 'Mission_apply'), ('mission_accept', 'Mission_accept'), ('mission_reject', 'Mission_reject'), ('mision_submit', 'Mission_submit'), ('mission_complete', 'Mission_complete'), ('chat', 'Chat'), ('report', 'Report'), ('scrap', 'Scrap')], max_length=20)),
                ('confirmation', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='accounts.Profile')),
                ('notifi_post_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifi_post', to='request.Post')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to', to='accounts.Profile')),
            ],
        ),
    ]
