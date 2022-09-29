import datetime
import requests
import pandas as pd

api_url = 'https://ftx.com/api'


def actual_data():
    api = "/markets"
    url = api_url + api
    markets = requests.get(url).json()
    data = markets['result']
    df = pd.DataFrame(data)
    return df

def individual(market_name):
    path = f'/markets/{market_name}'
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res)['result']
    return df

def historical(market_name, start_year, start_month, start_day, resolution = 86400, end_year = None, end_month = None, end_day = None):

    start_time = datetime.datetime(start_year, start_month, start_day).timestamp()
    if end_year != None and end_month != None and end_day != None:
        end_time = datetime.datetime(end_year, end_month, end_day).timestamp()
        path = f'/markets/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
    else:
        path = f'/markets/{market_name}/candles?resolution={resolution}&start_time={start_time}'
    
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res['result'])
    df['date'] = pd.to_datetime(df['startTime'])
    df = df.set_index('date')
    df = df.drop(columns = ['startTime', 'time'])
    return df

def historical_datetime(market_name, start_time, end_time, resolution = 86400):
    path = f'/markets/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res['result'])
    df['date'] = pd.to_datetime(df['startTime'])
    df = df.set_index('date')
    df = df.drop(columns = ['startTime', 'time'])
    return df

def historical_datetime_no(market_name, start_time, resolution = 15):
    path = f'/markets/{market_name}/candles?resolution={resolution}&start_time={start_time}'
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res['result'])
    df['date'] = pd.to_datetime(df['startTime'])
    df = df.set_index('date')
    df = df.drop(columns = ['startTime', 'time'])
    return df