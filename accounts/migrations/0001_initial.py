# Generated by Django 2.1.8 on 2019-07-26 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hashtag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=200, null=True)),
                ('department', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('introduction', models.TextField(null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('approval', models.BooleanField(default=False)),
                ('ssn', models.CharField(max_length=200, null=True)),
                ('connector', models.IntegerField(null=True)),
                ('profile_id', models.CharField(max_length=200, null=True, unique=True)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('hashtag', models.ManyToManyField(related_name='my_tag', to='hashtag.Hashtag')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
