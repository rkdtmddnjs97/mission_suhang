# Generated by Django 2.1.8 on 2019-08-04 18:03

from django.db import migrations
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0005_auto_20190805_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit_form',
            name='attachment',
            field=django_fields.fields.DefaultStaticImageField(blank=True, null=True, upload_to='submit_file/'),
        ),
    ]