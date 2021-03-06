#!/usr/bin/env python3
from data_aquisition.requester import get_binance_data
from data_processing.data_processor import data_cruncher
import time


def main():
    """
    Program is going to run unless interrupted manually
    :return: Nothing
    """
    while True:
        data = get_binance_data()
        data_cruncher(data)
        update_time = 5;
        # Updates data every update_time seconds
        time.sleep(update_time)


if __name__ == "__main__":
    main()
