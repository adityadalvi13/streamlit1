import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
 
class STOCK_API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
        }
 
    def symbol_search(self, keyword):
        querystring = {
            "datatype": "json",
            "keywords": keyword,
            "function": "SYMBOL_SEARCH"
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        dict1 = {}
        for i in data.get('bestMatches', []):
            symbols = i["1. symbol"]
            dict1[symbols] = [i['2. name'], i['4. region'], i['8. currency']]
        return dict1
 
    def daily_data(self, symbol):
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json"
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        df = data['Time Series (Daily)']
        df = pd.DataFrame(df).T
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        return df
 
    def plot_chart(self, df):
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df["1. open"],
            high=df["2. high"],
            low=df["3. low"],
            close=df["4. close"]
        )])
        fig.update_layout(title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
        return fig
    
 