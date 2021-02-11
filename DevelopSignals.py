import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from plotly.subplots import make_subplots

stock = "MSFT"
stock1 = "GME"

df = web.DataReader(stock, data_source = 'yahoo', start = '01-01-2019')


def vwap(df):
    v = df.Volume
    p = df.Close
    return df.assign(vwap = (v *p).cumsum() / v.cumsum())

def bands(df):
    df['rolling_mean'] = df.vwap.rolling(10).mean()
    df['rolling_std'] = df.vwap.rolling(10).std()
    df['upper_band'] = df.rolling_mean + 2*df.rolling_std
    df['lower_band'] = df.rolling_mean - 2*df.rolling_std
    
    return df
    
    

df = df.groupby(df.index, group_keys = False).apply(vwap)
df = bands(df)

trace1 = {
    'x': df.index,
    'open':df.Open,
    'close': df.Close,
    'high': df.High,
    'low':df.Low,
    'type': 'candlestick',
    'name': stock,
    'showlegend': True
}

trace2 = {
    'x': df.index,
    'y': df.vwap,
    'name': 'vwap'
}

trace3  = {
    'x': df.index,
    'y': df.upper_band,
    'name': 'resistance'
}

trace4 = {
    'x' : df.index,
    'y' : df.lower_band,
    'name':'support'
}

trace5 = {
    'x': df.index,
    'y': df.Volume,
    'name':'volume'
}

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.1)




fig.add_trace(go.Candlestick(trace1), row = 1, col = 1)
fig.add_trace(go.Scatter(trace2), row = 1, col = 1)
fig.add_trace(go.Scatter(trace3), row = 1, col = 1)
fig.add_trace(go.Scatter(trace4), row = 1, col = 1)
fig.add_trace(go.Bar(trace5), row = 2, col =1)
fig.show()
