import pandas as pd

def analyze_stock(data):
    if data.empty:
        return {}
    return {
        'mean_close': round(data['Close'].mean(), 2),
        'max_close': round(data['Close'].max(), 2),
        'min_close': round(data['Close'].min(), 2),
        'std_close': round(data['Close'].std(), 2),
        'latest_price': round(data['Close'].iloc[-1], 2)
    }