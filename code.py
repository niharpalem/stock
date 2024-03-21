import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Ticker'] = ticker  # Add a column for the ticker symbol
    return data

def is_valid_ticker(ticker):
    data = yf.download(ticker, period='1d', interval='1m')
    return not data.empty

def calculate_daily_return(data):
    return (data['Close'] / data['Close'].shift(1)) - 1

def calculate_volatility(data, period):
    daily_return = calculate_daily_return(data)
    return daily_return.rolling(window=period).std()

def calculate_moving_average(data, period):
    return data['Close'].rolling(window=period).mean()

def calculate_ema(data, span=20):
    return data['Close'].ewm(span=span, adjust=False).mean()

def calculate_macd(data):
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd - signal

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=period-1, adjust=False).mean()
    ema_down = down.ewm(com=period-1, adjust=False).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))

# Streamlit UI code
st.title('Stock Data App')
tickers = st.text_input('Enter ticker symbols (e.g. AAPL,MSFT), separated by commas:')
start_date = st.date_input('Start date')
end_date = st.date_input('End date')

formulas = st.multiselect('Select formulas to apply', ['Daily Return', 'Moving Average', 'Volatility', 'Exponential Moving Average', 'MACD', 'RSI'])

# Additional UI elements for selecting periods
ma_period = st.sidebar.slider('Moving Average Period', min_value=1, max_value=30, value=5, step=1)
vol_period = st.sidebar.slider('Volatility Period', min_value=1, max_value=30, value=5, step=1)

if tickers and st.button('Fetch Data'):
    tickers = [ticker.strip() for ticker in tickers.split(',')]
    for ticker in tickers:
        if is_valid_ticker(ticker):
            data = load_data(ticker, start_date, end_date)
            st.write(f'Data for {ticker}:')
            if 'Daily Return' in formulas:
                data['Daily Return'] = calculate_daily_return(data)
            if 'Volatility' in formulas:
                data['Volatility'] = calculate_volatility(data, vol_period)
            if 'Moving Average' in formulas:
                data['Moving Average'] = calculate_moving_average(data, ma_period)
            if 'Exponential Moving Average' in formulas:
                data['EMA'] = calculate_ema(data)
            if 'MACD' in formulas:
                data['MACD'] = calculate_macd(data)
            if 'RSI' in formulas:
                data['RSI'] = calculate_rsi(data)
            st.dataframe(data)
        else:
            st.error(f'Invalid ticker symbol: {ticker}. Please enter a valid ticker symbol.')
