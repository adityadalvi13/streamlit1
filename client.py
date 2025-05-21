import requests
import pandas as pd
import plotly.graph_objects as go

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
        if response.status_code != 200:
            return {}
        data = response.json()
        dict1 = {}
        for i in data.get('bestMatches', []):
            symbols = i.get("1. symbol")
            name = i.get("2. name")
            region = i.get("4. region")
            currency = i.get("8. currency")
            if symbols and name and region and currency:
                dict1[symbols] = [name, region, currency]
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
        df = data.get('Time Series (Daily)', {})
        if not df:
            return pd.DataFrame()
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
