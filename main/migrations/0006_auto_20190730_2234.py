# Generated by Django 2.1.8 on 2019-07-30 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190730_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='announcement_file',
            field=models.FileField(blank=True, default='settings.MEDIA_ROOT/django_fields/dummy.txt', null=True, upload_to='announcement_file/'),
        ),
    ]
