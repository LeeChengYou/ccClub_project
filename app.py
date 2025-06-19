#@author Jeff Lee
# flask_stock_analysis/
# ├── app.py               # Flask 主應用程式
# ├── stock_scraper.py     # 股票爬蟲模組
# ├── stock_analysis.py    # 股票分析模組
# ├── templates/           # HTML 模板資料夾 (Flask 用)
# │   └── index.html
# └── static/              # 靜態檔案 (CSS, JS)
from flask import Flask, render_template, request
from stock_parser import get_stock_data
from stock_analysis import analyze_stock, calculate_sma5, calculate_sma20
import matplotlib.pyplot as plt
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
                    
                    sma5 = calculate_sma5(full_data)
                    sma20 = calculate_sma20(full_data)
                    
                    plt.figure(figsize=(10, 5))
                    data['Close'].plot(label='收盤價')
                    sma5[data.index].dropna().plot(label='SMA5', linestyle='--')
                    sma20[data.index].dropna().plot(label='SMA20', linestyle=':')
                    
                    plt.title(f"{symbol}")
                    plt.xlabel('日期', fontproperties=font_prop)
                    plt.ylabel('收盤價', fontproperties=font_prop)

                    plt.legend(prop=font_prop) # 顯示圖例（線條標籤）
                    plt.tight_layout() # 自動調整間距
                    img_path = f'static/{symbol}_plot.png'
                    plt.savefig(img_path)
                    plt.close()
            except Exception as e:
                error_msg = f"資料取得錯誤：{e}"

    return render_template('index.html', symbols=symbols, analysis_dict=analysis_dict, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)