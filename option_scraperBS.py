from datetime import datetime
import pandas as pd
import requests
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from constants import *


def get_tickers():

    re = requests.get(API_BASE_URL, params=API_PARAMS)
    tickers = [t[0] for t in re.json()['records']]

    return tickers

def get_all_options_data(tickers):

    with ThreadPoolExecutor(max_workers=100) as p:
         results = p.map(get_options_data, tickers)

    calls = []
    puts = []

    for result in results:
        calls.extend(result[0])
        puts.extend(result[1])

    calls = [item for sublist in calls for item in sublist]
    puts = [item for sublist in puts for item in sublist]
    df_calls = pd.DataFrame.from_records(calls)
    df_puts = pd.DataFrame.from_records(puts)
    df_calls['duration'] = df_calls['expiration'] - df_calls['lastTradeDate']
    df_calls['duration'] = df_calls['duration'].apply(lambda x: x.days)
    df_puts['duration'] = df_puts['expiration'] - df_puts['lastTradeDate']
    df_puts['duration'] = df_puts['duration'].apply(lambda x: x.days)

    return df_calls, df_puts


def get_options_data(ticker):

    calls = []
    puts = []

    stock = yf.Ticker(ticker)
    for expiration_date in stock.options:
        opt = stock.option_chain(expiration_date)
        opt_calls = opt.calls
        opt_puts = opt.puts
        expiration_datetime = datetime.strptime(expiration_date, '%Y-%m-%d')
        opt_calls['lastTradeDate'] = opt_calls['lastTradeDate'].apply(lambda x: x.replace(tzinfo=None))
        opt_puts['lastTradeDate'] = opt_puts['lastTradeDate'].apply(lambda x: x.replace(tzinfo=None))
        opt_calls = opt_calls.assign(expiration=expiration_datetime)
        opt_puts = opt_puts.assign(expiration=expiration_datetime)
        calls.append(opt_calls.to_dict(orient='records'))
        puts.append(opt_puts.to_dict(orient='records'))

    return calls, puts

if __name__ == '__main__':

    tickers = get_tickers()[:N_TICKERS]
    print(get_all_options_data(tickers))
