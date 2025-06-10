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

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    analysis = None
    symbol = ''
    error_msg = None
    if request.method == 'POST':
        symbol = request.form['symbol'].strip()
        try:
            stock_data = get_stock_data(symbol)
            if stock_data.empty:
                error_msg = "查無資料，請確認股票代號是否正確"
            else:
                analysis = analyze_stock(stock_data)
        except Exception as e:
            error_msg = f"資料取得錯誤：{e}"
    return render_template('index.html', symbol=symbol, stock_data=stock_data, analysis=analysis, error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True)
