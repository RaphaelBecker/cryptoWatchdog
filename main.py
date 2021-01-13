#!/usr/bin/env python3
from data_aquisition.requester import get_binance_data
from data_processing.data_processor import data_cruncher
from telegram_bot.notificator import bot_ready

import time


def main():
    """
    Program is going to run unless interrupted manually
    :return: void
    """
    i = 0
    while True:
        bot_ready("-------Analyzing market data-------")
        update_time = 10
        i += 1
        print("Running...", i)
        data = get_binance_data()
        data_cruncher(data)
        # Updates data every update_time seconds
        bot_ready("-----------Task finished-----------")

        time.sleep(update_time)

if __name__ == "__main__":
    main()
