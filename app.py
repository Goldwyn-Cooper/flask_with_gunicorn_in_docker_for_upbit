from flask import Flask, request
from biz import get_account_balance, buy_market_order, sell_market_order, deposit_krw, get_deposit_list, get_withdraw_list

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

@app.route('/account_deposit', methods=['POST'])
def account_deposit():
    payload : dict = request.get_json()
    ak = payload.get('ak')
    sk = payload.get('sk')
    currency = payload.get('currency')
    dt = payload.get('dt')
    print(ak, sk, currency, dt)
    return get_deposit_list(ak, sk, currency, dt)

@app.route('/account_withdraw', methods=['POST'])
def account_withdraw():
    payload : dict = request.get_json()
    ak = payload.get('ak')
    sk = payload.get('sk')
    currency = payload.get('currency')
    dt = payload.get('dt')
    return get_withdraw_list(ak, sk, currency, dt)