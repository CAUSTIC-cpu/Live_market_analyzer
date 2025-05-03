# utils/data_fetcher.py

import pandas as pd
import numpy as np
import datetime

def get_price_data(use_mock=True):
    if use_mock:
        return generate_mock_data()
    else:
        # Placeholder for API-based fetch
        raise NotImplementedError("API fetch not implemented yet.")

def generate_mock_data():
    dates = pd.date_range(end=datetime.datetime.today(), periods=100, freq='H')
    prices = np.cumsum(np.random.normal(0, 1, size=100)) + 2350
    return pd.DataFrame({'datetime': dates, 'price': prices})
