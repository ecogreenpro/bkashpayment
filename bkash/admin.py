from django.contrib import admin

from bkash.models import *

# Register your models here.
admin.site.register(BkashToken)
admin.site.register(BkashPaymentRecord)
admin.site.register(ErrorHandle)
