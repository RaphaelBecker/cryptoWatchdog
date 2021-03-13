# #%% <-  Delete # for scientific mode!
# https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
#%%
import cufflinks as cf
import pandas as pd
import plotly.graph_objects as go

apple_df = pd.read_csv('visualization/AAPL.csv', index_col=0, parse_dates=True)
dt_range = pd.date_range(start="2020-03-01", end="2020-03-31")
apple_df = apple_df[apple_df.index.isin(dt_range)]
print(apple_df.head())

qf = cf.QuantFig(apple_df, title='Apple Quant Figure', legend='top', name='GS')

qf.add_bollinger_bands(periods=20, boll_std=2, colors=['magenta', 'grey'], fill=True)
qf.add_sma([10, 20], width=2, color=['green', 'lightgreen'],legendgroup=True)
qf.add_rsi(periods=20, color='java')


print(type(qf))
plot = qf.figure()
print(type(plot))
plot.show(renderer="svg")
fig = go.Figure()

qf.iplot()
# qf.iplot(asImage=True)







