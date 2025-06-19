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


def calculate_ema(data, span):  # 計算 EMA（指數移動平均）
    return data['Close'].ewm(span=span, adjust=False).mean()

def calculate_macd(data):  # 計算 MACD 指標
    ema12 = calculate_ema(data, 12)
    ema26 = calculate_ema(data, 26)
    dif = ema12 - ema26
    macd = dif.ewm(span=9, adjust=False).mean()
    histogram = dif - macd
    return dif, macd, histogram