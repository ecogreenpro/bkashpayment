import random

from django.db import models
from django.utils import timezone


# Create your models here.

def generate_tid():
    number = random.randint(1000, 9999)
    return "TK{}{}".format(timezone.now().strftime("%y%m"), number)


class BkashToken(models.Model):
    token_id = models.CharField(default=generate_tid, max_length=100, verbose_name="Token ID")
    token_type = models.CharField(blank=True, max_length=100, verbose_name="Token Type")
    token = models.TextField(blank=True, verbose_name="Token")
    refresh_token = models.TextField(blank=True, verbose_name="Refresh Token")
    expires_in = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token_id


class BkashPaymentRecord(models.Model):
    payment_id = models.CharField(max_length=50, unique=True, editable=False, primary_key=True)
    createTime = models.TextField(blank=True)
    orgLogo = models.URLField(max_length=250, blank=True)
    orgName = models.CharField(max_length=100, blank=True)
    transactionStatus = models.CharField(max_length=50, blank=True)
    amount = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=20, blank=True)
    intent = models.CharField(max_length=20, blank=True)
    payment_response = models.TextField()
    transaction_id = models.CharField(max_length=100, blank=True)
    transaction_status = models.CharField(max_length=100, blank=True)
    merchant_inovice_number = models.CharField(max_length=100, blank=True)
    transaction_amount = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.payment_id


class ErrorHandle(models.Model):
    error_type = models.CharField(max_length=100, blank=True)
    message = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.error_type
