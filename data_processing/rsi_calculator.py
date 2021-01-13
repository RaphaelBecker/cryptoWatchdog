import warnings

import numpy as np
from math import nan


def rsi_calculator(coin_data, coin_price: float, time_span=14):
    """
    :param coin_data: stored historic data
    :param coin_price: The current price of the coin
    :param time_span: Time for calculating RSI
    :return: rsi, rs, average_gain, average_loss, loss, gain
    """
    # Calculate loss or gain
    last_price = float(coin_data["Price"].tail(1))
    change = coin_price - last_price
    if change >= 0:
        # Case for loss
        gain = abs(change)
        loss = 0
    elif change < 0:
        # Case for win
        loss = abs(change)
        gain = 0
    else:
        raise ValueError("Non Numeric Operations took place")

    # Calculating average wins and losses
    if len(coin_data.index) > time_span - 1:
        historic_gains = coin_data["Gain"].tail(time_span - 1) \
            .tolist()
        historic_gains.append(gain)
        historic_losses = coin_data["Loss"].tail(time_span - 1) \
            .tolist()
        historic_losses.append(loss)
        average_gain = np.mean(historic_gains)
        average_loss = np.mean(historic_losses)
        rs = average_gain / average_loss
        rsi = 100 - 100 / (1 + rs)
    else:
        average_gain = nan
        average_loss = nan
        rs = nan
        rsi = nan
        warnings.warn("price data needs to be >" + str(time_span))

    return rsi, rs, average_gain, average_loss, loss, gain
