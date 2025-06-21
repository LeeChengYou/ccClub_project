def sma_signal(sma_short, sma_long):
    if not sma_short.isna().iloc[-2] and not sma_short.isna().iloc[-1] and \
   not sma_long.isna().iloc[-2] and not sma_long.isna().iloc[-1]:
        if sma_short.iloc[-2] < sma_long.iloc[-2] and sma_short.iloc[-1] > sma_long.iloc[-1]:
            return "黃金交叉"
        elif sma_short.iloc[-2] > sma_long.iloc[-2] and sma_short.iloc[-1] < sma_long.iloc[-1]:
            return "死亡交叉"
        else:
            return ""

def macd_signal(dif, macd):
    if dif.iloc[-2] < macd.iloc[-2] and dif.iloc[-1] > macd.iloc[-1]:
        return "黃金交叉"
    elif dif.iloc[-2] > macd.iloc[-2] and dif.iloc[-1] < macd.iloc[-1]:
        return "死亡交叉"
    else:
        return ""