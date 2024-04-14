import sys
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import requests
from pyupbit import Upbit
from auth import get_jwt_token

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

def get_deposit_list(ak, sk, currency, dt):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    data = upbit.get_deposit_list(currency)
    df = pd.DataFrame(data)
    df.query('state == "ACCEPTED"', inplace=True)
    df = df.loc[:, ['done_at', 'amount']]
    df.done_at = pd.to_datetime(df.done_at)
    df.set_index('done_at', inplace=True)
    df.query(f'index >= "{dt} 00:00:00+09:00"', inplace=True)
    return df

def get_withdraw_list(ak, sk, currency, dt):
    if not ak or not sk:
        return 'Unauthorized : API Key 또는 Secret Key가 필요합니다.', 400
    upbit = Upbit(ak, sk)
    data = upbit.get_withdraw_list(currency)
    df = pd.DataFrame(data)
    df.query('state == "DONE"', inplace=True)
    df = df.loc[:, ['done_at', 'amount']]
    df.done_at = pd.to_datetime(df.done_at)
    df.set_index('done_at', inplace=True)
    df.query(f'index >= "{dt}"', inplace=True)
    return df

if __name__ == '__main__':
    argument = sys.argv[1:]
    print(argument)
    print(get_deposit_list(argument[0], argument[1], 'KRW', '2024-03-25 00:00:00+09:00'))
    print(get_withdraw_list(argument[0], argument[1], 'ETH', '2024-03-25 00:00:00+09:00'))
    