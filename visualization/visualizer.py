# #%% <-  Delete # for scientific mode!
# https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
# https://www.youtube.com/watch?v=pkk5U-8Vl7A
#%%

import pandas as pd
import mplfinance as mpf
import plotly as py
import requests
import io
# test: displays images


print(py.__version__)

apple_df = pd.read_csv('visualization/AAPL.csv', index_col=0, parse_dates=True)
apple_df.info()
# dt_range = pd.date_range(start="2020-03-01", end="2020-03-31")
# apple_df = apple_df[apple_df.index.isin(dt_range)]
print(apple_df.head())
# apple_df = apple_df.set_index('Date')
imageBuffer = io.BytesIO()
mpf.plot(apple_df, type='candle', volume=True, mav=(20,40), savefig=imageBuffer)
mpf.savefig(imageBuffer, format='png')











