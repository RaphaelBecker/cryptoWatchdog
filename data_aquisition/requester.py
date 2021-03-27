import os
from pathlib import Path

import requests
import pandas as pd
import numpy as np
import csv
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
    # Getting time and date data for api request
    date = current_datetime.strftime("%Y-%m-%d")
    # month = current_datetime.strftime("%m")
    # day = current_datetime.strftime("%d")
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

    # Filter only the coins we require
    bnn_df = filter_required_coins(bnn_df)
    cwd = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_processing', 'resources'
                                       , 'nameSymbolDictionary.csv'))

    with open(cwd) as file:
        abv_to_coin_name_dict = csv.reader(file)
        abv_to_coin_name_dict = dict(abv_to_coin_name_dict)

    bnn_df = bnn_df.replace({"base": abv_to_coin_name_dict})
    # Populating data frame with time and date data
    bnn_df['date_stamp'] = pd.to_datetime(date)
    # bnn_df['Month'] = month
    # bnn_df['Day'] = day
    bnn_df['time_stamp'] = pd.to_datetime(time)

    return bnn_df


def filter_required_coins(dataframe):
    cwd = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_processing', 'resources'
                                       , 'selectedCurrencies.csv'))
    with open(cwd) as file:
        reader = csv.reader(file)
        filtered_coin_list = list(reader)
        filtered_coin_list = filtered_coin_list[0]
        file.close()

    dataframe = dataframe[dataframe["base"].isin(filtered_coin_list)]
    return dataframe


if __name__ == '__main__':
    crypto_data = get_binance_data()
    print(crypto_data)
