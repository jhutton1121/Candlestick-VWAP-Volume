# Candlestick-VWAP-Volume
This is a simple script that uses pandas and plotly to graph stock data. It reads data from yahoo finance.

It calculates volatility weighted average price, vwap, as well as resistance and support levels. Resistance and support are defined by +/- 2 10 period rolling
standard deviations away from the 10 period rolling mean of vwap. 


To do:
Develop buy/sell signals as well as buy/sell visualization on the graph. Expand the blueprint to a dashboard where the graph changess depending on which stock you select
via Dash.
