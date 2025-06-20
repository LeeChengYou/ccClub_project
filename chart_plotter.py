import matplotlib.pyplot as plt

def draw_chart(data, full_data, symbol, font_prop, sma5, sma20, dif, macd, histogram):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    data['Close'].plot(ax=ax1, label='收盤價')
    sma5[data.index].dropna().plot(ax=ax1, label='SMA5', linestyle='--')
    sma20[data.index].dropna().plot(ax=ax1, label='SMA20', linestyle=':')

    ax1.set_title(f"{symbol}", fontproperties=font_prop)
    ax1.set_ylabel('收盤價', fontproperties=font_prop)
    ax1.legend(prop=font_prop) # 顯示圖例（線條標籤）
    ax1.grid(False)

    dif[data.index].dropna().plot(ax=ax2, label='DIF')
    macd[data.index].dropna().plot(ax=ax2, label='MACD')
    
    ax2.bar(data.index, histogram[data.index], color='gray', alpha=0.3)
    ax2.set_xlabel('日期', fontproperties=font_prop)
    ax2.set_ylabel('MACD / DIF', fontproperties=font_prop)
    ax2.legend(prop=font_prop)
    ax2.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    ax2.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.6)

    plt.tight_layout() # 自動調整間距
    img_path = f'static/{symbol}_plot.png'
    plt.savefig(img_path)
    plt.close()
