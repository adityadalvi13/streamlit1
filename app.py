import streamlit as st
from client import STOCK_API
import plotly.graph_objects as go
 
st.set_page_config(page_title="STOCK MARKET APP", layout='wide')
 
st.title("Stock Market App")
st.subheader("by Aditya Dalvi")
 
company = st.text_input("Enter Company Name")
 
@st.cache_resource(ttl=3600)
def fetch_data():
    return STOCK_API(api_key=st.secrets["API_KEY"])
 
stock_api = fetch_data()
 
@st.cache_data(ttl=3600)
def get_symbol(company_name):
    return stock_api.symbol_search(company_name)
 
@st.cache_data(ttl=3600)
def plot_graph(symbol):
    df = stock_api.daily_data(symbol)
    fig = stock_api.plot_chart(df)
    return fig
 
if company:
    company_data = get_symbol(company)
 
    if company_data:
        symbol_list = list(company_data.keys())
        option = st.selectbox("Select Stock Symbol", symbol_list)
 
        selected_info = company_data[option]
 
        st.success(f"**Company Name:** {selected_info[0]}")
        st.success(f"**Region:** {selected_info[1]}")
        st.success(f"**Currency:** {selected_info[2]}")
 
        submit = st.button("plot" , type  = "primary")
 
 
 
        # Show chart immediately
        if submit:
            fig = plot_graph(option)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No matching company found.")
 