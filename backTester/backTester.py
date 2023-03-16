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
    
    # This function will take close prices and return a list of the RSI values for each day. Windows are considered "candles"

    def customIndicator(self, close, rsi_window = 14, ma_window = 50):
        # Relative strength index based on closing prices
        rsi = vbt.RSI.run(close, window = [rsi_window]).rsi.to_numpy()
        # Moving average based on closing prices
        ma = vbt.MA.run(close, window = [ma_window]).ma.to_numpy()

        # If it is above 70, exit the position. If it is below 30, enter the position. If it is between 30 and 70, do nothing. 
        # Only buy if the closing price is below the moving average.
        trend = np.where(rsi > 70, -1, 0)
        trend = np.where((rsi < 30) & (close < ma), 1, trend)
        return trend

    # This function will take the custom indicator function and return a list of the RSI values for each day.
    def indicatorFact(self, arrOfTickers, startDate, endDate):
        ticker_prices = vbt.YFData.download(arrOfTickers, missing_index = 'drop', start = startDate, end = endDate, interval = "1m").get('Close')
        # indicator factory
        indicator = vbt.IndicatorFactory(
            class_name = "Combination",
            short_name = "comb",
            input_names = ["close"],
            param_names = ["rsi_window", "ma_window"],
            output_names = ["value"]
        ).from_apply_func(
            self.customIndicator,
            rsi_window = 14,
            ma_window = 50
        )
        # Testing out the function above
        comb = indicator.run(ticker_prices, rsi_window = 21, ma_window = 50)
        # Entries and exits that returns a boolean value
        entries = comb.value == 1.0
        exits = comb.value == -1.0

        portfolio = vbt.Portfolio.from_signals(ticker_prices, entries, exits)
        # print(portfolio.stats()) #Prints stats for tickers as a whole
        print(portfolio.total_return())  # returns a percentage of total returns and losses for each ticker
        return comb.value.to_string()

    


test = BackTester("AAPL", "2023-03-09", "2023-03-16")
# if it returns 0, nothing happens. If it returns 1, buy. If it returns -1, sell.
test.indicatorFact(["MSFT", "AAPL", "IBM"], "2023-03-09", "2023-03-16")
#print(test.indicatorFact())

