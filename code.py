import streamlit as st
import yfinance as yf
import pandas as pd

def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

st.title('Stock Data App')

# User enters a ticker symbol
ticker = st.text_input('Enter a ticker symbol (e.g. AAPL):')

start_date = st.date_input('Start date')
end_date = st.date_input('End date')

if ticker and st.button('Fetch Data'):
    try:
        data = load_data(ticker, start_date, end_date)
        st.dataframe(data)  # Display data as a table
    except Exception as e:
        st.error('Failed to fetch data. Please make sure the ticker symbol is correct.')
