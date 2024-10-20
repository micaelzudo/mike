from datetime import timedelta, date
import requests
import json

def get_eur_price():
    start_date = date.today() - timedelta(days=7)
    url = f'https://api.exchangerate-api.com/v4/latest/EUR?start_date={start_date}'
    response = requests.get(url)
    data = response.json()
    prices = data['rates']
    usd_price = round(prices['USD'], 2)
    return usd_price

eur_price = get_eur_price()
print(f'The EUR price in USD for the last week is: {eur_price}')