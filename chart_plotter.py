import matplotlib
matplotlib.use('Agg')  # 禁用 GUI 後端，使用純圖片模式

import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
import mplfinance as mpf

def align(series, index, drop_zero=True): 
    s = series.reindex(index)
    if drop_zero:
        s = s.where(s != 0)
    return s.dropna()

def draw_chart(data, full_data, symbol, font_prop, sma5, sma20, dif, macd, histogram, rsi):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True, gridspec_kw={'height_ratios': [2.2, 1, 1]})
    data['Close'].plot(ax=ax1, label='收盤價', linewidth=1.5, color='#1E90FF')
    align(sma5, data.index).plot(ax=ax1, label='SMA5', linestyle='--', color='#FFA07A')
    align(sma20, data.index).plot(ax=ax1, label='SMA20', linestyle=':', color='#006400')

    ax1.set_ylabel('價格', fontsize=14, fontproperties=font_prop)
    ax1.tick_params(axis='x', labelsize=10)
    ax1.legend(loc='best', fontsize=14, frameon=False, prop=font_prop)
    ax1.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    ax1.tick_params(axis='y', labelsize=12)

    align(rsi, data.index).plot(ax=ax2, label='RSI', linewidth=1.5, color='#4169E1')
    ax2.axhline(70, color='#CC0000', linestyle='--', linewidth=1)
    ax2.axhline(30, color='#228B22', linestyle='--', linewidth=1)
    # ax2.text(data.index[2], 72, 'Overbought', color='#CC0000', alpha=0.7, fontsize=14, ha='left', va='bottom', fontproperties=font_prop)
    # ax2.text(data.index[2], 32, 'Oversold', color='#228B22', alpha=0.7, fontsize=14, ha='left', va='bottom', fontproperties=font_prop)

    ax2.set_ylabel('RSI', fontsize=14, fontproperties=font_prop)
    ax2.tick_params(axis='x', labelsize=10)
    ax2.legend(loc='best', fontsize=14, frameon=False, prop=font_prop)
    ax2.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    ax2.tick_params(axis='y', labelsize=12)

    align(dif, data.index).plot(ax=ax3, label='DIF', linewidth=1, color='#1E90FF')
    align(macd, data.index).plot(ax=ax3, label='MACD', linewidth=1, color='#FF6347')   
    hist_to_plot = align(histogram, data.index, drop_zero=False)
    ax3.bar(hist_to_plot.index, hist_to_plot, color='gray', alpha=0.3)
    
    ax3.set_xlabel("日期", fontsize=14, fontproperties=font_prop)
    ax3.set_ylabel('MACD / DIF', fontsize=14, fontproperties=font_prop)
    ax3.tick_params(axis='both', labelsize=12)
    ax3.legend(loc='best', fontsize=14, frameon=False, prop=font_prop)
    ax3.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    ax3.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.6)
    ax3.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))

    fig.autofmt_xdate()
    plt.tight_layout()
    img_path = f'static/{symbol}_plot.png'
    plt.savefig(img_path)
    plt.close()

def draw_bollinger_bands(data, symbol, sma_boll, upper_band, lower_band, font_prop):   
    apds = [
        mpf.make_addplot(align(sma_boll, data.index), color='#888888', linestyle='--', label='SMA'),
        mpf.make_addplot(align(upper_band, data.index), color='#FF0000', linestyle='--', label='Upper Band'),
        mpf.make_addplot(align(lower_band, data.index), color='#228B22', linestyle='--', label='Lower Band')
    ]

    mc = mpf.make_marketcolors(
    up='red',
    down='green',
    edge='inherit',
    wick='inherit',
    volume='inherit'
    )

    custom_style = mpf.make_mpf_style(
        base_mpf_style='classic',
        marketcolors=mc,
        rc={
            'font.family': font_prop.get_name(),
            'axes.unicode_minus': False,
            'axes.labelweight': 'bold',
            'axes.labelsize': 24,
            'ytick.labelsize': 20,
            'xtick.labelsize': 20,
        },
        y_on_right=False
    )

    fig, axes = mpf.plot(
        data,
        type='candle',
        addplot=apds,
        style=custom_style,
        ylabel='價格',
        volume=False,
        figratio=(6, 4),
        figscale=2.0,
        returnfig=True,
        datetime_format='%Y-%m-%d'
    )
    
    fig.tight_layout()
    fig.savefig(f'static/{symbol}_bollinger.png')
    plt.close(fig)

def draw_equity_curve(result, symbol, font_prop):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    ax1_2 = ax1.twinx()
    line_equity = ax1.plot(result.index, result['equity'], label='總資產變化曲線', linewidth=1.5, color='#FF6347')[0]
    line_price = ax1_2.plot(result.index, result['price'], label='股價', linewidth=1.5, color='#1E90FF')[0]
    initial_cash = 100_000
    line_initial_cash = ax1.axhline(initial_cash, color='#000000', linestyle='-', linewidth=0.6, label='初始資金')

    ax1.set_xlabel("日期", fontsize=14, fontproperties=font_prop)
    ax1.set_ylabel("總資產", fontsize=14, fontproperties=font_prop)
    ax1_2.set_ylabel("價格", fontsize=14, fontproperties=font_prop)
    ax1.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.tick_params(axis='both', labelsize=12)
    ax1_2.tick_params(axis='both', labelsize=12)

    lines = [line_equity, line_price, line_initial_cash]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='best', fontsize=14, frameon=False, prop=font_prop)

    fig.autofmt_xdate()
    plt.savefig(f'static/{symbol}_equitycurve.png')
    plt.close()