import requests
import pandas as pd
import streamlit as st
 
 
class StockApi:
 
    def __init__(self , api_key):
        self.api_key = st.secrets["API_KEY"]
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {"x-rapidapi-key": api_key,
        "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"}
 
    def search_symbol(self , keywords):
        querystring = {"datatype":"json",
                       "keywords":keywords,
                       "function":"SYMBOL_SEARCH"}
        response = requests.get(self.url,
                                headers=self.headers,
                                params=querystring)
        response.raise_for_status()
        data = response.json()
        symbol_list = []
        for i in data['bestMatches']:
            symbol_list.append(i['1. symbol'])
        return symbol_list
   
   
 
    def time_series_daily_data(self, symbol):
        querystring = {"function":"TIME_SERIES_DAILY",
                       "symbol":symbol,
                       "outputsize":"compact",
                       "datatype":"json"}
        response = requests.get(self.url,
                                headers=self.headers,
                                params=querystring)
        df = response.json()
 
        # fetch time series data and convert in dataframe
        df =  pd.DataFrame(df['Time Series (Daily)']).T
 
        # converting data from object to float
        df =  df.astype(float)
 
        # changing datatype of index
 
        df.index  = pd.to_datetime(df.index)
 
        # give name to index
        df.index.name  = "Date"
 
        return df
 
 
    def plot_graph(self , df):
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open  =df['1. open'],
            high=df['2. high'],
            low=df["3. low"],
            close=df['4. close'],
            increasing_line_color='green',
            decreasing_line_color='red')])
        fig.show()