import requests
from django.db.models.functions import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.settings import BKASH_APP_KEY, BKASH_APP_SECRET, BKASH_APP_USERNAME, BKASH_APP_PASSWORD, \
    BKASH_API_BASE_URL, BKASH_APP_VERSION
from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import json
import requests
from .models import *

# def pay_bkash(request):
#     return render(request, 'pay_bkash.html')
#
#
# @csrf_exempt
# def get_token(request):
#     get_token_url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/token/grant"
#
#     get_token_payload = {
#         "app_key": "5tunt4masn6pv2hnvte1sb5n3j",
#         "app_secret": "1vggbqd4hqk9g96o9rrrp2jftvek578v7d2bnerim12a87dbrrka"
#     }
#     get_token_headers = {
#         "username": "sandboxTestUser",
#         "password": "hWD@8vtzw0",
#     }
#
#     get_token_response = requests.post(get_token_url, json=get_token_payload, headers=get_token_headers)
#
#     token = get_token_response.json()
#     # token_id = token['id_token']
#     request.session['token'] = token["id_token"]
#     return JsonResponse(token)
#
#
# def create_payment(request, token):
#     url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create"
#     create_payment_payload = {
#         "mode": "0011",
#         "payerReference": "01723888888",
#         "callbackURL": "http://127.0.0.1:800/",
#         "amount": "50",
#         "currency": "BDT",
#         "intent": "sale",
#         "merchantInvoiceNumber": "CS-52222"
#     }
#     create_payment_headers = {
#         "accept": "application/json",
#         "Authorization": token,
#         "X-APP-Key": "5tunt4masn6pv2hnvte1sb5n3j",
#         "content-type": "application/json"
#     }
#     create_payment_response = requests.post(url, json=create_payment_payload, headers=create_payment_headers)
#     payment_id_response = create_payment_response.json()
#     payment_id = payment_id_response['paymentID']
#     print(payment_id_response)
#     return JsonResponse(payment_id_response)
#
#
# def excute_payment(request, token, payment_id):
#     execute_payment_url = f"https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/execute/{payment_id}"
#     print(execute_payment_url)
#     execute_payment_headers = {
#         "accept": "application/json",
#         "Authorization": token,
#         "X-APP-Key": "5tunt4masn6pv2hnvte1sb5n3j",
#         "content-type": "application/json"
#     }
#
#     execute_payment_response = requests.post(execute_payment_url, headers=execute_payment_headers)
#     return JsonResponse(execute_payment_response.json())

BKASH_ERROR_DICT = {
    "2001": "Invalid App Key",
    "2002": "Invalid Payment ID",
    "2003": "Process failed",
    "2004": "Invalid firstPaymentDate",
    "2005": "Invalid frequency",
    "2006": "Invalid amount",
    "2007": "Invalid currency",
    "2008": "Invalid intent",
    "2009": "Invalid Wallet",
    "2010": "Invalid OTP",
    "2011": "Invalid PIN",
    "2012": "Invalid Receiver MSISDN",
    "2013": "Resend Limit Exceeded",
    "2014": "Wrong PIN",
    "2015": "Wrong PIN count exceeded",
    "2016": "Wrong verification code",
    "2017": "Wrong verification limit exceeded",
    "2018": "OTP verification time expired",
    "2019": "PIN verification time expired",
    "2020": "Exception Occurred",
    "2021": "Invalid Mandate ID",
    "2022": "The mandate does not exist",
    "2023": "Insufficient Balance",
    "2024": "Exception occurred",
    "2025": "Invalid request body",
    "2026": "The reversal amount cannot be greater than the original transaction amount",
    "2027": "The mandate corresponding to the payer reference number already exists and cannot be created again",
    "2028": "Reverse failed because the transaction serial number does not exist",
    "2029": "Duplicate for all transactions",
    "2030": "Invalid mandate request type",
    "2031": "Invalid merchant invoice number",
    "2032": "Invalid transfer type",
    "2033": "Transaction not found",
    "2034": "The transaction cannot be reversed because the original transaction has been reversed",
    "2035": "Reverse failed because the initiator has no permission to reverse the transaction",
    "2036": "The direct debit mandate is not in Active state",
    "2037": "The account of the debit party is in a state which prohibits execution of this transaction",
    "2038": "Debit party identity tag prohibits execution of this transaction",
    "2039": "The account of the credit party is in a state which prohibits execution of this transaction",
    "2040": "Credit party identity tag prohibits execution of this transaction",
    "2041": "Credit party identity is in a state which does not support the current service",
}


class BkashPayment:
    def get_token(self):
        if BkashToken.objects.all().exists():
            token = BkashToken.objects.all()[0]
            print('token query========', token)
            print('timezone now=========', timezone.now())
            print('update time === ', token.updated_at)
            if token.updated_at + timedelta(minutes=50) < timezone.now():
                print(token.updated_at)
                token = self.refresh_token(token)
                print('token', token)
                return token.token
            return token.token
        else:
            token = self.create_new_token()
            return token.token

    def create_new_token(self):
        print('create new token')
        url = BKASH_API_BASE_URL + "/" + BKASH_APP_VERSION + "/checkout/token/grant"

        payload = "{\"app_key\":\"" + BKASH_APP_KEY + \
                  "\",\"app_secret\":\"" + BKASH_APP_SECRET + "\"}"

        headers = {
            'username': BKASH_APP_USERNAME,
            'password': BKASH_APP_PASSWORD,
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print('response', response)
        response = response.json()
        print('json response', response)
        expires_in = datetime.now() + timedelta(days=1)
        print('expires in ===', expires_in)
        print('response expires in ===', response.get("expires_in"))

        token = BkashToken.objects.create(
            token_type=response.get("token_type"),
            token=response.get("id_token"),
            refresh_token=response.get("refresh_token"),
            expires_in=expires_in
        )
        print('token', token)

        token.save()
        return token

    def refresh_token(self, token):
        print('refresh token')

        url = BKASH_API_BASE_URL + "/" + BKASH_APP_VERSION + "/checkout/token/refresh"

        payload = "{\"refresh_token\":\"" + token.refresh_token + "\",\"app_key\":\"" + \
                  BKASH_APP_KEY + "\",\"app_secret\":\"" + BKASH_APP_SECRET + "\"}"

        headers = {
            'username': BKASH_APP_USERNAME,
            'password': BKASH_APP_PASSWORD,
        }

        response = requests.request(
            "POST", url, data=payload, headers=headers).json()
        print(response)
        expires_in = datetime.now() + timedelta(days=2)
        token.token_type = response.get("token_type")
        token.token = response.get("id_token")
        token.refresh_token = response.get("refresh_token")
        token.expires_in = expires_in
        token.save()

        return token
