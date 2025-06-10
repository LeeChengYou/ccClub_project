import pandas as pd

def analyze_stock(data):
    if data.empty:
        return {}
    return {
        'mean_close': data['Close'].mean(),
        'max_close': data['Close'].max(),
        'min_close': data['Close'].min(),
        'std_close': data['Close'].std()
    }