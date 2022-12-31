import yfinance as yf
import streamlit as st
import pandas as  pd    

st.write("""
    ## Simple Stock Price App
    Shown are the stock **closing price** and ***volume*** of Google!



""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period= 'id', start='2010-5-31', end='2023-5-31')
# Open High Low Close Volume Dividens Stock price
st.write( """
Close Price """)
st.line_chart(tickerDf.Close)

st.write(""" Volume Price """)
st.line_chart(tickerDf.Volume)