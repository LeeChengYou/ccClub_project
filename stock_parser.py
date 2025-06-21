import yfinance as yf

def get_stock_data(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return hist
def download_stock_data(symbol, period="1mo"):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    if hist.empty:
        return 0
    else:
        yf.download(symbol, period=period, auto_adjust=True, progress=False)
        return yf.Ticker(symbol).history(period=period) 
