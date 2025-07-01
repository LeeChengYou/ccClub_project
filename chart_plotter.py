import matplotlib
matplotlib.use('Agg')  # 禁用 GUI 後端，使用純圖片模式
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import mplfinance as mpf
from plotly.subplots import make_subplots

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
    
def draw_combined_technical_plot(data, full_data, symbol, sma5, sma20, dif, macd, histogram, sma_boll, upper_band, lower_band):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        row_heights=[0.65, 0.35],
        #subplot_titles=(f"{symbol} 技術分析", "MACD 指標")
    )

    # --- 上層：價格 + SMA + 布林通道 ---
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='收盤價', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=sma5.index, y=sma5, mode='lines', name='SMA5', line=dict(color='orange', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=sma20.index, y=sma20, mode='lines', name='SMA20', line=dict(color='green', dash='dot')), row=1, col=1)

    fig.add_trace(go.Scatter(x=upper_band.index, y=upper_band, mode='lines', name='布林上軌', line=dict(color='red', width=1, dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=lower_band.index, y=lower_band, mode='lines', name='布林下軌', line=dict(color='purple', width=1, dash='dot')), row=1, col=1)

    # --- 下層：MACD + DIF + 柱狀圖 ---
    fig.add_trace(go.Scatter(x=macd.index, y=macd, mode='lines', name='MACD', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=dif.index, y=dif, mode='lines', name='DIF', line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Bar(x=histogram.index, y=histogram, name='Histogram', marker=dict(color='gray'), opacity=0.4), row=2, col=1)

    # --- 圖表美化 ---
    fig.update_layout(
        height=750,
        width=1000,
        template="plotly_white",
        showlegend=True,
        margin=dict(t=60, b=40, l=40, r=60),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            bordercolor="lightgray",
            align="left"
        ),
        legend=dict(
            x=0.95,
            y=0.95,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='lightgray',
            borderwidth=1
        )
    )

    fig.update_xaxes(title_text="日期", row=2, col=1)
    fig.update_yaxes(title_text="價格", row=1, col=1)
    fig.update_yaxes(title_text="MACD / DIF", row=2, col=1)

    # --- 輸出 HTML 檔案 ---
    output_path = f"static/{symbol}_technical_plot.html"
    fig.write_html(output_path)
    
