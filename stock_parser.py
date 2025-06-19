import yfinance as yf

def get_stock_data(symbol, period="1mo"):
    extra_days = 25  

    period_map = {
        "7d": 7,
        "1mo": 30,
        "3mo": 90,
        "6mo": 180
    }

    if period in period_map:
        days = period_map[period]
        total_days = days + extra_days
        full_period = f"{total_days}d"
        stock = yf.Ticker(symbol)
        full_data = stock.history(period=full_period) # 用於數值計算
        display_data = full_data.tail(days)
        return full_data, display_data

    # 若輸入無法解析，就只抓原本的資料
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data, data
