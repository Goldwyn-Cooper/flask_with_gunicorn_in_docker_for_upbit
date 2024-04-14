from flask import Flask, request
from biz import get_account_balance, buy_market_order, sell_market_order, deposit_krw

app = Flask(__name__)

@app.route('/account_balance', methods=['POST'])
def account_balance():
    pass
    payload : dict = request.get_json()
    ak = payload.get('ak')
    sk = payload.get('sk')
    return get_account_balance(ak, sk)

@app.route('/buy', methods=['POST'])
def buy():
    payload : dict = request.get_json()
    ak = payload.get('ak')
    sk = payload.get('sk')
    ticker = f'KRW-{payload.get("ticker")}'
    amount = payload.get('amount')
    return buy_market_order(ak, sk, ticker, amount)

@app.route('/sell', methods=['POST'])
def sell():
    payload : dict = request.get_json()
    ak = payload.get('ak')
    sk = payload.get('sk')
    ticker = f'KRW-{payload.get("ticker")}'
    volume = payload.get('volume')
    return sell_market_order(ak, sk, ticker, volume)

@app.route('/deposit', methods=['POST'])
def deposit():
    payload : dict = request.get_json()
    ak = payload.get('ak')
    sk = payload.get('sk')
    amount = payload.get('amount')
    return deposit_krw(ak, sk, amount)
