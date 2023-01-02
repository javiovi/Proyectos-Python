import requests
from PIL import Image
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
from bs4 import BeautifulSoup
import json
import time
from pandasql import sqldf


pysqldf = lambda q: sqldf(q, globals())

st.set_page_config(layout="wide")

image = Image.open('descarga.jpg')

st.image(image, width=500)
st.title("Crypto Price App")
st.markdown(
    """
This app retrieves cryptocurrency financial information for the top 100 cryptocurrency from the **CoinMarketCap**!
"""
)

expander_bar = st.expander("About")
expander_bar.markdown(
    """
* **Data source:** Use the API Free Service of http://coinmarketcap.com.
* **Credit:** Code on https://github.com/dataprofessor/streamlit_freecodecamp/blob/main/app_6_eda_cryptocurrency/crypto-price-app.py serves a guide for the design of the fronted interface!
* **Update:** Since the data is from the API service it update every minute.
"""
)



col1 = st.sidebar


col1.header("Input Options")


currency_price_unit = col1.selectbox("Select currency for price", ("USD", "BTC", "ETH"))

###API call - getting the data
# BASE_DIR = os.path.dirname(__file__)
# @st.cache
def get_data():
    my_api_key="c6c41791-1913-42f2-977d-ef13f907799c"
    headers = {
        "X-CMC_PRO_API_KEY" : my_api_key,
        'Accepts' : 'application/json'
    }
    params = {
        "start": "1",
        "limit": "100",
        "convert": "USD"
    }
    url= "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    data = requests.get(url, params=params, headers=headers).json()
    coins= data["data"]

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []
    for i in coins:
        coin_name.append(i["name"])
        coin_symbol.append(i["symbol"])
        price.append(i["quote"]["USD"]["price"])
        percent_change_24h.append(i["quote"]["USD"]["percent_change_24h"])
        percent_change_7d.append(i["quote"]["USD"]["percent_change_7d"])
        percent_change_1h.append(i["quote"]["USD"]["percent_change_1h"])
        market_cap.append(i["quote"]["USD"]["market_cap"])
        volume_24h.append(i["quote"]["USD"]["volume_24h"])
    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h

    

    return df


df= get_data()

# Sidebar - Cryptocurrency selections
query_sorting_coins="""
select coin_symbol
from df
order by coin_symbol asc
"""
result_1=sqldf(query_sorting_coins)
sorted_coin=list(result_1["coin_symbol"])

selected_coin = tuple(col1.multiselect("Cryptocurrency", sorted_coin, sorted_coin))
query_for_df_selected_coin = """
SELECT
* 
FROM 
df 
WHERE 
coin_symbol IN  {}
""".format(selected_coin)

df_selected_coin=sqldf(query_for_df_selected_coin)

# Sidebar - Number of coins to display
num_coin = col1.slider("Display Top N Coins", 1, 100, 100)
query_for_df_coins="""
SELECT
*
FROM 
df_selected_coin
LIMIT %s
"""%num_coin
df_coins=sqldf(query_for_df_coins)

# Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox("Percent change time frame", ["7d", "24h", "1h"])
percent_dict = {
    "7d": "percent_change_7d",
    "24h": "percent_change_24h",
    "1h": "percent_change_1h"
}
selected_percent_timeframe = percent_dict[percent_timeframe]
# Sidebar - Sorting values
sort_values = col1.selectbox("Sort values?", ["Yes", "No"])


query_for_df_change="""
SELECT 
coin_symbol, percent_change_1h, percent_change_24h, percent_change_7d
FROM 
df_selected_coin
LIMIT %s
"""%num_coin

df_change = sqldf(query_for_df_change)

df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0

#---- data selection for metrics ----- BTC ,ETH, USDT
####BTC
query_df_change_BTC_1h= """
select percent_change_1h, price
from df_selected_coin
where coin_symbol = "BTC"
"""
df_change_BTC_1h = sqldf(query_df_change_BTC_1h)
price_BTC = "${:.2f}".format(float(df_change_BTC_1h["price"].astype(float)))
change_BTC_1h = "%{:.2f}".format(float(df_change_BTC_1h["percent_change_1h"].astype(float))*100)

## ETH
query_df_change_ETH_1h= """
select percent_change_1h, price
from df_selected_coin
where coin_symbol = "ETH"
"""
df_change_ETH_1h = sqldf(query_df_change_ETH_1h)
price_ETH = "${:.2f}".format(float(df_change_ETH_1h["price"].astype(float)))
change_ETH_1h = "%{:.2f}".format(float(df_change_ETH_1h["percent_change_1h"].astype(float))*100)

