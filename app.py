#@author Jeff Lee
# flask_stock_analysis/
# ├── app.py               # Flask 主應用程式
# ├── stock_scraper.py     # 股票爬蟲模組
# ├── stock_analysis.py    # 股票分析模組
# ├── chart_plotter.py     # 繪圖模組
# ├── strategy_engine.py   # 策略邏輯判斷模組
# ├── backtester.py        # 回測模擬模組
# ├── templates/           # HTML 模板資料夾 (Flask 用)
# │   └── index.html
# └── static/              # 靜態檔案 (CSS, JS)
from flask import Flask, render_template, request
from stock_parser import get_stock_data
from stock_analysis import analyze_stock, calculate_sma5, calculate_sma20, calculate_macd, calculate_bollinger_bands, calculate_rsi
from chart_plotter import draw_chart, draw_bollinger_bands, draw_equity_curve
from strategy_engine import sma_signal, macd_signal, decide_capital_adjustment
from backtester import backtest_strategy
import os
from matplotlib.font_manager import FontProperties
font_path = "./static/fronts/mingliu.ttc"
font_prop = FontProperties(fname=font_path)

app = Flask(__name__)
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # 在這裡可以添加用戶註冊邏輯
#         return f"註冊成功：{username}"
#     return render_template('register.html')
# @app.route('/')
# def signin():
#     return render_template('signin.html')
@app.route('/index', methods=['GET', 'POST'])
def index():
    stock_data_dict = {}
    analysis_dict = {}
    symbols = ''
    error_msg = None
    period = '1mo'

    if request.method == 'POST':
        symbols = request.form['symbol'].strip()
        period = request.form.get('period', '1mo')
        symbol_list = [s.strip() for s in symbols.split(',') if s.strip()]

        for symbol in symbol_list:
            try:
                full_data, data = get_stock_data(symbol, period)
                if data.empty:
                    error_msg = f"查無資料：{symbol}"
                else:
                    stock_data_dict[symbol] = data
                    analysis_dict[symbol] = analyze_stock(data)

                    if len(full_data) < 50:
                        analysis_dict[symbol]['備註'] = f"資料不足 50 筆，略過策略分析與圖表繪製"
                        continue
                    
                    dif, macd, histogram = calculate_macd(full_data)
                    sma5 = calculate_sma5(full_data)
                    sma20 = calculate_sma20(full_data)
                    rsi = calculate_rsi(full_data)
                    sma_boll, upper_band, lower_band = calculate_bollinger_bands(full_data)

                    signal_sma = sma_signal(sma5, sma20)
                    if signal_sma:
                        analysis_dict[symbol]['SMA 訊號'] = signal_sma
                    signal_macd = macd_signal(dif, macd)
                    if signal_macd:
                        analysis_dict[symbol]['MACD 訊號'] = signal_macd

                    draw_chart(data, full_data, symbol, font_prop, sma5, sma20, dif, macd, histogram, rsi)
                    draw_bollinger_bands(data, symbol, sma_boll, upper_band, lower_band, font_prop)
                    
                    sma5_today = sma5.iloc[-1]
                    sma20_today = sma20.iloc[-1]
                    capital_today = decide_capital_adjustment(0, sma5_today, sma20_today, rsi)

                    signal_text = f"資金配置建議：{int(capital_today * 100)}%"
                    analysis_dict[symbol]["策略訊號"] = signal_text

                    result = backtest_strategy(full_data)
                    start_date = result.index[0].strftime("%Y-%m")
                    end_date = result.index[-1].strftime("%Y-%m")
                    total_return = result['returns'].iloc[-1]

                    analysis_dict[symbol]["回測期間"] = f"{start_date} ～ {end_date}"
                    analysis_dict[symbol]["回測報酬"] = f"{total_return:.2%}"
                    draw_equity_curve(result, symbol, font_prop)

            except Exception as e:
                error_msg = f"資料取得錯誤：{e}"

    return render_template('index.html', symbols=symbols, analysis_dict=analysis_dict, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)