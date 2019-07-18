# Generated by Django 2.1.8 on 2019-07-18 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='con',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='con', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(default='ready', max_length=200),
        ),
    ]
