from kafka import KafkaConsumer
import psycopg2
import json
import os
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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id SERIAL PRIMARY KEY,
        ticker VARCHAR(10),
        price FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

consumer = KafkaConsumer(
    "stock_prices",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("Listening for stock prices") #To showcase that the consumer is running

for message in consumer:
    data = message.value
    print(f"Received: {data}")

    cursor.execute(
        "INSERT INTO stocks (ticker, price, timestamp) VALUES (%s, %s, to_timestamp(%s))",
        (data["ticker"], float(data["price"]), data["timestamp"]),
    )
    conn.commit()
    print(f"Inserted into DB: {data}")
