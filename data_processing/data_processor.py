import pandas as pd
import os.path


def data_cruncher(raw_dataframe):
    """
    :param raw_dataframe:
    :return: new dataframe for each coin
    """
    print(raw_dataframe.head())
    for coin in raw_dataframe.iterrows():
        # Gathering data for each specific coin
        coin_name, coin_price, coin_volume, date_time = get_key_coin_data(coin)

        # Generate dataframe for particular time instance
        coin_data = pd.DataFrame({"Coin Name": coin_name, "Price": coin_price,
                                  "Volume": coin_volume, "Date/Time": date_time},
                                 index=[0])

        # Save data to csv file
        save_data_to_file(coin_name, coin_data)

    # TODO: Filter relevant coins
    # TODO: Map coin abbreviation to coin full name
    # TODO: Check how heroku works


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


def save_data_to_file(coin_name, data: pd.DataFrame):
    """
    :param coin_name:
    :param data:
    Checks if csv file exists. If it doesnt, creates
    file otherwise append to file
    """
    file_name = "./data/coin_price_data/" + coin_name + "_data.csv"
    if os.path.isfile(file_name):
        data.to_csv(file_name, mode='a', header=False)
    else:
        data.to_csv(file_name)
