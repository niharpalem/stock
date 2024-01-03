import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
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

def create_custom_plot(data, ticker):
    # Custom Plot
    if st.checkbox('Create a custom plot for {}'.format(ticker)):
        plot_types = ['scatter', 'line', 'area', 'bar', 'box', 'histogram']
        plot_type = st.selectbox('Select plot type', plot_types)
        x_var = st.selectbox('Select x variable', data.columns)
        y_var = st.selectbox('Select y variable', data.columns)
        color = st.color_picker('Pick a color for your plot')
        fig = px.__dict__[plot_type](data, x=x_var, y=y_var, color_discrete_sequence=[color])
        st.plotly_chart(fig)

st.title('Stock Data App')

# User enters a list of ticker symbols, separated by commas
tickers = st.text_input('Enter ticker symbols (e.g. AAPL,MSFT), separated by commas:')

start_date = st.date_input('Start date')
end_date = st.date_input('End date')

if tickers and st.button('Fetch Data'):
    tickers = [ticker.strip() for ticker in tickers.split(',')]
    for ticker in tickers:
        if end_date == date.today():
            st.warning('Today\'s data for {} may not be available yet.'.format(ticker))
        elif is_valid_ticker(ticker):
            data = load_data(ticker, start_date, end_date)
            st.write('Data for {}:'.format(ticker))
            st.dataframe(data)  # Display data as a table
            create_custom_plot(data, ticker)
        else:
            st.error('Invalid ticker symbol: {}. Please enter a valid ticker symbol.'.format(ticker))
