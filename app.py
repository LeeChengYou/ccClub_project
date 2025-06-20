#@author Jeff Lee
# flask_stock_analysis/
# ├── app.py               # Flask 主應用程式
# ├── stock_scraper.py     # 股票爬蟲模組
# ├── stock_analysis.py    # 股票分析模組
# ├── chart_plotter.py     # 繪圖模組
# ├── templates/           # HTML 模板資料夾 (Flask 用)
# │   └── index.html
# └── static/              # 靜態檔案 (CSS, JS)
from flask import Flask, render_template, request
from stock_parser import get_stock_data
from stock_analysis import analyze_stock, calculate_sma5, calculate_sma20, calculate_macd
from chart_plotter import draw_chart
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

                    dif, macd, histogram = calculate_macd(full_data)
                    sma5 = calculate_sma5(full_data)
                    sma20 = calculate_sma20(full_data)
                    
                    draw_chart(data, full_data, symbol, font_prop, sma5, sma20, dif, macd, histogram)

            except Exception as e:
                error_msg = f"資料取得錯誤：{e}"

    return render_template('index.html', symbols=symbols, analysis_dict=analysis_dict, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)