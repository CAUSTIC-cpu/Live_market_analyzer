import pandas as pd
import numpy as np
import datetime

def generate_mock_ohlc_data():
    dates = pd.date_range(end=datetime.datetime.now(), periods=100, freq='H')
    base = np.cumsum(np.random.normal(0, 1, 100)) + 2350
    open_ = base
    close = base + np.random.normal(0, 0.5, size=100)
    high = np.maximum(open_, close) + np.random.uniform(0, 1, size=100)
    low = np.minimum(open_, close) - np.random.uniform(0, 1, size=100)

    return pd.DataFrame({
        'datetime': dates,
        'open': open_,
        'high': high,
        'low': low,
        'close': close
    })
