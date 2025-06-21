import matplotlib
matplotlib.use('Agg')  # 禁用 GUI 後端，使用純圖片模式

import matplotlib.pyplot as plt
from matplotlib import rcParams
import mplfinance as mpf

def draw_chart(data, full_data, symbol, font_prop, sma5, sma20, dif, macd, histogram):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True, gridspec_kw={'height_ratios': [2.2, 1]})
    data['Close'].plot(ax=ax1, label='收盤價', linewidth=1.5, color='#1E90FF')
    sma5[data.index].dropna().plot(ax=ax1, label='SMA5', linestyle='--', color='#FFA500')
    sma20[data.index].dropna().plot(ax=ax1, label='SMA20', linestyle=':', color='#32CD32')

    ax1.set_title(f"{symbol}", fontsize=20, fontname='DejaVu Sans')
    ax1.set_ylabel('價格', fontsize=14, fontproperties=font_prop)
    ax1.tick_params(axis='x', labelsize=0)
    ax1.legend(loc='best', fontsize=14, frameon=False, prop=font_prop)
    ax1.grid(False)

    dif[data.index].dropna().plot(ax=ax2, label='DIF', linewidth=1, color='#1E90FF')
    macd[data.index].dropna().plot(ax=ax2, label='MACD', linewidth=1, color='#FF6347')
    
    ax2.bar(data.index, histogram[data.index], color='gray', alpha=0.3)
    ax2.set_xlabel("日期", fontsize=14, fontproperties=font_prop)
    ax2.set_ylabel('MACD / DIF', fontsize=14, fontproperties=font_prop)
    ax2.tick_params(axis='x', labelsize=14)
    ax2.legend(loc='best', fontsize=14, frameon=False, prop=font_prop)
    ax2.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    ax2.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.6)
    ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
    
    fig.autofmt_xdate()
    plt.tight_layout()
    img_path = f'static/{symbol}_plot.png'
    plt.savefig(img_path)
    plt.close()

def draw_bollinger_bands(data, symbol, sma_boll, upper_band, lower_band, font_prop):   
    apds = [
        mpf.make_addplot(sma_boll[data.index], color='#888888', linestyle='--', label='SMA'),
        mpf.make_addplot(upper_band[data.index], color='#FF0000', linestyle='--', label='Upper Band'),
        mpf.make_addplot(lower_band[data.index], color='#228B22', linestyle='--', label='Lower Band')
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
    
    fig.suptitle('布林通道', fontsize=24, fontproperties=font_prop, y=0.95)
    fig.tight_layout()
    fig.savefig(f'static/{symbol}_bollinger.png')
    plt.close(fig)