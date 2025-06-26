import pandas as pd
from stock_analysis import calculate_rsi, calculate_sma5, calculate_sma20
from strategy_engine import decide_capital_adjustment

def backtest_strategy(data):
    sma5 = calculate_sma5(data)
    sma20 = calculate_sma20(data)
    rsi = calculate_rsi(data)

    initial_cash = 100_000
    cash = initial_cash
    shares = 0
    capital = 0

    equity_curve = []
    returns_curve = []
    stock_price = []

    for i in range(len(data)):
        price = data['Close'].iloc[i]
        stock_price.append(price)

        if i < 25: # 避免技術指標不穩定
            equity_curve.append(cash)
            returns_curve.append(0)
            continue

        rsi_slice = rsi.iloc[max(0, i-4):i+1]
        sma5_today = sma5.iloc[i]
        sma20_today = sma20.iloc[i]
        new_capital = decide_capital_adjustment(capital, sma5_today, sma20_today, rsi_slice)

        if new_capital != capital:
            total_value = cash + shares * price
            shares = total_value * new_capital / price
            cash = total_value - shares * price
            capital = new_capital

        total_equity = cash + shares * price
        equity_curve.append(total_equity)
        returns_curve.append((total_equity / initial_cash) - 1)

    result = pd.DataFrame({
        'equity': equity_curve,
        'returns': returns_curve,
        'price': stock_price
        }, index=data.index)

    return result