from flask import Flask, render_template, request
from stock_parser import get_stock_data
from stock_analysis import analyze_stock

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    analysis = None
    symbol = ''
    if request.method == 'POST':
        symbol = request.form['symbol']
        stock_data = get_stock_data(symbol)
        analysis = analyze_stock(stock_data)
    return render_template('index.html', symbol=symbol, stock_data=stock_data, analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)