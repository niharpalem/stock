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

# Add options to select the time period for Moving Average and Volatility
ma_period = st.sidebar.slider('Moving Average Period', min_value=1, max_value=30, value=5, step=1)
vol_period = st.sidebar.slider('Volatility Period', min_value=1, max_value=30, value=5, step=1)

# Add explanations for each calculation
explanations = {
    'Daily Return': 'The daily return is the percentage change in the closing price from one day to the next. It\'s a measure of the profitability of the investment.',
    'Moving Average': 'The moving average is the average closing price over a certain number of days. It\'s used to analyze price trends by smoothing out price fluctuations.',
    'Volatility': 'The volatility is the standard deviation of the daily returns over a certain number of days. It\'s a measure of the riskiness of the stock.',
    'Exponential Moving Average': 'The exponential moving average is a type of moving average that gives more weight to recent prices, making it more responsive to new information.',
    'MACD': 'The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.',
    'RSI': 'The Relative Strength Index (RSI) is a momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset.'
}
if tickers and st.button('Fetch Data'):
    tickers = [ticker.strip() for ticker in tickers.split(',')]
    for ticker in tickers:
        if end_date == date.today():
            st.warning('Today\'s data for {} may not be available yet.'.format(ticker))
        elif is_valid_ticker(ticker):
            data = load_data(ticker, start_date, end_date)
            st.write('Data for {}:'.format(ticker))
            for formula in formulas:
                if formula == 'Daily Return':
                    data['Daily Return'] = (data['Close'] / data['Close'].shift(1)) - 1
                elif formula == 'Moving Average':
                    data['Moving Average'] = data['Close'].rolling(window=ma_period).mean()
                elif formula == 'Volatility':
                    data['Volatility'] = data['Daily Return'].rolling(window=vol_period).std()
                elif formula == 'Exponential Moving Average':
                    data['EMA'] = data['Close'].ewm(span=20, adjust=False).mean()
                elif formula == 'MACD':
                    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                    macd = exp1-exp2
                    signal = macd.ewm(span=9, adjust=False).mean()
                    data['MACD'] = macd - signal
                elif formula == 'RSI':
                    delta = data['Close'].diff()
                    up = delta.clip(lower=0)
                    down = -1*delta.clip(upper=0)
                    ema_up = up.ewm(com=13, adjust=False).mean()
                    ema_down = down.ewm(com=13, adjust=False).mean()
                    rs = ema_up/ema_down
                    data['RSI'] = 100 - (100/(1 + rs))
                st.markdown('**{}**: {}'.format(formula, explanations[formula]))
            st.dataframe(data)  # Display data as a table
        else:
            st.error('Invalid ticker symbol: {}. Please enter a valid ticker symbol.'.format(ticker))
