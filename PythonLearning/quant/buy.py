import requests
import json
import base64
import hmac
import hashlib
import datetime
import time
import timeit

base_url = "https://api.sandbox.gemini.com"
endpoint = "/v1/order/new"
url = base_url + endpoint

gemini_api_key = "123"
gemini_api_secret = "123".encode()

t = datetime.datetime.now()
payload_nonce = str(int(time.mktime(t.timetuple())*1000))

payload = {
    "request": "/v1/order/new",
    "nonce": payload_nonce,
    "symbol": "btcusd",
    "amount": 5,
    "price": "3",
    "side": "buy",
    "type": "exchange limit",
    "options": ["maker-or-cancel"]
}

encoded_payload = json.dumps(payload).encode()
b64 = base64.b64encode(encoded_payload)
signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

requests_headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': gemini_api_key,
    'X-GEMINI-PAYLOAD': b64,
    'X-GEMINI-SIGNATURE': signature,
    'Cache-Control': "no-cache"
}


response = requests.post(url, 
                         data=None,
                         headers=requests_headers)

new_order = response.json()
print(new_order)


def get_orderbook():
    orderbook = requests.get("https://api.gemini.com/v1/book/btcusd").json()

n = 10
latency = timeit.timeit('get_orderbook()', setup='from __main__ import get_orderbook', number=n) * 1.0 / n 
print('Latency is {} ms'.format(latency * 1000))




