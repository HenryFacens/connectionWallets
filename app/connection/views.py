import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjM4ZDAzYThkLWQ2ZmQtNDMzYy04MTA1LWNmOGFlMjhlNGE3NyIsIm9yZ0lkIjoiMzcxNzk4IiwidXNlcklkIjoiMzgyMTAxIiwidHlwZUlkIjoiYjI3NjU1OTQtYmU5NS00Y2I2LTkyNTAtZTAwMDBlZmIwODVlIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MDQ5OTA5OTQsImV4cCI6NDg2MDc1MDk5NH0.-fQYOwoB46Qu6DDwGalN_99xBBrPYsWNCBxpl7ywHQA'
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit


def moralis_auth(request):
    return render(request, 'home/login.html', {})

def my_profile(request):
    return render(request, 'home/profile.html', {})

def request_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "defi.finance",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": "2024-02-01T00:00:00.000Z",
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})

    return JsonResponse(json.loads(x.text))


def verify_message(request):
    data = json.loads(request.body)
    print(f'teste = ===== {data}')
    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjM4ZDAzYThkLWQ2ZmQtNDMzYy04MTA1LWNmOGFlMjhlNGE3NyIsIm9yZ0lkIjoiMzcxNzk4IiwidXNlcklkIjoiMzgyMTAxIiwidHlwZUlkIjoiYjI3NjU1OTQtYmU5NS00Y2I2LTkyNTAtZTAwMDBlZmIwODVlIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MDQ5OTA5OTQsImV4cCI6NDg2MDc1MDk5NH0.-fQYOwoB46Qu6DDwGalN_99xBBrPYsWNCBxpl7ywHQA"})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))