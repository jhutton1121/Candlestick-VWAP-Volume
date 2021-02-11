import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from plotly.subplots import make_subplots

stock = "MSFT"

df = web.DataReader(stock, data_source = 'yahoo', start = '01-01-2019')


def vwap(df):
    v = df.Volume
    p = df.Close
    return df.assign(vwap = (v *p).cumsum() / v.cumsum())

def bands(df):
    df['rolling_mean'] = df.vwap.rolling(10).mean()
    df['rolling_std'] = df.vwap.rolling(10).std()
    df['upper_band'] = df.vwap + 2*df.rolling_std
    df['lower_band'] = df.vwap - 2*df.rolling_std
    
    return df
    
    

df = df.groupby(df.index, group_keys = False).apply(vwap)
df = bands(df)

trace_candle = {
    'x': df.index,
    'open':df.Open,
    'close': df.Close,
    'high': df.High,
    'low':df.Low,
    'type': 'candlestick',
    'name': stock,
    'showlegend': True
}

trace_vwap = {
    'x': df.index,
    'y': df.vwap,
    'name': 'vwap'
}

trace_res  = {
    'x': df.index,
    'y': df.upper_band,
    'name': 'resistance'
}

trace_sup = {
    'x' : df.index,
    'y' : df.lower_band,
    'name':'support'
}

trace_vol = {
    'x': df.index,
    'y': df.Volume,
    'name':'volume'
}

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.1)




fig.add_trace(go.Candlestick(trace_candle), row = 1, col = 1)
fig.add_trace(go.Scatter(trace_vwap), row = 1, col = 1)
fig.add_trace(go.Scatter(trace_sup), row = 1, col = 1)
fig.add_trace(go.Scatter(trace_res), row = 1, col = 1)
fig.add_trace(go.Bar(trace_vol), row = 2, col =1)
fig.show()
