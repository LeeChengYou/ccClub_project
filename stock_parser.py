import yfinance as yf

def get_stock_data(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    full_data = stock.history(period="365d") # 數值計算、回測
    data = stock.history(period=period)
    return full_data, data