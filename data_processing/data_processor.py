import csv
from math import isnan

import pandas as pd
import os.path
from numpy import nan

from data_processing.rsi_calculator import rsi_calculator
from telegram_bot.notificator import alert_rsi


def data_cruncher(raw_dataframe):
    """
    :param raw_dataframe:
    :return: new dataframe for each coin
    """
    for coin in raw_dataframe.iterrows():
        # Gathering data for each specific coin
        coin_name, coin_price, coin_volume, date_time = get_key_coin_data(coin)

        # Save data to csv file
        cache_file_name = "./data/runtime_coin_price_data/" + coin_name + "_data.csv"
        archived_file_name = "./data/archived_coin_price_data/" + coin_name + "_data.csv"
        # Timespan to calculate the RSI Index, default is 14
        time_span = 14

        # Check is historic data exists. If it does try to calculate the RSI
        if os.path.isfile(cache_file_name):
            with open(cache_file_name) as coin_cached_data:
                historic_data = pd.read_csv(coin_cached_data, index_col=[0])

                coin_cached_data.close()

            rsi, rs, average_gain, average_loss, loss, gain = \
                rsi_calculator(historic_data, coin_price, time_span)
        else:
            gain = nan
            loss = nan
            average_gain = nan
            average_loss = nan
            rs = nan
            rsi = nan
            historic_data = nan

        alert_rsi(coin_name, rsi, date_time)

        # Generate dataframe for particular time instance
        coin_data = pd.DataFrame({"Coin Name": coin_name, "Price": coin_price,
                                  "Volume": coin_volume, "Gain": gain, "Loss": loss,
                                  "Average Gains": average_gain, "Average Loss": average_loss,
                                  "Relative Strength": rs, "RSI": rsi}, index=[date_time])
        coin_data.index.name = "TimeStamp"

        if not isinstance(historic_data, pd.DataFrame):
            historic_data = coin_data.copy()
        elif historic_data.shape[0] < time_span:
            historic_data = historic_data.append(coin_data)
        elif historic_data.shape[0] == time_span:
            historic_data = historic_data.tail(13)
            historic_data = historic_data.append(coin_data)

        # Save updated file
        save_data_to_archive(archived_file_name, coin_data)
        save_data_to_cache(cache_file_name, historic_data)


def get_key_coin_data(coin):
    """
    Extract important data from coin
    :param coin:
    :return:
    """
    coin_name = coin[1].base
    coin_price = coin[1].price
    coin_volume = coin[1].volume
    date_time = coin[1].Time

    return coin_name, coin_price, coin_volume, date_time


def save_data_to_archive(file_name, data: pd.DataFrame):
    """
    :param file_name:
    :param data:
    Checks if csv file exists. If it doesnt, creates
    file otherwise append to file
    """
    if os.path.isfile(file_name):
        data.to_csv(file_name, mode='a', header=False)
    else:
        data.to_csv(file_name)


def save_data_to_cache(file_name, data: pd.DataFrame):
    data.to_csv(file_name)

