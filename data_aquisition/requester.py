import requests
import pandas as pd
import numpy as np
from datetime import datetime


def get_binance_data():
    """
    Pulls Binance Spot Prices. Returns Datafram with: ask, bid, price, volume, base, quote, spread, exchange.
    Requests all data at once w/ 1 API pull
    Reference: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.m
    """

    def split_pair(ticker_string):
        # Split conversion pairs
        if ticker_string[-4:] == 'USDT':
            return [ticker_string.split('USDT')[0].lower(), 'usdt']
        elif ticker_string[-3:] == 'ETH':
            return [ticker_string.split('ETH')[0].lower(), 'eth']
        elif ticker_string[-3:] == 'BTC':
            return [ticker_string.split('BTC')[0].lower(), 'btc']
        elif ticker_string[-3:] == 'BNB':
            return [ticker_string.split('BNB')[0].lower(), 'bnb']
        return np.nan

    url = 'https://api.binance.com/api/v1/ticker/24hr'
    # Generate dataframe from json file
    bnn_df = pd.DataFrame(requests.get(url).json())
    current_datetime = datetime.now()
    year = current_datetime.strftime("%Y")
    month = current_datetime.strftime("%m")
    day = current_datetime.strftime("%d")
    time = current_datetime.strftime("%H:%M:%S")

    bnn_df['symbol'] = bnn_df.apply(lambda x: split_pair(x['symbol']), axis=1)
    bnn_df = bnn_df.dropna()
    bnn_df['base'] = bnn_df.apply(lambda x: x['symbol'][0], axis=1)
    bnn_df['quote'] = bnn_df.apply(lambda x: x['symbol'][1], axis=1)
    bnn_df['quote'] = bnn_df['quote'].str.replace('usdt', 'usd')
    bnn_df = bnn_df.rename(index=str, columns={'askPrice': 'ask',
                                               'bidPrice': 'bid',
                                               'lastPrice': 'price'})
    columns = ['ask', 'bid', 'price', 'volume']
    bnn_df['exchange'] = 'binance'
    bnn_df[columns] = bnn_df[columns].astype(float)
    bnn_df['spread'] = bnn_df.ask - bnn_df.bid
    columns.extend(['base', 'quote', 'spread', 'exchange'])
    bnn_df = bnn_df[columns]

    # Filter data to only get price conversion to USD and drop all other data
    bnn_df = bnn_df[bnn_df["quote"] == "usd"].reset_index() \
        .drop("index", axis=1)
    bnn_df['Year'] = year
    bnn_df['Month'] = month
    bnn_df['Day'] = day
    bnn_df['Time'] = time

    return bnn_df


if __name__ == '__main__':
    crypto_data = get_binance_data()
    crypto_data.to_csv('sandbox_data.csv')
    print(crypto_data)
