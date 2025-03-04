import streamlit as st
import pandas as pd
import psycopg2
import os
import time
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Streamlit UI 
st.set_page_config(page_title="Real-Time Stock Dashboard", layout="wide")
st.title("Real-Time Stock Dashboard")


stock_ticker = st.selectbox(
    "Select Stock",
    ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]
)

def get_stock_data():
    query = "SELECT ticker, price, timestamp FROM stocks WHERE ticker = %s ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, conn, params=(stock_ticker,))
    return df

st.header(f"Live Stock Price for {stock_ticker}")
latest_data = get_stock_data()
if not latest_data.empty:
    st.metric(label="Latest Price", value=round(latest_data.iloc[0]['price'], 2))

st.subheader("Stock Price Over Time")
if not latest_data.empty:
    chart_data = latest_data[["timestamp", "price"]].set_index("timestamp")
    st.line_chart(chart_data)

time.sleep(60)
st.experimental_rerun()
