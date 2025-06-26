import pandas as pd

def sma_signal(sma_short, sma_long):
    if len(sma_short) >= 2 and len(sma_long) >= 2 and \
        not sma_short.iloc[-2:].isna().any() and not sma_long.iloc[-2:].isna().any():
        if sma_short.iloc[-2] < sma_long.iloc[-2] and sma_short.iloc[-1] > sma_long.iloc[-1]:
            return "黃金交叉"
        elif sma_short.iloc[-2] > sma_long.iloc[-2] and sma_short.iloc[-1] < sma_long.iloc[-1]:
            return "死亡交叉"
        else:
            return "無交叉"
    return ""

def macd_signal(dif, macd):
    if len(dif) >= 2 and len(macd) >= 2 and \
       not dif.iloc[-2:].isna().any() and not macd.iloc[-2:].isna().any():
        if dif.iloc[-2] < macd.iloc[-2] and dif.iloc[-1] > macd.iloc[-1]:
            return "黃金交叉"
        elif dif.iloc[-2] > macd.iloc[-2] and dif.iloc[-1] < macd.iloc[-1]:
            return "死亡交叉"
        else:
            return "無交叉"
    return ""
    
def decide_capital_adjustment(capital, sma5_today, sma20_today, rsi):
    if rsi.count() < 5 or pd.isna(sma20_today): # 資料不足，不操作
        return capital
    
    rsi_today = rsi.iloc[-1]
    
    rsi_extremely_low = rsi_today < 20 # 超賣反彈
    trend_up = (rsi_today < 30) and (sma5_today > sma20_today) # 低檔順勢進場
    
    fake_break = rsi.tail(5).max() < 25 # 假跌破
    overheat_drop = (rsi.tail(3).max() > 85) and (rsi_today < 75) # 過熱
    rsi_slowing = (rsi_today < 70) and (not overheat_drop) # 未過熱，RSI減弱
    trend_decline = (sma5_today < sma20_today) and (rsi_today < 65) # 趨勢反轉
    
    if capital == 0:
        if trend_up:
            return 1.0
        elif rsi_extremely_low:
            return 0.5
        else:
            return 0.0

    elif capital == 0.5:
        if fake_break or trend_decline:
            return 0.0
        elif trend_up:
            return 1.0
        else:
            return 0.5

    elif capital == 1.0:
        if fake_break or trend_decline:
            return 0.0
        elif overheat_drop or rsi_slowing:
            return 0.5
        else:
            return 1.0