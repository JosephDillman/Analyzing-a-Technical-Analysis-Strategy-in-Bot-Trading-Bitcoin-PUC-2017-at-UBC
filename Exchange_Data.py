import datetime as date
import requests
import pytz
import tableprint
import numpy as np

"""
String -> Float
String must be given in year, month, date, hour, minute, second format.
Year is a four digit number, month is a two digit number,
date is a two digit number, hour is a two digit number,
minute is a two digit number and second is a two digit number.
For example, "2016-01-01 14:30:00" is a valid string.
For a given string, yeilds a unix time stamp."""

def unix_date_converter(string):
	UNIVERSAL_TIME = pytz.utc.localize(date.datetime.strptime(string,"%Y-%m-%d %H:%M:%S"))
	UNIX_TIMESTAMP = date.datetime.timestamp(UNIVERSAL_TIME)
	return(UNIX_TIMESTAMP)


"""
String & Float & Float & Float -> ListOfFloat
For a currency pair, unix start time,
unix end time and period between price data in seconds,
yeild a list of dictionaries containing exchange information."""

def past_exchange_data(currency_pair, start_time, end_time, period):
	DETAILS = {'command' : 'returnChartData', 'currencyPair' : currency_pair, 'start' : start_time, 'end' : end_time, 'period' : period}
	REQUESTS = requests.get('https://poloniex.com/public', params = DETAILS)
	return(REQUESTS.json())


"""
REQUESTS_1 = requests.get('https://poloniex.com/public?command=returnChartData&currencyPair={0}&start={1}&end={2}&period={3}'.format(str(currency_pair), str(start_time), str(end_time), str(period)))

REQUESTS_2 = requests.get('https://poloniex.com/public', params = {'command' : 'returnChartData', 'currencyPair' : currency_pair, 'start' : start_time, 'end' : end_time, 'period' : period})"""

print(past_exchange_data('USDT_BTC', unix_date_converter('2017-05-20 00:00:00'), unix_date_converter('2017-07-22 00:00:00'), 1800))
