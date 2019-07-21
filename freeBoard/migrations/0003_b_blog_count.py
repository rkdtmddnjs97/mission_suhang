# Generated by Django 2.1.8 on 2019-07-18 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freeBoard', '0002_remove_b_blog_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='b_blog',
            name='count',
            field=models.ManyToManyField(default=0, related_name='count', to=settings.AUTH_USER_MODEL),
        ),
    ]