# Generated by Django 2.1.8 on 2019-08-04 16:45

from django.db import migrations
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190802_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=django_fields.fields.DefaultStaticImageField(blank=True, upload_to='profile_img/'),
        ),
    ]
