import yfinance as yf
import pandas as pd

def get_stock_data(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    full_data = stock.history(period="252d") # 數值計算、回測

    full_data = full_data.dropna(subset=['Close'])
    full_data.index = pd.to_datetime(full_data.index)

    period_map = {
        '7d': 7,
        '1mo': 22,
        '3mo': 66,
        '6mo': 132
    }

    data = full_data.tail(period_map.get(period, 22))
    return full_data, data