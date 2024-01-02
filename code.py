import streamlit as st
import yfinance as yf
import pandas as pd

def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

st.title('Stock Data App')

ticker = st.text_input('Enter a stock symbol (e.g. AAPL):', value='AAPL')

start_date = st.date_input('Start date')
end_date = st.date_input('End date')

if st.button('Fetch Data'):
    data = load_data(ticker, start_date, end_date)
    st.dataframe(data)  # Display data as a table
