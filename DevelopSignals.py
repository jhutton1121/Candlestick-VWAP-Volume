import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import date
from datetime import datetime as dt


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
    
def trace_vwap(df):
    trace_vwap = {
        'x': df.index,
        'y': df.vwap,
        'name': 'vwap'
        }
    return trace_vwap

def trace_res(df):
     trace_res  = {
        'x': df.index,
        'y': df.upper_band,
        'name': 'resistance'
    }
     return trace_res

def trace_sup(df):
    trace_sup = {
        'x' : df.index,
        'y' : df.lower_band,
        'name':'support'
    }
    return trace_sup

def trace_vol(df):
    trace_vol = {
        'x': df.index,
        'y': df.Volume,
        'name':'volume'
    }
    return trace_vol

def trace_candle(df, value):
    trace_candle = {
    'x': df.index,
    'open':df.Open,
    'close': df.Close,
    'high': df.High,
    'low':df.Low,
    'type': 'candlestick',
    'name': value,
    'showlegend': True
    }
    return trace_candle


stocks = ['MSFT','AAPL','TSLA']


app = dash.Dash("Candlesticks")

app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker-range', #id to be used for callback
        start_date=dt(2019, 1, 1), #default start date
        min_date_allowed=dt(2010,1,1), #default minimum date
        end_date=dt.now(),
        ),
    dcc.Dropdown(
        id = 'dropdown',
        options = [{'label':stock, 'value':stock} for stock in stocks],
        value = 'AAPL'
        ),
    
    dcc.Graph(id='candles')
    ])

@app.callback(Output('candles', 'figure'),
              [Input('dropdown', 'value'),
               Input('date-picker-range', 'start_date'),
               Input('date-picker-range', 'end_date')])
def update_graph(selected_dropdown_value, start_date, end_date):
    
    df = web.DataReader(
        selected_dropdown_value,
        'yahoo',
        start_date,
        end_date
    )

    df = df.groupby(df.index, group_keys = False).apply(vwap)
    df = bands(df)   
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.1)
    fig.add_trace(go.Candlestick(trace_candle(df,selected_dropdown_value)), row = 1, col = 1)
    fig.add_trace(go.Scatter(trace_vwap(df)), row = 1, col = 1)
    fig.add_trace(go.Scatter(trace_sup(df)), row = 1, col = 1)
    fig.add_trace(go.Scatter(trace_res(df)), row = 1, col = 1)
    fig.add_trace(go.Bar(trace_vol(df)), row = 2, col =1)
    
    return fig



    

    




app.run_server()
