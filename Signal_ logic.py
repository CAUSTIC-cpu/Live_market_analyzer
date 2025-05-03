signal_logic.py

def detect_fibonacci_signal(data, levels, rsi_threshold=50): """ Detects buy or sell signals based on price interaction with key Fibonacci levels and RSI crossing the midline (default: 50).

Parameters:
- data: DataFrame with 'price' and 'RSI' columns
- levels: dict of Fibonacci levels
- rsi_threshold: RSI level for confirming direction (default=50)

Returns:
- dict with signal info or None
"""
latest_price = data['price'].iloc[-1]
latest_rsi = data['RSI'].iloc[-1]
previous_rsi = data['RSI'].iloc[-2] if len(data['RSI']) > 1 else latest_rsi

# Check for Buy setup (price near support + RSI rising)
for level_label in ['0.618', '0.5', '0.382']:
    level_price = levels[level_label]
    if abs(latest_price - level_price) / latest_price < 0.003:  # ~0.3% proximity
        if previous_rsi < rsi_threshold and latest_rsi > rsi_threshold:
            return {
                'signal': 'BUY',
                'level': level_label,
                'price': latest_price,
                'rsi': latest_rsi
            }

# Check for Sell setup (price near resistance + RSI falling)
for level_label in ['0.382', '0.5', '0.618']:
    level_price = levels[level_label]
    if abs(latest_price - level_price) / latest_price < 0.003:
        if previous_rsi > rsi_threshold and latest_rsi < rsi_threshold:
            return {
                'signal': 'SELL',
                'level': level_label,
                'price': latest_price,
                'rsi': latest_rsi
            }

return None  # No valid signal

