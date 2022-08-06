import re
import requests
import pprint


def get_btc_price():
    try:
        btc_price = 0
        r = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false')
        coins = r.json()
        for coin in coins:
            if coin['id'] == 'bitcoin':
                btc_price = coin['current_price']
        return btc_price
    except:
        return 23000


if __name__ == "__main__":
    get_btc_price()
