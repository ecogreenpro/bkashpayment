from django.urls import path

from . import bkash, url_based_bkash

app_name = 'core'
urlpatterns = [
    path('/', bkash.pay_bkash, name='pay_bkash'),
    path('/gettoken/', bkash.get_token, name='get_token'),
    path('/create-payment/<token>/', bkash.create_payment, name='create_payment'),
    path('/excute-payment/<token>/<paymenht_id>/', bkash.excute_payment, name='excute_payment'),
    path('/token/gettoken/', url_based_bkash.tokenized_get_token, name='tokenized_bkash_get_token'),
]
