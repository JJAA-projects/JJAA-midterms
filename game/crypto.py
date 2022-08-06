import re
import requests
import pprint


def get_crypto_price(symbol):
    price = 23000
    try:
        r = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
                         '&per_page=100&page=1&sparkline=false')
        coins = r.json()
        for coin in coins:
            if coin['symbol'] == symbol:
                price = coin['current_price']
                print(f"{symbol} price", price)
        return price
    except e:
        return price


if __name__ == "__main__":
    get_crypto_price()
