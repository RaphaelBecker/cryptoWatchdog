#!/usr/bin/env python3
from data_aquisition.requester import DataGrab
import datetime

def main():
    data = DataGrab.getBinanceSpot()
    print(data)


if __name__ == "__main__":
    main()
