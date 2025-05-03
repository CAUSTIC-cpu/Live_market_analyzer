import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# --- Mock Data Generator ---
def generate_mock_data():
    dates = pd.date_range(end=datetime.datetime.today(), periods=100, freq='H')
    prices = np.cumsum(np.random.normal(0, 1, size=100)) + 2350  # Simulated XAU/USD prices
    return pd.DataFrame({'datetime': dates, 'price': prices})

# --- Calculate RSI ---
def calculate_rsi(data, period=14):
    delta = data['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# --- Fibonacci Levels ---
def calculate_fibonacci_levels(data):
    max_price = data['price'].max()
    min_price = data['price'].min()
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

# --- Plotting Function ---
def plot_chart(data, levels):
    # Price chart with Fibonacci levels
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(data['datetime'], data['price'], label='Price', color='blue')
    for level, value in levels.items():
        ax1.axhline(y=value, linestyle='--', alpha=0.5, label=f'Fib {level}')
    ax1.set_title('Mock XAU/USD with Fibonacci Levels')
    ax1.set_ylabel('Price')
    ax1.legend()
    st.pyplot(fig)

    # RSI chart
    fig, ax2 = plt.subplots(figsize=(10, 2))
    ax2.plot(data['datetime'], data['RSI'], color='purple', label='RSI')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.axhline(50, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('RSI (14)')
    ax2.set_ylabel('RSI')
    ax2.legend()
    st.pyplot(fig)

# --- Streamlit App ---
st.set_page_config(layout="wide")
st.title("Fibonacci + RSI Trading Strategy (Mock XAU/USD)")

# Load and process data
data = generate_mock_data()
data = calculate_rsi(data)
fib_levels = calculate_fibonacci_levels(data)

# Show plots
plot_chart(data, fib_levels)

# Add TradingView Chart Widget
st.markdown("""
<iframe src="https://www.tradingview.com/widgetembed/?frameElementId=tradingview_34d1b&symbol=OANDA%3AXAUUSD&interval=60&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=F1F3F6&studies=[]&theme=dark&style=1&timezone=Etc%2FUTC&withdateranges=1&hideideas=1&allow_symbol_change=true&watchlist=[]&enabled_features=[]&disabled_features=[]&locale=en"
width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
""", unsafe_allow_html=True)

st.caption("This app uses mock data for demo purposes. RSI and Fibonacci levels are calculated on-the-fly.")
