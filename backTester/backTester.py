import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import vectorbt as vbt
import yfinance as yf

import keras 
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM


from alpha_vantage.timeseries import TimeSeries
from decouple import config
import datetime
from datetime import date, timedelta


class BackTester(object):


    def __init__(self, ticker, start, end):
        self.key = config('ALPHA_ADVANTAGE')
        self.ticker = ticker
        self.start = start
        self.end = end

    
    # This function is used to get information such as open, high, low, close, adjusted close, volume, dividend amount, and split coefficient of a ticker 
    # between a given start and end date.
    def getDayData(self):
        data = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&outputsize=full&apikey={self.key}"
        data = pd.read_json(data)
        returnData = {}
        
        startYear = int(self.start[0:4])
        startMonth = int(self.start[5:7])
        startDay = int(self.start[8:10])

        endYear = int(self.end[0:4])
        endMonth = int(self.end[5:7])
        endDay = int(self.end[8:10])

        start_date = date(startYear, startMonth, startDay)
        end_date = date(endYear, endMonth, endDay)

        delta = timedelta(days=1)
        while start_date <= end_date:

           
            try:
                
                dayData = data['Time Series (Daily)'][str(start_date)]
                returnData[str(start_date)] = dayData
                
                start_date += delta
            except:
                start_date += delta
                continue
        return returnData
    
    # This function will print out the data for the function above.
    def printDayData(self):
        data = BackTester.getDayData(self)
        print(f"Data for {self.ticker} between {self.start} and {self.end}:")
        for key in data:
            print(f"{key}: {data[key]}")
    
    # Quickstart with vectorbt
    def vectorBtQuickStart(self):
        # prints ticker data given range of dates
        # Max interval is 1m for 7 days, 15m for 60 days, etc.
        ticker_price = vbt.YFData.download([self.ticker], interval = "1m", start = self.start, end = self.end).get('Close')
        print(ticker_price)


        # whatever the window is, the first of those days will be NaN
        rsi = vbt.RSI.run(ticker_price, window =[14, 21])
        rsiValue = rsi.rsi


        # only give a value of true if the rsi is crossed above or below 30
        entries = rsi.rsi_crossed_below(30)

        # only give a value of true if the rsi is crossed above or below 70
        exits = rsi.rsi_crossed_above(70)
        
        pf = vbt.Portfolio.from_signals(ticker_price, entries, exits, freq='1D')
    
    def customIndicator(self, window = 14):
        ticker_prices = vbt.YFData.download([self.ticker], missing_index = 'drop', interval = "1m", start = self.start, end = datetime.datetime.now()).get('Close')
        print(ticker_prices)
    
    


test = BackTester("AAPL", "2023-03-11", "2023-03-15")
print(test.customIndicator())