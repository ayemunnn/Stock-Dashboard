from kafka import KafkaProducer
import yfinance as yf
import json
import time

# Setting up Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",  
    value_serializer=lambda v: json.dumps(v).encode("utf-8"), 
)

# List of stock tickers to track
stocks_to_track = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]

def fetch_stock_price(ticker):
    """Fetches real-time stock price from Yahoo Finance API"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")  
    last_row = data.tail(1) 

    if not last_row.empty:
        price = round(last_row["Close"].values[0], 2)  
        message = {"ticker": ticker, "price": price, "timestamp": time.time()}
        producer.send("stock_prices", message) 
        print(f"Published: {message}")  

# Fetching stock prices every minute
while True:
    for stock in stocks_to_track:
        fetch_stock_price(stock)
    time.sleep(60) 
