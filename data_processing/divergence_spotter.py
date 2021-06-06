import matplotlib.pyplot as plt
import data_aquisition.database_requester as rq
import visualization.visualizer as vs
from datetime import datetime, timedelta
from scipy.signal import find_peaks

lower_barrier = 30
upper_barrier = 70
width = 5

def spot_bearish_divergence(dataframe):
    index = dataframe.index
    number_of_rows = len(index)
    # print(dataframe.head())
    # 0:ask, 1:RSI
    max_price_rsi_tuple_prev_iterator = (0, 0)
    max_price_rsi_tuple_iterator = (0, 0)
    max_price_rsi_tuple_first = (0, 0)
    max_price_rsi_tuple_second = (0, 0)
    first_top_flag = 0
    second_top_flag = 0
    # Check if the last RSI update broke from >=70 to <70
    if (dataframe.at[number_of_rows - 1, 'RSI'] < 70) & (dataframe.at[number_of_rows - 2, 'RSI'] >= 70):
        print('Divergence spotting necessary!')

        # Bearish Divergence
        for index in range(number_of_rows - 2, -1, -1):
            try:
                if dataframe.at[index, 'RSI'] > upper_barrier:
                    for a in range(index - 1, index - width):
                        if dataframe.at[a, 'RSI'] < upper_barrier:
                            for r in range(a - 1, a - width):
                                if dataframe.at[r, 'RSI'] > upper_barrier and dataframe.at[r, 'RSI'] < dataframe.at[index, 'RSI'] and dataframe.at[r, 'ask'] > dataframe.at[index, 'ask']:
                                    for s in range(r - 1, r - width):
                                        if dataframe.at[s, 'RSI'] < upper_barrier:
                                            print('Something detected')
                                            break
                                        else:
                                            continue
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
            except IndexError:
                pass

        vs.plot_from_dataframe(dataframe)


        #for index in range(number_of_rows - 2, -1, -1):


        """
        if dataframe.at[index, 'RSI'] > 70:
            max_price_rsi_tuple_prev_iterator = (dataframe.at[index, 'ask'], dataframe.at[index, 'RSI'])
            #search for max RIS as long as RSI > 70:
            if max_price_rsi_tuple_prev_iterator[1] >= max_price_rsi_tuple_iterator[1]:
                max_price_rsi_tuple_iterator = (dataframe.at[index, 'ask'], dataframe.at[index, 'RSI'])
        # If RSI is broken through from top to bottom:
        if (max_price_rsi_tuple_prev_iterator[1] >= 70) & (dataframe.at[index, 'RSI'] < 70):
            print('Local RSI tops: ' + str(max_price_rsi_tuple_iterator))
            if max_price_rsi_tuple_iterator[1] > max_price_rsi_tuple_first[1]:
                max_price_rsi_tuple_first = max_price_rsi_tuple_iterator
            if (max_price_rsi_tuple_iterator[0] > max_price_rsi_tuple_first[0]) & (max_price_rsi_tuple_iterator[1] < max_price_rsi_tuple_first[1]):
                print('Divergence detected: ' + str(max_price_rsi_tuple_iterator))
                print('Compare: first: ' + str(max_price_rsi_tuple_first) + ' sec ' + str(max_price_rsi_tuple_iterator))
                max_price_rsi_tuple_first = (0, 0)
            max_price_rsi_tuple_iterator = (0, 0)
            max_price_rsi_tuple_prev_iterator = (0, 0)
    print('')
    """

# var0 = Preis am RSI pieck
# Setze flag var0 = True
