from django.urls import path

from . import bkash, url_based_bkash, views

app_name = 'core'
urlpatterns = [
    path('/', bkash.pay_bkash, name='pay_bkash'),
    path('/gettoken/', bkash.get_token, name='get_token'),
    path('/create-payment/<token>/', bkash.create_payment, name='create_payment'),
    path('/excute-payment/<token>/<paymenht_id>/', bkash.excute_payment, name='excute_payment'),
    path('/url/gettoken/', url_based_bkash.tokenized_get_token, name='tokenized_bkash_get_token'),

    path('create_bkash_payment/', views.CreateBkashToken.as_view(), name='create_bkash_payment'),
    path('execute_bkash_payment/', views.ExecuteBkashPayment.as_view(), name='execute_bkash_payment'),
    path('bkash_payment_error/', views.BkashPaymentError.as_view(), name='bkash_payment_error'),
    path('bkash_payment_success/', views.BkashPaymentSuccess.as_view(), name='bkash_payment_success'),
    path('bkash_payment_refund/', views.BkashRefundView.as_view(), name='bkash_refund'),

]
