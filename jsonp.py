import re
import requests
import json

def loads_jsonp(_jsonp):
        json_object = {x.split('=')[0]:str(x.split('=')[1]) for x in _jsonp.split("&")}
        return json_object
    


url = 'http://muslimsalat.com/daily.json'
response = requests.get("https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities/USD000UTSTOM.jsonp?iss.meta=off&iss.only=securities,marketdata&lang=ru")

_jsonp = response.json()
mk = _jsonp['marketdata']['data']
print(mk[0][8])