# Generated by Django 3.2.16 on 2022-11-24 03:36

import bkash.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BkashToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_id', models.CharField(default=bkash.models.generate_tid, max_length=100, verbose_name='Token Type')),
                ('token_type', models.CharField(blank=True, max_length=100, verbose_name='Token Type')),
                ('token', models.CharField(blank=True, max_length=5000, verbose_name='Token')),
                ('refresh_token', models.CharField(blank=True, max_length=5000, verbose_name='Token')),
                ('expires_in', models.TextField()),
                ('updated_at', models.TextField()),
            ],
        ),
    ]
