# Create history of last 60 days for BTC, in USD. It then creates a chart of the data using plotly
# Depends on ploty pandas pandas-datareader kaleido, all available on conda-forge repo
# Adapted from https://itnext.io/create-beautiful-cryptocurrency-graphs-in-python-bec7b9cbc21a

from datetime import datetime, timedelta
from re import template

import pandas as pd
import pandas_datareader as pdr
import plotly.graph_objects as go
import plotly.io as pio

CRYPTO = 'BTC'
CURRENCY = 'USD'

# Get data from Yahoo API using data_reader


def getData(cryptocurrency):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    last_year_date = (now - timedelta(days=60)).strftime("%Y-%m-%d")
    start = pd.to_datetime(last_year_date)
    end = pd.to_datetime(current_date)
    data = pdr.get_data_yahoo(f'{cryptocurrency}-{CURRENCY}', start, end)
    return data


crypto_data = getData(CRYPTO)

fig = go.Figure(
    data=[
        go.Candlestick(
            x=crypto_data.index,
            open=crypto_data.Open,
            high=crypto_data.High,
            low=crypto_data.Low,
            close=crypto_data.Close
        ),
        go.Scatter(
            x=crypto_data.index,
            y=crypto_data.Close.rolling(window=10).mean(),
            mode='lines',
            name='10SMA',
            line={'color': '#ff006a'}
        )
    ]
)

fig.update_layout(
    title=f'{CRYPTO} history over 60 days',
    yaxis_title=f'Price ({CURRENCY})',
    template='plotly_dark',
    xaxis_rangeslider_visible=False
)

fig.update_yaxes(tickprefix='$')
fig.write_image("images/crypto.png")
