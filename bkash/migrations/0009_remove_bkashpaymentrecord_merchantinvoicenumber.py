# Generated by Django 3.2.16 on 2022-11-24 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bkash', '0008_alter_bkashtoken_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bkashpaymentrecord',
            name='merchantInvoiceNumber',
        ),
    ]