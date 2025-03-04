import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

app = dash.Dash(__name__)

def get_stock_data():
    query = "SELECT ticker, price, timestamp FROM stocks ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, conn)
    return df

app.layout = html.Div([
    html.H1("Real-Time Stock Dashboard"),
    
    
    html.Label("Select Stock:"),
    dcc.Dropdown(
        id="stock-dropdown",
        options=[{"label": "AAPL", "value": "AAPL"},
                 {"label": "GOOGL", "value": "GOOGL"},
                 {"label": "TSLA", "value": "TSLA"},
                 {"label": "MSFT", "value": "MSFT"},
                 {"label": "AMZN", "value": "AMZN"}],
        value="AAPL",  
        clearable=False
    ),

    dcc.Graph(id="live-stock-chart"),
   
    dcc.Interval(id="interval-component", interval=60000, n_intervals=0)
])

@app.callback(
    dash.Output("live-stock-chart", "figure"), 
    [dash.Input("interval-component", "n_intervals"), dash.Input("stock-dropdown", "value")]
)
def update_stock_chart(n, selected_stock):
    df = get_stock_data()
    
    
    df = df[df["ticker"] == selected_stock]

   
    fig = go.Figure([go.Scatter(x=df["timestamp"], y=df["price"], mode="lines", name=f"{selected_stock} Price")])
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
