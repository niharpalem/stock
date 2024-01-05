import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Ticker'] = ticker  # Add a column for the ticker symbol
    return data

def is_valid_ticker(ticker):
    # Try to fetch a small amount of data
    data = yf.download(ticker, period='1d', interval='1m')
    # If the data is empty, the ticker is probably invalid
    return not data.empty

st.title('Stock Data App')

# User enters a list of ticker symbols, separated by commas
tickers = st.text_input('Enter ticker symbols (e.g. AAPL,MSFT), separated by commas:')

start_date = st.date_input('Start date')
end_date = st.date_input('End date')

formulas = st.multiselect('Select formulas to apply', ['Daily Return', 'Moving Average', 'Volatility', 'Exponential Moving Average', 'MACD', 'RSI'])

if tickers and st.button('Fetch Data'):
    tickers = [ticker.strip() for ticker in tickers.split(',')]
    for ticker in tickers:
        if end_date == date.today():
            st.warning('Today\'s data for {} may not be available yet.'.format(ticker))
        elif is_valid_ticker(ticker):
            data = load_data(ticker, start_date, end_date)
            st.write('Data for {}:'.format(ticker))
            if 'Daily Return' in formulas:
                data['Daily Return'] = (data['Close'] / data['Close'].shift(1)) - 1
            if 'Moving Average' in formulas:
                data['Moving Average'] = data['Close'].rolling(window=5).mean()
            if 'Volatility' in formulas:
                data['Volatility'] = data['Daily Return'].rolling(window=5).std()
            if 'Exponential Moving Average' in formulas:
                data['EMA'] = data['Close'].ewm(span=20, adjust=False).mean()
            if 'MACD' in formulas:
                exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                macd = exp1-exp2
                signal = macd.ewm(span=9, adjust=False).mean()
                data['MACD'] = macd - signal
            if 'RSI' in formulas:
                delta = data['Close'].diff()
                up = delta.clip(lower=0)
                down = -1*delta.clip(upper=0)
                ema_up = up.ewm(com=13, adjust=False).mean()
                ema_down = down.ewm(com=13, adjust=False).mean()
                rs = ema_up/ema_down
                data['RSI'] = 100 - (100/(1 + rs))
            st.dataframe(data)  # Display data as a table
        else:
            st.error('Invalid ticker symbol: {}. Please enter a valid ticker symbol.'.format(ticker))
