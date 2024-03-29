from flask import Flask, request
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import requests
from pyupbit import Upbit
from auth import get_jwt_token
app = Flask(__name__)

# ✅ 자산 현황, 평균 매수가
# ✅ 매수
# ✅ 매도
# ✅ 원화 입금    

def deposit_krw(ak, sk, amount):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    url = 'https://api.upbit.com/v1/deposits/krw'
    payload = {'amount': amount, 'two_factor_type': 'naver'}
    headers = {'Authorization': f'Bearer {get_jwt_token(ak, sk, payload)}'}
    response = requests.post(url, headers=headers, data=payload).json()
    if response and 'error' in response:
        name = response['error']['name']
        message = response['error']['message']
        return f'{name} : {message}', 400
    return response or ('알 수 없는 에러가 발생했습니다.', 500)
    
def sell_market_order(ak, sk, ticker, volume):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    response = upbit.sell_market_order(ticker, volume)
    if response and 'error' in response:
        name = response['error']['name']
        message = response['error']['message']
        return f'{name} : {message}', 400
    return response or ('알 수 없는 에러가 발생했습니다.', 500)

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
    return response or ('알 수 없는 에러가 발생했습니다.', 500)

def get_account_balance(ak, sk):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    data = upbit.get_balances()
    # print(data)
    balances = pd.DataFrame(data).set_index('currency')
    # print(balances)
    result = {}
    for ticker in balances.index:
        if ticker == 'KRW':
            result['KRW'] = balances.loc[ticker, ['balance']].to_dict()
        else:
            result[ticker] = balances.loc[ticker, ['balance', 'avg_buy_price']].to_dict()
    return result

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