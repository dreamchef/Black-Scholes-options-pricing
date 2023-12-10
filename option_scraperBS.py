import pandas as pd
import requests
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from constants import *


def get_tickers():

    re = requests.get(API_BASE_URL, params=API_PARAMS)
    tickers = [t[0] for t in re.json()['records']]

    return tickers


def generate_options_df(options):
    
    options = [item for sublist in options for item in sublist]
    df_opts = pd.DataFrame.from_records(options)
    df_opts['duration'] = df_opts['expiration'] - df_opts['lastTradeDate']
    df_opts['duration'] = df_opts['duration'].apply(lambda x: x.days)

    return df_opts


def get_all_options_data(tickers):

    with ThreadPoolExecutor(max_workers=100) as p:
         results = p.map(get_options_data, tickers)

    calls = []
    puts = []

    for result in results:
        calls.extend(result[0])
        puts.extend(result[1])

    df_calls = generate_options_df(calls)
    df_puts = generate_options_df(puts)

    return df_calls, df_puts


def convert_options_to_dict(df, expiration_date):

    expiration_datetime = datetime.strptime(expiration_date, '%Y-%m-%d')
    df = df.assign(expiration=expiration_datetime)
    df['lastTradeDate'] = df['lastTradeDate'].apply(lambda x: x.replace(tzinfo=None))

    return df.to_dict(orient='records')


def get_options_data(ticker):

    calls = []
    puts = []

    stock = yf.Ticker(ticker)
    for expiration_date in stock.options:
        opt = stock.option_chain(expiration_date)
        opt_calls = opt.calls
        opt_puts = opt.puts
        calls.append(convert_options_to_dict(opt_calls, expiration_date))
        puts.append(convert_options_to_dict(opt_puts, expiration_date))

    return calls, puts


if __name__ == '__main__':

    tickers = get_tickers()[:N_TICKERS]
    print(get_all_options_data(tickers))
