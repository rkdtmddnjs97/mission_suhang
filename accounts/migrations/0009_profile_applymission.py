# Generated by Django 2.1.8 on 2019-07-22 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0012_remove_post_applier'),
        ('accounts', '0008_remove_profile_applymission'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='applyMission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='request.Post'),
        ),
    ]
