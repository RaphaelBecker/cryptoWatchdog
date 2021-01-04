#!/usr/bin/env python3
from data_aquisition.requester import DataGrab


def main():
    data = DataGrab.getBinanceSpot()
    print(data)


if __name__ == "__main__":
    main()
