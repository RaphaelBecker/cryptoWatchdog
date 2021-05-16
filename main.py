#!/usr/bin/env python3
from data_aquisition.requester import get_binance_data
from data_processing.data_processor import data_cruncher
from telegram_bot.notificator import bot_ready
from data_processing.rsi_calculator import rsi_calculator
from datetime import date
import csv
import os
import time

def main():
    """
    Program is going to run unless interrupted manually
    :return: void
    """
    i = 0
    while True:
        # TODO: Undo this after testing
        bot_ready('---Analyzing market data on "{}"'.format(date.today()) + "---")
        # TODO: change sleep time after testing
        update_time = 10 #60*60*6
        i += 1
        print("Running...", i)
        with open('./data_processing/resources/selectedCurrencies.csv', newline='') as f:
            reader = csv.reader(f)
            coins = list(reader)
            coins = coins[0]
        cwd = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_processing', 'resources'
                         , 'nameSymbolDictionary.csv'))

        # To convert from coin symbol to coin name as that is how they are stored in the database
        with open('./data_processing/resources/nameSymbolDictionary.csv') as file:
            abv_to_coin_name_dict = csv.reader(file)
            abv_to_coin_name_dict = dict(abv_to_coin_name_dict)

        for coin in coins:
            rsi_calculator(abv_to_coin_name_dict[coin])
        # No longer needed as data is being fetched from the database.
        # data = get_binance_data()
        # data_cruncher(data)
        # RSI Calculation

        # Updates data every update_time seconds
        # TODO: Undo this after testing
        # bot_ready("-----------Task finished-----------")
        time.sleep(update_time)
#
if __name__ == "__main__":
    main()
