from flask import Flask, request
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from pyupbit import Upbit

app = Flask(__name__)

# ✅ 자산 현황, 평균 매수가
# ✅ 매수
# ✅ 매도

def sell_market_order(ak, sk, ticker, volume):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    response = upbit.sell_market_order(ticker, volume)
    if response and 'error' in response:
        name = response['error']['name']
        message = response['error']['message']
        return f'{name} : {message}', 400
    return response or '알 수 없는 에러가 발생했습니다.', 500

def buy_market_order(ak, sk, ticker, amount):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    if amount < 5000:
        return 'UnderMinTotalBid : 최소 주문 금액은 5,000원입니다.', 400
    if upbit.get_balance('KRW') < amount:
        return 'InsufficientFundsBid : 원화 잔고가 부족합니다.', 400
    response = upbit.buy_market_order(ticker, amount)
    if response and 'error' in response:
        name = response['error']['name']
        message = response['error']['message']
        return f'{name} : {message}', 400
    return response or '알 수 없는 에러가 발생했습니다.', 500

def get_account_balance(ak, sk):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    data = upbit.get_balances()
    balances = pd.DataFrame(data).set_index('currency')
    # print(balances)
    return dict(
        krw=balances.loc['KRW', ['balance']].to_dict(),
        btc=balances.loc['BTC', ['balance', 'avg_buy_price']].to_dict(),
        eth=balances.loc['ETH', ['balance', 'avg_buy_price']].to_dict(),
    )

@app.route('/account_balance', methods=['POST'])
def account_balance():
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