# SOL
query_df_change_SOL_1h= """
select percent_change_1h, price
from df_selected_coin
where coin_symbol = "SOL"
"""
df_change_SOL_1h = sqldf(query_df_change_SOL_1h)
price_SOL = "${:.2f}".format(float(df_change_SOL_1h["price"].astype(float)))
change_SOL_1h = "%{:.2f}".format(float(df_change_SOL_1h["percent_change_1h"].astype(float))*100)

col1, col2, col3 = st.columns(3)
col1.metric(label = "BTC Price Change 1h", value = price_BTC , delta=change_BTC_1h )
col2.metric(label = "ETH Price Change 1h", value = price_ETH , delta= change_ETH_1h)
col3.metric(label = "SOL Price Change 1h", value = price_SOL , delta=change_SOL_1h)



st.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        query_for_df_change_7d= """
        SELECT *
        FROM df_change
        ORDER BY percent_change_7d
        """
        df_change_7d=sqldf(query_for_df_change_7d)

        st.write('*7 days period*')
        y_axis= list(df_change_7d["percent_change_7d"])
        x_axis = list(df_change_7d["coin_symbol"])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("% percentage",fontsize=7)
        plt.ylabel("Symbol Coin",fontsize=7)
        plt.barh(x_axis, y_axis, color = df_change_7d.positive_percent_change_7d.map({1: 'g', 0: 'r'}))
        plt.title("Price Change Period 7d", fontsize= 8)
        st.pyplot(plt)
            
    else:
        st.write('*7 days period*')
        y_axis= list(df_change["percent_change_7d"])
        x_axis = list(df_change["coin_symbol"])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("% percentage",fontsize=7)
        plt.ylabel("Symbol Coin",fontsize=7)
        plt.barh(x_axis, y_axis, color = df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
        plt.title("Price Change Period 7d", fontsize= 8)
        st.pyplot(plt)
        
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        query_for_df_change_24h= """
        SELECT *
        FROM df_change
        ORDER BY percent_change_24h
        """
        df_change_24h=sqldf(query_for_df_change_24h)
 
        st.write('*24 hour period*')
        y_axis= list(df_change_24h["percent_change_24h"])
        x_axis = list(df_change["coin_symbol"])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("% percentage",fontsize=7)
        plt.ylabel("Symbol Coin",fontsize=7)
        plt.barh(x_axis, y_axis, color = df_change_24h.positive_percent_change_24h.map({1: 'g', 0: 'r'}))
        plt.title("Price Change Period 24h", fontsize= 8)
        st.pyplot(plt)
        
    else:
        st.write('*24 hour period*')
        y_axis= list(df_change["percent_change_24h"])
        x_axis = list(df_change["coin_symbol"])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("% percentage",fontsize=7)
        plt.ylabel("Symbol Coin",fontsize=7)
        plt.barh(x_axis, y_axis, color = df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
        plt.title("Price Change Period 24h", fontsize= 8)
        st.pyplot(plt)
elif percent_timeframe == '1h':
    if sort_values == 'Yes':
        query_for_df_change_1h= """
        SELECT *
        FROM df_change
        ORDER BY percent_change_1h
        """
        df_change_1h=sqldf(query_for_df_change_1h)

        st.write('*1 hour period*')
        y_axis= list(df_change_1h["percent_change_1h"])
        x_axis = list(df_change_1h["coin_symbol"])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("% percentage",fontsize=7)
        plt.ylabel("Symbol Coin",fontsize=7)
        plt.barh(x_axis, y_axis, color = df_change_1h.positive_percent_change_1h.map({1: 'g', 0: 'r'}))
        plt.title("Price Change Period 1h", fontsize= 8)
        st.pyplot(plt)
        
    else:
        st.write('*1 hour period*')
        y_axis= list(df_change["percent_change_1h"])
        x_axis = list(df_change["coin_symbol"])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("% percentage",fontsize=7)
        plt.ylabel("Symbol Coin",fontsize=7)
        plt.barh(x_axis, y_axis, color = df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
        plt.title("Price Change Period 1h", fontsize= 8)
        st.pyplot(plt)

#-----------Table of selected coins

st.subheader("Price Data of Selected Cryptocurrency")
st.write(
    "Data Dimension: "
    + str(df_selected_coin.shape[0])
    + " rows and "
    + str(df_selected_coin.shape[1])
    + " columns."
)

st.dataframe(df_coins)

#-----------Table of price change

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)    
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)


#------Table of price change
st.subheader('Table of % Price Change')

st.dataframe(df_change)