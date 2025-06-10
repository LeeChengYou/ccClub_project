import yfinance as yf

def get_stock_data(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return hist
