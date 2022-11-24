from django.contrib import admin

from bkash.models import *


# Register your models here.
class BkashTokenAdmin(admin.ModelAdmin):
    list_display = [
        'token_id',
        'token_type',
        'expires_in',
        'updated_at',
    ]


admin.site.register(BkashToken, BkashTokenAdmin)


class BkashPaymentRecordAdmin(admin.ModelAdmin):
    list_display = [
        'payment_id',
        'createTime',
        'payment_response',
    ]


admin.site.register(BkashPaymentRecord, BkashPaymentRecordAdmin)
admin.site.register(ErrorHandle)
