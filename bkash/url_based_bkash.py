import requests
from django.http import HttpResponse
from django.shortcuts import render


def tokenized_get_token(request):
    get_token_url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"

    get_token_payload = {
        "app_key": "5tunt4masn6pv2hnvte1sb5n3j",
        "app_secret": "1vggbqd4hqk9g96o9rrrp2jftvek578v7d2bnerim12a87dbrrka"
    }
    get_token_headers = {
        "accept": "application/json",
        "username": "sandboxTestUser",
        "password": "hWD@8vtzw0",
        "content-type": "application/json"
    }

    get_token_response = requests.post(get_token_url, json=get_token_payload, headers=get_token_headers)

    token = get_token_response.json()
    return HttpResponse(get_token_response)
    # url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create"
    #
    # create_payment_payload = {
    #     "mode": "0011",
    #     "payerReference": "01723888888",
    #     "callbackURL": "http://127.0.0.1:800/",
    #     "amount": "50",
    #     "currency": "BDT",
    #     "intent": "sale",
    #     "merchantInvoiceNumber": "CS-52222"
    # }
    # create_payment_headers = {
    #     "accept": "application/json",
    #     "Authorization": "",
    #     "X-APP-Key": "5tunt4masn6pv2hnvte1sb5n3j",
    #     "content-type": "application/json"
    # }
    # create_payment_response = requests.post(url, json=create_payment_payload, headers=create_payment_headers)
    # payment_id_response = create_payment_response.json()
    # payment_id = payment_id_response['paymentID']
    # print(payment_id_response)
    #
    # execute_payment_url = f"https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/execute/{payment_id}"
    # print(execute_payment_url)
    # execute_payment_headers = {
    #     "accept": "application/json",
    #     "Authorization": "",
    #     "X-APP-Key": "5tunt4masn6pv2hnvte1sb5n3j",
    #     "content-type": "application/json"
    # }
    #
    # execute_payment_response = requests.post(execute_payment_url, headers=execute_payment_headers)
    #
