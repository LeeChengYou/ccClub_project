# app.py
# @author Jeff Lee

from flask import Flask, render_template, request, redirect, url_for, session
from stock_parser import get_stock_data
from stock_analysis import analyze_stock, calculate_sma5, calculate_sma20, calculate_macd, calculate_bollinger_bands
from chart_plotter import draw_chart, draw_bollinger_bands
from strategy_engine import sma_signal, macd_signal
from db import init_db, register_user, validate_user
import os
from matplotlib.font_manager import FontProperties

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 設定中文字型
font_path = "./static/fonts/mingliu.ttc"
font_prop = FontProperties(fname=font_path)

# 初始化使用者資料表
init_db()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('signin'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = None
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            msg = '註冊成功，請登入'
            return redirect(url_for('signin'))
        else:
            error = '使用者名稱已存在，請換一個'
    return render_template('register.html', msg=msg, error=error)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    print("已進入 /signin")
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = '帳號或密碼錯誤'
    return render_template('signin.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))

    stock_data_dict = {}
    analysis_dict = {}
    symbols = ''
    error_msgs = []
    period = '1mo'

    if request.method == 'POST':
        symbols = request.form['symbol'].strip()
        period = request.form.get('period', '1mo')
        symbol_list = [s.strip() for s in symbols.split(',') if s.strip()]

        for symbol in symbol_list:
            try:
                full_data, data = get_stock_data(symbol, period)
                if data.empty:
                    error_msgs.append(f"查無資料：{symbol}")
                    continue

                stock_data_dict[symbol] = data
                analysis_dict[symbol] = analyze_stock(data)

                # 技術指標計算
                dif, macd, histogram = calculate_macd(full_data)
                sma5 = calculate_sma5(full_data)
                sma20 = calculate_sma20(full_data)
                sma_boll, upper_band, lower_band = calculate_bollinger_bands(full_data)

                # 訊號判斷
                signal_sma = sma_signal(sma5, sma20)
                if signal_sma:
                    analysis_dict[symbol]['SMA 訊號'] = signal_sma

                signal_macd = macd_signal(dif, macd)
                if signal_macd:
                    analysis_dict[symbol]['MACD 訊號'] = signal_macd

                # 圖表繪製
                draw_chart(data, full_data, symbol, font_prop, sma5, sma20, dif, macd, histogram)
                draw_bollinger_bands(data, symbol, sma_boll, upper_band, lower_band, font_prop)

            except Exception as e:
                error_msgs.append(f"{symbol} 取得錯誤：{str(e)}")

    return render_template('index.html',
                           username=session['username'],
                           symbols=symbols,
                           analysis_dict=analysis_dict,
                           error_msg='<br>'.join(error_msgs) if error_msgs else None)