import uuid

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from core.settings import BKASH_APP_KEY, BKASH_APP_SECRET, BKASH_APP_USERNAME, BKASH_APP_PASSWORD, \
    BKASH_API_BASE_URL, BKASH_APP_VERSION
from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import json
import requests

from .bkash import BkashPayment, BKASH_ERROR_DICT
from .models import *


@method_decorator(csrf_exempt, name='dispatch')
class CreateBkashToken(LoginRequiredMixin, BkashPayment, View):
    def post(self, request, *args, **kwargs):
        body_unicode = self.request.body.decode('utf-8')

        body = json.loads(body_unicode)
        print('body json========', body)
        amount = body['amount']
        url = BKASH_API_BASE_URL + "/" + BKASH_APP_VERSION + "/checkout/payment/create"

        payload = "{\"amount\":\"" + str(amount) + "\",\"currency\":\"BDT\",\"intent\":\"sale\"," \
                                                   "\"merchantInvoiceNumber\":\"" + \
                  str(uuid.uuid4()) + \
                  "\"}"

        headers = {
            'authorization': self.get_token(),
            'x-app-key': BKASH_APP_KEY
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print('response========', response)
        response = response.json()
        print('response json========', response)
        payment_id = response.get("paymentID")
        print(payment_id, 'create')
        payment_detail = PaymentsDetails.objects.get(
            current_uid=body["payment_details"])
        payment_detail.payment_method = PaymentMethodEnum.bkash.value['key']
        payment_detail.payment_status = PaymentStatusEnum.unpaid.value['key']
        payment_detail.transaction_status = PaymentTransactionStatusEnum.initiated.value[
            'key']
        payment_detail.paid_time = timezone.now()
        payment_detail.save()
        BkashPaymentRecord.objects.create(
            payment_id=payment_id, payment_details=payment_detail, payment_response=response)

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class ExecuteBkashPayment(LoginRequiredMixin, BkashPayment, View):
    def post(self, request, *args, **kwargs):
        body_unicode = self.request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print('body=====', body)

        payment_record = BkashPaymentRecord.objects.filter(
            payment_id=body['paymentID']).first()
        print('execute payment record =========', payment_record)
        bkash_payment_current_uid = str(payment_record.payment_details)

        url = BKASH_API_BASE_URL + "/" + BKASH_APP_VERSION + "/checkout/payment/execute/" + \
              str(body['paymentID'])

        headers = {
            'authorization': self.get_token(),
            'x-app-key': BKASH_APP_KEY
        }

        response = requests.request("POST", url, headers=headers)
        print('execute response==========', response)
        response = response.json()
        print('execute response =====', response)

        if "transactionStatus" in response.keys() and response.get("transactionStatus") == "Completed":
            payment_record.transaction_id = response.get("trxID")
            payment_record.transaction_status = response.get(
                'transactionStatus')
            payment_record.amount = response.get('amount')
            payment_record.currency = response.get('currency')
            payment_record.intent = response.get('intent')
            payment_record.merchant_inovice_number = response.get(
                'merchantInvoiceNumber')
            payment_record.transaction_amount = response.get("amount")
            payment_record.payment_response = response
            payment_record.is_paid = True
            payment_record.save()

            payment_detail = PaymentsDetails.objects.get(
                current_uid=bkash_payment_current_uid)
            print('payment details === ', payment_detail)
            payment_detail.payment_method = PaymentMethodEnum.bkash.value['key']
            payment_detail.payment_status = PaymentStatusEnum.paid.value['key']
            payment_detail.transaction_status = PaymentTransactionStatusEnum.completed.value[
                'key']
            payment_detail.paid_time = timezone.now()

            payment_detail.save()

            # after successfull payment redirect to your desired page/url
            # return redirect(reverse('payment:bkash_payment_success'))
            # return render(request, 'users/success_payment.html')
            return JsonResponse(response)

        else:
            payment_record.payment_response = response
            payment_record.save()
            response["error_msg"] = BKASH_ERROR_DICT.get(
                response.get("errorCode"))
            return JsonResponse(response)


def create_error_handling(error_type, message):
    error_handle = ErrorHandle.objects.create(
        error_type=error_type, message=message)
    print('error handle = ', error_handle)


class BkashPaymentError(View):

    def dispatch(self, request, *args, **kwargs):

        try:
            print('All is Right')

        except requests.exceptions.HTTPError as errh:
            error_type = 'HTTPError'
            message = errh
            create_error_handling(error_type, message)

        except requests.exceptions.ConnectionError as errc:
            error_type = 'ConnectionError'
            message = errc
            create_error_handling(error_type, message)
        except requests.exceptions.Timeout as errt:
            error_type = 'Timeout'
            message = errt
            create_error_handling(error_type, message)

        except requests.exceptions.TooManyRedirects as errtmr:
            error_type = 'TooManyRedirects'
            message = errtmr
            create_error_handling(error_type, message)
        except requests.exceptions.RequestException as err:
            error_type = 'RequestException'
            message = err
            create_error_handling(error_type, message)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'users/error_payment.html', {'payment_method': PaymentMethodEnum.bkash.value['val']})


class BkashPaymentSuccess(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/success_payment.html', {'payment_method': PaymentMethodEnum.bkash.value['val']})


class BkashRefundView(LoginRequiredMixin, BkashPayment, View):
    def get(self, request, *args, **kwargs):
        form = BkashRefundForm()
        context = {
            'form': BkashRefundForm()
        }

        return render(request, 'bkash_refund.html', context)

    def post(self, request, *args, **kwargs):
        form = BkashRefundForm(request.POST)

        if form.is_valid():
            bkash_setup = BkashSetup.objects.all()[0]
            print('setup ==== ', bkash_setup)
            url = BKASH_API_BASE_URL + "/" + BKASH_APP_VERSION + "/checkout/payment/refund"

            transaction_id = request.POST.get('transaction_id')

            payment_record_obj = BkashPaymentRecord.objects.filter(
                transaction_id=transaction_id).first()
            print('payment record obj', payment_record_obj)
            print(
                f'paymentId : {payment_record_obj.payment_id} --- transactionId: {payment_record_obj.transaction_id}')

            payload = "{\"paymentID\":\"" + payment_record_obj.payment_id + \
                      "\",\"amount\":\"" + str(
                payment_record_obj.amount) + "\",\"trxID\":\"" + payment_record_obj.transaction_id + \
                      "\",\"sku\":\"Amar Iccha\",\"reason\":\"Amar Iccha\"}"
            print('payload ====', payload)
            headers = {
                'authorization': self.get_token(),
                'x-app-key': BKASH_APP_KEY
            }

            response = requests.request(
                "POST", url, data=payload, headers=headers)
            print('response===', response)
            response = response.json()
            print('response json=== ', response)
            if "transactionStatus" in response.keys() and response.get("transactionStatus") == "Completed":

                completed_time = response.get("completedTime")
                original_trxID = response.get("originalTrxID")
                refund_trxID = response.get("refundTrxID")
                transaction_status = response.get("transactionStatus")
                amount = response.get("amount")
                currency = response.get("currency")
                BkashRefund.objects.create(
                    payment_details=payment_record_obj.payment_details,
                    completed_time=completed_time,
                    original_trxID=original_trxID,
                    refund_trxID=refund_trxID,
                    transaction_status=transaction_status,
                    amount=amount,
                    currency=currency
                )
                return HttpResponse('Success')

            else:
                return HttpResponse('something went wrong')

        else:
            context = {
                'form': form
            }

            return render(request, 'bkash_refund.html', context)
