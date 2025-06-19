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

def calculate_sma5(data):  # 5 日簡單移動平均
    return data['Close'].rolling(window=5).mean()

def calculate_sma20(data):  # 20 日簡單移動平均
    return data['Close'].rolling(window=20).mean()