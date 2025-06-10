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
from stock_analysis import analyze_stock
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties
font_path = "C:/Windows/Fonts/msjh.ttc"
font_prop = FontProperties(fname=font_path)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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
                data = get_stock_data(symbol, period)
                if data.empty:
                    error_msg = f"查無資料：{symbol}"
                else:
                    stock_data_dict[symbol] = data
                    analysis_dict[symbol] = analyze_stock(data)
                    plt.figure()
                    data['Close'].plot(title=f"{symbol} ")
                    plt.xlabel('日期', fontproperties=font_prop)
                    plt.ylabel('收盤價', fontproperties=font_prop)
                    plt.tight_layout()
                    img_path = f'static/{symbol}_plot.png'
                    plt.savefig(img_path)
                    plt.close()
            except Exception as e:
                error_msg = f"資料取得錯誤：{e}"

    return render_template('index.html', symbols=symbols, analysis_dict=analysis_dict, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)