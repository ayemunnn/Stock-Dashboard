# **Kafka-Powered Real-Time Stock Dashboard**  

A real-time stock price tracking system that streams live stock prices, processes them using Apache Kafka, stores them in PostgreSQL, and visualizes them in a dynamic web dashboard built with Dash and Plotly. This project is designed for real-time financial data tracking and analysis.  

## **Features**  
- Real-time stock price streaming using Yahoo Finance API  
- Apache Kafka for data streaming and message queuing  
- PostgreSQL for persistent data storage  
- Dash and Plotly for live data visualization  
- User-selectable stocks with a dropdown menu  

## **Tech Stack**  
- **Apache Kafka** - Real-time event streaming  
- **Yahoo Finance API (`yfinance`)** - Fetching stock data  
- **PostgreSQL (`psycopg2`)** - Database for storing stock prices  
- **Dash & Plotly** - Web-based data visualization  
- **Python (`kafka-python`, `pandas`)** - Backend processing  

## **How It Works**  

1. **Kafka Producer (`fetch_data_kafka.py`)** fetches stock prices every minute and publishes them to Kafka.  
2. **Kafka Broker (`stock_prices` topic)** acts as a message queue to store stock data temporarily.  
3. **Kafka Consumer (`kafka_consumer.py`)** reads stock prices from Kafka and stores them in PostgreSQL.  
4. **Live Dashboard (`dashboard_kafka.py`)** retrieves stock prices from PostgreSQL and visualizes them in real time.  

## **Setup Instructions**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/yourusername/kafka-stock-dashboard.git
cd kafka-stock-dashboard
```

### **2. Create a Virtual Environment and Install Dependencies**  
```bash
conda create --name kafka_dashboard python=3.9 -y
conda activate kafka_dashboard
pip install -r requirements.txt
```

### **3. Set Up PostgreSQL**  
1. Install PostgreSQL and create a database  
2. Run the following SQL commands to create a table:  
```sql
CREATE DATABASE stock_data;
\c stock_data;
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    price FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
3. Store database credentials in a `.env` file:  
```ini
DB_NAME=stock_data
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### **4. Start Kafka and Zookeeper**  
```bash
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
bin\windows\kafka-server-start.bat config\server.properties
```

### **5. Start the Kafka Producer**  
```bash
python fetch_data_kafka.py
```

### **6. Start the Kafka Consumer**  
```bash
python kafka_consumer.py
```

### **7. Start the Live Dashboard**  
```bash
python dashboard_kafka.py
```
Open a browser and go to `http://127.0.0.1:8050/` to view the dashboard.  

## **Future Enhancements**  
- Add sentiment analysis for stocks based on news and social media data  
- Store historical stock prices for long-term trend analysis  
- Deploy the dashboard on a cloud platform like AWS, Heroku, or Streamlit  
- Optimize performance using Apache Spark for large-scale streaming  

## **Contributing**  
Contributions are welcome. Fork the repository and submit a pull request with your improvements.  

## **License**  
This project is open-source and available under the MIT License.