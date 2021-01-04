#!/usr/bin/env python3
from data_aquisition.requester import get_binance_data
from data_processing.data_processor import data_cruncher


def main():
    data = get_binance_data()
    data_cruncher(data)


if __name__ == "__main__":
    main()
