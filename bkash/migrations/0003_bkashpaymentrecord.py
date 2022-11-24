# Generated by Django 3.2.16 on 2022-11-24 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkash', '0002_auto_20221124_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='BkashPaymentRecord',
            fields=[
                ('paymentID', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('createTime', models.TextField()),
                ('orgLogo', models.URLField(max_length=250)),
                ('orgName', models.CharField(max_length=100)),
                ('transactionStatus', models.CharField(max_length=50)),
                ('amount', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=20)),
                ('intent', models.CharField(max_length=20)),
                ('merchantInvoiceNumber', models.CharField(max_length=30)),
                ('response', models.TextField()),
            ],
        ),
    ]