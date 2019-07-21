# Generated by Django 2.1.8 on 2019-07-20 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0006_auto_20190720_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_writer', models.CharField(max_length=200)),
                ('o_content', models.TextField(null=True)),
                ('o_edit', models.BooleanField(default=False)),
                ('o_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Post')),
            ],
        ),
    ]