# %% <- scientific mode

import telegram_bot.notificator as nfr
import visualization.visualizer as vsr
import data_aquisition.database_requester as rq
from datetime import datetime, timedelta
import data_processing.divergence_spotter as dsp
import matplotlib.pyplot as plt


caption = 'backtesting!'
ticker_symbol = 'Ethereum'
# Number of rows for 2 Weeks in 30 min updation time: 14d * 24h * 2 = 672
spotter_timeframe_in_rows = 672
number_of_rows = 0

data_base_df = rq.get_db_as_dataframe()
ticker_dataframe = data_base_df[(data_base_df["base"] == ticker_symbol)]
# Reset indexes of the rows in the dataframe
ticker_dataframe.reset_index(drop=True, inplace=True)

# RSI calculation:
delta = ticker_dataframe['ask'].diff()
up = delta.clip(lower=0)
down = -1 * delta.clip(upper=0)
ema_up = up.ewm(com=13, adjust=False).mean()
ema_down = down.ewm(com=13, adjust=False).mean()
rs = ema_up / ema_down
ticker_dataframe['RSI'] = 100 - (100 / (1 + rs))

# Skip first 14 entries to have real values
dataframe = ticker_dataframe.iloc[14:]
index = dataframe.index
number_of_rows = len(index)
print(number_of_rows)
vsr.plot_from_dataframe(ticker_dataframe)
counter = 0

# random start index number 800 for test purpose for limit calculation time
for index in range(0, number_of_rows - spotter_timeframe_in_rows):
    start = 0 + index
    end = spotter_timeframe_in_rows + index
    iterator_dataframe = ticker_dataframe[start:end]
    # Reset indexes of the rows in the dataframe
    iterator_dataframe.reset_index(drop=True, inplace=True)
    #print(iterator_dataframe[0:1])
    dsp.spot_bearish_divergence(iterator_dataframe)
    counter = counter + 1

print('Backtest iterator was called ' + str(counter) + ' times ')
