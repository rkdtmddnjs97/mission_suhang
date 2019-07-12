# Generated by Django 2.1.8 on 2019-07-12 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountinfo',
            name='Fin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='department',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='introduction',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='nickname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='university',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
