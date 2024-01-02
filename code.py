import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def is_valid_ticker(ticker):
    # Try to fetch a small amount of data
    data = yf.download(ticker, period='1d', interval='1m')
    # If the data is empty, the ticker is probably invalid
    return not data.empty

st.title('Stock Data App')

# User enters a ticker symbol
ticker = st.text_input('Enter a ticker symbol (e.g. AAPL):')

start_date = st.date_input('Start date')
end_date = st.date_input('End date')

if ticker and st.button('Fetch Data'):
    if end_date == date.today():
        st.warning('Today\'s data may not be available yet.')
    elif is_valid_ticker(ticker):
        data = load_data(ticker, start_date, end_date)
        st.dataframe(data)  # Display data as a table
    else:
        st.error('Invalid ticker symbol. Please enter a valid ticker symbol.')
