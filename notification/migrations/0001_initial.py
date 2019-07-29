# Generated by Django 2.1.8 on 2019-07-29 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_profile_mission_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('like', 'Like'), ('comment', 'Comment'), ('mission_application', 'Mission_application')], max_length=20)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='accounts.Profile')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to', to='accounts.Profile')),
            ],
        ),
    ]
