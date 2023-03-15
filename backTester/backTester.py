import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import vectorbt as vbt
import yfinance as yf

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
    
    # This function will take close prices and return a list of the RSI values for each day.
    def customIndicator(self, close, rsi_window = 14, ma_window = 50):
        # Relative strength index based on closing prices
        rsi = vbt.RSI.run(close, window = [rsi_window])
        ma = vbt.MA.run(close, window = [ma_window])
        rsiValue = rsi.rsi
        return rsiValue

    # This function will take the custom indicator function and return a list of the RSI values for each day.
    def indicatorFact(self):
        ticker_prices = vbt.YFData.download([self.ticker], missing_index = 'drop', start = self.start, end = self.end, interval = "1m").get('Close')
        # indicator factory
        indicator = vbt.IndicatorFactory(
            class_name = "Combination",
            short_name = "comb",
            input_names = ["close"],
            param_names = ["rsi_window", "ma_window"],
            output_names = ["value"]
        ).from_apply_func(
            self.customIndicator,
            window = 14
        )
        comb = indicator.run(ticker_prices, window = 21)
        print(comb.value)
        return comb.value

    


test = BackTester("AAPL", "2023-03-09", "2023-03-16")
test.indicatorFact()
