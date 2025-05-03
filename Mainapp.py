import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
pip install googlefinance

# --- Streamlit App Config ---
st.set_page_config(layout="wide")
st.title("Fibonacci + RSI Trading Strategy (Mock XAU/USD)")

# --- Generate Mock OHLC Data ---
def generate_mock_ohlc(periods=100):
    dates = pd.date_range(end=datetime.datetime.now(), periods=periods, freq='H')
    price = 2350 + np.cumsum(np.random.normal(0, 2, size=periods))
    open_ = price
    close = open_ + np.random.normal(0, 1, size=periods)
    high = np.maximum(open_, close) + np.random.uniform(0.5, 2.0, size=periods)
    low = np.minimum(open_, close) - np.random.uniform(0.5, 2.0, size=periods)
    
    return pd.DataFrame({
        'datetime': dates,
        'open': open_,
        'high': high,
        'low': low,
        'close': close
    })

# --- RSI Calculation ---
def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# --- Fibonacci Levels ---
def calculate_fibonacci_levels(data):
    max_price = data['high'].max()
    min_price = data['low'].min()
    diff = max_price - min_price
    levels = {
        '0.0': max_price,
        '0.236': max_price - 0.236 * diff,
        '0.382': max_price - 0.382 * diff,
        '0.5': max_price - 0.5 * diff,
        '0.618': max_price - 0.618 * diff,
        '0.786': max_price - 0.786 * diff,
        '1.0': min_price
    }
    return levels

# --- Plot Candlestick Chart ---
def plot_candlestick(data, fib_levels):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data['datetime'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
    ))

    for level, value in fib_levels.items():
        fig.add_hline(y=value, line_dash="dot", annotation_text=f"Fib {level}", annotation_position="right")

    fig.update_layout(
        title="Mock XAU/USD Candlestick Chart with Fibonacci Levels",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Plot RSI ---
def plot_rsi(data):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.plot(data['datetime'], data['RSI'], label='RSI', color='purple')
    ax.axhline(70, color='red', linestyle='--')
    ax.axhline(30, color='green', linestyle='--')
    ax.axhline(50, color='gray', linestyle='--', alpha=0.5)
    ax.set_title('RSI (14)')
    ax.set_ylabel('RSI')
    ax.legend()
    st.pyplot(fig)

# --- Main Execution ---
data = generate_mock_ohlc()
data = calculate_rsi(data)
fib_levels = calculate_fibonacci_levels(data)

plot_candlestick(data, fib_levels)
plot_rsi(data)

st.caption("This app uses simulated OHLC data for XAU/USD. Fibonacci levels and RSI are calculated in real-time.")
