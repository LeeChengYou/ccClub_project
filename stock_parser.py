import yfinance as yf

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1mo")
    return hist
