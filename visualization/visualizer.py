# #%% <-  Delete # for scientific mode!
# https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
# %%

import matplotlib.pyplot as plt
import telegram_bot.notificator as nf
import data_aquisition.database_requester as rq
from datetime import datetime, timedelta

# TODO: Only for standalone TEST. Delete when integrated
caption = 'caption_text'
ticker_symbol = 'Bitcoin'
days_to_plot = 34


def create_plot(ticker, days_from_now):
    # preparations:
    file_path = './visualization/plots/' + ticker + '.png'
    data_base_df = rq.get_db_as_dataframe()
    date_time_obj = datetime.now()
    date_time_minus = date_time_obj - timedelta(days=days_from_now)

    # creates dataframe with all columns of 'ticker' of the last 'days_from_now' days
    ticker_dataframe = data_base_df[(data_base_df["base"] == ticker) & (data_base_df["date_stamp"] > date_time_minus)]
    # calculate min and max dates included in dataframe:
    date_min = datetime.date(ticker_dataframe['date_stamp'].min())
    date_max = datetime.date(ticker_dataframe['date_stamp'].max())

    # RSI calculation:
    delta = ticker_dataframe['ask'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / ema_down
    ticker_dataframe['RSI'] = 100 - (100 / (1 + rs))

    # Skip first 14 entries to have real values
    ticker_dataframe = ticker_dataframe.iloc[14:]

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.get_xaxis().set_visible(False)
    fig.suptitle(ticker + ' ' + str(date_min) + ' - ' + str(date_max))

    ticker_dataframe['ask'].plot(ax=ax1)
    ax1.set_ylabel('Price ($)')
    ticker_dataframe['RSI'].plot(ax=ax2)
    ax2.set_ylim(0, 100)
    ax2.get_xaxis().set_visible(False)

    ax2.axhline(30, color='r', linestyle='--')
    ax2.axhline(70, color='r', linestyle='--')
    ax2.set_ylabel('RSI')

    plt.savefig(file_path, dpi=300, transparent=True)
    plt.show()


# TODO: Delete and integrate into project when standalone TEST is removed:

# posts photo to chat group:
create_plot(ticker_symbol, days_to_plot)
# sends photo to telegram group:
nf.post_photo_to_chat_group(caption, ticker_symbol)
